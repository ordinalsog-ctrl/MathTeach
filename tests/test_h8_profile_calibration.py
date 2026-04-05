from pathlib import Path

import pytest

from mathteach.models import (
    BlockSequenceIntent,
    BlockType,
    DecisionRecord,
    EnrichedPathEvaluation,
    EvidenceCombinationPattern,
    OutcomeMetrics,
    RawBlockObservation,
    SessionRequest,
)
from mathteach.services.calibration_engine import CalibrationEngine
from mathteach.services.calibration_store import CalibrationStore
from mathteach.services.planner import build_teaching_plan, record_decision_outcome


def _profile_request() -> SessionRequest:
    return SessionRequest(
        objective="Explain this example in clear steps.",
        learner_profile={
            "age_group": "teen",
            "math_level": "middle_school",
            "confidence": "low",
            "preferred_pace": "balanced",
            "language": "de",
            "wants_visuals": True,
            "wants_history": False,
            "declared_support_needs": [
                "adhd_aware_support",
                "dyscalculia_aware_support",
            ],
        },
        runtime_observations=[
            {"evidence": ["rapid_success", "pattern_recognized", "transfer_success"]},
            {"evidence": ["rapid_success", "pattern_recognized", "transfer_success"]},
        ],
    )


def test_planner_exposes_profile_aware_calibration_context() -> None:
    engine = CalibrationEngine(min_samples_for_calibration=1)

    plan = build_teaching_plan(_profile_request(), calibration_engine=engine)

    assert plan.calibration_context is not None
    assert plan.calibration_context.calibration_profile_id is not None
    assert plan.calibration_context.stratification_dimensions["support_profile"] == (
        "adhd_aware_support+dyscalculia_aware_support"
    )
    assert plan.enriched_paths[0].calibration_profile_id == (
        plan.calibration_context.calibration_profile_id
    )
    assert plan.calibration_context.active_weights == (
        plan.enriched_paths[0].calibration_weights_used
    )


def test_profile_specific_calibration_persists_and_accumulates_history(
    tmp_path: Path,
) -> None:
    store_path = tmp_path / "calibration.json"
    engine = CalibrationEngine(
        store=CalibrationStore(store_path),
        autosave_threshold=1,
        min_samples_for_calibration=1,
    )

    profile_id: str | None = None
    for block_index in range(2, 5):
        plan = build_teaching_plan(_profile_request(), calibration_engine=engine)
        assert plan.calibration_context is not None
        profile_id = plan.calibration_context.calibration_profile_id
        updated = record_decision_outcome(
            plan.calibration_context.decision_id,
            RawBlockObservation(
                block_index=block_index,
                current_mode=plan.lesson_mode,
                evidence=["visible_small_success", "transfer_success"],
                duration_seconds=80.0 - block_index,
                accuracy_estimate=0.84,
                engagement_estimate="high",
            ),
            confidence_change=0.12,
            calibration_engine=engine,
        )
        assert updated is True

    engine.force_save()
    reloaded = CalibrationStore(store_path).load()

    assert profile_id is not None
    assert profile_id in reloaded.calibration_profiles
    profile = reloaded.calibration_profiles[profile_id]
    assert profile.sample_size >= 3
    assert profile.outcome_count >= 3
    assert profile.current_weights.calibration_rounds >= 1
    assert profile.weights_history


def test_profile_list_prefers_context_profiles_with_observed_data(tmp_path: Path) -> None:
    store_path = tmp_path / "calibration.json"
    engine = CalibrationEngine(
        store=CalibrationStore(store_path),
        autosave_threshold=1,
        min_samples_for_calibration=1,
    )

    plan = build_teaching_plan(_profile_request(), calibration_engine=engine)
    assert plan.calibration_context is not None
    record_decision_outcome(
        plan.calibration_context.decision_id,
        RawBlockObservation(
            block_index=2,
            current_mode=plan.lesson_mode,
            evidence=["visible_small_success", "transfer_success"],
            duration_seconds=76.0,
            accuracy_estimate=0.88,
            engagement_estimate="high",
        ),
        confidence_change=0.16,
        calibration_engine=engine,
    )

    profiles = engine.list_profiles()

    assert profiles
    assert any(
        profile["stratification_dimensions"].get("support_profile")
        == "adhd_aware_support+dyscalculia_aware_support"
        for profile in profiles
    )


