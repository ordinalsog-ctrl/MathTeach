from dataclasses import dataclass
from itertools import combinations

from mathteach.models import ConflictResolutionSummary
from mathteach.response_matrix import SupportNeed, TutorResponseSettings


PROFILE_APPLICATION_ORDER: tuple[SupportNeed, ...] = (
    "adhd_aware_support",
    "dyscalculia_aware_support",
    "dyslexia_aware_support",
    "autism_spectrum_aware_support",
    "language_sensitive_support",
    "scarcity_aware_support",
)

PROFILE_COMPATIBILITY: dict[frozenset[SupportNeed], tuple[str, ...]] = {
    frozenset({"adhd_aware_support", "dyscalculia_aware_support"}): (
        "session_duration",
        "break_pattern",
        "worked_example_ratio",
        "fading_speed",
        "primary_representation",
    ),
    frozenset({"adhd_aware_support", "dyslexia_aware_support"}): (),
    frozenset({"adhd_aware_support", "autism_spectrum_aware_support"}): (
        "session_duration",
        "break_pattern",
        "check_frequency",
    ),
    frozenset({"adhd_aware_support", "language_sensitive_support"}): (),
    frozenset({"adhd_aware_support", "scarcity_aware_support"}): (
        "worked_example_ratio",
        "check_frequency",
        "language_support",
    ),
    frozenset({"dyscalculia_aware_support", "dyslexia_aware_support"}): (),
    frozenset({"dyscalculia_aware_support", "autism_spectrum_aware_support"}): (),
    frozenset({"dyscalculia_aware_support", "language_sensitive_support"}): (
        "symbolic_vs_verbal_balance",
        "primary_representation",
        "language_support",
    ),
    frozenset({"dyscalculia_aware_support", "scarcity_aware_support"}): (
        "session_duration",
        "worked_example_ratio",
        "check_frequency",
    ),
    frozenset({"dyslexia_aware_support", "autism_spectrum_aware_support"}): (),
    frozenset({"dyslexia_aware_support", "language_sensitive_support"}): (),
    frozenset({"dyslexia_aware_support", "scarcity_aware_support"}): (),
    frozenset({"autism_spectrum_aware_support", "language_sensitive_support"}): (),
    frozenset({"autism_spectrum_aware_support", "scarcity_aware_support"}): (),
    frozenset({"language_sensitive_support", "scarcity_aware_support"}): (),
}

TRIAD_PRIORITY_LADDERS: dict[frozenset[SupportNeed], dict[str, tuple[str, ...]]] = {
    frozenset(
        {
            "adhd_aware_support",
            "dyscalculia_aware_support",
            "scarcity_aware_support",
        }
    ): {
        "priority_ladder": (
            "conceptual_grounding_before_speed",
            "visible_progress_before_problem_volume",
            "regulation_cadence_before_long_unbroken_work",
        ),
        "axes": (
            "session_duration",
            "break_pattern",
            "worked_example_ratio",
            "check_frequency",
            "language_support",
        ),
    },
    frozenset(
        {
            "adhd_aware_support",
            "autism_spectrum_aware_support",
            "scarcity_aware_support",
        }
    ): {
        "priority_ladder": (
            "predictable_structure_before_novelty",
            "sensory_stability_before_task_volume",
            "immediate_relevance_before_formal_depth",
        ),
        "axes": (
            "session_duration",
            "break_pattern",
            "check_frequency",
            "sensory_load_level",
            "language_support",
        ),
    },
    frozenset(
        {
            "dyscalculia_aware_support",
            "language_sensitive_support",
            "scarcity_aware_support",
        }
    ): {
        "priority_ladder": (
            "quantity_meaning_before_symbol_compression",
            "language_bridge_before_formal_vocabulary",
            "visible_success_before_session_density",
        ),
        "axes": (
            "symbolic_vs_verbal_balance",
            "primary_representation",
            "language_support",
            "check_frequency",
            "session_duration",
        ),
    },
}

BLOCK_TRIAD_PRIORITY_LADDERS: dict[frozenset[SupportNeed], tuple[SupportNeed, ...]] = {
    frozenset(
        {
            "adhd_aware_support",
            "dyscalculia_aware_support",
            "language_sensitive_support",
        }
    ): (
        "dyscalculia_aware_support",
        "language_sensitive_support",
        "adhd_aware_support",
    ),
    frozenset(
        {
            "adhd_aware_support",
            "autism_spectrum_aware_support",
            "dyslexia_aware_support",
        }
    ): (
        "dyslexia_aware_support",
        "autism_spectrum_aware_support",
        "adhd_aware_support",
    ),
    frozenset(
        {
            "dyscalculia_aware_support",
            "language_sensitive_support",
            "scarcity_aware_support",
        }
    ): (
        "dyscalculia_aware_support",
        "language_sensitive_support",
        "scarcity_aware_support",
    ),
}

BLOCK_PAIR_PRIORITY_LADDERS: dict[frozenset[SupportNeed], tuple[SupportNeed, ...]] = {
    frozenset({"adhd_aware_support", "dyscalculia_aware_support"}): (
        "dyscalculia_aware_support",
        "adhd_aware_support",
    ),
    frozenset({"adhd_aware_support", "language_sensitive_support"}): (
        "language_sensitive_support",
        "adhd_aware_support",
    ),
    frozenset({"dyscalculia_aware_support", "autism_spectrum_aware_support"}): (
        "autism_spectrum_aware_support",
        "dyscalculia_aware_support",
    ),
    frozenset({"adhd_aware_support", "dyslexia_aware_support"}): (
        "dyslexia_aware_support",
        "adhd_aware_support",
    ),
    frozenset({"dyscalculia_aware_support", "language_sensitive_support"}): (
        "language_sensitive_support",
        "dyscalculia_aware_support",
    ),
    frozenset({"autism_spectrum_aware_support", "language_sensitive_support"}): (
        "autism_spectrum_aware_support",
        "language_sensitive_support",
    ),
}

