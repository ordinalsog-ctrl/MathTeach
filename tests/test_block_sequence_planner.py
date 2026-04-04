from mathteach.models import (
    BlockSequenceIntent,
    BlockTransitionReason,
    BlockType,
    EvidenceCombinationPattern,
)
from mathteach.services.block_sequence_planner import plan_next_block


def test_sequence_planner_routes_worked_example_to_guided_practice_on_rapid_success() -> None:
    decision = plan_next_block(
        current_block_type=BlockType.WORKED_EXAMPLE,
        evidence_patterns=[EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS],
        active_supports=["adhd_aware_support", "dyscalculia_aware_support"],
        recent_block_types=[BlockType.WORKED_EXAMPLE],
    )

    assert decision.suggested_next_block_type == BlockType.GUIDED_PRACTICE
    assert decision.transition_reason == BlockTransitionReason.EVIDENCE_PATTERN
    assert decision.sequence_intent == BlockSequenceIntent.MASTERY_PATH
    assert BlockType.BRIDGE_TO_APPLICATION in decision.lookahead_block_types


def test_sequence_planner_routes_guided_practice_to_error_recovery_on_stagnation() -> None:
    decision = plan_next_block(
        current_block_type=BlockType.GUIDED_PRACTICE,
        evidence_patterns=[EvidenceCombinationPattern.STAGNATION_PATTERN],
        active_supports=["language_sensitive_support"],
        recent_block_types=[BlockType.CONCEPT_INTRODUCTION, BlockType.GUIDED_PRACTICE],
    )

    assert decision.suggested_next_block_type == BlockType.ERROR_RECOVERY
    assert decision.transition_reason == BlockTransitionReason.EVIDENCE_PATTERN
    assert decision.sequence_intent == BlockSequenceIntent.ADAPTIVE_REMEDIATION


def test_sequence_planner_keeps_concept_intro_under_vocabulary_gap() -> None:
    decision = plan_next_block(
        current_block_type=BlockType.CONCEPT_INTRODUCTION,
        evidence_patterns=[EvidenceCombinationPattern.VOCABULARY_GAP],
        active_supports=["language_sensitive_support", "dyscalculia_aware_support"],
        recent_block_types=[BlockType.CONCEPT_INTRODUCTION],
    )

    assert decision.suggested_next_block_type == BlockType.CONCEPT_INTRODUCTION
    assert decision.transition_reason == BlockTransitionReason.EVIDENCE_PATTERN
    assert decision.sequence_intent == BlockSequenceIntent.CONCEPT_BUILDUP


def test_sequence_planner_inserts_concept_check_for_adhd_and_dyscalculia() -> None:
    decision = plan_next_block(
        current_block_type=BlockType.WORKED_EXAMPLE,
        evidence_patterns=[],
        active_supports=["adhd_aware_support", "dyscalculia_aware_support"],
        recent_block_types=[BlockType.CONCEPT_INTRODUCTION],
    )

    assert decision.suggested_next_block_type == BlockType.CONCEPT_CHECK
    assert decision.transition_reason == BlockTransitionReason.SUPPORT_PROFILE
    assert decision.sequence_intent == BlockSequenceIntent.CONFIDENCE_BUILDING
