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
)
from mathteach.services.session_store import SessionStore


class SessionConflictError(ValueError):
    pass


class SessionManager:
    def __init__(
        self,
        store: SessionStore,
        migrator: CheckpointMigrator | None = None,
    ) -> None:
        self.store = store
        self.migrator = migrator or CheckpointMigrator()

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
                return request, None
            return (
                request.model_copy(
                    update={"mode_adaptation_checkpoint": inline_checkpoint}
                ),
                None,
            )

        stored_checkpoint = self._load_stored_checkpoint(request.session_id)
        if stored_checkpoint is None:
            return request.model_copy(update={"session_id": None}), request.session_id

        return (
            request.model_copy(
                update={
                    "session_id": None,
                    "mode_adaptation_checkpoint": stored_checkpoint,
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
                migrated = self.migrator.migrate_checkpoint(checkpoint)
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
                migrated = self.migrator.migrate_checkpoint(checkpoint)
            except CheckpointMigrationError as migration_exc:
                raise CheckpointMigrationRequired(
                    f"Checkpoint for session {session_id} requires migration. {migration_exc}"
                ) from exc
            validate_checkpoint_for_resume(migrated)
            self.store.save_checkpoint(session_id, migrated)
            return migrated
        except SessionValidationError as exc:
            raise SessionValidationError(
                f"Stored checkpoint for session {session_id} is invalid. {exc}"
            ) from exc


def as_http_error(
    exc: SessionConflictError | SessionValidationError | CheckpointMigrationRequired,
) -> HTTPException:
    if isinstance(exc, SessionConflictError):
        return HTTPException(status_code=422, detail=str(exc))
    if isinstance(exc, CheckpointMigrationRequired):
        return HTTPException(status_code=410, detail=str(exc))
    return HTTPException(status_code=400, detail=str(exc))
