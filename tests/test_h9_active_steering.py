import pytest

from mathteach.models import (
    BlockSequenceIntent,
    BlockType,
    EvidenceCombinationPattern,
    MetaTransferHistoryEntry,
    SessionRequest,
)
from mathteach.services.calibration_engine import CalibrationEngine
from mathteach.services.planner import build_teaching_plan


def _steering_request() -> SessionRequest:
    return SessionRequest(
        objective="Walk through this math example carefully.",
        learner_profile={
            "age_group": "teen",
            "math_level": "middle_school",
            "confidence": "low",
            "preferred_pace": "balanced",
            "language": "de",
            "wants_visuals": True,
            "wants_history": False,
            "declared_support_needs": ["adhd_aware_support"],
        },
        runtime_observations=[
            {"evidence": ["rapid_success", "pattern_recognized", "transfer_success"]},
            {"evidence": ["rapid_success", "pattern_recognized", "transfer_success"]},
        ],
    )


def test_weak_edge_penalty_deprioritizes_weak_transfer_candidate() -> None:
    engine = CalibrationEngine(min_samples_for_calibration=999)

    target_profile = engine._get_or_create_profile(
        {
            "support_profile": "adhd_aware_support",
            "sequence_intent": BlockSequenceIntent.MASTERY_PATH.value,
            "evidence_pattern": EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS.value,
            "block_type": BlockType.WORKED_EXAMPLE.value,
        }
    )
    donor_weak = engine._get_or_create_profile(
        {
            "support_profile": "adhd_aware_support",
            "sequence_intent": BlockSequenceIntent.MASTERY_PATH.value,
            "evidence_pattern": EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS.value,
            "block_type": BlockType.GUIDED_PRACTICE.value,
        }
    )
    donor_alternative = engine._get_or_create_profile(
        {
            "support_profile": "adhd_aware_support",
            "sequence_intent": BlockSequenceIntent.MASTERY_PATH.value,
            "evidence_pattern": EvidenceCombinationPattern.STAGNATION_PATTERN.value,
            "block_type": BlockType.GUIDED_PRACTICE.value,
        }
    )
    donor_weak.confidence_score = 0.8
    donor_alternative.confidence_score = 0.8
    donor_weak.outcome_count = 24
    donor_alternative.outcome_count = 24
    target_profile.outcome_count = 12
    target_profile.confidence_score = 0.15

    target_profile.meta_transfer_history.append(
        MetaTransferHistoryEntry(
            target_profile_id=target_profile.profile_id,
            source_profile_ids=[donor_weak.profile_id],
            decision_id="weak_edge_history",
            transfer_strength=0.2,
            outcome_score=0.05,
            similarity_by_source={donor_weak.profile_id: 0.85},
            source_shares={donor_weak.profile_id: 1.0},
            effective_weight_delta=0.1,
        )
    )

    candidates = engine._meta_transfer_candidates(
        target_profile,
        excluded_profile_ids={target_profile.profile_id},
    )

    assert candidates
    assert candidates[0][0].profile_id == donor_alternative.profile_id
    weak_candidate = next(
        item for item in candidates if item[0].profile_id == donor_weak.profile_id
    )
    assert weak_candidate[3]["weak_edge_penalty_applied"] is True
    assert weak_candidate[3]["penalty_multiplier"] == pytest.approx(0.6, abs=1e-6)
    assert weak_candidate[3]["edge_transfer_policy"] == "guarded_edge"
    assert weak_candidate[3]["edge_transfer_policy_multiplier"] == pytest.approx(
        0.9,
        abs=1e-6,
    )
    assert weak_candidate[4] < weak_candidate[3]["final_candidate_strength"]


