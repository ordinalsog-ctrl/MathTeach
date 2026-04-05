from mathteach.models import (
    BlockType,
    DecisionAlternative,
    DecisionRecord,
    EvidenceCombinationPattern,
    OutcomeMetrics,
    RawBlockObservation,
    SessionRequest,
)
from mathteach.services.calibration_engine import CalibrationEngine
from mathteach.services.planner import build_teaching_plan, record_decision_outcome


def test_calibration_engine_starts_with_h5_weight_profile() -> None:
    engine = CalibrationEngine(min_samples_for_calibration=3)

    weights = engine.current_weights.get_current_weights()

    assert weights["heuristic"] == 0.35
    assert weights["goal_alignment"] == 0.2
    assert engine.current_weights.calibration_rounds == 0


def test_calibration_engine_logs_and_updates_decisions() -> None:
    engine = CalibrationEngine(min_samples_for_calibration=3)
    record = DecisionRecord(
        session_id="session-1",
        current_block_type=BlockType.WORKED_EXAMPLE,
        evidence_patterns=[EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS],
        active_supports=["adhd_aware_support"],
        available_candidate_paths=["path_1", "path_2"],
        chosen_path_id="path_1",
        chosen_path_score=0.81,
        chosen_path_score_breakdown={
            "heuristic": 0.72,
            "goal_alignment": 0.8,
            "history_alignment": 0.6,
            "evidence_continuity": 0.78,
            "profile_match": 0.7,
            "pilot_data_adjustment": 0.68,
        },
        alternative_paths=[
            DecisionAlternative(
                path_id="path_2",
                score=0.74,
                score_breakdown={"heuristic": 0.7},
            )
        ],
    )

    engine.log_decision(record)
    updated = engine.update_outcome(
        record.decision_id,
        OutcomeMetrics(
            observed_evidence=["visible_small_success"],
            confidence_change=0.12,
            mastery_gain_estimate=0.31,
            error_rate_trend="improving",
            observed_engagement="high",
        ),
    )

    assert updated is True
    assert engine.decision_log[0].observed_outcome is not None
    assert engine.decision_log[0].observed_outcome.mastery_gain_estimate == 0.31


def test_calibration_engine_reweights_after_enough_completed_samples() -> None:
    engine = CalibrationEngine(min_samples_for_calibration=3)

    for index, goal_alignment in enumerate((0.3, 0.7, 0.95), start=1):
        record = DecisionRecord(
            session_id=f"session-{index}",
            current_block_type=BlockType.WORKED_EXAMPLE,
            evidence_patterns=[EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS],
            active_supports=["adhd_aware_support"],
            available_candidate_paths=["path_1", "path_2"],
            chosen_path_id="path_1",
            chosen_path_score=0.7,
            chosen_path_score_breakdown={
                "heuristic": 0.2,
                "goal_alignment": goal_alignment,
                "history_alignment": 0.25,
                "evidence_continuity": 0.2,
                "profile_match": 0.2,
                "pilot_data_adjustment": 0.2,
            },
            alternative_paths=[],
        )
        engine.log_decision(record)
        engine.update_outcome(
            record.decision_id,
            OutcomeMetrics(
                observed_evidence=["transfer_success"],
                confidence_change=0.05 * index,
                mastery_gain_estimate=0.15 * index,
                error_rate_trend="improving",
                observed_engagement="high",
            ),
        )

    assert engine.current_weights.calibration_rounds >= 1
    assert engine.current_weights.last_calibration is not None
    assert engine.current_weights.adjusted_weights
    assert engine.current_weights.adjusted_weights != engine.current_weights.baseline_weights
    assert engine.current_weights.adjusted_weights["goal_alignment"] > 0.0


def test_planner_logs_decision_and_accepts_outcome_updates() -> None:
    engine = CalibrationEngine(min_samples_for_calibration=1)
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
                "declared_support_needs": ["adhd_aware_support"],
            },
            runtime_observations=[
                {"evidence": ["rapid_success_three_blocks", "transfer_success"]},
            ],
        ),
        calibration_engine=engine,
    )

    assert plan.calibration_context is not None
    assert plan.calibration_context.decision_id is not None
    assert len(engine.decision_log) == 1

    updated = record_decision_outcome(
        plan.calibration_context.decision_id,
        RawBlockObservation(
            block_index=2,
            current_mode=plan.lesson_mode,
            evidence=["visible_small_success", "transfer_success"],
            duration_seconds=95.0,
            accuracy_estimate=0.86,
            engagement_estimate="high",
        ),
        confidence_change=0.14,
        calibration_engine=engine,
    )

    assert updated is True
    assert engine.decision_log[0].observed_outcome is not None
    assert engine.current_weights.calibration_rounds >= 1