MOVE_OWNER_HINTS: dict[SupportNeed, set[str]] = {
    "adhd_aware_support": {
        "announce_short_goal_before_block",
        "use_step_labels_and_micro_checkpoints",
        "keep_feedback_near_immediate",
        "tighten_attention_window_after_drift",
        "increase_pacing_after_stable_success",
        "increase_pacing_monitor_only_after_concept_recovery",
        "increase_pacing_gently_after_language_clarification",
        "increase_pacing_after_text_clarity",
        "increase_pacing_after_concept_and_language_stabilize",
        "increase_pacing_only_with_predictable_sequence",
        "fade_one_scaffold_after_stable_success",
        "offer_more_independent_challenge",
        "pair_shorter_text_with_clear_reading_path",
    },
    "dyscalculia_aware_support": {
        "keep_quantity_representation_visible",
        "delay_dense_symbolic_compression",
        "rebuild_errors_from_quantity_model",
        "return_to_quantity_model_before_symbols",
        "stop_retry_loop_and_reframe_concept",
        "switch_from_attempt_counting_to_model_rebuild",
        "reframe_concept_with_everyday_language_bridge",
        "reframe_concept_with_simple_language_and_quantity_support",
        "reframe_concept_with_minimal_language_overhead",
        "pair_visual_explanation_with_simple_language",
    },
    "dyslexia_aware_support": {
        "reduce_text_load_before_problem_solving",
        "check_reading_load_before_math_correction",
        "split_problem_text_into_shorter_chunks",
        "reduce_text_load_with_readaloud_anchor",
        "split_problem_text_into_shorter_predictable_chunks",
        "use_predictable_visual_reading_sequence",
    },
    "autism_spectrum_aware_support": {
        "keep_structure_predictable_and_literal",
        "stabilize_layout_before_variation",
        "freeze_format_changes_until_reorientation",
        "stabilize_layout_before_new_quantity_variation",
        "bridge_language_with_consistent_patterning",
        "clarify_terms_with_literal_consistent_frame",
        "keep_structure_predictable_with_visual_reading_anchors",
        "use_consistent_bilingual_patterns",
    },
    "language_sensitive_support": {
        "bridge_everyday_language_and_math_terms",
        "confirm_term_meaning_at_major_steps",
        "clarify_terms_before_retrying_math_step",
        "keep_glossary_visible_across_blocks",
        "restate_key_term_before_new_symbolic_step",
        "clarify_terms_inside_quantity_rebuild",
        "pair_visual_explanation_with_simple_language",
        "bridge_language_with_consistent_patterning",
        "clarify_terms_with_literal_consistent_frame",
    },
    "scarcity_aware_support": {
        "state_success_criteria_up_front",
        "mark_small_visible_wins",
        "protect_momentum_with_near_term_success_target",
        "shrink_goal_to_single_recoverable_win",
        "reset_success_criteria_for_next_attempt",
        "state_tiny_success_criteria_before_concept_repair",
        "keep_concept_repair_within_visible_resource_limits",
    },
}


@dataclass(frozen=True)
class DetectedProfileConflict:
    profiles: tuple[SupportNeed, SupportNeed]
    axes: tuple[str, ...]

    @property
    def slug(self) -> str:
        return f"{self.profiles[0]}__{self.profiles[1]}"


@dataclass(frozen=True)
class DetectedProfileTriad:
    profiles: tuple[SupportNeed, SupportNeed, SupportNeed]
    priority_ladder: tuple[str, ...]
    axes: tuple[str, ...]

    @property
    def slug(self) -> str:
        return f"{self.profiles[0]}__{self.profiles[1]}__{self.profiles[2]}"


def _merge_unique(existing: list[str], additions: list[str]) -> list[str]:
    merged = list(existing)
    seen = set(existing)
    for item in additions:
        if item not in seen:
            merged.append(item)
            seen.add(item)
    return merged


def ordered_active_supports(active_supports: list[SupportNeed]) -> list[SupportNeed]:
    ordered = [need for need in PROFILE_APPLICATION_ORDER if need in active_supports]
    extras = [need for need in active_supports if need not in ordered]
    return ordered + extras


def detect_profile_conflicts(active_supports: list[SupportNeed]) -> list[DetectedProfileConflict]:
    conflicts: list[DetectedProfileConflict] = []
    ordered = ordered_active_supports(active_supports)
    for left, right in combinations(ordered, 2):
        axes = PROFILE_COMPATIBILITY.get(frozenset({left, right}), ())
        if axes:
            conflicts.append(DetectedProfileConflict(profiles=(left, right), axes=axes))
    return conflicts


def detect_profile_triads(active_supports: list[SupportNeed]) -> list[DetectedProfileTriad]:
    triads: list[DetectedProfileTriad] = []
    ordered = ordered_active_supports(active_supports)
    for trio in combinations(ordered, 3):
        triad_meta = TRIAD_PRIORITY_LADDERS.get(frozenset(trio))
        if triad_meta:
            triads.append(
                DetectedProfileTriad(
                    profiles=trio,
                    priority_ladder=triad_meta["priority_ladder"],
                    axes=triad_meta["axes"],
                )
            )
    return triads