def test_proven_donor_boost_prioritizes_effective_history() -> None:
    engine = CalibrationEngine(min_samples_for_calibration=999)

    target_profile = engine._get_or_create_profile(
        {
            "support_profile": "adhd_aware_support",
            "sequence_intent": BlockSequenceIntent.MASTERY_PATH.value,
            "evidence_pattern": EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS.value,
            "block_type": BlockType.WORKED_EXAMPLE.value,
        }
    )
    donor_proven = engine._get_or_create_profile(
        {
            "support_profile": "adhd_aware_support",
            "sequence_intent": BlockSequenceIntent.MASTERY_PATH.value,
            "evidence_pattern": EvidenceCombinationPattern.STAGNATION_PATTERN.value,
            "block_type": BlockType.GUIDED_PRACTICE.value,
        }
    )
    donor_unknown = engine._get_or_create_profile(
        {
            "support_profile": "adhd_aware_support",
            "sequence_intent": BlockSequenceIntent.MASTERY_PATH.value,
            "evidence_pattern": EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS.value,
            "block_type": BlockType.GUIDED_PRACTICE.value,
        }
    )
    donor_proven.confidence_score = 0.8
    donor_unknown.confidence_score = 0.8
    donor_proven.outcome_count = 20
    donor_unknown.outcome_count = 20

    for index in range(4):
        target_profile.meta_transfer_history.append(
            MetaTransferHistoryEntry(
                target_profile_id=target_profile.profile_id,
                source_profile_ids=[donor_proven.profile_id],
                decision_id=f"proven_boost_history_{index}",
                transfer_strength=0.2,
                outcome_score=0.82,
                similarity_by_source={donor_proven.profile_id: 0.7},
                source_shares={donor_proven.profile_id: 1.0},
                effective_weight_delta=0.08,
            )
        )

    candidates = engine._meta_transfer_candidates(
        target_profile,
        excluded_profile_ids={target_profile.profile_id},
    )

    assert candidates
    assert candidates[0][0].profile_id == donor_proven.profile_id
    proven_candidate = candidates[0]
    assert proven_candidate[3]["proven_donor_boost_applied"] is True
    assert proven_candidate[3]["boost_multiplier"] == pytest.approx(1.3, abs=1e-6)
    assert proven_candidate[3]["edge_transfer_policy"] == "trusted_edge"
    assert proven_candidate[3]["edge_transfer_policy_multiplier"] == pytest.approx(
        1.05,
        abs=1e-6,
    )
    assert proven_candidate[4] > proven_candidate[3]["final_candidate_strength"]


def test_steering_signals_absent_reverts_to_h91_order() -> None:
    engine = CalibrationEngine(min_samples_for_calibration=999)

    target_profile = engine._get_or_create_profile(
        {
            "support_profile": "adhd_aware_support",
            "sequence_intent": BlockSequenceIntent.MASTERY_PATH.value,
            "evidence_pattern": EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS.value,
            "block_type": BlockType.WORKED_EXAMPLE.value,
        }
    )
    donor_high_similarity = engine._get_or_create_profile(
        {
            "support_profile": "adhd_aware_support",
            "sequence_intent": BlockSequenceIntent.MASTERY_PATH.value,
            "evidence_pattern": EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS.value,
            "block_type": BlockType.GUIDED_PRACTICE.value,
        }
    )
    donor_lower_similarity = engine._get_or_create_profile(
        {
            "support_profile": "adhd_aware_support",
            "sequence_intent": BlockSequenceIntent.MASTERY_PATH.value,
            "evidence_pattern": EvidenceCombinationPattern.STAGNATION_PATTERN.value,
            "block_type": BlockType.GUIDED_PRACTICE.value,
        }
    )
    donor_high_similarity.confidence_score = 0.8
    donor_lower_similarity.confidence_score = 0.8
    donor_high_similarity.outcome_count = 20
    donor_lower_similarity.outcome_count = 20

    candidates = engine._meta_transfer_candidates(
        target_profile,
        excluded_profile_ids={target_profile.profile_id},
    )

    assert candidates
    assert candidates[0][0].profile_id == donor_high_similarity.profile_id
    assert all(item[3]["weak_edge_penalty_applied"] is False for item in candidates)
    assert all(item[3]["proven_donor_boost_applied"] is False for item in candidates)


