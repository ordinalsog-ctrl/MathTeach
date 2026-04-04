from mathteach.models import (
    BlockSequenceDecision,
    BlockSequenceIntent,
    BlockSequenceState,
    BlockTransitionReason,
    BlockType,
    EvidenceCombinationPattern,
)
from mathteach.response_matrix import SupportNeed


LOOKAHEAD_TEMPLATES: dict[BlockSequenceIntent, tuple[BlockType, ...]] = {
    BlockSequenceIntent.CONCEPT_BUILDUP: (
        BlockType.CONCEPT_INTRODUCTION,
        BlockType.WORKED_EXAMPLE,
        BlockType.GUIDED_PRACTICE,
        BlockType.CONCEPT_CHECK,
        BlockType.BRIDGE_TO_APPLICATION,
    ),
    BlockSequenceIntent.CONFIDENCE_BUILDING: (
        BlockType.WORKED_EXAMPLE,
        BlockType.CONCEPT_CHECK,
        BlockType.GUIDED_PRACTICE,
        BlockType.CONCEPT_CHECK,
        BlockType.BRIDGE_TO_APPLICATION,
    ),
    BlockSequenceIntent.ERROR_RECOVERY_CYCLE: (
        BlockType.ERROR_RECOVERY,
        BlockType.WORKED_EXAMPLE,
        BlockType.GUIDED_PRACTICE,
        BlockType.CONCEPT_CHECK,
    ),
    BlockSequenceIntent.MASTERY_PATH: (
        BlockType.WORKED_EXAMPLE,
        BlockType.GUIDED_PRACTICE,
        BlockType.BRIDGE_TO_APPLICATION,
        BlockType.CONCEPT_CHECK,
    ),
    BlockSequenceIntent.ADAPTIVE_REMEDIATION: (
        BlockType.ERROR_RECOVERY,
        BlockType.CONCEPT_INTRODUCTION,
        BlockType.WORKED_EXAMPLE,
        BlockType.GUIDED_PRACTICE,
    ),
}


DEFAULT_BLOCK_PROGRESSIONS: dict[BlockType, BlockType] = {
    BlockType.CONCEPT_INTRODUCTION: BlockType.WORKED_EXAMPLE,
    BlockType.WORKED_EXAMPLE: BlockType.GUIDED_PRACTICE,
    BlockType.GUIDED_PRACTICE: BlockType.CONCEPT_CHECK,
    BlockType.ERROR_RECOVERY: BlockType.WORKED_EXAMPLE,
    BlockType.CONCEPT_CHECK: BlockType.BRIDGE_TO_APPLICATION,
    BlockType.BRIDGE_TO_APPLICATION: BlockType.REFLECTION,
    BlockType.REFLECTION: BlockType.CONCEPT_CHECK,
}


def _determine_sequence_intent(
    current_block_type: BlockType,
    evidence_patterns: set[EvidenceCombinationPattern],
    active_supports: set[SupportNeed],
) -> BlockSequenceIntent:
    if (
        EvidenceCombinationPattern.CONCEPT_CONFUSION in evidence_patterns
        or current_block_type == BlockType.ERROR_RECOVERY
    ):
        return BlockSequenceIntent.ERROR_RECOVERY_CYCLE
    if EvidenceCombinationPattern.STAGNATION_PATTERN in evidence_patterns:
        return BlockSequenceIntent.ADAPTIVE_REMEDIATION
    if EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS in evidence_patterns:
        return BlockSequenceIntent.MASTERY_PATH
    if {
        "adhd_aware_support",
        "dyscalculia_aware_support",
    }.issubset(active_supports):
        return BlockSequenceIntent.CONFIDENCE_BUILDING
    if (
        EvidenceCombinationPattern.VOCABULARY_GAP in evidence_patterns
        or "language_sensitive_support" in active_supports
    ):
        return BlockSequenceIntent.CONCEPT_BUILDUP
    return BlockSequenceIntent.CONCEPT_BUILDUP


def _build_lookahead(
    intent: BlockSequenceIntent,
    current_block_type: BlockType,
    next_block_type: BlockType,
) -> list[BlockType]:
    lookahead: list[BlockType] = [next_block_type]
    for block_type in LOOKAHEAD_TEMPLATES[intent]:
        if block_type != current_block_type and block_type not in lookahead:
            lookahead.append(block_type)
        if len(lookahead) == 4:
            break
    return lookahead


def _default_alternatives(
    current_block_type: BlockType,
    next_block_type: BlockType,
    intent: BlockSequenceIntent,
) -> list[BlockType]:
    candidates = _build_lookahead(intent, current_block_type, next_block_type)
    alternatives = [block_type for block_type in candidates if block_type != next_block_type]
    return alternatives[:2]