def resolve_block_support_conflicts(
    support_moves: list[str],
    active_supports: list[SupportNeed],
    evidence: list[str],
) -> tuple[list[str], ConflictResolutionSummary | None]:
    ordered_supports = ordered_active_supports(active_supports)
    pair_conflicts = detect_profile_conflicts(ordered_supports)
    triad_slug, priority_ladder = _resolve_block_priority_ladder(ordered_supports, evidence)

    summary = ConflictResolutionSummary(
        pair_conflicts=[conflict.slug for conflict in pair_conflicts],
        triad_group=triad_slug,
        priority_ladder=list(priority_ladder),
        evidence_used=sorted(evidence),
    )

    resolved_moves = list(support_moves)
    evidence_set = set(evidence)

    resolved_moves = _apply_pair_level_move_adaptations(
        resolved_moves,
        ordered_supports,
        evidence_set,
        summary,
    )
    resolved_moves = _apply_triad_level_move_adaptations(
        resolved_moves,
        ordered_supports,
        evidence_set,
        summary,
    )
    resolved_moves = _apply_move_dependency_graph(
        resolved_moves,
        evidence_set,
        summary,
    )

    resolved_moves = _sort_moves_by_priority_ladder(
        resolved_moves,
        active_supports=ordered_supports,
        priority_ladder=priority_ladder,
    )

    if (
        not summary.pair_conflicts
        and summary.triad_group is None
        and not summary.suppressed_moves
        and not summary.adapted_moves
        and not summary.generated_moves
        and not summary.move_dependencies_applied
    ):
        return resolved_moves, None
    return resolved_moves, summary


def _resolve_block_priority_ladder(
    active_supports: list[SupportNeed],
    evidence: list[str],
) -> tuple[str | None, tuple[SupportNeed, ...]]:
    active_support_set = frozenset(active_supports)
    evidence_set = set(evidence)

    triad_ladder = BLOCK_TRIAD_PRIORITY_LADDERS.get(active_support_set)
    if triad_ladder is not None:
        triad_slug = "__".join(triad_ladder)
        if evidence_set & {
            "repeated_attempt_three_plus",
            "repeated_concept_error",
            "repeated_concept_error_across_blocks",
        }:
            triad_ladder = _move_support_to_front(
                triad_ladder, "dyscalculia_aware_support"
            )
        elif evidence_set & {
            "text_overload",
            "vocabulary_request",
            "vocabulary_request_again",
        }:
            triad_ladder = _move_support_to_front(
                triad_ladder, "language_sensitive_support"
            )
        elif evidence_set & {"reading_load_issue"}:
            triad_ladder = _move_support_to_front(triad_ladder, "dyslexia_aware_support")
        elif evidence_set & {"structure_break", "answer_abandoned"}:
            triad_ladder = _move_support_to_front(
                triad_ladder, "autism_spectrum_aware_support"
            )
        elif evidence_set & {
            "no_progress_two_blocks",
            "no_progress_three_blocks",
            "no_success_visible_two_blocks",
        }:
            triad_ladder = _move_support_to_front(triad_ladder, "scarcity_aware_support")
        elif evidence_set & {"rapid_success_two_blocks", "rapid_success_three_blocks"}:
            triad_ladder = _move_support_to_front(triad_ladder, "adhd_aware_support")
        return triad_slug, triad_ladder

    for pair in combinations(active_supports, 2):
        pair_ladder = BLOCK_PAIR_PRIORITY_LADDERS.get(frozenset(pair))
        if pair_ladder is None:
            continue
        pair_set = frozenset(pair)
        if (
            pair_set == frozenset({"adhd_aware_support", "language_sensitive_support"})
            and evidence_set & {"rapid_success_two_blocks", "rapid_success_three_blocks"}
            and not evidence_set
            & {"text_overload", "vocabulary_request", "vocabulary_request_again"}
        ):
            pair_ladder = _move_support_to_front(pair_ladder, "adhd_aware_support")
        elif (
            pair_set == frozenset({"adhd_aware_support", "dyslexia_aware_support"})
            and evidence_set & {"rapid_success_two_blocks", "rapid_success_three_blocks"}
            and not evidence_set & {"text_overload", "reading_load_issue"}
        ):
            pair_ladder = _move_support_to_front(pair_ladder, "adhd_aware_support")
        elif (
            pair_set == frozenset({"dyscalculia_aware_support", "language_sensitive_support"})
            and evidence_set
            & {
                "repeated_attempt_three_plus",
                "repeated_concept_error",
                "repeated_concept_error_across_blocks",
            }
        ):
            pair_ladder = _move_support_to_front(pair_ladder, "dyscalculia_aware_support")
        elif (
            pair_set == frozenset({"autism_spectrum_aware_support", "language_sensitive_support"})
            and evidence_set & {"vocabulary_request", "vocabulary_request_again"}
            and not evidence_set & {"structure_break", "text_overload"}
        ):
            pair_ladder = _move_support_to_front(
                pair_ladder, "language_sensitive_support"
            )
        return None, pair_ladder

    return None, tuple(active_supports)


def _move_support_to_front(
    ladder: tuple[SupportNeed, ...],
    support_need: SupportNeed,
) -> tuple[SupportNeed, ...]:
    if support_need not in ladder:
        return ladder
    return (support_need, *tuple(item for item in ladder if item != support_need))