def test_edge_seeking_boosts_insufficient_history_candidates_for_sparse_profile() -> None:
    engine = CalibrationEngine(min_samples_for_calibration=999)

    target_profile = engine._get_or_create_profile(
        {
            "support_profile": "adhd_aware_support",
            "sequence_intent": BlockSequenceIntent.MASTERY_PATH.value,
            "evidence_pattern": EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS.value,
            "block_type": BlockType.WORKED_EXAMPLE.value,
        }
    )
    target_profile.outcome_count = 1
    target_profile.confidence_score = 0.0

    donor_probe = engine._get_or_create_profile(
        {
            "support_profile": "adhd_aware_support",
            "sequence_intent": BlockSequenceIntent.MASTERY_PATH.value,
            "evidence_pattern": EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS.value,
            "block_type": BlockType.GUIDED_PRACTICE.value,
        }
    )
    donor_secondary = engine._get_or_create_profile(
        {
            "support_profile": "adhd_aware_support",
            "sequence_intent": BlockSequenceIntent.MASTERY_PATH.value,
            "evidence_pattern": EvidenceCombinationPattern.STAGNATION_PATTERN.value,
            "block_type": BlockType.GUIDED_PRACTICE.value,
        }
    )
    donor_probe.confidence_score = 0.8
    donor_secondary.confidence_score = 0.8
    donor_probe.outcome_count = 20
    donor_secondary.outcome_count = 18

    candidates = engine._meta_transfer_candidates(
        target_profile,
        excluded_profile_ids={target_profile.profile_id},
    )

    assert candidates
    probe_candidate = next(
        item for item in candidates if item[0].profile_id == donor_probe.profile_id
    )
    assert probe_candidate[3]["edge_seeking_applied"] is True
    assert probe_candidate[3]["edge_seeking_reason"] == (
        "probe_insufficient_history_for_sparse_target"
    )
    assert probe_candidate[3]["edge_seeking_multiplier"] == pytest.approx(1.15, abs=1e-6)
    assert probe_candidate[3]["edge_transfer_policy"] == "explore_edge"
    assert probe_candidate[3]["edge_transfer_policy_multiplier"] == pytest.approx(
        1.02,
        abs=1e-6,
    )
    assert probe_candidate[3]["adjusted_similarity_score"] > probe_candidate[3][
        "base_similarity_score"
    ]


def test_edge_seeking_partially_recovers_weak_edge_for_sparse_profile() -> None:
    engine = CalibrationEngine(min_samples_for_calibration=999)

    target_profile = engine._get_or_create_profile(
        {
            "support_profile": "adhd_aware_support",
            "sequence_intent": BlockSequenceIntent.MASTERY_PATH.value,
            "evidence_pattern": EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS.value,
            "block_type": BlockType.WORKED_EXAMPLE.value,
        }
    )
    target_profile.outcome_count = 1
    target_profile.confidence_score = 0.0

    donor_weak = engine._get_or_create_profile(
        {
            "support_profile": "adhd_aware_support",
            "sequence_intent": BlockSequenceIntent.MASTERY_PATH.value,
            "evidence_pattern": EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS.value,
            "block_type": BlockType.GUIDED_PRACTICE.value,
        }
    )
    donor_weak.confidence_score = 0.8
    donor_weak.outcome_count = 24

    target_profile.meta_transfer_history.append(
        MetaTransferHistoryEntry(
            target_profile_id=target_profile.profile_id,
            source_profile_ids=[donor_weak.profile_id],
            decision_id="weak_edge_recovery_history",
            transfer_strength=0.2,
            outcome_score=0.05,
            similarity_by_source={donor_weak.profile_id: 0.85},
            source_shares={donor_weak.profile_id: 1.0},
            effective_weight_delta=0.1,
        )
    )

    candidates = engine._meta_transfer_candidates(
        target_profile,
        excluded_profile_ids={target_profile.profile_id},
    )

    assert candidates
    weak_candidate = candidates[0]
    assert weak_candidate[3]["weak_edge_penalty_applied"] is True
    assert weak_candidate[3]["edge_seeking_applied"] is True
    assert weak_candidate[3]["edge_seeking_reason"] == "recover_weak_edge_for_sparse_target"
    assert weak_candidate[3]["edge_seeking_multiplier"] == pytest.approx(1.2, abs=1e-6)
    assert weak_candidate[3]["edge_transfer_policy"] == "recovery_edge"
    assert weak_candidate[3]["edge_transfer_policy_multiplier"] == pytest.approx(
        0.98,
        abs=1e-6,
    )
    assert weak_candidate[3]["adjusted_similarity_score"] == pytest.approx(
        0.612,
        abs=1e-3,
    )


