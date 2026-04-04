from __future__ import annotations

from fastapi import HTTPException

from mathteach.models import (
    ModeAdaptationCheckpoint,
    SessionRequest,
    TeachingPlan,
)
from mathteach.services.session_store import SessionStore


class SessionConflictError(ValueError):
    pass


class SessionManager:
    def __init__(self, store: SessionStore) -> None:
        self.store = store

    def prepare_planner_request(
        self,
        request: SessionRequest,
    ) -> tuple[SessionRequest, str | None]:
        self._ensure_non_conflicting_resume_input(request)

        if request.session_id is None:
            return request, None

        stored_checkpoint = self.store.load_checkpoint(request.session_id)
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
        if checkpoint.schema_version != "phase_h1_v1":
            raise SessionConflictError(
                f"Unsupported mode adaptation checkpoint version: {checkpoint.schema_version}"
            )

    def _ensure_non_conflicting_resume_input(self, request: SessionRequest) -> None:
        if request.session_id is not None and (
            request.mode_adaptation_state is not None
            or request.mode_adaptation_checkpoint is not None
        ):
            raise SessionConflictError(
                "Provide either session_id or inline mode adaptation resume data, not both."
            )


def as_http_conflict(exc: SessionConflictError) -> HTTPException:
    return HTTPException(status_code=422, detail=str(exc))