def _apply_pair_level_move_adaptations(
    moves: list[str],
    active_supports: list[SupportNeed],
    evidence: set[str],
    summary: ConflictResolutionSummary,
) -> list[str]:
    resolved_moves = list(moves)

    if {
        "adhd_aware_support",
        "dyscalculia_aware_support",
    }.issubset(active_supports) and evidence & {
        "repeated_attempt_three_plus",
        "repeated_concept_error",
        "repeated_concept_error_across_blocks",
    }:
        if evidence & {"rapid_success_two_blocks", "rapid_success_three_blocks"}:
            resolved_moves = _replace_move(
                resolved_moves,
                "increase_pacing_after_stable_success",
                "increase_pacing_monitor_only_after_concept_recovery",
                summary,
            )
            resolved_moves = _remove_move(
                resolved_moves,
                "offer_more_independent_challenge",
                summary,
                (
                    "Suppressed independent challenge while dyscalculia-oriented concept repair "
                    "has priority for this block."
                ),
            )

    if {
        "adhd_aware_support",
        "language_sensitive_support",
    }.issubset(active_supports) and evidence & {
        "text_overload",
        "vocabulary_request",
        "vocabulary_request_again",
    }:
        if evidence & {"rapid_success_two_blocks", "rapid_success_three_blocks"}:
            resolved_moves = _replace_move(
                resolved_moves,
                "increase_pacing_after_stable_success",
                "increase_pacing_gently_after_language_clarification",
                summary,
            )
            resolved_moves = _remove_move(
                resolved_moves,
                "offer_more_independent_challenge",
                summary,
                (
                    "Suppressed independent challenge until language load is clarified for this "
                    "block."
                ),
            )

    if {
        "dyscalculia_aware_support",
        "autism_spectrum_aware_support",
    }.issubset(active_supports) and evidence & {
        "repeated_attempt_three_plus",
        "structure_break",
        "repeated_concept_error",
    }:
        resolved_moves = _replace_move(
            resolved_moves,
            "stabilize_layout_before_variation",
            "stabilize_layout_before_new_quantity_variation",
            summary,
        )

    if {
        "adhd_aware_support",
        "dyslexia_aware_support",
    }.issubset(active_supports) and evidence & {
        "text_overload",
        "reading_load_issue",
    }:
        resolved_moves = _replace_move(
            resolved_moves,
            "reduce_text_load_before_problem_solving",
            "reduce_text_load_with_readaloud_anchor",
            summary,
        )
        if evidence & {"rapid_success_two_blocks", "rapid_success_three_blocks"}:
            resolved_moves = _replace_move(
                resolved_moves,
                "increase_pacing_after_stable_success",
                "increase_pacing_after_text_clarity",
                summary,
            )
            resolved_moves = _remove_move(
                resolved_moves,
                "offer_more_independent_challenge",
                summary,
                (
                    "Suppressed independent challenge until dyslexia-aware readability "
                    "supports have stabilized this block."
                ),
            )

    if {
        "dyscalculia_aware_support",
        "language_sensitive_support",
    }.issubset(active_supports) and evidence & {
        "repeated_attempt_three_plus",
        "repeated_concept_error",
        "repeated_concept_error_across_blocks",
        "text_overload",
        "vocabulary_request",
        "vocabulary_request_again",
    }:
        resolved_moves = _replace_move(
            resolved_moves,
            "stop_retry_loop_and_reframe_concept",
            "reframe_concept_with_everyday_language_bridge",
            summary,
        )
        resolved_moves = _replace_move(
            resolved_moves,
            "clarify_terms_before_retrying_math_step",
            "clarify_terms_inside_quantity_rebuild",
            summary,
        )

    if {
        "autism_spectrum_aware_support",
        "language_sensitive_support",
    }.issubset(active_supports) and evidence & {
        "text_overload",
        "structure_break",
        "vocabulary_request_again",
    }:
        resolved_moves = _replace_move(
            resolved_moves,
            "bridge_everyday_language_and_math_terms",
            "bridge_language_with_consistent_patterning",
            summary,
        )
        resolved_moves = _replace_move(
            resolved_moves,
            "clarify_terms_before_retrying_math_step",
            "clarify_terms_with_literal_consistent_frame",
            summary,
        )

    return resolved_moves


def _apply_triad_level_move_adaptations(
    moves: list[str],
    active_supports: list[SupportNeed],
    evidence: set[str],
    summary: ConflictResolutionSummary,
) -> list[str]:
    active_support_set = frozenset(active_supports)
    resolved_moves = list(moves)

    if active_support_set == frozenset(
        {
            "adhd_aware_support",
            "dyscalculia_aware_support",
            "language_sensitive_support",
        }
    ) and evidence & {
        "repeated_attempt_three_plus",
        "text_overload",
        "vocabulary_request_again",
    }:
        resolved_moves = _replace_first_available_move(
            resolved_moves,
            (
                "reframe_concept_with_everyday_language_bridge",
                "stop_retry_loop_and_reframe_concept",
            ),
            "reframe_concept_with_simple_language_and_quantity_support",
            summary,
        )
        resolved_moves = _replace_first_available_move(
            resolved_moves,
            (
                "increase_pacing_monitor_only_after_concept_recovery",
                "increase_pacing_gently_after_language_clarification",
                "increase_pacing_after_stable_success",
            ),
            "increase_pacing_after_concept_and_language_stabilize",
            summary,
        )
        resolved_moves = _remove_move(
            resolved_moves,
            "offer_more_independent_challenge",
            summary,
            (
                "Suppressed independent challenge until concept repair and language "
                "clarification stabilize together."
            ),
        )

    if active_support_set == frozenset(
        {
            "adhd_aware_support",
            "autism_spectrum_aware_support",
            "dyslexia_aware_support",
        }
    ) and evidence & {"text_overload", "reading_load_issue", "structure_break"}:
        resolved_moves = _replace_move(
            resolved_moves,
            "split_problem_text_into_shorter_chunks",
            "split_problem_text_into_shorter_predictable_chunks",
            summary,
        )
        resolved_moves = _replace_move(
            resolved_moves,
            "keep_structure_predictable_and_literal",
            "keep_structure_predictable_with_visual_reading_anchors",
            summary,
        )
        if evidence & {"rapid_success_two_blocks", "rapid_success_three_blocks"}:
            resolved_moves = _replace_first_available_move(
                resolved_moves,
                (
                    "increase_pacing_after_text_clarity",
                    "increase_pacing_after_stable_success",
                ),
                "increase_pacing_only_with_predictable_sequence",
                summary,
            )
            resolved_moves = _remove_move(
                resolved_moves,
                "offer_more_independent_challenge",
                summary,
                (
                    "Suppressed independent challenge until readable and predictable "
                    "sequencing stay stable together."
                ),
            )

    if active_support_set == frozenset(
        {
            "dyscalculia_aware_support",
            "language_sensitive_support",
            "scarcity_aware_support",
        }
    ) and evidence & {
        "repeated_attempt_three_plus",
        "no_progress_two_blocks",
        "no_progress_three_blocks",
        "text_overload",
        "vocabulary_request_again",
    }:
        resolved_moves = _replace_first_available_move(
            resolved_moves,
            (
                "reframe_concept_with_everyday_language_bridge",
                "stop_retry_loop_and_reframe_concept",
            ),
            "reframe_concept_with_minimal_language_overhead",
            summary,
        )
        resolved_moves = _replace_move(
            resolved_moves,
            "state_success_criteria_up_front",
            "state_tiny_success_criteria_before_concept_repair",
            summary,
        )

    return resolved_moves


