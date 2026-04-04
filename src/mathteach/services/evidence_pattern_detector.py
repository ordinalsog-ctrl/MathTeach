from mathteach.models import BlockType, EvidenceCombination, EvidenceCombinationPattern


def detect_evidence_patterns(
    current_evidence: set[str],
    previous_evidence: set[str] | None = None,
) -> list[EvidenceCombinationPattern]:
    previous = previous_evidence or set()
    patterns: list[EvidenceCombinationPattern] = []

    if (
        "rapid_success_three_blocks" in current_evidence
        or {
            "rapid_success_two_blocks",
            "visible_small_success",
        }.issubset(current_evidence)
    ) and not current_evidence & {
        "no_progress_two_blocks",
        "no_progress_three_blocks",
        "text_overload",
    }:
        patterns.append(EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS)

    if current_evidence & {
        "repeated_attempt_three_plus",
        "no_progress_two_blocks",
        "no_progress_three_blocks",
        "no_success_visible_two_blocks",
    } and not current_evidence & {
        "rapid_success_two_blocks",
        "rapid_success_three_blocks",
    }:
        patterns.append(EvidenceCombinationPattern.STAGNATION_PATTERN)

    if "mixed_success_inconsistent" in current_evidence and (
        "error_recovery_with_hint" in current_evidence
        or "error_recovery_with_hint" in previous
        or "transfer_success_two_blocks" in current_evidence
    ):
        patterns.append(EvidenceCombinationPattern.INCONSISTENT_SUCCESS)

    if "text_overload" in current_evidence and current_evidence & {
        "vocabulary_request",
        "vocabulary_request_again",
    }:
        patterns.append(EvidenceCombinationPattern.VOCABULARY_GAP)

    if {
        "visible_small_success",
        "rapid_success_two_blocks",
    }.issubset(current_evidence) and not current_evidence & {
        "repeated_attempt_three_plus",
        "repeated_concept_error",
    }:
        patterns.append(EvidenceCombinationPattern.CONFIDENCE_BUILDUP)

    if (
        "repeated_concept_error" in current_evidence
        and current_evidence
        & {
            "repeated_attempt_three_plus",
            "repeated_concept_error_across_blocks",
        }
    ):
        patterns.append(EvidenceCombinationPattern.CONCEPT_CONFUSION)

    return patterns


def build_evidence_combination(
    current_evidence: list[str],
    block_type: BlockType,
    block_sequence: int,
    previous_evidence: list[str] | None = None,
) -> EvidenceCombination:
    current = set(current_evidence)
    previous = set(previous_evidence or [])
    return EvidenceCombination(
        patterns=detect_evidence_patterns(current, previous),
        current_evidence=sorted(current),
        previous_evidence=sorted(previous),
        block_type=block_type,
        block_sequence=block_sequence,
    )
