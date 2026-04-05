from datetime import UTC, datetime

import pytest

from mathteach.models import (
    BlockSequenceIntent,
    BlockType,
    DecisionRecord,
    EvidenceCombinationPattern,
    MetaTransferHistoryEntry,
    MetaTransferLink,
)
from mathteach.services.calibration_engine import CalibrationEngine


def test_transfer_network_summary_aggregates_edges_and_flags_weak_links() -> None:
    engine = CalibrationEngine(min_samples_for_calibration=999)

    target = engine._get_or_create_profile(
        {
            "support_profile": "adhd_aware_support+dyscalculia_aware_support",
            "sequence_intent": BlockSequenceIntent.MASTERY_PATH.value,
            "evidence_pattern": EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS.value,
            "block_type": BlockType.WORKED_EXAMPLE.value,
        }
    )
    donor_strong = engine._get_or_create_profile(
        {
            "support_profile": "adhd_aware_support",
            "sequence_intent": BlockSequenceIntent.MASTERY_PATH.value,
            "evidence_pattern": EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS.value,
            "block_type": BlockType.GUIDED_PRACTICE.value,
        }
    )
    donor_weak = engine._get_or_create_profile(
        {
            "support_profile": "dyscalculia_aware_support",
            "sequence_intent": BlockSequenceIntent.MASTERY_PATH.value,
            "evidence_pattern": EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS.value,
            "block_type": BlockType.CONCEPT_CHECK.value,
        }
    )
    donor_strong.outcome_count = 20
    donor_weak.outcome_count = 20
    donor_strong.confidence_score = 0.8
    donor_weak.confidence_score = 0.7
    target.meta_transfer_links[donor_strong.profile_id] = MetaTransferLink(
        source_profile_id=donor_strong.profile_id,
        use_count=2,
        cumulative_outcome_score=0.6,
        average_outcome_score=0.3,
    )
    target.meta_transfer_links[donor_weak.profile_id] = MetaTransferLink(
        source_profile_id=donor_weak.profile_id,
        use_count=2,
        cumulative_outcome_score=0.08,
        average_outcome_score=0.04,
    )
    target.meta_transfer_history = [
        MetaTransferHistoryEntry(
            timestamp=datetime.now(UTC),
            target_profile_id=target.profile_id,
            source_profile_ids=[donor_strong.profile_id],
            decision_id="dec_strong",
            transfer_strength=0.3,
            outcome_score=0.6,
            similarity_by_source={donor_strong.profile_id: 0.9},
            source_shares={donor_strong.profile_id: 1.0},
            effective_weight_delta=0.1,
        ),
        MetaTransferHistoryEntry(
            timestamp=datetime.now(UTC),
            target_profile_id=target.profile_id,
            source_profile_ids=[donor_weak.profile_id],
            decision_id="dec_weak",
            transfer_strength=0.3,
            outcome_score=0.08,
            similarity_by_source={donor_weak.profile_id: 0.7},
            source_shares={donor_weak.profile_id: 1.0},
            effective_weight_delta=0.12,
        ),
    ]
    engine.decision_log = [
        DecisionRecord(
            session_id="network_strong",
            current_block_type=BlockType.WORKED_EXAMPLE,
            selected_block_type=BlockType.WORKED_EXAMPLE,
            evidence_patterns=[EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS],
            active_supports=["adhd_aware_support", "dyscalculia_aware_support"],
            sequence_intent=BlockSequenceIntent.MASTERY_PATH,
            available_candidate_paths=["path_strong"],
            chosen_path_id="path_strong",
            chosen_path_score=0.7,
            chosen_path_score_breakdown={"heuristic": 0.7},
            calibration_profile_id=target.profile_id,
            meta_transfer_strength=0.3,
            meta_transfer_source_profiles=[donor_strong.profile_id],
            meta_transfer_source_shares={donor_strong.profile_id: 1.0},
            meta_transfer_weight_delta=0.1,
            meta_transfer_was_effective=True,
        ),
        DecisionRecord(
            session_id="network_weak",
            current_block_type=BlockType.WORKED_EXAMPLE,
            selected_block_type=BlockType.WORKED_EXAMPLE,
            evidence_patterns=[EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS],
            active_supports=["adhd_aware_support", "dyscalculia_aware_support"],
            sequence_intent=BlockSequenceIntent.MASTERY_PATH,
            available_candidate_paths=["path_weak"],
            chosen_path_id="path_weak",
            chosen_path_score=0.5,
            chosen_path_score_breakdown={"heuristic": 0.5},
            calibration_profile_id=target.profile_id,
            meta_transfer_strength=0.3,
            meta_transfer_source_profiles=[donor_weak.profile_id],
            meta_transfer_source_shares={donor_weak.profile_id: 1.0},
            meta_transfer_weight_delta=0.12,
            meta_transfer_was_effective=True,
        ),
    ]

    summary = engine.compute_transfer_network_summary()

    assert summary["total_profiles"] >= 3
    assert summary["profiles_with_transfer"] == 1
    assert summary["effective_transfer_decisions"] == 2
    assert len(summary["edges"]) == 2
    strong_edge = next(
        edge
        for edge in summary["edges"]
        if edge["source_profile_id"] == donor_strong.profile_id
    )
    weak_edge = next(
        edge
        for edge in summary["edges"]
        if edge["source_profile_id"] == donor_weak.profile_id
    )
    assert strong_edge["average_outcome_score"] == pytest.approx(0.6, abs=1e-6)
    assert strong_edge["average_effective_weight_delta"] == pytest.approx(0.1, abs=1e-6)
    assert weak_edge["average_outcome_score"] == pytest.approx(0.08, abs=1e-6)
    assert any(
        edge["source_profile_id"] == donor_weak.profile_id
        for edge in summary["weak_edges"]
    )


