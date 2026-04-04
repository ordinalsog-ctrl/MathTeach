import uuid

from mathteach.models import (
    LearnerProfile,
    ModeAdaptationCheckpoint,
    ModeAdaptationState,
    SessionRequest,
    TeachingPlan,
)
from mathteach.services.session_manager import SessionConflictError, SessionManager
from mathteach.services.planner import build_teaching_plan
from mathteach.services.session_store import SessionStore


def _teaching_plan(checkpoint: ModeAdaptationCheckpoint) -> TeachingPlan:
    return build_teaching_plan(
        SessionRequest(
            objective="Erklaere mir die quadratische Gleichung anschaulich.",
            learner_profile=LearnerProfile(
                age_group="teen",
                math_level="high_school",
                confidence="low",
                preferred_pace="balanced",
                language="de",
                wants_visuals=True,
                wants_history=True,
            ),
            mode_adaptation_checkpoint=checkpoint,
        )
    )


def _request(session_id: str | None = None, checkpoint=None) -> SessionRequest:
    return SessionRequest(
        objective="Erklaere mir die quadratische Gleichung anschaulich.",
        learner_profile=LearnerProfile(
            age_group="teen",
            math_level="high_school",
            confidence="low",
            preferred_pace="balanced",
            language="de",
            wants_visuals=True,
            wants_history=True,
        ),
        session_id=session_id,
        mode_adaptation_checkpoint=checkpoint,
    )


def test_session_manager_loads_existing_session(tmp_path) -> None:
    store = SessionStore(tmp_path)
    manager = SessionManager(store)
    checkpoint = ModeAdaptationCheckpoint(
        mode_adaptation_state=ModeAdaptationState(
            current_mode="worked_example_tutoring",
            blocks_in_current_mode=2,
            mode_changes_in_session=1,
        )
    )
    store.save_checkpoint("session-one", checkpoint)

    planner_request, session_id = manager.prepare_planner_request(_request("session-one"))

    assert session_id == "session-one"
    assert planner_request.mode_adaptation_checkpoint == checkpoint
    assert planner_request.session_id is None


def test_session_manager_treats_unknown_session_as_new(tmp_path) -> None:
    manager = SessionManager(SessionStore(tmp_path))

    planner_request, session_id = manager.prepare_planner_request(_request("unknown-session"))

    assert session_id == "unknown-session"
    assert planner_request.mode_adaptation_checkpoint is None
    assert planner_request.session_id is None


def test_session_manager_rejects_dual_input(tmp_path) -> None:
    manager = SessionManager(SessionStore(tmp_path))
    checkpoint = ModeAdaptationCheckpoint(
        mode_adaptation_state=ModeAdaptationState(
            current_mode="guided_concept_explanation",
            blocks_in_current_mode=1,
            mode_changes_in_session=0,
        )
    )

    try:
        manager.prepare_planner_request(_request("session-conflict", checkpoint=checkpoint))
    except SessionConflictError as exc:
        assert "either session_id or inline mode adaptation resume data" in str(exc)
    else:
        raise AssertionError("Expected SessionManager to reject conflicting resume inputs.")


def test_session_manager_persists_new_checkpoint(tmp_path) -> None:
    store = SessionStore(tmp_path)
    manager = SessionManager(store)
    session_id = f"session-{uuid.uuid4()}"
    checkpoint = ModeAdaptationCheckpoint(
        mode_adaptation_state=ModeAdaptationState(
            current_mode="guided_concept_explanation",
            blocks_in_current_mode=0,
            mode_changes_in_session=0,
        )
    )

    persisted_plan = manager.persist_plan_result(session_id, _teaching_plan(checkpoint))

    assert persisted_plan.session_id == session_id
    assert store.load_checkpoint(session_id) == checkpoint
