from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from mathteach.config import get_settings
from mathteach.models import CalibrationOutcomeRequest, SessionRequest
from mathteach.services.corpus import (
    build_chronology_program,
    build_corpus_blueprint,
    build_network_program,
    build_source_access_program,
)
from mathteach.services.foundation import build_foundation
from mathteach.services.calibration_engine import CalibrationEngine
from mathteach.services.calibration_observability import (
    AdaptiveCapsTrendQuery,
    EdgePolicyTrendQuery,
    SteeringLogQuery,
)
from mathteach.services.calibration_store import CalibrationStore
from mathteach.services.planner import (
    build_stack,
    build_teaching_plan,
    record_decision_outcome,
)
from mathteach.services.checkpoint_validation import (
    CheckpointMigrationRequired,
    SessionValidationError,
)
from mathteach.services.session_manager import SessionManager, SessionConflictError, as_http_error
from mathteach.services.session_store import SessionStore

settings = get_settings()
app = FastAPI(title=settings.app_name, version="0.1.0")
_UI_DIR = Path(__file__).resolve().parent / "ui"
_UI_STATIC_DIR = _UI_DIR / "static"
session_store = SessionStore(settings.session_store_dir)
session_manager = SessionManager(session_store)
calibration_store = (
    CalibrationStore(settings.calibration_store_path)
    if settings.calibration_store_path
    else None
)
calibration_engine = CalibrationEngine(
    store=calibration_store,
    autosave_threshold=settings.calibration_autosave_threshold,
)
app.mount("/device-static", StaticFiles(directory=_UI_STATIC_DIR), name="device-static")


def _resolve_calibration_engine(
    store_path: str | None = None,
) -> CalibrationEngine:
    if store_path:
        return CalibrationEngine(
            store=CalibrationStore(Path(store_path)),
            autosave_threshold=settings.calibration_autosave_threshold,
        )
    return calibration_engine


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name}


@app.get("/device")
def device_shell() -> FileResponse:
    return FileResponse(_UI_DIR / "device.html")


@app.get("/api/v1/stack")
def stack():
    return build_stack(settings)


@app.get("/api/v1/foundation")
def foundation():
    return build_foundation()


@app.get("/api/v1/corpus/blueprint")
def corpus_blueprint():
    return build_corpus_blueprint()


@app.get("/api/v1/corpus/chronology")
def corpus_chronology():
    return build_chronology_program()


@app.get("/api/v1/corpus/source-access")
def corpus_source_access():
    return build_source_access_program()


@app.get("/api/v1/corpus/network")
def corpus_network():
    return build_network_program()


@app.post("/api/v1/tutoring/plan")
def tutoring_plan(request: SessionRequest):
    """Build the next tutoring plan and return the current calibration snapshot.

    The returned ``calibration_context.adaptive_cap_distribution`` describes only
    the active donor-cap mix of the selected path for this response. It is not
    a historical statistic across earlier plans, sessions, or the whole engine.
    """
    try:
        planner_request, session_id = session_manager.prepare_planner_request(request)
        plan = build_teaching_plan(
            planner_request,
            calibration_engine=calibration_engine,
        )
        return session_manager.persist_plan_result(session_id, plan)
    except (
        SessionConflictError,
        SessionValidationError,
        CheckpointMigrationRequired,
    ) as exc:
        raise as_http_error(exc) from exc


@app.post("/api/v1/tutoring/outcome")
def tutoring_outcome(
    request: CalibrationOutcomeRequest,
    store_path: str | None = Query(default=None),
):
    engine = _resolve_calibration_engine(store_path)
    recorded = record_decision_outcome(
        request.decision_id,
        request.observation,
        confidence_change=request.confidence_change,
        engagement_estimate=request.engagement_estimate,
        calibration_engine=engine,
    )
    if not recorded:
        raise HTTPException(status_code=404, detail="No calibration decision found.")
    decision_record = engine.get_decision(request.decision_id)
    profile_summary = (
        engine.get_profile_summary(decision_record.calibration_profile_id)
        if decision_record is not None and decision_record.calibration_profile_id
        else None
    )
    return {
        "status": "recorded",
        "decision_id": request.decision_id,
        "calibration_rounds": engine.current_weights.calibration_rounds,
        "calibration_profile_updated": profile_summary,
    }