def plan_next_block(
    current_block_type: BlockType,
    evidence_patterns: list[EvidenceCombinationPattern],
    active_supports: list[SupportNeed],
    recent_block_types: list[BlockType] | None = None,
) -> BlockSequenceDecision:
    patterns = set(evidence_patterns)
    supports = set(active_supports)
    recent = list(recent_block_types or [])
    recent_set = set(recent[-2:])
    intent = _determine_sequence_intent(current_block_type, patterns, supports)

    suggested_next_block_type: BlockType | None = None
    transition_reason: BlockTransitionReason | None = None
    rationale: list[str] = []
    confidence = 0.55

    if (
        current_block_type == BlockType.GUIDED_PRACTICE
        and EvidenceCombinationPattern.STAGNATION_PATTERN in patterns
    ):
        suggested_next_block_type = BlockType.ERROR_RECOVERY
        transition_reason = BlockTransitionReason.EVIDENCE_PATTERN
        confidence = 0.9
        rationale.append(
            "Guided practice stalled, so the next block should pivot into explicit error recovery."
        )
    elif (
        current_block_type == BlockType.ERROR_RECOVERY
        and EvidenceCombinationPattern.CONCEPT_CONFUSION in patterns
    ):
        suggested_next_block_type = BlockType.WORKED_EXAMPLE
        transition_reason = BlockTransitionReason.EVIDENCE_PATTERN
        confidence = 0.88
        rationale.append(
            "Concept confusion after recovery suggests returning to an explicit modeled example."
        )
    elif (
        current_block_type == BlockType.CONCEPT_INTRODUCTION
        and EvidenceCombinationPattern.VOCABULARY_GAP in patterns
    ):
        suggested_next_block_type = BlockType.CONCEPT_INTRODUCTION
        transition_reason = BlockTransitionReason.EVIDENCE_PATTERN
        confidence = 0.82
        rationale.append(
            "Vocabulary friction keeps the learner in a concept-introduction loop with lower language load."
        )
    elif (
        current_block_type == BlockType.WORKED_EXAMPLE
        and EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS in patterns
        and EvidenceCombinationPattern.STAGNATION_PATTERN not in patterns
    ):
        suggested_next_block_type = BlockType.GUIDED_PRACTICE
        transition_reason = BlockTransitionReason.EVIDENCE_PATTERN
        confidence = 0.86
        rationale.append(
            "Rapid consecutive success makes guided practice the next productive release step."
        )
    elif (
        current_block_type == BlockType.GUIDED_PRACTICE
        and EvidenceCombinationPattern.CONFIDENCE_BUILDUP in patterns
    ):
        suggested_next_block_type = BlockType.BRIDGE_TO_APPLICATION
        transition_reason = BlockTransitionReason.EVIDENCE_PATTERN
        confidence = 0.78
        rationale.append(
            "Confidence buildup in guided practice supports a move toward transfer and application."
        )
    elif (
        current_block_type == BlockType.BRIDGE_TO_APPLICATION
        and EvidenceCombinationPattern.STAGNATION_PATTERN in patterns
    ):
        suggested_next_block_type = BlockType.GUIDED_PRACTICE
        transition_reason = BlockTransitionReason.EVIDENCE_PATTERN
        confidence = 0.8
        rationale.append(
            "Transfer stalled, so the next block should fall back to guided practice."
        )
    elif (
        current_block_type == BlockType.WORKED_EXAMPLE
        and {
            "adhd_aware_support",
            "dyscalculia_aware_support",
        }.issubset(supports)
        and BlockType.CONCEPT_CHECK not in recent_set
        and EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS not in patterns
    ):
        suggested_next_block_type = BlockType.CONCEPT_CHECK
        transition_reason = BlockTransitionReason.SUPPORT_PROFILE
        confidence = 0.72
        rationale.append(
            "ADHD plus dyscalculia benefits from an explicit stability check before more release."
        )

    if suggested_next_block_type is None or transition_reason is None:
        suggested_next_block_type = DEFAULT_BLOCK_PROGRESSIONS[current_block_type]
        transition_reason = BlockTransitionReason.LOOKAHEAD_FALLBACK
        confidence = 0.5
        rationale.append(
            "No stronger routing signal fired, so the planner falls back to the default progression."
        )

    if current_block_type in recent_set and suggested_next_block_type == current_block_type:
        rationale.append(
            "The same block type is repeated deliberately because the current evidence still blocks a safe advance."
        )
    elif suggested_next_block_type in recent_set:
        rationale.append(
            "Recent sequence history keeps the next block close to the current support need instead of jumping ahead."
        )

    lookahead = _build_lookahead(intent, current_block_type, suggested_next_block_type)
    alternatives = _default_alternatives(current_block_type, suggested_next_block_type, intent)

    return BlockSequenceDecision(
        current_block_type=current_block_type,
        suggested_next_block_type=suggested_next_block_type,
        alternative_next_block_types=alternatives,
        transition_reason=transition_reason,
        sequence_intent=intent,
        rationale=rationale,
        confidence=confidence,
        lookahead_block_types=lookahead,
    )


def advance_sequence_state(
    state: BlockSequenceState,
    current_block_type: BlockType,
    evidence_patterns: list[EvidenceCombinationPattern],
    decision: BlockSequenceDecision,
) -> BlockSequenceState:
    history = [*state.block_type_history, current_block_type][-6:]
    recent_patterns = [*state.recent_evidence_patterns, *evidence_patterns][-6:]
    adaptive_transitions_applied = state.adaptive_transitions_applied
    if decision.transition_reason != BlockTransitionReason.LOOKAHEAD_FALLBACK:
        adaptive_transitions_applied += 1

    return BlockSequenceState(
        block_type_history=history,
        recent_evidence_patterns=recent_patterns,
        active_sequence_intent=decision.sequence_intent,
        adaptive_transitions_applied=adaptive_transitions_applied,
        last_recommended_block_type=decision.suggested_next_block_type,
        lookahead_block_types=decision.lookahead_block_types,
    )