def test_edge_seeking_stays_off_when_proven_donor_exists() -> None:
    engine = CalibrationEngine(min_samples_for_calibration=999)

    target_profile = engine._get_or_create_profile(
        {
            "support_profile": "adhd_aware_support",
            "sequence_intent": BlockSequenceIntent.MASTERY_PATH.value,
            "evidence_pattern": EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS.value,
            "block_type": BlockType.WORKED_EXAMPLE.value,
        }
    )
    target_profile.outcome_count = 1
    target_profile.confidence_score = 0.0

    donor_proven = engine._get_or_create_profile(
        {
            "support_profile": "adhd_aware_support",
            "sequence_intent": BlockSequenceIntent.MASTERY_PATH.value,
            "evidence_pattern": EvidenceCombinationPattern.STAGNATION_PATTERN.value,
            "block_type": BlockType.GUIDED_PRACTICE.value,
        }
    )
    donor_unknown = engine._get_or_create_profile(
        {
            "support_profile": "adhd_aware_support",
            "sequence_intent": BlockSequenceIntent.MASTERY_PATH.value,
            "evidence_pattern": EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS.value,
            "block_type": BlockType.GUIDED_PRACTICE.value,
        }
    )
    donor_proven.confidence_score = 0.8
    donor_unknown.confidence_score = 0.8
    donor_proven.outcome_count = 24
    donor_unknown.outcome_count = 20

    for index in range(5):
        target_profile.meta_transfer_history.append(
            MetaTransferHistoryEntry(
                target_profile_id=target_profile.profile_id,
                source_profile_ids=[donor_proven.profile_id],
                decision_id=f"proven_edge_{index}",
                transfer_strength=0.2,
                outcome_score=0.84,
                similarity_by_source={donor_proven.profile_id: 0.7},
                source_shares={donor_proven.profile_id: 1.0},
                effective_weight_delta=0.08,
            )
        )

    candidates = engine._meta_transfer_candidates(
        target_profile,
        excluded_profile_ids={target_profile.profile_id},
    )

    assert candidates
    assert candidates[0][0].profile_id == donor_proven.profile_id
    assert all(item[3]["edge_seeking_applied"] is False for item in candidates)


def test_low_effectiveness_edge_gets_cautious_policy() -> None:
    engine = CalibrationEngine(min_samples_for_calibration=999)

    target_profile = engine._get_or_create_profile(
        {
            "support_profile": "adhd_aware_support",
            "sequence_intent": BlockSequenceIntent.MASTERY_PATH.value,
            "evidence_pattern": EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS.value,
            "block_type": BlockType.WORKED_EXAMPLE.value,
        }
    )
    donor_cautious = engine._get_or_create_profile(
        {
            "support_profile": "adhd_aware_support",
            "sequence_intent": BlockSequenceIntent.MASTERY_PATH.value,
            "evidence_pattern": EvidenceCombinationPattern.STAGNATION_PATTERN.value,
            "block_type": BlockType.GUIDED_PRACTICE.value,
        }
    )
    donor_cautious.confidence_score = 0.8
    donor_cautious.outcome_count = 20

    for index in range(4):
        target_profile.meta_transfer_history.append(
            MetaTransferHistoryEntry(
                target_profile_id=target_profile.profile_id,
                source_profile_ids=[donor_cautious.profile_id],
                decision_id=f"low_effectiveness_{index}",
                transfer_strength=0.2,
                outcome_score=0.35,
                similarity_by_source={donor_cautious.profile_id: 0.7},
                source_shares={donor_cautious.profile_id: 1.0},
                effective_weight_delta=0.08,
            )
        )

    candidates = engine._meta_transfer_candidates(
        target_profile,
        excluded_profile_ids={target_profile.profile_id},
    )

    cautious_candidate = next(
        item for item in candidates if item[0].profile_id == donor_cautious.profile_id
    )
    assert cautious_candidate[3]["edge_transfer_policy"] == "cautious_edge"
    assert cautious_candidate[3]["edge_transfer_policy_multiplier"] == pytest.approx(
        0.96,
        abs=1e-6,
    )
    assert cautious_candidate[4] < cautious_candidate[3]["final_candidate_strength"]


