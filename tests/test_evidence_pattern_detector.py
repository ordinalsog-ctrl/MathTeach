from mathteach.models import BlockType, EvidenceCombinationPattern
from mathteach.services.evidence_pattern_detector import (
    build_evidence_combination,
    detect_evidence_patterns,
)


def test_detect_evidence_patterns_reads_rapid_consecutive_success() -> None:
    patterns = detect_evidence_patterns(
        {"rapid_success_two_blocks", "visible_small_success"}
    )

    assert EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS in patterns


def test_detect_evidence_patterns_reads_vocabulary_gap() -> None:
    patterns = detect_evidence_patterns({"text_overload", "vocabulary_request_again"})

    assert EvidenceCombinationPattern.VOCABULARY_GAP in patterns


def test_detect_evidence_patterns_blocks_rapid_pattern_when_progress_is_stalled() -> None:
    patterns = detect_evidence_patterns(
        {"rapid_success_three_blocks", "no_progress_two_blocks"}
    )

    assert EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS not in patterns


def test_build_evidence_combination_preserves_block_context() -> None:
    combination = build_evidence_combination(
        current_evidence=["text_overload", "vocabulary_request_again"],
        previous_evidence=["vocabulary_request"],
        block_type=BlockType.CONCEPT_INTRODUCTION,
        block_sequence=2,
    )

    assert combination.block_type == BlockType.CONCEPT_INTRODUCTION
    assert combination.block_sequence == 2
    assert combination.previous_evidence == ["vocabulary_request"]
    assert EvidenceCombinationPattern.VOCABULARY_GAP in combination.patterns