@app.get("/api/v1/admin/calibration/statistics")
def admin_calibration_statistics(
    store_path: str | None = Query(default=None),
):
    engine = _resolve_calibration_engine(store_path)
    if store_path:
        return CalibrationStore(Path(store_path)).get_statistics()
    return engine.get_statistics()


@app.get("/api/v1/admin/calibration/history")
def admin_calibration_history(
    store_path: str | None = Query(default=None),
    limit: int = Query(default=100, ge=1, le=1000),
):
    engine = _resolve_calibration_engine(store_path)
    history = engine.weights_history[-limit:]
    return {
        "history": [
            {
                "timestamp": snapshot.timestamp.isoformat(),
                "trigger_decision_id": snapshot.trigger_decision_id,
                "outcome_score": snapshot.outcome_score,
                "active_weights": snapshot.active_weights,
                "adjustment_reason": snapshot.adjustment_reason,
            }
            for snapshot in history
        ]
    }


@app.get("/api/v1/admin/calibration/profiles")
def admin_calibration_profiles(
    store_path: str | None = Query(default=None),
):
    engine = _resolve_calibration_engine(store_path)
    profiles = engine.list_profiles()
    return {
        "profiles": profiles,
        "profile_count": len(profiles),
    }


@app.get("/api/v1/admin/calibration/profiles/{profile_id}")
def admin_calibration_profile_detail(
    profile_id: str,
    store_path: str | None = Query(default=None),
):
    engine = _resolve_calibration_engine(store_path)
    profile = engine.get_profile_summary(profile_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="No calibration profile found.")
    return profile


@app.get("/api/v1/admin/calibration/profiles/{profile_id}/transfer-candidates")
def admin_calibration_profile_transfer_candidates(
    profile_id: str,
    store_path: str | None = Query(default=None),
    limit: int = Query(default=5, ge=1, le=20),
):
    engine = _resolve_calibration_engine(store_path)
    profile = engine.get_profile(profile_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="No calibration profile found.")
    return {
        "profile_id": profile_id,
        "transfer_candidates": engine.profile_transfer_candidates(profile_id, limit=limit),
    }


@app.get("/api/v1/admin/calibration/profiles/{profile_id}/transfer-history")
def admin_calibration_profile_transfer_history(
    profile_id: str,
    store_path: str | None = Query(default=None),
    limit: int = Query(default=10, ge=1, le=50),
):
    engine = _resolve_calibration_engine(store_path)
    history = engine.get_profile_transfer_history(profile_id, limit=limit)
    if history is None:
        raise HTTPException(status_code=404, detail="No calibration profile found.")
    return history


@app.get("/api/v1/admin/calibration/transfer-network")
def admin_calibration_transfer_network(
    store_path: str | None = Query(default=None),
):
    engine = _resolve_calibration_engine(store_path)
    return engine.compute_transfer_network_summary()


@app.get("/api/v1/admin/calibration/weak-transfers")
def admin_calibration_weak_transfers(
    store_path: str | None = Query(default=None),
    min_average_strength: float = Query(default=0.05, ge=0.0, le=1.0),
    max_average_outcome: float = Query(default=0.12, ge=0.0, le=1.0),
):
    engine = _resolve_calibration_engine(store_path)
    weak_edges = engine.compute_weak_transfers(
        min_average_strength=min_average_strength,
        max_average_outcome=max_average_outcome,
    )
    return {
        "weak_edges": weak_edges,
        "count": len(weak_edges),
    }


@app.get("/api/v1/admin/calibration/profile-density")
def admin_calibration_profile_density(
    store_path: str | None = Query(default=None),
):
    engine = _resolve_calibration_engine(store_path)
    return engine.profile_density_summary()