def test_planner_and_decision_record_expose_h92_steering_signals() -> None:
    engine = CalibrationEngine(min_samples_for_calibration=1)

    initial_plan = build_teaching_plan(_steering_request(), calibration_engine=engine)
    assert initial_plan.calibration_context is not None
    target_profile_id = initial_plan.calibration_context.calibration_profile_id
    assert target_profile_id is not None

    target_profile = engine.calibration_profiles[target_profile_id]
    donor_profile = engine._get_or_create_profile(
        {
            **target_profile.stratification_dimensions,
            "evidence_pattern": EvidenceCombinationPattern.STAGNATION_PATTERN.value,
            "block_type": (
                BlockType.GUIDED_PRACTICE.value
                if target_profile.stratification_dimensions.get("block_type")
                != BlockType.GUIDED_PRACTICE.value
                else BlockType.CONCEPT_CHECK.value
            ),
        }
    )
    donor_profile.confidence_score = 0.8
    donor_profile.outcome_count = 20
    target_profile.meta_transfer_history.append(
        MetaTransferHistoryEntry(
            target_profile_id=target_profile.profile_id,
            source_profile_ids=[donor_profile.profile_id],
            decision_id="planner_boost_history",
            transfer_strength=0.2,
            outcome_score=0.84,
            similarity_by_source={donor_profile.profile_id: 0.7},
            source_shares={donor_profile.profile_id: 1.0},
            effective_weight_delta=0.07,
        )
    )

    plan = build_teaching_plan(_steering_request(), calibration_engine=engine)

    assert plan.calibration_context is not None
    assert plan.enriched_paths[0].steering_proven_donor_boost_applied is True
    assert plan.calibration_context.steering_proven_donor_boost_applied is True
    assert donor_profile.profile_id in plan.calibration_context.meta_transfer_source_steering_factors
    assert (
        plan.calibration_context.meta_transfer_source_steering_factors[donor_profile.profile_id][
            "proven_donor_boost_applied"
        ]
        is True
    )
    assert donor_profile.profile_id in plan.calibration_context.meta_transfer_source_adaptive_caps
    assert (
        plan.calibration_context.meta_transfer_source_adaptive_caps[donor_profile.profile_id][
            "reason"
        ]
        == "insufficient_history"
    )
    assert (
        plan.calibration_context.adaptive_cap_distribution["insufficient_history"]["count"]
        >= 1
    )
    assert engine.decision_log[-1].steering_proven_donor_boost_applied is True


