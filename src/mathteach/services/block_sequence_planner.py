from mathteach.models import (
    BlockSequenceDecision,
    BlockSequenceIntent,
    BlockSequencePathOption,
    BlockSequenceState,
    BlockTransitionReason,
    BlockType,
    EnrichedPathEvaluation,
    EvidenceCombinationPattern,
    LongTermLearningGoal,
    PathScoringCriteria,
    SessionProgressTracker,
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


PILOT_DATA_SUCCESS_RATES: dict[
    tuple[BlockType, EvidenceCombinationPattern | None],
    float,
] = {
    (BlockType.WORKED_EXAMPLE, EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS): 0.86,
    (BlockType.CONCEPT_INTRODUCTION, EvidenceCombinationPattern.VOCABULARY_GAP): 0.68,
    (BlockType.ERROR_RECOVERY, EvidenceCombinationPattern.STAGNATION_PATTERN): 0.72,
    (BlockType.BRIDGE_TO_APPLICATION, EvidenceCombinationPattern.CONFIDENCE_BUILDUP): 0.77,
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


def _score_candidate_path(
    path: list[BlockType],
    preferred_next_block_type: BlockType,
    current_block_type: BlockType,
    intent: BlockSequenceIntent,
    patterns: set[EvidenceCombinationPattern],
    supports: set[SupportNeed],
    recent: list[BlockType],
) -> tuple[float, list[str]]:
    score = 0.35
    rationale: list[str] = []

    if not path:
        return 0.0, ["Empty path candidate cannot guide sequencing."]

    if path[0] == preferred_next_block_type:
        score += 0.22
        rationale.append(
            "This path starts from the strongest immediate routing recommendation."
        )
    else:
        score += 0.08
        rationale.append(
            "This path is kept as a viable fallback if the primary release path proves too aggressive."
        )

    if intent == BlockSequenceIntent.MASTERY_PATH and BlockType.BRIDGE_TO_APPLICATION in path:
        score += 0.08
        rationale.append(
            "The path preserves a transfer step, which fits the current mastery trajectory."
        )
    if (
        intent == BlockSequenceIntent.ADAPTIVE_REMEDIATION
        and BlockType.ERROR_RECOVERY in path[:2]
    ):
        score += 0.1
        rationale.append(
            "Early remediation keeps the path aligned with the detected stagnation pattern."
        )
    if (
        intent == BlockSequenceIntent.ERROR_RECOVERY_CYCLE
        and BlockType.WORKED_EXAMPLE in path[:3]
    ):
        score += 0.08
        rationale.append(
            "A modeled example appears early enough to stabilize the recovery cycle."
        )
    if (
        intent == BlockSequenceIntent.CONCEPT_BUILDUP
        and (
            BlockType.CONCEPT_INTRODUCTION in path[:2]
            or BlockType.WORKED_EXAMPLE in path[:2]
        )
    ):
        score += 0.07
        rationale.append(
            "The path keeps language and concept grounding close to the front of the sequence."
        )

    if EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS in patterns:
        if path[0] == BlockType.GUIDED_PRACTICE:
            score += 0.08
            rationale.append(
                "Rapid success supports an early release into guided practice."
            )
        if BlockType.BRIDGE_TO_APPLICATION in path[:3]:
            score += 0.05
            rationale.append(
                "A near-term bridge block keeps momentum without overextending the learner."
            )

    if EvidenceCombinationPattern.STAGNATION_PATTERN in patterns:
        if path[0] == BlockType.ERROR_RECOVERY:
            score += 0.1
            rationale.append(
                "The path reacts quickly to stagnation by prioritizing explicit recovery."
            )
        if BlockType.CONCEPT_INTRODUCTION in path[:3]:
            score += 0.04
            rationale.append(
                "The path still leaves room for re-grounding if recovery alone is not enough."
            )

    if EvidenceCombinationPattern.VOCABULARY_GAP in patterns:
        if path[0] in {BlockType.CONCEPT_INTRODUCTION, BlockType.WORKED_EXAMPLE}:
            score += 0.07
            rationale.append(
                "The opening block remains language-manageable under vocabulary strain."
            )
        if BlockType.BRIDGE_TO_APPLICATION in path[:2]:
            score -= 0.08
            rationale.append(
                "The path delays transfer because vocabulary friction still needs direct support."
            )

    if EvidenceCombinationPattern.CONCEPT_CONFUSION in patterns:
        if path[0] == BlockType.WORKED_EXAMPLE:
            score += 0.07
            rationale.append(
                "Concept confusion benefits from an early return to modeled structure."
            )

    if {
        "adhd_aware_support",
        "dyscalculia_aware_support",
    }.issubset(supports) and BlockType.CONCEPT_CHECK in path[:2]:
        score += 0.05
        rationale.append(
            "Early stability checks fit the ADHD plus dyscalculia profile mix."
        )

    if "language_sensitive_support" in supports and (
        BlockType.CONCEPT_INTRODUCTION in path[:2]
        or BlockType.WORKED_EXAMPLE in path[:2]
    ):
        score += 0.04
        rationale.append(
            "The path keeps language support near the front where it is most useful."
        )

    if "autism_spectrum_aware_support" in supports and path[0] == current_block_type:
        score += 0.03
        rationale.append(
            "A predictable near-repeat can help preserve structure for autism-aware support."
        )

    if recent:
        if path[0] == recent[-1] and path[0] == current_block_type:
            score -= 0.04
            rationale.append(
                "The path repeats the same block type immediately, so it pays a small variety penalty."
            )
        if len(path) >= 2 and path[0] == path[1]:
            score -= 0.03
            rationale.append(
                "Two identical starting blocks reduce variety unless the evidence clearly demands it."
            )

    return max(0.0, min(1.0, score)), rationale


def _build_candidate_paths(
    current_block_type: BlockType,
    preferred_next_block_type: BlockType,
    alternative_next_block_types: list[BlockType],
    intent: BlockSequenceIntent,
    patterns: set[EvidenceCombinationPattern],
    supports: set[SupportNeed],
    recent: list[BlockType],
) -> list[BlockSequencePathOption]:
    seen: set[tuple[BlockType, ...]] = set()
    path_starts = [preferred_next_block_type, *alternative_next_block_types]
    candidates: list[BlockSequencePathOption] = []

    for next_block_type in path_starts:
        path = _build_lookahead(intent, current_block_type, next_block_type)
        key = tuple(path)
        if key in seen:
            continue
        seen.add(key)
        score, rationale = _score_candidate_path(
            path=path,
            preferred_next_block_type=preferred_next_block_type,
            current_block_type=current_block_type,
            intent=intent,
            patterns=patterns,
            supports=supports,
            recent=recent,
        )
        candidates.append(
            BlockSequencePathOption(
                block_types=path,
                score=score,
                rationale=rationale,
            )
        )

    candidates.sort(key=lambda candidate: candidate.score, reverse=True)
    return candidates


def _goal_alignment_for_path(
    path: BlockSequencePathOption,
    learning_goals: list[LongTermLearningGoal],
    current_concept: str,
    current_mastery: float,
) -> tuple[float, str]:
    if not learning_goals:
        return 0.5, "No long-term goals were available, so goal alignment stays neutral."

    score = 0.0
    matched_goals = 0
    transfer_bonus = 0.0

    for goal in learning_goals:
        if goal.concept != current_concept:
            continue
        matched_goals += 1
        if goal.category.value in {"concept_mastery", "conceptual_understanding"}:
            if any(
                block_type
                in {
                    BlockType.CONCEPT_INTRODUCTION,
                    BlockType.WORKED_EXAMPLE,
                    BlockType.GUIDED_PRACTICE,
                    BlockType.CONCEPT_CHECK,
                }
                for block_type in path.block_types
            ):
                score += 0.22
        if goal.category.value == "transfer_ability" and BlockType.BRIDGE_TO_APPLICATION in path.block_types:
            transfer_bonus += 0.18

    mastery_gap = 1.0 - current_mastery
    total = min(1.0, score + transfer_bonus + mastery_gap * 0.2)
    explanation = (
        f"{matched_goals} long-term goals target {current_concept}; "
        f"current mastery is {current_mastery:.0%}, so remaining gap still matters."
    )
    return total, explanation


def _history_alignment_for_path(
    path: BlockSequencePathOption,
    tracker: SessionProgressTracker,
) -> tuple[float, str]:
    if not tracker.history_entries:
        return 0.5, "No session history was available, so history alignment stays neutral."

    recent_types = [entry.block_type for entry in tracker.history_entries[-3:]]
    score = 0.45
    if recent_types and path.block_types:
        last_type = recent_types[-1]
        if path.block_types[0] == last_type:
            score -= 0.08
        elif (
            last_type == BlockType.ERROR_RECOVERY
            and path.block_types[0] == BlockType.WORKED_EXAMPLE
        ):
            score += 0.18
        elif (
            last_type == BlockType.WORKED_EXAMPLE
            and path.block_types[0] in {BlockType.GUIDED_PRACTICE, BlockType.CONCEPT_CHECK}
        ):
            score += 0.14

    unique_recent_types = len(set(recent_types))
    score += min(0.15, unique_recent_types * 0.04)
    explanation = (
        f"The path is compared against the last {len(recent_types)} completed block types "
        f"and gets a continuity bonus when it extends a stable progression."
    )
    return max(0.0, min(1.0, score)), explanation


def _evidence_continuity_for_path(
    path: BlockSequencePathOption,
    active_patterns: set[EvidenceCombinationPattern],
) -> tuple[float, str]:
    score = 0.45

    if EvidenceCombinationPattern.STAGNATION_PATTERN in active_patterns and path.block_types[:1] == [BlockType.ERROR_RECOVERY]:
        score += 0.22
    if EvidenceCombinationPattern.VOCABULARY_GAP in active_patterns and path.block_types[:1] in ([BlockType.CONCEPT_INTRODUCTION], [BlockType.WORKED_EXAMPLE]):
        score += 0.18
    if EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS in active_patterns and BlockType.BRIDGE_TO_APPLICATION in path.block_types[:3]:
        score += 0.14
    if EvidenceCombinationPattern.CONCEPT_CONFUSION in active_patterns and path.block_types[:1] == [BlockType.WORKED_EXAMPLE]:
        score += 0.18

    explanation = (
        "The path gets continuity credit when its first steps stay consistent with the currently active evidence patterns."
    )
    return max(0.0, min(1.0, score)), explanation


def _profile_match_for_path(
    path: BlockSequencePathOption,
    active_supports: set[SupportNeed],
) -> tuple[float, str]:
    score = 0.45

    if {
        "adhd_aware_support",
        "dyscalculia_aware_support",
    }.issubset(active_supports) and BlockType.CONCEPT_CHECK in path.block_types[:2]:
        score += 0.2
    if "language_sensitive_support" in active_supports and path.block_types[:1] in (
        [BlockType.CONCEPT_INTRODUCTION],
        [BlockType.WORKED_EXAMPLE],
    ):
        score += 0.15
    if "autism_spectrum_aware_support" in active_supports and len(path.block_types) >= 2 and path.block_types[0] == path.block_types[1]:
        score += 0.1

    explanation = (
        "The profile-match score checks whether the early path structure fits the active support mix."
    )
    return max(0.0, min(1.0, score)), explanation


def _pilot_data_adjustment_for_path(
    path: BlockSequencePathOption,
    active_patterns: set[EvidenceCombinationPattern],
) -> tuple[float, list[str]]:
    references: list[str] = []
    matches: list[float] = []

    for block_type in path.block_types[:3]:
        matched = False
        for pattern in active_patterns:
            key = (block_type, pattern)
            if key in PILOT_DATA_SUCCESS_RATES:
                value = PILOT_DATA_SUCCESS_RATES[key]
                matches.append(value)
                references.append(f"{block_type.value}: {value:.0%} success under {pattern.value}")
                matched = True
                break
        if not matched:
            key = (block_type, None)
            if key in PILOT_DATA_SUCCESS_RATES:
                value = PILOT_DATA_SUCCESS_RATES[key]
                matches.append(value)
                references.append(f"{block_type.value}: {value:.0%} baseline success")

    if not matches:
        return 0.5, ["No pilot-style references matched this path, so the adjustment stays neutral."]

    return sum(matches) / len(matches), references


def _mastery_projection_for_path(
    path: BlockSequencePathOption,
    current_mastery: float,
) -> float:
    projected = current_mastery
    for block_type in path.block_types[:3]:
        projected += {
            BlockType.CONCEPT_INTRODUCTION: 0.08,
            BlockType.WORKED_EXAMPLE: 0.14,
            BlockType.GUIDED_PRACTICE: 0.12,
            BlockType.ERROR_RECOVERY: 0.09,
            BlockType.CONCEPT_CHECK: 0.06,
            BlockType.BRIDGE_TO_APPLICATION: 0.1,
            BlockType.REFLECTION: 0.04,
        }.get(block_type, 0.05)
    return max(0.0, min(1.0, projected))


def enrich_candidate_paths(
    candidate_paths: list[BlockSequencePathOption],
    learning_goals: list[LongTermLearningGoal],
    session_tracker: SessionProgressTracker,
    active_supports: list[SupportNeed],
    active_patterns: list[EvidenceCombinationPattern],
    scoring_criteria: PathScoringCriteria | None = None,
) -> list[EnrichedPathEvaluation]:
    criteria = scoring_criteria or PathScoringCriteria()
    current_concept = session_tracker.current_concept
    current_mastery = session_tracker.concept_mastery_tracking.get(current_concept, 0.0)
    support_set = set(active_supports)
    pattern_set = set(active_patterns)
    enriched_paths: list[EnrichedPathEvaluation] = []

    for index, path in enumerate(candidate_paths, start=1):
        goal_alignment_score, goal_alignment_explanation = _goal_alignment_for_path(
            path,
            learning_goals,
            current_concept,
            current_mastery,
        )
        history_alignment_score, history_alignment_explanation = _history_alignment_for_path(
            path,
            session_tracker,
        )
        evidence_continuity_score, evidence_continuity_explanation = _evidence_continuity_for_path(
            path,
            pattern_set,
        )
        profile_match_score, profile_match_explanation = _profile_match_for_path(
            path,
            support_set,
        )
        pilot_data_adjustment_score, pilot_data_references = _pilot_data_adjustment_for_path(
            path,
            pattern_set,
        )

        total_score = (
            path.score * criteria.heuristic_weight
            + goal_alignment_score * criteria.goal_alignment_weight
            + history_alignment_score * criteria.history_alignment_weight
            + evidence_continuity_score * criteria.evidence_continuity_weight
            + profile_match_score * criteria.profile_match_weight
            + pilot_data_adjustment_score * criteria.pilot_data_adjustment_weight
        )

        enriched_paths.append(
            EnrichedPathEvaluation(
                path_id=f"path_{index}",
                block_types=path.block_types,
                raw_score=path.score,
                total_score=max(0.0, min(1.0, total_score)),
                mastery_projection=_mastery_projection_for_path(path, current_mastery),
                score_breakdown={
                    "heuristic": round(path.score, 4),
                    "goal_alignment": round(goal_alignment_score, 4),
                    "history_alignment": round(history_alignment_score, 4),
                    "evidence_continuity": round(evidence_continuity_score, 4),
                    "profile_match": round(profile_match_score, 4),
                    "pilot_data_adjustment": round(pilot_data_adjustment_score, 4),
                },
                goal_alignment_explanation=goal_alignment_explanation,
                history_alignment_explanation=history_alignment_explanation,
                evidence_continuity_explanation=evidence_continuity_explanation,
                profile_match_explanation=profile_match_explanation,
                pilot_data_references=pilot_data_references,
            )
        )

    enriched_paths.sort(key=lambda item: item.total_score, reverse=True)
    return enriched_paths


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

    alternatives = _default_alternatives(
        current_block_type,
        suggested_next_block_type,
        intent,
    )
    candidate_paths = _build_candidate_paths(
        current_block_type=current_block_type,
        preferred_next_block_type=suggested_next_block_type,
        alternative_next_block_types=alternatives,
        intent=intent,
        patterns=patterns,
        supports=supports,
        recent=recent,
    )
    if candidate_paths:
        selected_path = candidate_paths[0]
        lookahead = selected_path.block_types
        selected_path_score = selected_path.score
        rationale.append(
            f"Lookahead compared {len(candidate_paths)} candidate paths and selected the highest-scoring route."
        )
    else:
        lookahead = _build_lookahead(intent, current_block_type, suggested_next_block_type)
        selected_path_score = confidence

    return BlockSequenceDecision(
        current_block_type=current_block_type,
        suggested_next_block_type=suggested_next_block_type,
        alternative_next_block_types=alternatives,
        transition_reason=transition_reason,
        sequence_intent=intent,
        rationale=rationale,
        confidence=confidence,
        lookahead_block_types=lookahead,
        selected_path_score=selected_path_score,
        candidate_paths=candidate_paths,
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