def test_profile_transfer_history_counts_effective_and_phantom_transfer_records() -> None:
    engine = CalibrationEngine(min_samples_for_calibration=999)

    target = engine._get_or_create_profile(
        {
            "support_profile": "adhd_aware_support",
            "sequence_intent": BlockSequenceIntent.MASTERY_PATH.value,
            "evidence_pattern": EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS.value,
            "block_type": BlockType.WORKED_EXAMPLE.value,
        }
    )
    donor = engine._get_or_create_profile(
        {
            "support_profile": "adhd_aware_support",
            "sequence_intent": BlockSequenceIntent.MASTERY_PATH.value,
            "evidence_pattern": EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS.value,
            "block_type": BlockType.GUIDED_PRACTICE.value,
        }
    )
    target.meta_transfer_links[donor.profile_id] = MetaTransferLink(
        source_profile_id=donor.profile_id,
        use_count=1,
        cumulative_outcome_score=0.4,
        average_outcome_score=0.4,
        last_transfer_strength=0.2,
        last_used=datetime.now(UTC),
    )
    target.meta_transfer_history = [
        MetaTransferHistoryEntry(
            timestamp=datetime.now(UTC),
            target_profile_id=target.profile_id,
            source_profile_ids=[donor.profile_id],
            decision_id="effective_decision",
            transfer_strength=0.2,
            outcome_score=0.4,
            similarity_by_source={donor.profile_id: 0.8},
            source_shares={donor.profile_id: 1.0},
            effective_weight_delta=0.05,
        )
    ]
    engine.decision_log = [
        DecisionRecord(
            session_id="effective_transfer",
            current_block_type=BlockType.WORKED_EXAMPLE,
            selected_block_type=BlockType.WORKED_EXAMPLE,
            evidence_patterns=[EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS],
            active_supports=["adhd_aware_support"],
            sequence_intent=BlockSequenceIntent.MASTERY_PATH,
            available_candidate_paths=["path_ok"],
            chosen_path_id="path_ok",
            chosen_path_score=0.6,
            chosen_path_score_breakdown={"heuristic": 0.6},
            calibration_profile_id=target.profile_id,
            meta_transfer_strength=0.2,
            meta_transfer_source_profiles=[donor.profile_id],
            meta_transfer_source_shares={donor.profile_id: 1.0},
            meta_transfer_weight_delta=0.05,
            meta_transfer_was_effective=True,
        ),
        DecisionRecord(
            session_id="phantom_transfer",
            current_block_type=BlockType.WORKED_EXAMPLE,
            selected_block_type=BlockType.WORKED_EXAMPLE,
            evidence_patterns=[EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS],
            active_supports=["adhd_aware_support"],
            sequence_intent=BlockSequenceIntent.MASTERY_PATH,
            available_candidate_paths=["path_phantom"],
            chosen_path_id="path_phantom",
            chosen_path_score=0.6,
            chosen_path_score_breakdown={"heuristic": 0.6},
            calibration_profile_id=target.profile_id,
            meta_transfer_strength=0.3,
            meta_transfer_source_profiles=[donor.profile_id],
            meta_transfer_source_shares={donor.profile_id: 1.0},
            meta_transfer_weight_delta=0.0,
            meta_transfer_was_effective=False,
        ),
    ]

    history = engine.get_profile_transfer_history(target.profile_id)

    assert history is not None
    assert history["total_decisions_using_transfer"] == 2
    assert history["effective_transfers"] == 1
    assert history["phantom_filters"] == 1
    assert history["top_donors"][0]["donor_id"] == donor.profile_id
    assert history["recent_transfer_sequence"][0]["source_shares"] == {
        donor.profile_id: 1.0
    }


def test_profile_density_summary_reports_sparse_isolated_profiles_with_candidates() -> None:
    engine = CalibrationEngine(min_samples_for_calibration=999)

    sparse_profile = engine._get_or_create_profile(
        {
            "support_profile": "language_sensitive_support",
            "sequence_intent": BlockSequenceIntent.CONFIDENCE_BUILDING.value,
            "evidence_pattern": EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS.value,
            "block_type": BlockType.CONCEPT_CHECK.value,
        }
    )
    sparse_profile.outcome_count = 2
    sparse_profile.confidence_score = 0.0
    donor_profile = engine._get_or_create_profile(
        {
            "support_profile": "language_sensitive_support",
            "sequence_intent": BlockSequenceIntent.CONFIDENCE_BUILDING.value,
            "evidence_pattern": EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS.value,
            "block_type": BlockType.GUIDED_PRACTICE.value,
        }
    )
    donor_profile.outcome_count = 24
    donor_profile.confidence_score = 0.8

    density = engine.profile_density_summary()
    candidates = engine.profile_transfer_candidates(sparse_profile.profile_id)

    assert density["total_profiles"] >= 2
    assert density["sparse_profiles"] >= 1
    assert candidates
    assert candidates[0]["profile_id"] == donor_profile.profile_id
    assert density["isolated_profiles"]
    assert any(
        item["profile_id"] == sparse_profile.profile_id
        for item in density["isolated_profiles"]
    )