def test_runtime_context_exposes_trusted_edge_policy_distribution() -> None:
    engine = CalibrationEngine(min_samples_for_calibration=1)

    initial_plan = build_teaching_plan(_steering_request(), calibration_engine=engine)
    assert initial_plan.calibration_context is not None
    target_profile_id = initial_plan.calibration_context.calibration_profile_id
    assert target_profile_id is not None

    target_profile = engine.calibration_profiles[target_profile_id]
    donor_profile = engine._get_or_create_profile(
        {
            **target_profile.stratification_dimensions,
            "evidence_pattern": EvidenceCombinationPattern.STAGNATION_PATTERN.value,
            "block_type": (
                BlockType.GUIDED_PRACTICE.value
                if target_profile.stratification_dimensions.get("block_type")
                != BlockType.GUIDED_PRACTICE.value
                else BlockType.CONCEPT_CHECK.value
            ),
        }
    )
    donor_profile.confidence_score = 0.8
    donor_profile.outcome_count = 24

    for index in range(5):
        target_profile.meta_transfer_history.append(
            MetaTransferHistoryEntry(
                target_profile_id=target_profile.profile_id,
                source_profile_ids=[donor_profile.profile_id],
                decision_id=f"trusted_policy_{index}",
                transfer_strength=0.2,
                outcome_score=0.84,
                similarity_by_source={donor_profile.profile_id: 0.7},
                source_shares={donor_profile.profile_id: 1.0},
                effective_weight_delta=0.07,
            )
        )

    plan = build_teaching_plan(_steering_request(), calibration_engine=engine)

    assert plan.calibration_context is not None
    assert plan.enriched_paths[0].steering_edge_policy_applied is True
    assert plan.calibration_context.steering_edge_policy_applied is True
    assert plan.calibration_context.edge_policy_distribution["trusted_edge"] >= 1
    assert (
        plan.calibration_context.meta_transfer_source_steering_factors[donor_profile.profile_id][
            "edge_transfer_policy"
        ]
        == "trusted_edge"
    )
    assert engine.decision_log[-1].steering_edge_policy_applied is True
    assert donor_profile.profile_id in engine.decision_log[-1].meta_transfer_source_adaptive_caps


def test_planner_and_decision_record_expose_phase4_edge_seeking_signals() -> None:
    engine = CalibrationEngine(min_samples_for_calibration=1)

    initial_plan = build_teaching_plan(_steering_request(), calibration_engine=engine)
    assert initial_plan.calibration_context is not None
    target_profile_id = initial_plan.calibration_context.calibration_profile_id
    assert target_profile_id is not None

    target_profile = engine.calibration_profiles[target_profile_id]
    donor_profile = engine._get_or_create_profile(
        {
            **target_profile.stratification_dimensions,
            "block_type": (
                BlockType.GUIDED_PRACTICE.value
                if target_profile.stratification_dimensions.get("block_type")
                != BlockType.GUIDED_PRACTICE.value
                else BlockType.CONCEPT_CHECK.value
            ),
        }
    )
    donor_profile.confidence_score = 0.8
    donor_profile.outcome_count = 20

    plan = build_teaching_plan(_steering_request(), calibration_engine=engine)

    assert plan.calibration_context is not None
    assert plan.enriched_paths[0].steering_edge_seeking_applied is True
    assert plan.calibration_context.steering_edge_seeking_applied is True
    assert (
        plan.calibration_context.meta_transfer_source_steering_factors[donor_profile.profile_id][
            "edge_seeking_applied"
        ]
        is True
    )
    assert engine.decision_log[-1].steering_edge_seeking_applied is True


def test_edge_effectiveness_history_weights_multi_source_outcomes() -> None:
    engine = CalibrationEngine(min_samples_for_calibration=999)

    target_profile = engine._get_or_create_profile(
        {
            "support_profile": "adhd_aware_support",
            "sequence_intent": BlockSequenceIntent.MASTERY_PATH.value,
            "evidence_pattern": EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS.value,
            "block_type": BlockType.WORKED_EXAMPLE.value,
        }
    )
    donor_a = engine._get_or_create_profile(
        {
            "support_profile": "adhd_aware_support",
            "sequence_intent": BlockSequenceIntent.MASTERY_PATH.value,
            "evidence_pattern": EvidenceCombinationPattern.STAGNATION_PATTERN.value,
            "block_type": BlockType.GUIDED_PRACTICE.value,
        }
    )
    donor_b = engine._get_or_create_profile(
        {
            "support_profile": "adhd_aware_support",
            "sequence_intent": BlockSequenceIntent.MASTERY_PATH.value,
            "evidence_pattern": EvidenceCombinationPattern.CONCEPT_CONFUSION.value,
            "block_type": BlockType.CONCEPT_CHECK.value,
        }
    )

    target_profile.meta_transfer_history.append(
        MetaTransferHistoryEntry(
            target_profile_id=target_profile.profile_id,
            source_profile_ids=[donor_a.profile_id, donor_b.profile_id],
            decision_id="multi_source_weighted_history",
            transfer_strength=0.3,
            outcome_score=0.5,
            similarity_by_source={
                donor_a.profile_id: 0.7,
                donor_b.profile_id: 0.5,
            },
            source_shares={
                donor_a.profile_id: 0.6,
                donor_b.profile_id: 0.4,
            },
            effective_weight_delta=0.08,
        )
    )

    assert engine._edge_effectiveness_history(
        donor_a.profile_id,
        target_profile.profile_id,
    ) == pytest.approx([0.3], abs=1e-6)
    assert engine._edge_effectiveness_history(
        donor_b.profile_id,
        target_profile.profile_id,
    ) == pytest.approx([0.2], abs=1e-6)
    assert engine._transfer_effectiveness_for_pair(
        donor_a.profile_id,
        target_profile.profile_id,
    ) == pytest.approx(0.3, abs=1e-6)
    assert engine._transfer_effectiveness_for_pair(
        donor_b.profile_id,
        target_profile.profile_id,
    ) == pytest.approx(0.2, abs=1e-6)