def test_exact_profile_preferred_over_broader_when_present() -> None:
    engine = CalibrationEngine(min_samples_for_calibration=999)

    for index in range(12):
        record = DecisionRecord(
            session_id="exact-session",
            current_block_type=BlockType.WORKED_EXAMPLE,
            evidence_patterns=[EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS],
            active_supports=["adhd_aware_support"],
            sequence_intent=BlockSequenceIntent.MASTERY_PATH,
            chosen_path_id=f"exact_path_{index}",
            chosen_path_score=0.8,
            chosen_path_score_breakdown={
                "heuristic": 0.7,
                "goal_alignment": 0.2,
                "history_alignment": 0.2,
                "evidence_continuity": 0.2,
                "profile_match": 0.2,
                "pilot_data_adjustment": 0.2,
            },
        )
        engine.log_decision(record)
        engine.update_outcome(
            record.decision_id,
            OutcomeMetrics(
                mastery_gain_estimate=0.5,
                observed_engagement="high",
                error_rate_trend="improving",
            ),
        )

    for index in range(20):
        record = DecisionRecord(
            session_id="broad-session",
            current_block_type=BlockType.GUIDED_PRACTICE,
            evidence_patterns=[EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS],
            active_supports=["adhd_aware_support"],
            sequence_intent=BlockSequenceIntent.ADAPTIVE_REMEDIATION,
            chosen_path_id=f"broad_path_{index}",
            chosen_path_score=0.75,
            chosen_path_score_breakdown={
                "heuristic": 0.6,
                "goal_alignment": 0.2,
                "history_alignment": 0.2,
                "evidence_continuity": 0.2,
                "profile_match": 0.2,
                "pilot_data_adjustment": 0.2,
            },
        )
        engine.log_decision(record)
        engine.update_outcome(
            record.decision_id,
            OutcomeMetrics(
                mastery_gain_estimate=0.4,
                observed_engagement="high",
                error_rate_trend="improving",
            ),
        )

    selected = engine._select_profile(
        active_supports=["adhd_aware_support"],
        sequence_intent=BlockSequenceIntent.MASTERY_PATH,
        evidence_patterns=[EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS],
        current_block_type=BlockType.WORKED_EXAMPLE,
    )

    assert selected is not None
    assert selected.stratification_dimensions["support_profile"] == "adhd_aware_support"
    assert (
        selected.stratification_dimensions["sequence_intent"]
        == BlockSequenceIntent.MASTERY_PATH.value
    )
    assert (
        selected.stratification_dimensions["evidence_pattern"]
        == EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS.value
    )
    assert selected.stratification_dimensions["block_type"] == BlockType.WORKED_EXAMPLE.value