def _apply_move_dependency_graph(
    moves: list[str],
    evidence: set[str],
    summary: ConflictResolutionSummary,
) -> list[str]:
    resolved_moves = list(moves)

    if {
        "keep_quantity_representation_visible",
        "clarify_terms_inside_quantity_rebuild",
    }.issubset(resolved_moves):
        resolved_moves = _append_generated_move(
            resolved_moves,
            "pair_visual_explanation_with_simple_language",
            summary,
            (
                "Generated pair_visual_explanation_with_simple_language from quantity "
                "support plus language clarification."
            ),
        )

    if {
        "reduce_text_load_with_readaloud_anchor",
        "use_step_labels_and_micro_checkpoints",
    }.issubset(resolved_moves):
        resolved_moves = _append_generated_move(
            resolved_moves,
            "pair_shorter_text_with_clear_reading_path",
            summary,
            (
                "Generated pair_shorter_text_with_clear_reading_path from readability "
                "support plus ADHD micro-checkpoints."
            ),
        )

    if {
        "split_problem_text_into_shorter_predictable_chunks",
        "keep_structure_predictable_with_visual_reading_anchors",
    }.issubset(resolved_moves):
        resolved_moves = _append_generated_move(
            resolved_moves,
            "use_predictable_visual_reading_sequence",
            summary,
            (
                "Generated use_predictable_visual_reading_sequence from predictable "
                "chunking plus stable reading anchors."
            ),
        )

    if {
        "bridge_language_with_consistent_patterning",
        "clarify_terms_with_literal_consistent_frame",
    }.issubset(resolved_moves):
        resolved_moves = _append_generated_move(
            resolved_moves,
            "use_consistent_bilingual_patterns",
            summary,
            (
                "Generated use_consistent_bilingual_patterns from language bridging plus "
                "literal consistent framing."
            ),
        )

    if {
        "reframe_concept_with_minimal_language_overhead",
        "state_tiny_success_criteria_before_concept_repair",
    }.issubset(resolved_moves):
        resolved_moves = _append_generated_move(
            resolved_moves,
            "keep_concept_repair_within_visible_resource_limits",
            summary,
            (
                "Generated keep_concept_repair_within_visible_resource_limits from "
                "scarcity-aware success framing plus minimal-language concept repair."
            ),
        )

    if "increase_pacing_after_concept_and_language_stabilize" in resolved_moves:
        resolved_moves = _remove_move(
            resolved_moves,
            "increase_pacing_monitor_only_after_concept_recovery",
            summary,
            "Suppressed the weaker pacing monitor move because a stronger stabilized pacing move was generated.",
        )
        resolved_moves = _remove_move(
            resolved_moves,
            "increase_pacing_gently_after_language_clarification",
            summary,
            "Suppressed the language-only pacing move because concept and language stabilization now gate pacing together.",
        )

    if "increase_pacing_after_text_clarity" in resolved_moves:
        resolved_moves = _remove_move(
            resolved_moves,
            "increase_pacing_after_stable_success",
            summary,
            "Suppressed generic pacing because dyslexia-aware readability now gates pacing.",
        )

    if "increase_pacing_only_with_predictable_sequence" in resolved_moves:
        resolved_moves = _remove_move(
            resolved_moves,
            "increase_pacing_after_stable_success",
            summary,
            "Suppressed generic pacing because predictable sequencing must hold first.",
        )

    if "reframe_concept_with_simple_language_and_quantity_support" in resolved_moves:
        resolved_moves = _remove_move(
            resolved_moves,
            "reframe_concept_with_everyday_language_bridge",
            summary,
            "Suppressed the narrower language bridge because the triad-specific concept repair move supersedes it.",
        )

    if "reframe_concept_with_minimal_language_overhead" in resolved_moves:
        resolved_moves = _remove_move(
            resolved_moves,
            "reframe_concept_with_everyday_language_bridge",
            summary,
            "Suppressed the broader language bridge because the scarcity-aware minimal-language repair move supersedes it.",
        )

    if "split_problem_text_into_shorter_predictable_chunks" in resolved_moves:
        resolved_moves = _remove_move(
            resolved_moves,
            "split_problem_text_into_shorter_chunks",
            summary,
            "Suppressed plain text chunking because predictable chunking is now active.",
        )

    if "keep_structure_predictable_with_visual_reading_anchors" in resolved_moves:
        resolved_moves = _remove_move(
            resolved_moves,
            "keep_structure_predictable_and_literal",
            summary,
            "Suppressed generic predictable structure because the reading-anchor variant is now active.",
        )

    if "bridge_language_with_consistent_patterning" in resolved_moves:
        resolved_moves = _remove_move(
            resolved_moves,
            "bridge_everyday_language_and_math_terms",
            summary,
            "Suppressed the generic language bridge because consistent patterning is now active.",
        )

    if "clarify_terms_with_literal_consistent_frame" in resolved_moves:
        resolved_moves = _remove_move(
            resolved_moves,
            "clarify_terms_before_retrying_math_step",
            summary,
            "Suppressed generic term clarification because the literal consistent variant is now active.",
        )

    if (
        "increase_pacing_after_concept_and_language_stabilize" in resolved_moves
        and "pair_visual_explanation_with_simple_language" in resolved_moves
        and not evidence & {"rapid_success_two_blocks", "rapid_success_three_blocks"}
    ):
        resolved_moves = _replace_move(
            resolved_moves,
            "increase_pacing_after_concept_and_language_stabilize",
            "increase_pacing_monitor_only_after_concept_recovery",
            summary,
        )

    return resolved_moves