def test_weak_edge_gets_low_adaptive_cap() -> None:
    engine = CalibrationEngine(min_samples_for_calibration=999)

    target_profile = engine._get_or_create_profile(
        {
            "support_profile": "adhd_aware_support",
            "sequence_intent": BlockSequenceIntent.MASTERY_PATH.value,
            "evidence_pattern": EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS.value,
            "block_type": BlockType.WORKED_EXAMPLE.value,
        }
    )
    donor_profile = engine._get_or_create_profile(
        {
            "support_profile": "adhd_aware_support",
            "sequence_intent": BlockSequenceIntent.MASTERY_PATH.value,
            "evidence_pattern": EvidenceCombinationPattern.STAGNATION_PATTERN.value,
            "block_type": BlockType.GUIDED_PRACTICE.value,
        }
    )

    for index in range(5):
        target_profile.meta_transfer_history.append(
            MetaTransferHistoryEntry(
                target_profile_id=target_profile.profile_id,
                source_profile_ids=[donor_profile.profile_id],
                decision_id=f"weak_cap_{index}",
                transfer_strength=0.25,
                outcome_score=0.1,
                similarity_by_source={donor_profile.profile_id: 0.7},
                source_shares={donor_profile.profile_id: 1.0},
                effective_weight_delta=0.05,
            )
        )

    cap, reason = engine._adaptive_transfer_max_blend(
        donor_profile.profile_id,
        target_profile.profile_id,
    )

    assert cap == pytest.approx(0.2, abs=1e-6)
    assert reason == "weak_edge"


def test_strong_edge_gets_high_adaptive_cap() -> None:
    engine = CalibrationEngine(min_samples_for_calibration=999)

    target_profile = engine._get_or_create_profile(
        {
            "support_profile": "adhd_aware_support",
            "sequence_intent": BlockSequenceIntent.MASTERY_PATH.value,
            "evidence_pattern": EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS.value,
            "block_type": BlockType.WORKED_EXAMPLE.value,
        }
    )
    donor_profile = engine._get_or_create_profile(
        {
            "support_profile": "adhd_aware_support",
            "sequence_intent": BlockSequenceIntent.MASTERY_PATH.value,
            "evidence_pattern": EvidenceCombinationPattern.STAGNATION_PATTERN.value,
            "block_type": BlockType.GUIDED_PRACTICE.value,
        }
    )

    for index in range(5):
        target_profile.meta_transfer_history.append(
            MetaTransferHistoryEntry(
                target_profile_id=target_profile.profile_id,
                source_profile_ids=[donor_profile.profile_id],
                decision_id=f"strong_cap_{index}",
                transfer_strength=0.25,
                outcome_score=0.82,
                similarity_by_source={donor_profile.profile_id: 0.7},
                source_shares={donor_profile.profile_id: 1.0},
                effective_weight_delta=0.05,
            )
        )

    cap, reason = engine._adaptive_transfer_max_blend(
        donor_profile.profile_id,
        target_profile.profile_id,
    )

    assert cap == pytest.approx(0.45, abs=1e-6)
    assert reason == "strong_edge"