def test_block_type_stratification_affects_path_ranking() -> None:
    engine = CalibrationEngine(min_samples_for_calibration=999)

    guided_profile = engine._get_or_create_profile(
        {
            "support_profile": "adhd_aware_support",
            "sequence_intent": BlockSequenceIntent.MASTERY_PATH.value,
            "evidence_pattern": EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS.value,
            "block_type": BlockType.GUIDED_PRACTICE.value,
        }
    )
    guided_profile.current_weights = guided_profile.current_weights.model_copy(
        update={
            "adjusted_weights": {
                "heuristic": 0.7,
                "goal_alignment": 0.1,
                "history_alignment": 0.05,
                "evidence_continuity": 0.05,
                "profile_match": 0.05,
                "pilot_data_adjustment": 0.05,
            }
        }
    )
    guided_profile.confidence_score = 0.8
    guided_profile.outcome_count = 20

    concept_profile = engine._get_or_create_profile(
        {
            "support_profile": "adhd_aware_support",
            "sequence_intent": BlockSequenceIntent.MASTERY_PATH.value,
            "evidence_pattern": EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS.value,
            "block_type": BlockType.CONCEPT_CHECK.value,
        }
    )
    concept_profile.current_weights = concept_profile.current_weights.model_copy(
        update={
            "adjusted_weights": {
                "heuristic": 0.1,
                "goal_alignment": 0.7,
                "history_alignment": 0.05,
                "evidence_continuity": 0.05,
                "profile_match": 0.05,
                "pilot_data_adjustment": 0.05,
            }
        }
    )
    concept_profile.confidence_score = 0.8
    concept_profile.outcome_count = 20

    enriched = engine.apply_to_enriched_paths(
        [
            EnrichedPathEvaluation(
                path_id="path_guided",
                block_types=[BlockType.GUIDED_PRACTICE, BlockType.BRIDGE_TO_APPLICATION],
                raw_score=0.5,
                total_score=0.5,
                score_breakdown={
                    "heuristic": 0.9,
                    "goal_alignment": 0.1,
                    "history_alignment": 0.1,
                    "evidence_continuity": 0.1,
                    "profile_match": 0.1,
                    "pilot_data_adjustment": 0.1,
                },
            ),
            EnrichedPathEvaluation(
                path_id="path_concept",
                block_types=[BlockType.CONCEPT_CHECK, BlockType.GUIDED_PRACTICE],
                raw_score=0.5,
                total_score=0.5,
                score_breakdown={
                    "heuristic": 0.4,
                    "goal_alignment": 0.6,
                    "history_alignment": 0.1,
                    "evidence_continuity": 0.1,
                    "profile_match": 0.1,
                    "pilot_data_adjustment": 0.1,
                },
            ),
        ],
        active_supports=["adhd_aware_support"],
        sequence_intent=BlockSequenceIntent.MASTERY_PATH,
        evidence_patterns=[EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS],
        current_block_type=BlockType.WORKED_EXAMPLE,
    )

    assert enriched[0].path_id == "path_guided"
    assert enriched[0].calibration_profile_id != enriched[1].calibration_profile_id
    assert enriched[0].calibration_weights_used != enriched[1].calibration_weights_used
    assert BlockType.GUIDED_PRACTICE.value in enriched[0].calibration_profile_id
    assert BlockType.CONCEPT_CHECK.value in enriched[1].calibration_profile_id


def test_plan_exposes_actual_blended_weights_not_global() -> None:
    engine = CalibrationEngine(min_samples_for_calibration=1)

    initial_plan = build_teaching_plan(_profile_request(), calibration_engine=engine)
    assert initial_plan.calibration_context is not None
    profile_id = initial_plan.calibration_context.calibration_profile_id
    assert profile_id is not None

    profile = engine.calibration_profiles[profile_id]
    profile.current_weights = profile.current_weights.model_copy(
        update={
            "adjusted_weights": {
                "heuristic": 0.5,
                "goal_alignment": 0.15,
                "history_alignment": 0.1,
                "evidence_continuity": 0.1,
                "profile_match": 0.1,
                "pilot_data_adjustment": 0.05,
            }
        }
    )
    profile.confidence_score = 0.8

    plan = build_teaching_plan(_profile_request(), calibration_engine=engine)

    assert plan.calibration_context is not None
    assert plan.calibration_context.calibration_profile_id == profile_id
    assert plan.enriched_paths[0].calibration_weights_used
    assert (
        plan.calibration_context.active_weights
        == plan.enriched_paths[0].calibration_weights_used
    )

    expected_heuristic = 0.8 * 0.5 + 0.2 * engine.current_weights.get_current_weights()["heuristic"]
    assert plan.calibration_context.active_weights["heuristic"] == pytest.approx(
        expected_heuristic,
        abs=1e-6,
    )