def _replace_move(
    moves: list[str],
    original: str,
    replacement: str,
    summary: ConflictResolutionSummary,
) -> list[str]:
    if original not in moves:
        return moves
    summary.adapted_moves.append(f"{original} -> {replacement}")
    summary.resolution_notes.append(
        f"Adapted {original} to {replacement} for the current evidence mix."
    )
    return [replacement if move == original else move for move in moves]


def _replace_first_available_move(
    moves: list[str],
    originals: tuple[str, ...],
    replacement: str,
    summary: ConflictResolutionSummary,
) -> list[str]:
    resolved_moves = list(moves)
    for original in originals:
        if original in resolved_moves:
            return _replace_move(resolved_moves, original, replacement, summary)
    return resolved_moves


def _remove_move(
    moves: list[str],
    move_to_remove: str,
    summary: ConflictResolutionSummary,
    note: str,
) -> list[str]:
    if move_to_remove not in moves:
        return moves
    summary.suppressed_moves.append(move_to_remove)
    summary.resolution_notes.append(note)
    return [move for move in moves if move != move_to_remove]


def _append_generated_move(
    moves: list[str],
    move_to_add: str,
    summary: ConflictResolutionSummary,
    note: str,
) -> list[str]:
    if move_to_add in moves:
        return moves
    summary.generated_moves.append(move_to_add)
    summary.move_dependencies_applied.append(note)
    summary.resolution_notes.append(note)
    return [*moves, move_to_add]


def _sort_moves_by_priority_ladder(
    moves: list[str],
    active_supports: list[SupportNeed],
    priority_ladder: tuple[SupportNeed, ...],
) -> list[str]:
    if not priority_ladder:
        return moves

    ranks = {support: index for index, support in enumerate(priority_ladder)}

    def sort_key(indexed_move: tuple[int, str]) -> tuple[int, int]:
        original_index, move = indexed_move
        owner = _infer_move_owner(move, active_supports)
        return (ranks.get(owner, len(ranks)), original_index)

    return [move for _, move in sorted(enumerate(moves), key=sort_key)]


def _infer_move_owner(
    move: str,
    active_supports: list[SupportNeed],
) -> SupportNeed | None:
    for support_need in active_supports:
        if move in MOVE_OWNER_HINTS.get(support_need, set()):
            return support_need
    return None


def _register_resolution(
    settings: TutorResponseSettings,
    slug: str,
    note: str,
    source_anchors: list[str],
) -> TutorResponseSettings:
    settings.conflict_pairs = _merge_unique(settings.conflict_pairs, [slug])
    settings.conflict_resolution_notes = _merge_unique(
        settings.conflict_resolution_notes, [note]
    )
    settings.rationale_summary = _merge_unique(settings.rationale_summary, [note])
    settings.source_anchors = _merge_unique(settings.source_anchors, source_anchors)
    return settings


def _register_triad_resolution(
    settings: TutorResponseSettings,
    slug: str,
    priority_ladder: tuple[str, ...],
    note: str,
    source_anchors: list[str],
) -> TutorResponseSettings:
    settings.triad_groups = _merge_unique(settings.triad_groups, [slug])
    settings.priority_ladders = _merge_unique(
        settings.priority_ladders, list(priority_ladder)
    )
    settings.conflict_resolution_notes = _merge_unique(
        settings.conflict_resolution_notes, [note]
    )
    settings.rationale_summary = _merge_unique(settings.rationale_summary, [note])
    settings.source_anchors = _merge_unique(settings.source_anchors, source_anchors)
    return settings


def _resolve_adhd_and_dyscalculia(settings: TutorResponseSettings) -> TutorResponseSettings:
    settings.session_duration = "15_to_18_minute_concrete_focus_blocks"
    settings.break_pattern = "ultradian_micro_breaks_within_concrete_work"
    settings.worked_example_ratio = "high_examples_with_varied_contexts"
    settings.fading_speed = "very_gradual_with_novel_variation"
    settings.primary_representation = "manipulative_or_quantity_visual_with_varied_contexts"
    settings.external_scaffolds = _merge_unique(
        settings.external_scaffolds,
        [
            "varied_concrete_materials",
            "ultradian_re_entry_cues",
        ],
    )
    return _register_resolution(
        settings,
        "adhd_aware_support__dyscalculia_aware_support",
        (
            "For ADHD plus dyscalculia, keep the longer concrete path but vary contexts and "
            "insert ultradian regulation breaks."
        ),
        [
            "barkley-executive-functions-adhd",
            "butterworth-varma-laurillard-dyscalculia-science",
        ],
    )