def test_legacy_links_without_effective_history_do_not_drive_monitoring() -> None:
    engine = CalibrationEngine(min_samples_for_calibration=999)

    target = engine._get_or_create_profile(
        {
            "support_profile": "adhd_aware_support",
            "sequence_intent": BlockSequenceIntent.MASTERY_PATH.value,
            "evidence_pattern": EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS.value,
            "block_type": BlockType.WORKED_EXAMPLE.value,
        }
    )
    legacy_only_target = engine._get_or_create_profile(
        {
            "support_profile": "language_sensitive_support",
            "sequence_intent": BlockSequenceIntent.CONFIDENCE_BUILDING.value,
            "evidence_pattern": EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS.value,
            "block_type": BlockType.CONCEPT_CHECK.value,
        }
    )
    donor_real = engine._get_or_create_profile(
        {
            "support_profile": "adhd_aware_support",
            "sequence_intent": BlockSequenceIntent.MASTERY_PATH.value,
            "evidence_pattern": EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS.value,
            "block_type": BlockType.GUIDED_PRACTICE.value,
        }
    )
    donor_legacy = engine._get_or_create_profile(
        {
            "support_profile": "adhd_aware_support",
            "sequence_intent": BlockSequenceIntent.MASTERY_PATH.value,
            "evidence_pattern": EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS.value,
            "block_type": BlockType.CONCEPT_CHECK.value,
        }
    )
    donor_real.outcome_count = 20
    donor_legacy.outcome_count = 20
    donor_real.confidence_score = 0.8
    donor_legacy.confidence_score = 0.8

    target.meta_transfer_links[donor_legacy.profile_id] = MetaTransferLink(
        source_profile_id=donor_legacy.profile_id,
        use_count=6,
        cumulative_outcome_score=5.4,
        average_outcome_score=0.9,
    )
    legacy_only_target.meta_transfer_links[donor_legacy.profile_id] = MetaTransferLink(
        source_profile_id=donor_legacy.profile_id,
        use_count=8,
        cumulative_outcome_score=6.4,
        average_outcome_score=0.8,
    )
    target.meta_transfer_history = [
        MetaTransferHistoryEntry(
            timestamp=datetime.now(UTC),
            target_profile_id=target.profile_id,
            source_profile_ids=[donor_real.profile_id],
            decision_id="effective_history_only",
            transfer_strength=0.22,
            outcome_score=0.36,
            similarity_by_source={donor_real.profile_id: 0.85},
            source_shares={donor_real.profile_id: 1.0},
            effective_weight_delta=0.08,
        )
    ]

    candidates = engine.profile_transfer_candidates(target.profile_id)
    history = engine.get_profile_transfer_history(target.profile_id)
    summary = engine.compute_transfer_network_summary()

    assert candidates
    assert candidates[0]["profile_id"] == donor_real.profile_id
    assert history is not None
    assert history["top_donors"][0]["donor_id"] == donor_real.profile_id
    assert summary["profiles_with_transfer"] == 1


def test_compute_weak_transfers_uses_runtime_thresholds() -> None:
    engine = CalibrationEngine(min_samples_for_calibration=999)

    target = engine._get_or_create_profile(
        {
            "support_profile": "adhd_aware_support",
            "sequence_intent": BlockSequenceIntent.MASTERY_PATH.value,
            "evidence_pattern": EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS.value,
            "block_type": BlockType.WORKED_EXAMPLE.value,
        }
    )
    donor = engine._get_or_create_profile(
        {
            "support_profile": "adhd_aware_support",
            "sequence_intent": BlockSequenceIntent.MASTERY_PATH.value,
            "evidence_pattern": EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS.value,
            "block_type": BlockType.GUIDED_PRACTICE.value,
        }
    )
    target.meta_transfer_history = [
        MetaTransferHistoryEntry(
            timestamp=datetime.now(UTC),
            target_profile_id=target.profile_id,
            source_profile_ids=[donor.profile_id],
            decision_id="edge_outside_defaults",
            transfer_strength=0.03,
            outcome_score=0.15,
            similarity_by_source={donor.profile_id: 0.8},
            source_shares={donor.profile_id: 1.0},
            effective_weight_delta=0.08,
        )
    ]

    assert engine.compute_weak_transfers() == []
    relaxed = engine.compute_weak_transfers(
        min_average_strength=0.01,
        max_average_outcome=0.2,
    )

    assert len(relaxed) == 1
    assert relaxed[0]["source_profile_id"] == donor.profile_id
