from __future__ import annotations

from fastapi import HTTPException
from pydantic import ValidationError

from mathteach.models import (
    ModeAdaptationCheckpoint,
    SessionRequest,
    TeachingPlan,
)
from mathteach.services.checkpoint_validation import (
    CheckpointMigrationRequired,
    SessionValidationError,
    validate_checkpoint_for_persist,
    validate_checkpoint_for_resume,
)
from mathteach.services.checkpoint_migrator import (
    CheckpointMigrationError,
    CheckpointMigrator,
    CheckpointMigrationResult,
)
from mathteach.services.session_audit import SessionAuditEvent, SessionAuditLogger
from mathteach.services.session_quarantine import SessionQuarantine
from mathteach.services.session_store import SessionStore


class SessionConflictError(ValueError):
    pass


class SessionManager:
    def __init__(
        self,
        store: SessionStore,
        migrator: CheckpointMigrator | None = None,
        audit_logger: SessionAuditLogger | None = None,
        quarantine: SessionQuarantine | None = None,
    ) -> None:
        self.store = store
        self.migrator = migrator or CheckpointMigrator()
        self.audit_logger = audit_logger or SessionAuditLogger(
            self.store.base_dir / "_audit" / "session_audit.jsonl"
        )
        self.quarantine = quarantine or SessionQuarantine(
            self.store.base_dir / "_quarantine"
        )

    def prepare_planner_request(
        self,
        request: SessionRequest,
    ) -> tuple[SessionRequest, str | None]:
        self._ensure_non_conflicting_resume_input(request)
        inline_checkpoint = self._validate_inline_checkpoint(
            request.mode_adaptation_checkpoint
        )

        if request.session_id is None:
            if inline_checkpoint is None:
                if request.mode_adaptation_state is not None:
                    return request.model_copy(update={"resume_source": "inline_state"}), None
                return request.model_copy(update={"resume_source": "fresh_start"}), None
            return (
                request.model_copy(
                    update={
                        "mode_adaptation_checkpoint": inline_checkpoint,
                        "resume_source": "inline_checkpoint",
                    }
                ),
                None,
            )

        stored_checkpoint = self._load_stored_checkpoint(request.session_id)
        if stored_checkpoint is None:
            return (
                request.model_copy(update={"session_id": None, "resume_source": "fresh_start"}),
                request.session_id,
            )

        return (
            request.model_copy(
                update={
                    "session_id": None,
                    "mode_adaptation_checkpoint": stored_checkpoint,
                    "resume_source": "stored_checkpoint",
                }
            ),
            request.session_id,
        )

    def persist_plan_result(
        self,
        session_id: str | None,
        plan: TeachingPlan,
    ) -> TeachingPlan:
        if session_id is None:
            return plan

        self.validate_session_state(plan.mode_adaptation_checkpoint)
        self.store.save_checkpoint(session_id, plan.mode_adaptation_checkpoint)
        return plan.model_copy(update={"session_id": session_id})

    def list_quarantined_sessions(self) -> list[dict[str, object]]:
        return [
            {
                "session_id": record.session_id,
                "reason": record.reason,
                "detail": record.detail,
                "timestamp": record.timestamp,
                "quarantine_path": record.quarantine_path,
                "metadata_path": record.metadata_path,
            }
            for record in self.quarantine.list_records()
        ]

    def inspect_quarantined_session(self, session_id: str) -> dict[str, object] | None:
        quarantined = self.quarantine.read_quarantined_text(session_id)
        if quarantined is None:
            return None
        record, raw_checkpoint = quarantined
        audit_events = [event.model_dump(mode="json") for event in self.audit_logger.read_events(session_id)]

        parsed_checkpoint: dict[str, object] | None = None
        preview_status = "unparseable"
        preview_detail: str | None = None
        try:
            checkpoint = ModeAdaptationCheckpoint.model_validate_json(raw_checkpoint)
            parsed_checkpoint = checkpoint.model_dump(mode="json")
            try:
                validate_checkpoint_for_resume(checkpoint)
                preview_status = "valid_current"
            except CheckpointMigrationRequired as exc:
                preview_status = "migration_required"
                preview_detail = str(exc)
            except SessionValidationError as exc:
                preview_status = "invalid"
                preview_detail = str(exc)
        except ValidationError as exc:
            preview_detail = str(exc)

        return {
            "session": record.model_dump(mode="json"),
            "audit_events": audit_events,
            "preview_status": preview_status,
            "preview_detail": preview_detail,
            "checkpoint_preview": parsed_checkpoint,
            "raw_checkpoint": raw_checkpoint,
        }

    def restore_quarantined_session(self, session_id: str) -> dict[str, object] | None:
        quarantined = self.quarantine.read_quarantined_text(session_id)
        if quarantined is None:
            return None
        record, raw_checkpoint = quarantined
        migration_result: CheckpointMigrationResult | None = None

        try:
            checkpoint = ModeAdaptationCheckpoint.model_validate_json(raw_checkpoint)
        except ValidationError as exc:
            raise SessionValidationError(
                f"Quarantined checkpoint for session {session_id} could not be parsed."
            ) from exc

        try:
            validate_checkpoint_for_resume(checkpoint)
            restored_checkpoint = checkpoint
        except CheckpointMigrationRequired:
            try:
                migration_result = self.migrator.migrate_checkpoint(checkpoint)
                restored_checkpoint = migration_result.checkpoint
            except CheckpointMigrationError as exc:
                raise CheckpointMigrationRequired(
                    f"Quarantined checkpoint for session {session_id} still requires unsupported migration."
                ) from exc
            validate_checkpoint_for_resume(restored_checkpoint)
        except SessionValidationError as exc:
            raise SessionValidationError(
                f"Quarantined checkpoint for session {session_id} is still invalid. {exc}"
            ) from exc

        validate_checkpoint_for_persist(restored_checkpoint)
        self.store.save_checkpoint(session_id, restored_checkpoint)
        self.quarantine.discard_latest(session_id)
        if migration_result is not None:
            self._record_migration_event(session_id, migration_result)
        self.audit_logger.record(
            SessionAuditEvent(
                event_type="checkpoint_restored",
                session_id=session_id,
                detail="Quarantined checkpoint restored to active session storage.",
                target_version=restored_checkpoint.schema_version,
            )
        )
        return {
            "session_id": session_id,
            "restored_checkpoint": restored_checkpoint.model_dump(mode="json"),
        }

    def discard_quarantined_session(self, session_id: str) -> dict[str, object] | None:
        record = self.quarantine.discard_latest(session_id)
        if record is None:
            return None
        self.audit_logger.record(
            SessionAuditEvent(
                event_type="checkpoint_discarded",
                session_id=session_id,
                detail="Quarantined checkpoint discarded by admin action.",
            )
        )
        return {"session_id": session_id, "discarded": True, "reason": record.reason}

    def validate_session_state(
        self,
        checkpoint: ModeAdaptationCheckpoint,
    ) -> None:
        validate_checkpoint_for_persist(checkpoint)

    def _ensure_non_conflicting_resume_input(self, request: SessionRequest) -> None:
        if request.session_id is not None and (
            request.mode_adaptation_state is not None
            or request.mode_adaptation_checkpoint is not None
        ):
            raise SessionConflictError(
                "Provide either session_id or inline mode adaptation resume data, not both."
            )

    def _validate_inline_checkpoint(
        self,
        checkpoint: ModeAdaptationCheckpoint | None,
    ) -> ModeAdaptationCheckpoint | None:
        if checkpoint is None:
            return None
        try:
            validate_checkpoint_for_resume(checkpoint)
            return checkpoint
        except CheckpointMigrationRequired as exc:
            try:
                migration_result = self.migrator.migrate_checkpoint(checkpoint)
                migrated = migration_result.checkpoint
            except CheckpointMigrationError as migration_exc:
                raise CheckpointMigrationRequired(
                    "Inline mode adaptation checkpoint requires migration before resume. "
                    f"{migration_exc}"
                ) from exc
            validate_checkpoint_for_resume(migrated)
            return migrated
        except SessionValidationError as exc:
            raise SessionValidationError(
                f"Inline mode adaptation checkpoint is invalid. {exc}"
            ) from exc

    def _load_stored_checkpoint(
        self,
        session_id: str,
    ) -> ModeAdaptationCheckpoint | None:
        try:
            checkpoint = self.store.load_checkpoint(session_id)
        except ValidationError as exc:
            self._quarantine_invalid_session(
                session_id,
                reason="invalid-checkpoint",
                detail=(
                    f"Stored checkpoint for session {session_id} is invalid and could not be resumed."
                ),
                source_version=None,
            )
            raise SessionValidationError(
                f"Stored checkpoint for session {session_id} is invalid and could not be resumed."
            ) from exc

        if checkpoint is None:
            return None

        try:
            validate_checkpoint_for_resume(checkpoint)
            return checkpoint
        except CheckpointMigrationRequired as exc:
            try:
                migration_result = self.migrator.migrate_checkpoint(checkpoint)
                migrated = migration_result.checkpoint
            except CheckpointMigrationError as migration_exc:
                self._quarantine_invalid_session(
                    session_id,
                    reason="migration-failed",
                    detail=str(migration_exc),
                    source_version=checkpoint.schema_version,
                    audit_event_type="checkpoint_migration_failed",
                )
                raise CheckpointMigrationRequired(
                    f"Checkpoint for session {session_id} requires migration. {migration_exc}"
                ) from exc
            validate_checkpoint_for_resume(migrated)
            self.store.save_checkpoint(session_id, migrated)
            self._record_migration_event(session_id, migration_result)
            return migrated
        except SessionValidationError as exc:
            self._quarantine_invalid_session(
                session_id,
                reason="invalid-checkpoint",
                detail=str(exc),
                source_version=checkpoint.schema_version,
            )
            raise SessionValidationError(
                f"Stored checkpoint for session {session_id} is invalid. {exc}"
            ) from exc

    def _quarantine_invalid_session(
        self,
        session_id: str,
        reason: str,
        detail: str,
        source_version: str | None,
        audit_event_type: str = "checkpoint_invalid",
    ) -> None:
        record = self.quarantine.quarantine_file(
            session_id=session_id,
            source_path=self.store.session_path(session_id),
            reason=reason,
            detail=detail,
        )
        self.audit_logger.record(
            SessionAuditEvent(
                event_type=audit_event_type,
                session_id=session_id,
                detail=detail,
                source_version=source_version,
                quarantine_path=record.quarantine_path if record is not None else None,
            )
        )

    def _record_migration_event(
        self,
        session_id: str,
        migration_result: CheckpointMigrationResult,
    ) -> None:
        if not migration_result.steps:
            return

        source_version = migration_result.steps[0].source_version
        target_version = migration_result.steps[-1].target_version
        migration_steps = [
            f"{step.source_version}->{step.target_version}"
            for step in migration_result.steps
        ]
        if len(migration_result.steps) == 1:
            event_type = "checkpoint_migrated"
            detail = f"Checkpoint migrated from {source_version} to {target_version}."
        else:
            event_type = "checkpoint_migration_chain"
            detail = (
                f"Checkpoint migrated from {source_version} to {target_version} via "
                f"{len(migration_result.steps)} steps."
            )

        self.audit_logger.record(
            SessionAuditEvent(
                event_type=event_type,
                session_id=session_id,
                detail=detail,
                source_version=source_version,
                target_version=target_version,
                migration_steps=migration_steps,
            )
        )


def as_http_error(
    exc: SessionConflictError | SessionValidationError | CheckpointMigrationRequired,
) -> HTTPException:
    if isinstance(exc, SessionConflictError):
        return HTTPException(status_code=422, detail=str(exc))
    if isinstance(exc, CheckpointMigrationRequired):
        return HTTPException(status_code=410, detail=str(exc))
    return HTTPException(status_code=400, detail=str(exc))