def _resolve_adhd_and_autism(settings: TutorResponseSettings) -> TutorResponseSettings:
    settings.session_duration = "predictable_15_to_18_minute_focus_blocks"
    settings.break_pattern = "predictable_ultradian_regulation_breaks"
    settings.transition_buffer = "explicit_transition_cue_before_every_shift"
    settings.check_frequency = "predictable_checkpoint_rhythm"
    settings.sensory_load_level = "minimal_and_high_contrast"
    settings.external_scaffolds = _merge_unique(
        settings.external_scaffolds,
        [
            "predictable_movement_breaks",
            "stable_visual_layout",
        ],
    )
    return _register_resolution(
        settings,
        "adhd_aware_support__autism_spectrum_aware_support",
        (
            "For ADHD plus autism-spectrum support, preserve predictable structure while keeping "
            "ultradian regulation breaks explicit and low in sensory clutter."
        ),
        [
            "barkley-executive-functions-adhd",
            "rutherford-visual-supports-autism-scoping-review",
        ],
    )


def _resolve_adhd_and_scarcity(settings: TutorResponseSettings) -> TutorResponseSettings:
    settings.worked_example_ratio = "examples_then_quick_success_practice_with_varied_contexts"
    settings.check_frequency = "every_two_problems_with_progress_confirmation"
    settings.language_support = "plain_goal_and_relevance_framing"
    settings.word_budget_per_chunk = "short_clear_chunks_with_immediate_relevance"
    settings.external_scaffolds = _merge_unique(
        settings.external_scaffolds,
        [
            "why_this_matters_now",
            "small_wins_sequence",
            "clear_success_criteria",
        ],
    )
    return _register_resolution(
        settings,
        "adhd_aware_support__scarcity_aware_support",
        (
            "For ADHD plus scarcity-aware support, combine novelty with immediate relevance and "
            "make progress visible after very short cycles."
        ),
        [
            "barkley-executive-functions-adhd",
            "mani-mullainathan-shafir-zhao-poverty-cognition",
            "ryan-deci-self-determination-theory",
        ],
    )


def _resolve_dyscalculia_and_language_sensitive(
    settings: TutorResponseSettings,
) -> TutorResponseSettings:
    settings.symbolic_vs_verbal_balance = (
        "quantity_and_everyday_language_before_symbol_compression"
    )
    settings.primary_representation = "manipulative_or_quantity_visual_with_term_support"
    settings.language_support = "translated_key_terms_glossary_and_quantity_language_support"
    settings.word_budget_per_chunk = "short_chunks_with_controlled_vocabulary"
    settings.external_scaffolds = _merge_unique(
        settings.external_scaffolds,
        [
            "quantity_word_bridge",
            "key_term_glossary",
        ],
    )
    return _register_resolution(
        settings,
        "dyscalculia_aware_support__language_sensitive_support",
        (
            "For dyscalculia plus language-sensitive support, keep quantity meaning visible and "
            "anchor each symbol in everyday mathematical language."
        ),
        [
            "butterworth-varma-laurillard-dyscalculia-science",
            "ies-english-learners-practice-guide",
            "sharma-sharma-multilingual-math-meta-analysis",
        ],
    )


def _resolve_dyscalculia_and_scarcity(settings: TutorResponseSettings) -> TutorResponseSettings:
    settings.session_duration = "18_to_22_minute_concrete_success_blocks"
    settings.worked_example_ratio = "high_examples_with_small_success_cycles"
    settings.check_frequency = "after_each_major_micro_step_with_progress_confirmation"
    settings.transition_buffer = "brief_explicit_transition_with_goal_reminder"
    settings.language_support = "plain_goal_and_relevance_framing"
    settings.external_scaffolds = _merge_unique(
        settings.external_scaffolds,
        [
            "clear_success_criteria",
            "small_wins_sequence",
            "re_entry_summary_after_interruption",
        ],
    )
    return _register_resolution(
        settings,
        "dyscalculia_aware_support__scarcity_aware_support",
        (
            "For dyscalculia plus scarcity-aware support, slow the pace just enough for concrete "
            "understanding while ending each block with visible success."
        ),
        [
            "butterworth-varma-laurillard-dyscalculia-science",
            "mani-mullainathan-shafir-zhao-poverty-cognition",
            "ryan-deci-self-determination-theory",
        ],
    )


