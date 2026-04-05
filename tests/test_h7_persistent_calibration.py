from pathlib import Path

from mathteach.models import RawBlockObservation, SessionRequest
from mathteach.services.calibration_engine import CalibrationEngine
from mathteach.services.calibration_store import CalibrationStore
from mathteach.services.planner import build_teaching_plan, record_decision_outcome


def test_calibration_engine_with_persistent_store_keeps_decisions(tmp_path: Path) -> None:
    store = CalibrationStore(tmp_path / "calibration.json")
    engine = CalibrationEngine(
        store=store,
        autosave_threshold=1,
        min_samples_for_calibration=1,
    )

    plan = build_teaching_plan(
        SessionRequest(
            objective="Explain this example in clear steps.",
            learner_profile={
                "age_group": "teen",
                "math_level": "middle_school",
                "confidence": "low",
                "preferred_pace": "balanced",
                "language": "en",
                "wants_visuals": True,
                "wants_history": False,
            },
            runtime_observations=[
                {"evidence": ["rapid_success_three_blocks", "transfer_success"]},
            ],
        ),
        calibration_engine=engine,
    )

    reloaded = store.load()

    assert plan.calibration_context is not None
    assert len(reloaded.decision_records) == 1
    assert reloaded.decision_records[0].decision_id == plan.calibration_context.decision_id


def test_calibration_persists_across_engine_instances(tmp_path: Path) -> None:
    store_path = tmp_path / "calibration.json"
    engine_1 = CalibrationEngine(
        store=CalibrationStore(store_path),
        autosave_threshold=1,
        min_samples_for_calibration=1,
    )
    plan = build_teaching_plan(
        SessionRequest(
            objective="Why do fractions matter?",
            learner_profile={
                "age_group": "teen",
                "math_level": "middle_school",
                "confidence": "low",
                "preferred_pace": "balanced",
                "language": "en",
                "wants_visuals": True,
                "wants_history": True,
            },
            runtime_observations=[
                {"evidence": ["text_overload", "vocabulary_request_again"]},
            ],
        ),
        calibration_engine=engine_1,
    )

    engine_2 = CalibrationEngine(
        store=CalibrationStore(store_path),
        autosave_threshold=1,
        min_samples_for_calibration=1,
    )

    assert plan.calibration_context is not None
    assert any(
        record.decision_id == plan.calibration_context.decision_id
        for record in engine_2.decision_log
    )


def test_weight_adjustment_and_history_are_persistent(tmp_path: Path) -> None:
    store_path = tmp_path / "calibration.json"
    engine = CalibrationEngine(
        store=CalibrationStore(store_path),
        autosave_threshold=1,
        min_samples_for_calibration=1,
    )
    plan = build_teaching_plan(
        SessionRequest(
            objective="Explain this example in clear steps.",
            learner_profile={
                "age_group": "teen",
                "math_level": "middle_school",
                "confidence": "low",
                "preferred_pace": "balanced",
                "language": "en",
                "wants_visuals": True,
                "wants_history": False,
            },
            runtime_observations=[
                {"evidence": ["rapid_success_three_blocks", "transfer_success"]},
            ],
        ),
        calibration_engine=engine,
    )

    assert plan.calibration_context is not None
    updated = record_decision_outcome(
        plan.calibration_context.decision_id,
        RawBlockObservation(
            block_index=2,
            current_mode=plan.lesson_mode,
            evidence=["visible_small_success", "transfer_success"],
            duration_seconds=80.0,
            accuracy_estimate=0.9,
            engagement_estimate="high",
        ),
        confidence_change=0.15,
        calibration_engine=engine,
    )

    assert updated is True

    reloaded = CalibrationStore(store_path).load()

    assert reloaded.outcome_metrics
    assert reloaded.calibration_weights.calibration_rounds >= 1
    assert reloaded.weights_history
