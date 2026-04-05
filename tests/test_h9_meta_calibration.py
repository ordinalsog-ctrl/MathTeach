from pathlib import Path

import pytest

from mathteach.models import (
    BlockSequenceIntent,
    BlockType,
    DecisionRecord,
    EnrichedPathEvaluation,
    EvidenceCombinationPattern,
    MetaTransferHistoryEntry,
    OutcomeMetrics,
    RawBlockObservation,
    SessionRequest,
)
from mathteach.services.calibration_engine import CalibrationEngine
from mathteach.services.calibration_store import CalibrationStore
from mathteach.services.planner import build_teaching_plan, record_decision_outcome


def _meta_request() -> SessionRequest:
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


def test_meta_transfer_blends_from_related_profile_for_sparse_exact_context() -> None:
    engine = CalibrationEngine(min_samples_for_calibration=999)

    donor_profile = engine._get_or_create_profile(
        {
            "support_profile": "adhd_aware_support",
            "sequence_intent": BlockSequenceIntent.MASTERY_PATH.value,
            "evidence_pattern": EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS.value,
            "block_type": BlockType.GUIDED_PRACTICE.value,
        }
    )
    donor_profile.current_weights = donor_profile.current_weights.model_copy(
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
    donor_profile.confidence_score = 0.8
    donor_profile.outcome_count = 20

    unrelated_profile = engine._get_or_create_profile(
        {
            "support_profile": "language_sensitive_support",
            "sequence_intent": BlockSequenceIntent.MASTERY_PATH.value,
            "evidence_pattern": EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS.value,
            "block_type": BlockType.GUIDED_PRACTICE.value,
        }
    )
    unrelated_profile.current_weights = unrelated_profile.current_weights.model_copy(
        update={
            "adjusted_weights": {
                "heuristic": 0.05,
                "goal_alignment": 0.7,
                "history_alignment": 0.1,
                "evidence_continuity": 0.05,
                "profile_match": 0.05,
                "pilot_data_adjustment": 0.05,
            }
        }
    )
    unrelated_profile.confidence_score = 1.0
    unrelated_profile.outcome_count = 40

    enriched = engine.apply_to_enriched_paths(
        [
            EnrichedPathEvaluation(
                path_id="path_worked_example",
                block_types=[BlockType.WORKED_EXAMPLE],
                raw_score=0.5,
                total_score=0.5,
                score_breakdown={
                    "heuristic": 0.8,
                    "goal_alignment": 0.2,
                    "history_alignment": 0.1,
                    "evidence_continuity": 0.1,
                    "profile_match": 0.1,
                    "pilot_data_adjustment": 0.1,
                },
            )
        ],
        active_supports=["adhd_aware_support"],
        sequence_intent=BlockSequenceIntent.MASTERY_PATH,
        evidence_patterns=[EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS],
        current_block_type=BlockType.WORKED_EXAMPLE,
    )

    selected_path = enriched[0]

    assert selected_path.calibration_profile_id is not None
    assert BlockType.WORKED_EXAMPLE.value in selected_path.calibration_profile_id
    assert selected_path.meta_transfer_strength is not None
    assert selected_path.meta_transfer_strength > 0.0
    assert selected_path.meta_transfer_source_profiles == [donor_profile.profile_id]
    assert selected_path.meta_transfer_source_shares == {donor_profile.profile_id: 1.0}
    assert selected_path.meta_transfer_weight_delta is not None
    assert selected_path.meta_transfer_weight_delta > 0.0
    assert selected_path.meta_transfer_was_effective is True
    assert unrelated_profile.profile_id not in selected_path.meta_transfer_source_profiles
    assert (
        selected_path.calibration_weights_used["heuristic"]
        > engine.current_weights.get_current_weights()["heuristic"]
    )


def test_meta_transfer_requires_support_overlap() -> None:
    engine = CalibrationEngine(min_samples_for_calibration=999)

    unrelated_profile = engine._get_or_create_profile(
        {
            "support_profile": "language_sensitive_support",
            "sequence_intent": BlockSequenceIntent.MASTERY_PATH.value,
            "evidence_pattern": EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS.value,
            "block_type": BlockType.GUIDED_PRACTICE.value,
        }
    )
    unrelated_profile.current_weights = unrelated_profile.current_weights.model_copy(
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
    unrelated_profile.confidence_score = 0.8
    unrelated_profile.outcome_count = 20

    enriched = engine.apply_to_enriched_paths(
        [
            EnrichedPathEvaluation(
                path_id="path_worked_example",
                block_types=[BlockType.WORKED_EXAMPLE],
                raw_score=0.5,
                total_score=0.5,
                score_breakdown={
                    "heuristic": 0.8,
                    "goal_alignment": 0.2,
                    "history_alignment": 0.1,
                    "evidence_continuity": 0.1,
                    "profile_match": 0.1,
                    "pilot_data_adjustment": 0.1,
                },
            )
        ],
        active_supports=["adhd_aware_support"],
        sequence_intent=BlockSequenceIntent.MASTERY_PATH,
        evidence_patterns=[EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS],
        current_block_type=BlockType.WORKED_EXAMPLE,
    )

    selected_path = enriched[0]
    expected_global = {
        key: round(value, 4)
        for key, value in engine.current_weights.get_current_weights().items()
    }

    assert selected_path.meta_transfer_source_profiles == []
    assert selected_path.meta_transfer_source_shares == {}
    assert selected_path.meta_transfer_strength == 0.0
    assert selected_path.meta_transfer_weight_delta == 0.0
    assert selected_path.meta_transfer_was_effective is False
    assert selected_path.calibration_weights_used == expected_global


def test_planner_exposes_meta_transfer_diagnostics() -> None:
    engine = CalibrationEngine(min_samples_for_calibration=1)

    initial_plan = build_teaching_plan(_meta_request(), calibration_engine=engine)
    assert initial_plan.calibration_context is not None
    exact_profile_id = initial_plan.calibration_context.calibration_profile_id
    assert exact_profile_id is not None

    exact_profile = engine.calibration_profiles[exact_profile_id]
    sibling_dimensions = {
        **exact_profile.stratification_dimensions,
        "block_type": (
            BlockType.GUIDED_PRACTICE.value
            if exact_profile.stratification_dimensions.get("block_type")
            != BlockType.GUIDED_PRACTICE.value
            else BlockType.CONCEPT_CHECK.value
        ),
    }
    donor_profile = engine._get_or_create_profile(sibling_dimensions)
    donor_profile.current_weights = donor_profile.current_weights.model_copy(
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
    donor_profile.confidence_score = 0.8
    donor_profile.outcome_count = 20

    plan = build_teaching_plan(_meta_request(), calibration_engine=engine)

    assert plan.calibration_context is not None
    assert plan.enriched_paths[0].meta_transfer_source_profiles == [donor_profile.profile_id]
    assert plan.calibration_context.meta_transfer_source_profiles == [
        donor_profile.profile_id
    ]
    assert (
        plan.calibration_context.meta_transfer_strength
        == plan.enriched_paths[0].meta_transfer_strength
    )
    assert (
        plan.calibration_context.meta_transfer_source_shares
        == plan.enriched_paths[0].meta_transfer_source_shares
    )
    assert (
        plan.calibration_context.meta_transfer_weight_delta
        == plan.enriched_paths[0].meta_transfer_weight_delta
    )
    assert (
        plan.calibration_context.meta_transfer_was_effective
        == plan.enriched_paths[0].meta_transfer_was_effective
    )
    assert plan.calibration_context.meta_transfer_strength is not None
    assert plan.calibration_context.meta_transfer_strength > 0.0
    assert plan.calibration_context.meta_transfer_weight_delta is not None
    assert plan.calibration_context.meta_transfer_weight_delta > 0.0
    assert plan.calibration_context.meta_transfer_was_effective is True


def test_meta_transfer_history_persists_after_outcome(tmp_path: Path) -> None:
    store_path = tmp_path / "calibration.json"
    engine = CalibrationEngine(
        store=CalibrationStore(store_path),
        autosave_threshold=1,
        min_samples_for_calibration=1,
    )

    initial_plan = build_teaching_plan(_meta_request(), calibration_engine=engine)
    assert initial_plan.calibration_context is not None
    target_profile_id = initial_plan.calibration_context.calibration_profile_id
    assert target_profile_id is not None

    target_profile = engine.calibration_profiles[target_profile_id]
    donor_dimensions = {
        **target_profile.stratification_dimensions,
        "block_type": (
            BlockType.GUIDED_PRACTICE.value
            if target_profile.stratification_dimensions.get("block_type")
            != BlockType.GUIDED_PRACTICE.value
            else BlockType.CONCEPT_CHECK.value
        ),
    }
    donor_profile = engine._get_or_create_profile(donor_dimensions)
    donor_profile.confidence_score = 0.8
    donor_profile.outcome_count = 20
    donor_profile.current_weights = donor_profile.current_weights.model_copy(
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

    plan = build_teaching_plan(_meta_request(), calibration_engine=engine)
    assert plan.calibration_context is not None
    assert plan.calibration_context.meta_transfer_source_profiles == [donor_profile.profile_id]
    assert plan.calibration_context.meta_transfer_source_shares == {
        donor_profile.profile_id: 1.0
    }
    assert plan.calibration_context.meta_transfer_was_effective is True

    updated = record_decision_outcome(
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
    assert updated is True

    target_profile = engine.calibration_profiles[target_profile_id]
    assert donor_profile.profile_id in target_profile.meta_transfer_links
    link = target_profile.meta_transfer_links[donor_profile.profile_id]
    assert link.use_count == 1
    assert link.average_outcome_score > 0.0
    assert link.last_transfer_strength == pytest.approx(
        plan.calibration_context.meta_transfer_strength,
        abs=1e-6,
    )
    assert target_profile.meta_transfer_history
    latest_entry = target_profile.meta_transfer_history[-1]
    assert latest_entry.source_shares == {donor_profile.profile_id: 1.0}
    assert latest_entry.effective_weight_delta == pytest.approx(
        plan.calibration_context.meta_transfer_weight_delta,
        abs=1e-6,
    )
    summary = engine.get_profile_summary(target_profile_id)
    assert summary is not None
    assert summary["meta_transfer_links"][0]["source_profile_id"] == donor_profile.profile_id
    assert summary["meta_transfer_history_length"] >= 1

    engine.force_save()
    reloaded = CalibrationStore(store_path).load()
    reloaded_profile = reloaded.calibration_profiles[target_profile_id]
    assert donor_profile.profile_id in reloaded_profile.meta_transfer_links
    assert reloaded_profile.meta_transfer_links[donor_profile.profile_id].use_count == 1
    assert reloaded_profile.meta_transfer_history


def test_meta_transfer_prior_can_be_nonzero_while_effective_delta_is_zero() -> None:
    engine = CalibrationEngine(min_samples_for_calibration=999)

    exact_profile = engine._get_or_create_profile(
        {
            "support_profile": "adhd_aware_support",
            "sequence_intent": BlockSequenceIntent.MASTERY_PATH.value,
            "evidence_pattern": EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS.value,
            "block_type": BlockType.WORKED_EXAMPLE.value,
        }
    )
    exact_profile.current_weights = exact_profile.current_weights.model_copy(
        update={
            "adjusted_weights": {
                "heuristic": 0.1,
                "goal_alignment": 0.5,
                "history_alignment": 0.1,
                "evidence_continuity": 0.1,
                "profile_match": 0.1,
                "pilot_data_adjustment": 0.1,
            }
        }
    )
    exact_profile.confidence_score = 1.0
    exact_profile.outcome_count = 60

    donor_profile = engine._get_or_create_profile(
        {
            "support_profile": "adhd_aware_support",
            "sequence_intent": BlockSequenceIntent.MASTERY_PATH.value,
            "evidence_pattern": EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS.value,
            "block_type": BlockType.GUIDED_PRACTICE.value,
        }
    )
    donor_profile.current_weights = donor_profile.current_weights.model_copy(
        update={
            "adjusted_weights": {
                "heuristic": 0.8,
                "goal_alignment": 0.05,
                "history_alignment": 0.05,
                "evidence_continuity": 0.03,
                "profile_match": 0.04,
                "pilot_data_adjustment": 0.03,
            }
        }
    )
    donor_profile.confidence_score = 0.8
    donor_profile.outcome_count = 30

    result = engine.apply_to_enriched_paths(
        [
            EnrichedPathEvaluation(
                path_id="path_exact_lock",
                block_types=[BlockType.WORKED_EXAMPLE],
                raw_score=0.5,
                total_score=0.5,
                score_breakdown={
                    "heuristic": 0.5,
                    "goal_alignment": 0.5,
                    "history_alignment": 0.1,
                    "evidence_continuity": 0.1,
                    "profile_match": 0.1,
                    "pilot_data_adjustment": 0.1,
                },
            )
        ],
        active_supports=["adhd_aware_support"],
        sequence_intent=BlockSequenceIntent.MASTERY_PATH,
        evidence_patterns=[EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS],
        current_block_type=BlockType.WORKED_EXAMPLE,
    )[0]

    assert result.meta_transfer_strength is not None
    assert result.meta_transfer_strength > 0.0
    assert result.meta_transfer_source_profiles == [donor_profile.profile_id]
    assert result.meta_transfer_source_shares == {donor_profile.profile_id: 1.0}
    assert result.meta_transfer_weight_delta == 0.0
    assert result.meta_transfer_was_effective is False
    assert result.calibration_weights_used == exact_profile.current_weights.summary()

    record = engine.log_decision(
        DecisionRecord(
            session_id="meta_exact_lock",
            current_block_type=BlockType.WORKED_EXAMPLE,
            selected_block_type=BlockType.WORKED_EXAMPLE,
            evidence_patterns=[EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS],
            active_supports=["adhd_aware_support"],
            sequence_intent=BlockSequenceIntent.MASTERY_PATH,
            available_candidate_paths=[result.path_id],
            chosen_path_id=result.path_id,
            chosen_path_score=result.total_score,
            chosen_path_score_breakdown=result.score_breakdown,
            calibration_profile_id=result.calibration_profile_id,
            calibration_profile_confidence=result.calibration_profile_confidence,
            meta_transfer_strength=result.meta_transfer_strength,
            meta_transfer_source_profiles=result.meta_transfer_source_profiles,
            meta_transfer_source_shares=result.meta_transfer_source_shares,
            meta_transfer_weight_delta=result.meta_transfer_weight_delta,
            meta_transfer_was_effective=result.meta_transfer_was_effective,
        )
    )
    outcome = OutcomeMetrics(
        mastery_gain_estimate=0.8,
        confidence_change=0.1,
        observed_engagement="high",
        error_rate_trend="improving",
        accuracy_estimate=0.9,
    )
    assert engine.update_outcome(record.decision_id, outcome) is True
    assert donor_profile.profile_id not in exact_profile.meta_transfer_links
    assert not exact_profile.meta_transfer_history


def test_multi_source_meta_transfer_attribution_uses_source_shares() -> None:
    engine = CalibrationEngine(min_samples_for_calibration=999)

    target_profile = engine._get_or_create_profile(
        {
            "support_profile": "adhd_aware_support+dyscalculia_aware_support",
            "sequence_intent": BlockSequenceIntent.MASTERY_PATH.value,
            "evidence_pattern": EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS.value,
            "block_type": BlockType.WORKED_EXAMPLE.value,
        }
    )
    target_profile.outcome_count = 2
    target_profile.confidence_score = 0.0

    donor_a = engine._get_or_create_profile(
        {
            "support_profile": "adhd_aware_support",
            "sequence_intent": BlockSequenceIntent.MASTERY_PATH.value,
            "evidence_pattern": EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS.value,
            "block_type": BlockType.GUIDED_PRACTICE.value,
        }
    )
    donor_b = engine._get_or_create_profile(
        {
            "support_profile": "dyscalculia_aware_support",
            "sequence_intent": BlockSequenceIntent.MASTERY_PATH.value,
            "evidence_pattern": EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS.value,
            "block_type": BlockType.GUIDED_PRACTICE.value,
        }
    )
    donor_a.current_weights = donor_a.current_weights.model_copy(
        update={
            "adjusted_weights": {
                "heuristic": 0.8,
                "goal_alignment": 0.05,
                "history_alignment": 0.05,
                "evidence_continuity": 0.04,
                "profile_match": 0.03,
                "pilot_data_adjustment": 0.03,
            }
        }
    )
    donor_b.current_weights = donor_b.current_weights.model_copy(
        update={
            "adjusted_weights": {
                "heuristic": 0.3,
                "goal_alignment": 0.4,
                "history_alignment": 0.1,
                "evidence_continuity": 0.08,
                "profile_match": 0.06,
                "pilot_data_adjustment": 0.06,
            }
        }
    )
    donor_a.outcome_count = 30
    donor_b.outcome_count = 12
    donor_a.confidence_score = 0.9
    donor_b.confidence_score = 0.5

    result = engine.apply_to_enriched_paths(
        [
            EnrichedPathEvaluation(
                path_id="path_multi_source",
                block_types=[BlockType.WORKED_EXAMPLE],
                raw_score=0.5,
                total_score=0.5,
                score_breakdown={
                    "heuristic": 0.5,
                    "goal_alignment": 0.5,
                    "history_alignment": 0.1,
                    "evidence_continuity": 0.1,
                    "profile_match": 0.1,
                    "pilot_data_adjustment": 0.1,
                },
            )
        ],
        active_supports=["adhd_aware_support", "dyscalculia_aware_support"],
        sequence_intent=BlockSequenceIntent.MASTERY_PATH,
        evidence_patterns=[EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS],
        current_block_type=BlockType.WORKED_EXAMPLE,
    )[0]

    assert len(result.meta_transfer_source_profiles) == 2
    assert result.meta_transfer_was_effective is True
    assert sum(result.meta_transfer_source_shares.values()) == pytest.approx(1.0, abs=1e-6)
    assert result.meta_transfer_source_shares[donor_a.profile_id] > result.meta_transfer_source_shares[donor_b.profile_id]

    record = engine.log_decision(
        DecisionRecord(
            session_id="meta_multi_source",
            current_block_type=BlockType.WORKED_EXAMPLE,
            selected_block_type=BlockType.WORKED_EXAMPLE,
            evidence_patterns=[EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS],
            active_supports=["adhd_aware_support", "dyscalculia_aware_support"],
            sequence_intent=BlockSequenceIntent.MASTERY_PATH,
            available_candidate_paths=[result.path_id],
            chosen_path_id=result.path_id,
            chosen_path_score=result.total_score,
            chosen_path_score_breakdown=result.score_breakdown,
            calibration_profile_id=result.calibration_profile_id,
            calibration_profile_confidence=result.calibration_profile_confidence,
            meta_transfer_strength=result.meta_transfer_strength,
            meta_transfer_source_profiles=result.meta_transfer_source_profiles,
            meta_transfer_source_shares=result.meta_transfer_source_shares,
            meta_transfer_weight_delta=result.meta_transfer_weight_delta,
            meta_transfer_was_effective=result.meta_transfer_was_effective,
        )
    )
    outcome = OutcomeMetrics(
        mastery_gain_estimate=0.8,
        confidence_change=0.1,
        observed_engagement="high",
        error_rate_trend="improving",
        accuracy_estimate=0.9,
    )
    expected_outcome_score = outcome.composite_score()
    assert engine.update_outcome(record.decision_id, outcome) is True

    target_profile = engine.calibration_profiles[result.calibration_profile_id]
    donor_a_link = target_profile.meta_transfer_links[donor_a.profile_id]
    donor_b_link = target_profile.meta_transfer_links[donor_b.profile_id]
    assert donor_a_link.use_count == 1
    assert donor_b_link.use_count == 1
    assert donor_a_link.average_outcome_score == pytest.approx(
        expected_outcome_score * result.meta_transfer_source_shares[donor_a.profile_id],
        abs=1e-6,
    )
    assert donor_b_link.average_outcome_score == pytest.approx(
        expected_outcome_score * result.meta_transfer_source_shares[donor_b.profile_id],
        abs=1e-6,
    )
    assert donor_a_link.last_transfer_strength == pytest.approx(
        result.meta_transfer_strength * result.meta_transfer_source_shares[donor_a.profile_id],
        abs=1e-6,
    )
    assert donor_b_link.last_transfer_strength == pytest.approx(
        result.meta_transfer_strength * result.meta_transfer_source_shares[donor_b.profile_id],
        abs=1e-6,
    )


def test_meta_transfer_history_influences_candidate_priority() -> None:
    engine = CalibrationEngine(min_samples_for_calibration=999)

    target_profile = engine._get_or_create_profile(
        {
            "support_profile": "adhd_aware_support+dyscalculia_aware_support",
            "sequence_intent": BlockSequenceIntent.CONFIDENCE_BUILDING.value,
            "evidence_pattern": EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS.value,
            "block_type": BlockType.CONCEPT_CHECK.value,
        }
    )
    donor_a = engine._get_or_create_profile(
        {
            "support_profile": "adhd_aware_support",
            "sequence_intent": BlockSequenceIntent.CONFIDENCE_BUILDING.value,
            "evidence_pattern": EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS.value,
            "block_type": BlockType.GUIDED_PRACTICE.value,
        }
    )
    donor_b = engine._get_or_create_profile(
        {
            "support_profile": "dyscalculia_aware_support",
            "sequence_intent": BlockSequenceIntent.CONFIDENCE_BUILDING.value,
            "evidence_pattern": EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS.value,
            "block_type": BlockType.GUIDED_PRACTICE.value,
        }
    )
    donor_a.confidence_score = 0.8
    donor_b.confidence_score = 0.8
    donor_a.outcome_count = 20
    donor_b.outcome_count = 20

    target_profile.meta_transfer_history.append(
        MetaTransferHistoryEntry(
            target_profile_id=target_profile.profile_id,
            source_profile_ids=[donor_b.profile_id],
            decision_id="priority_from_history",
            transfer_strength=0.25,
            outcome_score=0.8,
            similarity_by_source={donor_b.profile_id: 0.8},
            source_shares={donor_b.profile_id: 1.0},
            effective_weight_delta=0.1,
        )
    )

    candidates = engine._meta_transfer_candidates(
        target_profile,
        excluded_profile_ids={target_profile.profile_id},
    )

    assert candidates
    assert candidates[0][0].profile_id == donor_b.profile_id