@app.get("/api/v1/admin/calibration/steering-log")
def admin_calibration_steering_log(
    store_path: str | None = Query(default=None),
    session_id: str | None = Query(default=None),
    time_window_minutes: int = Query(default=1440, ge=1, le=10080),
    limit: int = Query(default=100, ge=1, le=1000),
    include_weak_edges: bool = Query(default=True),
    include_proven_boost: bool = Query(default=True),
    include_adaptive_caps: bool = Query(default=True),
    include_edge_seeking: bool = Query(default=True),
    include_edge_policy: bool = Query(default=True),
    include_family_policy: bool = Query(default=True),
):
    engine = _resolve_calibration_engine(store_path)
    query = SteeringLogQuery(engine)
    entries = query.get_steering_decisions(
        session_id=session_id,
        time_window_minutes=time_window_minutes,
        include_weak_edges=include_weak_edges,
        include_proven_boost=include_proven_boost,
        include_adaptive_caps=include_adaptive_caps,
        include_edge_seeking=include_edge_seeking,
        include_edge_policy=include_edge_policy,
        include_family_policy=include_family_policy,
    )
    return {
        "entries": [entry.model_dump(mode="json") for entry in entries[:limit]],
        "total_count": len(entries),
        "window_minutes": time_window_minutes,
    }


@app.get("/api/v1/admin/calibration/adaptive-caps-trends")
def admin_calibration_adaptive_caps_trends(
    store_path: str | None = Query(default=None),
    time_window_hours: int = Query(default=24, ge=1, le=168),
    aggregate_by: str = Query(default="reason"),
):
    engine = _resolve_calibration_engine(store_path)
    query = AdaptiveCapsTrendQuery(engine)
    try:
        trends = query.get_cap_distribution_trends(
            time_window_hours=time_window_hours,
            aggregate_by=aggregate_by,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {
        "trends": {
            key: value.model_dump(mode="json")
            for key, value in trends.items()
        },
        "window_hours": time_window_hours,
        "aggregate_by": aggregate_by,
    }


@app.get("/api/v1/admin/calibration/edge-policy-trends")
def admin_calibration_edge_policy_trends(
    store_path: str | None = Query(default=None),
    time_window_hours: int = Query(default=24, ge=1, le=168),
    aggregate_by: str = Query(default="policy"),
):
    engine = _resolve_calibration_engine(store_path)
    query = EdgePolicyTrendQuery(engine)
    try:
        trends = query.get_policy_trends(
            time_window_hours=time_window_hours,
            aggregate_by=aggregate_by,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {
        "trends": {
            key: value.model_dump(mode="json")
            for key, value in trends.items()
        },
        "window_hours": time_window_hours,
        "aggregate_by": aggregate_by,
    }


@app.get("/api/v1/admin/quarantine/sessions")
def admin_list_quarantined_sessions():
    return {"sessions": session_manager.list_quarantined_sessions()}


@app.get("/api/v1/admin/quarantine/{session_id}")
def admin_inspect_quarantined_session(session_id: str):
    inspection = session_manager.inspect_quarantined_session(session_id)
    if inspection is None:
        raise HTTPException(status_code=404, detail="No quarantined session found.")
    return inspection


@app.post("/api/v1/admin/quarantine/{session_id}/restore")
def admin_restore_quarantined_session(session_id: str):
    try:
        restored = session_manager.restore_quarantined_session(session_id)
    except (
        SessionConflictError,
        SessionValidationError,
        CheckpointMigrationRequired,
    ) as exc:
        raise as_http_error(exc) from exc
    if restored is None:
        raise HTTPException(status_code=404, detail="No quarantined session found.")
    return restored


@app.post("/api/v1/admin/quarantine/{session_id}/discard")
def admin_discard_quarantined_session(session_id: str):
    discarded = session_manager.discard_quarantined_session(session_id)
    if discarded is None:
        raise HTTPException(status_code=404, detail="No quarantined session found.")
    return discarded