def test_insufficient_history_defaults_to_conservative_cap() -> None:
    engine = CalibrationEngine(min_samples_for_calibration=999)

    target_profile = engine._get_or_create_profile(
        {
            "support_profile": "adhd_aware_support",
            "sequence_intent": BlockSequenceIntent.MASTERY_PATH.value,
            "evidence_pattern": EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS.value,
            "block_type": BlockType.WORKED_EXAMPLE.value,
        }
    )
    donor_profile = engine._get_or_create_profile(
        {
            "support_profile": "adhd_aware_support",
            "sequence_intent": BlockSequenceIntent.MASTERY_PATH.value,
            "evidence_pattern": EvidenceCombinationPattern.STAGNATION_PATTERN.value,
            "block_type": BlockType.GUIDED_PRACTICE.value,
        }
    )

    target_profile.meta_transfer_history.append(
        MetaTransferHistoryEntry(
            target_profile_id=target_profile.profile_id,
            source_profile_ids=[donor_profile.profile_id],
            decision_id="insufficient_history_cap",
            transfer_strength=0.25,
            outcome_score=0.5,
            similarity_by_source={donor_profile.profile_id: 0.7},
            source_shares={donor_profile.profile_id: 1.0},
            effective_weight_delta=0.05,
        )
    )

    cap, reason = engine._adaptive_transfer_max_blend(
        donor_profile.profile_id,
        target_profile.profile_id,
    )

    assert cap == pytest.approx(0.3, abs=1e-6)
    assert reason == "insufficient_history"


def test_meta_transfer_prior_applies_adaptive_caps_to_strength_and_audit() -> None:
    engine = CalibrationEngine(min_samples_for_calibration=999)

    target_profile = engine._get_or_create_profile(
        {
            "support_profile": "adhd_aware_support",
            "sequence_intent": BlockSequenceIntent.MASTERY_PATH.value,
            "evidence_pattern": EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS.value,
            "block_type": BlockType.WORKED_EXAMPLE.value,
        }
    )
    donor_profile = engine._get_or_create_profile(
        {
            "support_profile": "adhd_aware_support",
            "sequence_intent": BlockSequenceIntent.MASTERY_PATH.value,
            "evidence_pattern": EvidenceCombinationPattern.STAGNATION_PATTERN.value,
            "block_type": BlockType.GUIDED_PRACTICE.value,
        }
    )
    donor_profile.confidence_score = 0.9
    donor_profile.outcome_count = 24

    for index in range(5):
        target_profile.meta_transfer_history.append(
            MetaTransferHistoryEntry(
                target_profile_id=target_profile.profile_id,
                source_profile_ids=[donor_profile.profile_id],
                decision_id=f"prior_cap_{index}",
                transfer_strength=0.25,
                outcome_score=0.1,
                similarity_by_source={donor_profile.profile_id: 0.85},
                source_shares={donor_profile.profile_id: 1.0},
                effective_weight_delta=0.05,
            )
        )

    (
        _transfer_weights,
        meta_transfer_strength,
        source_profiles,
        source_shares,
        steering_factors,
        adaptive_caps,
    ) = engine._meta_transfer_prior(
        target_profile,
        excluded_profile_ids={target_profile.profile_id},
    )

    assert source_profiles == [donor_profile.profile_id]
    assert source_shares == {donor_profile.profile_id: pytest.approx(1.0, abs=1e-6)}
    assert meta_transfer_strength == pytest.approx(0.2, abs=1e-6)
    assert adaptive_caps[donor_profile.profile_id]["cap"] == pytest.approx(0.2, abs=1e-6)
    assert adaptive_caps[donor_profile.profile_id]["reason"] == "weak_edge"
    assert steering_factors[donor_profile.profile_id]["adaptive_transfer_cap"] == pytest.approx(
        0.2,
        abs=1e-6,
    )
    assert steering_factors[donor_profile.profile_id]["adaptive_transfer_cap_reason"] == (
        "weak_edge"
    )