def _resolve_adhd_dyscalculia_scarcity_triad(
    settings: TutorResponseSettings,
    triad: DetectedProfileTriad,
) -> TutorResponseSettings:
    settings.session_duration = "15_to_18_minute_concrete_success_blocks"
    settings.break_pattern = "ultradian_micro_breaks_within_concrete_work"
    settings.transition_buffer = "brief_explicit_transition_with_goal_reminder"
    settings.worked_example_ratio = "high_examples_with_varied_contexts_and_small_success_cycles"
    settings.fading_speed = "very_gradual_with_novel_variation"
    settings.symbolic_vs_verbal_balance = "quantity_plus_language_before_symbol_compression"
    settings.primary_representation = "manipulative_or_quantity_visual_with_varied_contexts"
    settings.check_frequency = "after_each_major_micro_step_with_progress_confirmation"
    settings.language_support = "plain_goal_and_relevance_framing"
    settings.external_scaffolds = _merge_unique(
        settings.external_scaffolds,
        [
            "varied_concrete_materials",
            "clear_success_criteria",
            "small_wins_sequence",
            "why_this_matters_now",
            "re_entry_summary_after_interruption",
            "ultradian_re_entry_cues",
        ],
    )
    return _register_triad_resolution(
        settings,
        triad.slug,
        triad.priority_ladder,
        (
            "For ADHD plus dyscalculia plus scarcity-aware support, keep deep concrete grounding, "
            "protect visible progress, and regulate effort with short structured cycles."
        ),
        [
            "barkley-executive-functions-adhd",
            "butterworth-varma-laurillard-dyscalculia-science",
            "mani-mullainathan-shafir-zhao-poverty-cognition",
            "ryan-deci-self-determination-theory",
        ],
    )


def _resolve_adhd_autism_scarcity_triad(
    settings: TutorResponseSettings,
    triad: DetectedProfileTriad,
) -> TutorResponseSettings:
    settings.session_duration = "predictable_15_to_18_minute_focus_blocks"
    settings.break_pattern = "predictable_ultradian_regulation_breaks"
    settings.transition_buffer = "explicit_transition_cue_before_every_shift"
    settings.check_frequency = "predictable_progress_confirmation_rhythm"
    settings.language_support = "plain_goal_and_relevance_framing"
    settings.sensory_load_level = "minimal_and_high_contrast"
    settings.external_scaffolds = _merge_unique(
        settings.external_scaffolds,
        [
            "predictable_movement_breaks",
            "stable_visual_layout",
            "clear_success_criteria",
            "small_wins_sequence",
            "why_this_matters_now",
        ],
    )
    return _register_triad_resolution(
        settings,
        triad.slug,
        triad.priority_ladder,
        (
            "For ADHD plus autism-spectrum plus scarcity-aware support, keep structure and sensory "
            "stability primary, then make relevance and progress explicit inside that frame."
        ),
        [
            "barkley-executive-functions-adhd",
            "rutherford-visual-supports-autism-scoping-review",
            "mani-mullainathan-shafir-zhao-poverty-cognition",
        ],
    )


def _resolve_dyscalculia_language_scarcity_triad(
    settings: TutorResponseSettings,
    triad: DetectedProfileTriad,
) -> TutorResponseSettings:
    settings.session_duration = "18_to_22_minute_concrete_success_blocks"
    settings.symbolic_vs_verbal_balance = (
        "quantity_and_everyday_language_before_symbol_compression"
    )
    settings.word_budget_per_chunk = "short_chunks_with_controlled_vocabulary"
    settings.primary_representation = "manipulative_or_quantity_visual_with_term_support"
    settings.check_frequency = "after_each_major_micro_step_with_progress_confirmation"
    settings.language_support = (
        "translated_key_terms_glossary_quantity_language_and_relevance_support"
    )
    settings.external_scaffolds = _merge_unique(
        settings.external_scaffolds,
        [
            "quantity_word_bridge",
            "key_term_glossary",
            "clear_success_criteria",
            "small_wins_sequence",
            "why_this_matters_now",
            "re_entry_summary_after_interruption",
        ],
    )
    return _register_triad_resolution(
        settings,
        triad.slug,
        triad.priority_ladder,
        (
            "For dyscalculia plus language-sensitive plus scarcity-aware support, keep quantity "
            "meaning primary, carry it with explicit language bridges, and keep success visible."
        ),
        [
            "butterworth-varma-laurillard-dyscalculia-science",
            "ies-english-learners-practice-guide",
            "sharma-sharma-multilingual-math-meta-analysis",
            "mani-mullainathan-shafir-zhao-poverty-cognition",
        ],
    )


def resolve_mixed_profile_settings(
    settings: TutorResponseSettings,
    active_supports: list[SupportNeed],
) -> TutorResponseSettings:
    for conflict in detect_profile_conflicts(active_supports):
        pair = frozenset(conflict.profiles)
        if pair == frozenset({"adhd_aware_support", "dyscalculia_aware_support"}):
            settings = _resolve_adhd_and_dyscalculia(settings)
        elif pair == frozenset({"adhd_aware_support", "autism_spectrum_aware_support"}):
            settings = _resolve_adhd_and_autism(settings)
        elif pair == frozenset({"adhd_aware_support", "scarcity_aware_support"}):
            settings = _resolve_adhd_and_scarcity(settings)
        elif pair == frozenset({"dyscalculia_aware_support", "language_sensitive_support"}):
            settings = _resolve_dyscalculia_and_language_sensitive(settings)
        elif pair == frozenset({"dyscalculia_aware_support", "scarcity_aware_support"}):
            settings = _resolve_dyscalculia_and_scarcity(settings)

    for triad in detect_profile_triads(active_supports):
        trio = frozenset(triad.profiles)
        if trio == frozenset(
            {
                "adhd_aware_support",
                "dyscalculia_aware_support",
                "scarcity_aware_support",
            }
        ):
            settings = _resolve_adhd_dyscalculia_scarcity_triad(settings, triad)
        elif trio == frozenset(
            {
                "adhd_aware_support",
                "autism_spectrum_aware_support",
                "scarcity_aware_support",
            }
        ):
            settings = _resolve_adhd_autism_scarcity_triad(settings, triad)
        elif trio == frozenset(
            {
                "dyscalculia_aware_support",
                "language_sensitive_support",
                "scarcity_aware_support",
            }
        ):
            settings = _resolve_dyscalculia_language_scarcity_triad(settings, triad)

    return settings
