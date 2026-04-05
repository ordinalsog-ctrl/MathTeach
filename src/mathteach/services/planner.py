from mathteach.config import Settings
from mathteach.models import (
    BlockSequenceState,
    BlockType,
    LearnerProfile,
    ModelAssignment,
    ModeAdaptationCheckpoint,
    ResumeContext,
    ResumeSource,
    ModeAdaptationTraceEntry,
    ModeAdaptationState,
    ModeSelection,
    PlannedTeachingBlock,
    RawBlockObservation,
    RetrievalPlan,
    RuntimeObservationInput,
    SequencePlanningMetadata,
    SessionRequest,
    StackResponse,
    TeachingPlan,
)
from mathteach.services.block_sequence_planner import (
    advance_sequence_state,
    plan_next_block,
)
from mathteach.services.mode_selector import select_mode
from mathteach.services.conflict_resolver import resolve_block_support_conflicts
from mathteach.services.evidence_pattern_detector import build_evidence_combination
from mathteach.services.response_engine import build_support_response
from mathteach.services.runtime_mode_adapter import RuntimeModeAdapter


AUDIENCE_MODES = {
    "child": ("concrete and encouraging", "Use stories, objects, and tiny steps."),
    "teen": ("clear and motivating", "Connect rules to intuition and school examples."),
    "adult": ("respectful and practical", "Tie math to goals, utility, and confidence rebuilding."),
    "expert": ("precise and compact", "Prefer formalism, provenance, and alternative derivations."),
}

LEVEL_DEPTH = {
    "early_school": ("foundational", False),
    "middle_school": ("guided", False),
    "high_school": ("layered", True),
    "undergraduate": ("formal", True),
    "graduate": ("advanced", True),
    "research": ("research-grade", True),
}

ORIGIN_HINTS = (
    "laie",
    "einfach",
    "ursprung",
    "notwendig",
    "angewandt",
    "geschichte",
    "grundidee",
    "wozu",
    "warum",
)

EXAMPLE_HINTS = (
    "beispiel",
    "zahlenbeispiel",
    "anhand",
    "aufgabe",
    "rechne",
    "loese",
    "loesen",
    "gegeben",
)


def _normalize_text(value: str) -> str:
    return (
        value.casefold()
        .replace("\u00e4", "ae")
        .replace("\u00f6", "oe")
        .replace("\u00fc", "ue")
        .replace("\u00df", "ss")
    )


def _infer_lesson_mode(request: SessionRequest) -> str:
    objective = _normalize_text(request.objective)
    has_origin = any(hint in objective for hint in ORIGIN_HINTS)
    has_example = any(hint in objective for hint in EXAMPLE_HINTS)

    if has_origin and has_example:
        return "origin_then_example"
    if has_origin:
        return "origin_story_explanation"
    if has_example:
        return "worked_example_tutoring"
    if request.learner_profile.age_group == "expert":
        return "formal_compact_explanation"
    return "guided_concept_explanation"


def _mode_response_arc(lesson_mode: str) -> list[str]:
    if lesson_mode == "origin_story_explanation":
        return [
            "Start with the motivating problem before formal notation.",
            "Explain why the concept became necessary.",
            "Use plain language before symbols.",
            "Connect the concept to one simple example.",
            "Close with a present-day application.",
        ]
    if lesson_mode == "origin_then_example":
        return [
            "Start with the historical or intuitive need for the concept.",
            "Name the core mathematical idea in simple language.",
            "Work through the learner example step by step.",
            "Check the result against the original problem.",
            "End with a transfer pattern for similar tasks.",
        ]
    if lesson_mode == "worked_example_tutoring":
        return [
            "Restate the learner problem in simple words.",
            "Classify the problem type before solving.",
            "Solve one step at a time with local justification.",
            "Check the answer against the original statement.",
            "End with a reusable pattern summary.",
        ]
    if lesson_mode == "formal_compact_explanation":
        return [
            "State the formal object first.",
            "Name assumptions and notation explicitly.",
            "Give the shortest valid derivation path.",
            "Point to one alternative formulation or proof route.",
            "Close with source-aware next steps.",
        ]
    return [
        "Start from intuition before notation.",
        "Name the core mathematical object clearly.",
        "Give one small worked example.",
        "State the main rule or pattern explicitly.",
        "End with a quick self-check question.",
    ]


def _mode_history_strategy(lesson_mode: str, wants_history: bool) -> tuple[bool, str]:
    if lesson_mode == "origin_story_explanation":
        return True, "origin_first"
    if lesson_mode == "origin_then_example":
        return True, "origin_then_example"
    if lesson_mode == "worked_example_tutoring":
        return wants_history, "supporting_only" if wants_history else "minimal"
    if lesson_mode == "formal_compact_explanation":
        return wants_history, "minimal"
    return wants_history, "supporting_only" if wants_history else "minimal"


def _mode_network_focus(lesson_mode: str) -> list[str]:
    if lesson_mode == "origin_story_explanation":
        return [
            "transmission_path",
            "domain_line",
            "application_bridge",
        ]
    if lesson_mode == "origin_then_example":
        return [
            "domain_line",
            "equation_line",
            "application_bridge",
        ]
    if lesson_mode == "worked_example_tutoring":
        return [
            "equation_line",
            "proof_line",
        ]
    if lesson_mode == "formal_compact_explanation":
        return [
            "proof_line",
            "domain_line",
        ]
    return [
        "domain_line",
        "equation_line",
    ]


def _block_goal(lesson_mode: str, objective: str) -> str:
    if lesson_mode == "worked_example_tutoring":
        return f"Arbeite den naechsten loesbaren Schritt explizit an: {objective}"
    if lesson_mode == "origin_then_example":
        return f"Verbinde Sinnaufbau und naechstes Beispiel zu: {objective}"
    if lesson_mode == "origin_story_explanation":
        return f"Baue die Grundidee und Notwendigkeit fuer dieses Thema auf: {objective}"
    if lesson_mode == "formal_compact_explanation":
        return f"Verdichte die formale Kernaussage zu: {objective}"
    return f"Fuehre die Kernidee klar und kleinschrittig zu diesem Ziel: {objective}"


def _block_focus(
    lesson_mode: str,
    response_settings,
) -> list[str]:
    if lesson_mode == "worked_example_tutoring":
        focus = [
            "expliziter naechster Rechenschritt",
            "lokaler Zwischenschritt-Check",
            "sichtbare Fehlerkorrektur",
        ]
    elif lesson_mode == "origin_then_example":
        focus = [
            "kurzer Sinnanker",
            "Bruecke vom Begriff ins Beispiel",
            "Transfer in dieselbe Aufgabenfamilie",
        ]
    elif lesson_mode == "origin_story_explanation":
        focus = [
            "Problemursprung",
            "warum die Idee noetig wurde",
            "Anschluss an ein erstes Beispiel",
        ]
    elif lesson_mode == "formal_compact_explanation":
        focus = [
            "klare Notation",
            "kurze Ableitung",
            "formaler Kern ohne Umweg",
        ]
    else:
        focus = [
            "Kernidee vor Symbolik",
            "gefuhrte Minierklaerung",
            "kleiner Selbstcheck",
        ]

    if "dyscalculia_aware_support" in response_settings.active_supports:
        focus.append("Mengenbedeutung sichtbar halten")
    if "dyslexia_aware_support" in response_settings.active_supports:
        focus.append("Leselast vor Mathefehler pruefen")
    if "scarcity_aware_support" in response_settings.active_supports:
        focus.append("sichtbaren kleinen Erfolg markieren")

    return focus


def _infer_block_type(
    lesson_mode: str,
    observed_evidence: list[str],
    previous_evidence: list[str] | None = None,
) -> BlockType:
    evidence = set(observed_evidence)
    previous = set(previous_evidence or [])

    if evidence & {
        "repeated_concept_error",
        "repeated_attempt_three_plus",
        "error_recovery_with_hint",
        "no_progress_two_blocks",
        "no_progress_three_blocks",
        "no_success_visible_two_blocks",
    }:
        return BlockType.ERROR_RECOVERY
    if lesson_mode == "worked_example_tutoring":
        return BlockType.WORKED_EXAMPLE
    if lesson_mode == "origin_story_explanation":
        return BlockType.CONCEPT_INTRODUCTION
    if lesson_mode == "origin_then_example":
        return BlockType.BRIDGE_TO_APPLICATION
    if evidence & {"transfer_success_two_blocks", "reduced_prompting"}:
        return BlockType.CONCEPT_CHECK
    if evidence & {"mixed_success_inconsistent", "text_overload"} or previous & {
        "mixed_success_inconsistent",
        "error_recovery_with_hint",
    }:
        return BlockType.GUIDED_PRACTICE
    return BlockType.REFLECTION


def _block_support_moves(
    lesson_mode: str,
    response_settings,
    observed_evidence: list[str],
) -> list[str]:
    moves: list[str] = []
    evidence = set(observed_evidence)

    if response_settings.transition_buffer != "brief_explicit_transition":
        moves.append("mark_transition_explicitly")
    if response_settings.check_frequency != "every_few_steps":
        moves.append("insert_frequent_understanding_checks")
    if response_settings.worked_example_ratio != "balanced_examples_then_practice":
        moves.append("model_before_independent_attempt")
    if response_settings.language_support != "standard":
        moves.append("carry_language_bridge_into_prompt")
    if response_settings.sensory_load_level != "standard":
        moves.append("keep_visual_field_low_clutter")

    if lesson_mode == "worked_example_tutoring":
        moves.extend(
            [
                "show_one_local_step_before_release",
                "anchor_next_attempt_to_last_worked_move",
            ]
        )
    elif lesson_mode == "origin_then_example":
        moves.extend(
            [
                "bridge_concept_to_example_with_micro_origin",
                "reconnect_example_to_core_idea_before_symbolic_push",
            ]
        )
    elif lesson_mode == "origin_story_explanation":
        moves.extend(
            [
                "keep_story_short_and_relevant",
                "return_from_origin_to_present_problem_fast",
            ]
        )
    elif lesson_mode == "formal_compact_explanation":
        moves.extend(
            [
                "compress_formalism_only_after_checkpoint",
                "name_symbolic_jump_before_using_it",
            ]
        )
    else:
        moves.extend(
            [
                "state_core_idea_before_symbolic_detail",
                "keep_explanation_guided_and_local",
            ]
        )

    if _has_overload_indicator(evidence):
        moves.extend(
            [
                "reduce_notation_and_restore_structure",
                "restate_current_goal_before_retry",
            ]
        )
    if evidence & {
        "single_concept_error",
        "repeated_concept_error",
        "repeated_concept_error_across_blocks",
        "repeated_attempt_three_plus",
        "persistent_same_question",
        "off_target_response",
    }:
        moves.extend(
            [
                "rebuild_last_step_after_confusion",
                "contrast_correct_and_incorrect_path_locally",
            ]
        )
    if "repeated_attempt_three_plus" in evidence:
        moves.extend(
            [
                "stop_retry_loop_and_reframe_concept",
                "switch_from_attempt_counting_to_model_rebuild",
            ]
        )
    if evidence & {
        "no_progress_block",
        "no_progress_two_blocks",
        "no_progress_three_blocks",
        "no_success_visible_two_blocks",
    }:
        moves.extend(
            [
                "shrink_goal_to_single_recoverable_win",
                "reset_success_criteria_for_next_attempt",
            ]
        )
    if "mixed_success_inconsistent" in evidence:
        moves.extend(
            [
                "stabilize_pattern_before_new_variation",
                "contrast_why_this_problem_changed",
            ]
        )
    if _has_visible_success_indicator(evidence):
        moves.extend(
            [
                "name_and_bank_visible_success",
                "hand_off_slightly_more_ownership",
            ]
        )
    if evidence & {"rapid_success_two_blocks", "rapid_success_three_blocks"}:
        moves.extend(
            [
                "increase_pacing_after_stable_success",
                "fade_one_scaffold_after_stable_success",
            ]
        )
    if "rapid_success_three_blocks" in evidence:
        moves.append("offer_more_independent_challenge")
    if "vocabulary_request_again" in evidence:
        moves.extend(
            [
                "keep_glossary_visible_across_blocks",
                "restate_key_term_before_new_symbolic_step",
            ]
        )
    if "error_recovery_with_hint" in evidence:
        moves.extend(
            [
                "name_why_the_hint_worked",
                "keep_hint_path_available_for_next_attempt",
            ]
        )

    active_supports = set(response_settings.active_supports)
    if "adhd_aware_support" in active_supports:
        moves.extend(
            [
                "announce_short_goal_before_block",
                "use_step_labels_and_micro_checkpoints",
                "keep_feedback_near_immediate",
            ]
        )
        if _has_overload_indicator(evidence):
            moves.append("tighten_attention_window_after_drift")
    if "dyscalculia_aware_support" in active_supports:
        moves.extend(
            [
                "keep_quantity_representation_visible",
                "delay_dense_symbolic_compression",
                "rebuild_errors_from_quantity_model",
            ]
        )
        if evidence & {
            "single_concept_error",
            "repeated_concept_error",
            "repeated_concept_error_across_blocks",
            "no_progress_two_blocks",
        }:
            moves.append("return_to_quantity_model_before_symbols")
    if "dyslexia_aware_support" in active_supports:
        moves.extend(
            [
                "reduce_text_load_before_problem_solving",
                "check_reading_load_before_math_correction",
            ]
        )
        if "text_overload" in evidence or "reading_load_issue" in evidence:
            moves.append("split_problem_text_into_shorter_chunks")
    if "autism_spectrum_aware_support" in active_supports:
        moves.extend(
            [
                "keep_structure_predictable_and_literal",
                "stabilize_layout_before_variation",
            ]
        )
        if _has_overload_indicator(evidence):
            moves.append("freeze_format_changes_until_reorientation")
    if "language_sensitive_support" in active_supports:
        moves.extend(
            [
                "bridge_everyday_language_and_math_terms",
                "confirm_term_meaning_at_major_steps",
            ]
        )
        if (
            "vocabulary_request" in evidence
            or "vocabulary_request_again" in evidence
            or "text_overload" in evidence
        ):
            moves.append("clarify_terms_before_retrying_math_step")
    if "scarcity_aware_support" in active_supports:
        moves.extend(
            [
                "state_success_criteria_up_front",
                "mark_small_visible_wins",
            ]
        )
        if evidence & {"no_success_visible_two_blocks", "no_progress_two_blocks"}:
            moves.append("protect_momentum_with_near_term_success_target")

    unique_moves: list[str] = []
    seen: set[str] = set()
    for move in moves:
        if move not in seen:
            unique_moves.append(move)
            seen.add(move)
    return unique_moves


def _block_support_scaffolds(
    lesson_mode: str,
    response_settings,
    observed_evidence: list[str],
) -> list[str]:
    selected: list[str] = []
    seen: set[str] = set()
    evidence = set(observed_evidence)
    support_priorities = {
        "adhd_aware_support": [
            "step_labels",
            "micro_checkpoints",
            "visible_progress_markers",
            "short_goal_for_this_block",
        ],
        "dyscalculia_aware_support": [
            "number_lines",
            "ten_frames_or_quantity_grids",
            "counters_or_token_like_objects",
            "visible_link_between_quantity_and_symbol",
            "explicit_step_labels",
        ],
        "dyslexia_aware_support": [
            "key_term_highlighting",
            "symbol_reading_support",
            "short_sentence_chunks",
            "step_labels",
        ],
        "autism_spectrum_aware_support": [
            "consistent_session_structure",
            "explicit_transition_cues",
            "stable_visual_layout",
            "visible_progress_markers",
        ],
        "language_sensitive_support": [
            "key_term_glossary",
            "everyday_to_math_language_bridge",
            "translated_key_terms_when_needed",
            "term_confirmation_checks",
        ],
        "scarcity_aware_support": [
            "clear_success_criteria",
            "visible_progress_markers",
            "why_this_matters_now",
            "small_wins_sequence",
        ],
    }

    evidence_priorities: list[str] = []
    if _has_overload_indicator(evidence):
        evidence_priorities.extend(
            [
                "micro_checkpoints",
                "explicit_transition_cues",
                "stable_visual_layout",
                "short_sentence_chunks",
            ]
        )
    if evidence & {
        "single_concept_error",
        "repeated_concept_error",
        "repeated_concept_error_across_blocks",
        "repeated_attempt_three_plus",
    }:
        evidence_priorities.extend(
            [
                "number_lines",
                "visible_link_between_quantity_and_symbol",
                "step_labels",
                "clear_step_boundary",
            ]
        )
    if evidence & {
        "text_overload",
        "reading_load_issue",
        "vocabulary_request",
        "vocabulary_request_again",
    }:
        evidence_priorities.extend(
            [
                "key_term_glossary",
                "term_confirmation_checks",
                "short_sentence_chunks",
                "translated_key_terms_when_needed",
            ]
        )
    if "error_recovery_with_hint" in evidence:
        evidence_priorities.extend(
            [
                "micro_checkpoints",
                "step_labels",
                "visible_progress_markers",
            ]
        )
    if "mixed_success_inconsistent" in evidence:
        evidence_priorities.extend(
            [
                "clear_success_criteria",
                "step_labels",
                "visible_progress_markers",
            ]
        )
    if evidence & {
        "no_progress_two_blocks",
        "no_progress_three_blocks",
        "no_success_visible_two_blocks",
    }:
        evidence_priorities.extend(
            [
                "clear_success_criteria",
                "small_wins_sequence",
                "visible_progress_markers",
            ]
        )
    if _has_visible_success_indicator(evidence):
        evidence_priorities.extend(
            [
                "visible_progress_markers",
                "small_wins_sequence",
            ]
        )

    mode_priorities = {
        "worked_example_tutoring": [
            "step_labels",
            "clear_step_boundary",
            "micro_checkpoints",
        ],
        "origin_then_example": [
            "why_this_matters_now",
            "everyday_to_math_language_bridge",
            "visual_hint",
        ],
        "origin_story_explanation": [
            "why_this_matters_now",
            "visual_hint",
            "clear_step_boundary",
        ],
        "formal_compact_explanation": [
            "symbol_reading_support",
            "clear_step_boundary",
            "key_term_glossary",
        ],
        "guided_concept_explanation": [
            "clear_step_boundary",
            "visual_hint",
            "step_labels",
        ],
    }

    for scaffold in evidence_priorities:
        if scaffold in response_settings.external_scaffolds and scaffold not in seen:
            selected.append(scaffold)
            seen.add(scaffold)
        if len(selected) == 4:
            return selected

    for support_need in response_settings.active_supports:
        for scaffold in support_priorities.get(support_need, []):
            if scaffold in response_settings.external_scaffolds and scaffold not in seen:
                selected.append(scaffold)
                seen.add(scaffold)
                break
        if len(selected) == 4:
            return selected

    for scaffold in mode_priorities.get(lesson_mode, []):
        if scaffold in response_settings.external_scaffolds and scaffold not in seen:
            selected.append(scaffold)
            seen.add(scaffold)
        if len(selected) == 4:
            return selected

    for support_need in response_settings.active_supports:
        per_support_added = 0
        for scaffold in support_priorities.get(support_need, []):
            if scaffold in response_settings.external_scaffolds and scaffold not in seen:
                selected.append(scaffold)
                seen.add(scaffold)
                per_support_added += 1
            if per_support_added == 1 or len(selected) == 4:
                break
        if len(selected) == 4:
            break

    for scaffold in response_settings.external_scaffolds:
        if scaffold not in seen:
            selected.append(scaffold)
            seen.add(scaffold)
        if len(selected) == 4:
            break
    return selected


def _build_planned_block(
    block_index: int,
    lesson_mode: str,
    objective: str,
    response_settings,
    transition_message: str | None,
    observed_evidence: list[str],
    previous_evidence: list[str] | None = None,
    block_type_override: BlockType | None = None,
) -> PlannedTeachingBlock:
    block_type = block_type_override or _infer_block_type(
        lesson_mode,
        observed_evidence,
        previous_evidence,
    )
    evidence_combination = build_evidence_combination(
        current_evidence=observed_evidence,
        block_type=block_type,
        block_sequence=block_index,
        previous_evidence=previous_evidence,
    )
    support_moves = _block_support_moves(
        lesson_mode, response_settings, observed_evidence
    )
    resolved_support_moves, conflict_resolution_summary = resolve_block_support_conflicts(
        support_moves=support_moves,
        active_supports=response_settings.active_supports,
        evidence=observed_evidence,
        lesson_mode=lesson_mode,
        block_type=block_type,
        evidence_patterns=evidence_combination.patterns,
    )
    return PlannedTeachingBlock(
        block_index=block_index,
        mode=lesson_mode,
        block_type=block_type,
        goal=_block_goal(lesson_mode, objective),
        focus=_block_focus(lesson_mode, response_settings),
        support_moves=resolved_support_moves,
        support_scaffolds=_block_support_scaffolds(
            lesson_mode, response_settings, observed_evidence
        ),
        evidence_combination=evidence_combination,
        conflict_resolution_summary=conflict_resolution_summary,
        transition_message=transition_message,
        observed_evidence=observed_evidence,
    )


def _attach_sequence_decision(
    planned_block: PlannedTeachingBlock,
    response_settings,
    sequence_state: BlockSequenceState,
) -> tuple[PlannedTeachingBlock, BlockSequenceState]:
    if planned_block.block_type is None or planned_block.evidence_combination is None:
        return planned_block, sequence_state

    decision = plan_next_block(
        current_block_type=planned_block.block_type,
        evidence_patterns=planned_block.evidence_combination.patterns,
        active_supports=response_settings.active_supports,
        recent_block_types=sequence_state.block_type_history,
    )
    updated_block = planned_block.model_copy(
        update={
            "sequence_intent": decision.sequence_intent,
            "transition_reason": decision.transition_reason,
            "next_block_type": decision.suggested_next_block_type,
            "alternative_next_block_types": decision.alternative_next_block_types,
            "routing_confidence": decision.confidence,
            "selected_path_score": decision.selected_path_score,
            "routing_rationale": decision.rationale,
            "candidate_paths": decision.candidate_paths,
        }
    )
    updated_state = advance_sequence_state(
        sequence_state,
        current_block_type=planned_block.block_type,
        evidence_patterns=planned_block.evidence_combination.patterns,
        decision=decision,
    )
    return updated_block, updated_state


def _has_overload_indicator(evidence: set[str]) -> bool:
    return bool(
        evidence
        & {
            "structure_break",
            "symbol_mix",
            "text_overload",
            "answer_abandoned",
            "context_loss",
        }
    )


def _has_visible_success_indicator(evidence: set[str]) -> bool:
    return bool(
        evidence
        & {
            "visible_small_success",
            "correct_with_guidance",
            "pattern_recognized",
            "rapid_success",
            "rapid_success_two_blocks",
            "rapid_success_three_blocks",
            "transfer_success",
            "transfer_success_two_blocks",
            "error_recovery_with_hint",
            "self_correction",
            "explains_next_step",
            "active_continue",
        }
    )


def _has_struggle_indicator(evidence: set[str]) -> bool:
    return bool(
        evidence
        & {
            "single_concept_error",
            "repeated_concept_error",
            "repeated_concept_error_across_blocks",
            "repeated_attempt_three_plus",
            "persistent_same_question",
            "off_target_response",
            "no_progress_block",
            "no_progress_two_blocks",
            "no_progress_three_blocks",
        }
    ) or _has_overload_indicator(evidence)


def _augment_observation_evidence(
    raw_evidence: list[str],
    previous_effective_evidence: set[str] | None,
) -> list[str]:
    evidence = set(raw_evidence)

    if "repeated_concept_error" in evidence and "attempt_count_three_plus" in evidence:
        evidence.add("repeated_attempt_three_plus")

    if _has_visible_success_indicator(evidence):
        evidence.add("visible_small_success")

    if (
        "hint_used" in evidence
        and evidence & {"correct_with_guidance", "self_correction"}
        and (
            evidence & {"single_concept_error", "repeated_concept_error", "repeated_attempt_three_plus"}
            or (
                previous_effective_evidence is not None
                and _has_struggle_indicator(previous_effective_evidence)
            )
        )
    ):
        evidence.add("error_recovery_with_hint")

    if previous_effective_evidence:
        if "repeated_concept_error" in evidence and (
            "repeated_concept_error" in previous_effective_evidence
            or "repeated_concept_error_across_blocks" in previous_effective_evidence
        ):
            evidence.add("repeated_concept_error_across_blocks")

        if "no_progress_block" in evidence:
            if "no_progress_two_blocks" in previous_effective_evidence:
                evidence.add("no_progress_three_blocks")
            elif "no_progress_block" in previous_effective_evidence:
                evidence.add("no_progress_two_blocks")

        if "transfer_success" in evidence and (
            "transfer_success" in previous_effective_evidence
            or "transfer_success_two_blocks" in previous_effective_evidence
        ):
            evidence.add("transfer_success_two_blocks")

        if "rapid_success" in evidence:
            if previous_effective_evidence & {
                "rapid_success_two_blocks",
                "rapid_success_three_blocks",
            }:
                evidence.add("rapid_success_two_blocks")
                evidence.add("rapid_success_three_blocks")
            elif "rapid_success" in previous_effective_evidence:
                evidence.add("rapid_success_two_blocks")

        if (
            ("pattern_recognized" in evidence or "transfer_success" in evidence)
            and "correct_with_guidance" in previous_effective_evidence
        ):
            evidence.add("reduced_prompting")

        if "vocabulary_request" in evidence and previous_effective_evidence & {
            "vocabulary_request",
            "vocabulary_request_again",
        }:
            evidence.add("vocabulary_request_again")

        if _has_overload_indicator(evidence) and (
            _has_overload_indicator(previous_effective_evidence)
            or "overload_persisted_after_simplification" in previous_effective_evidence
        ):
            evidence.add("overload_persisted_after_simplification")

        if (
            _has_visible_success_indicator(evidence)
            and _has_struggle_indicator(previous_effective_evidence)
        ) or (
            _has_struggle_indicator(evidence)
            and _has_visible_success_indicator(previous_effective_evidence)
        ):
            evidence.add("mixed_success_inconsistent")

        if (
            not _has_visible_success_indicator(evidence)
            and not _has_visible_success_indicator(previous_effective_evidence)
            and (
                _has_struggle_indicator(evidence)
                or _has_struggle_indicator(previous_effective_evidence)
            )
        ):
            evidence.add("no_success_visible_two_blocks")

    return sorted(evidence)


def _simulate_runtime_blocks(
    objective: str,
    initial_mode: str,
    runtime_observations: list[RuntimeObservationInput],
    initial_state: ModeAdaptationState | None,
    support_signal_profile,
    response_settings,
) -> tuple[
    list[PlannedTeachingBlock],
    list[ModeAdaptationTraceEntry],
    ModeAdaptationState,
    BlockSequenceState,
]:
    adapter = RuntimeModeAdapter()
    if initial_state is not None:
        state = initial_state.model_copy(deep=True)
        current_mode = initial_state.current_mode
        pending_transition_message = initial_state.pending_transition_message
    else:
        current_mode = initial_mode
        state = ModeAdaptationState(current_mode=current_mode)
        pending_transition_message = None
    planned_blocks: list[PlannedTeachingBlock] = []
    adaptation_trace: list[ModeAdaptationTraceEntry] = []
    sequence_state = BlockSequenceState()
    previous_effective_evidence = (
        set(initial_state.last_observation_evidence) if initial_state else None
    )

    if not runtime_observations:
        displayed_transition_message = pending_transition_message
        preview_evidence = (
            list(state.last_observation_evidence)
            if state.last_observation_evidence
            else []
        )
        preview_block, sequence_state = _attach_sequence_decision(
            _build_planned_block(
                block_index=1,
                lesson_mode=current_mode,
                objective=objective,
                response_settings=response_settings,
                transition_message=displayed_transition_message,
                observed_evidence=preview_evidence,
                previous_evidence=None,
            ),
            response_settings=response_settings,
            sequence_state=sequence_state,
        )
        planned_blocks.append(preview_block)
        if displayed_transition_message is not None:
            state = state.model_copy(update={"pending_transition_message": None})
        return planned_blocks, adaptation_trace, state, sequence_state

    last_routed_block_type: BlockType | None = None
    for block_index, observation_input in enumerate(runtime_observations, start=1):
        effective_evidence = _augment_observation_evidence(
            observation_input.evidence,
            previous_effective_evidence,
        )
        displayed_transition_message = pending_transition_message
        current_block, sequence_state = _attach_sequence_decision(
            _build_planned_block(
                block_index=block_index,
                lesson_mode=current_mode,
                objective=objective,
                response_settings=response_settings,
                transition_message=displayed_transition_message,
                observed_evidence=effective_evidence,
                previous_evidence=sorted(previous_effective_evidence or set()),
            ),
            response_settings=response_settings,
            sequence_state=sequence_state,
        )
        planned_blocks.append(current_block)
        last_routed_block_type = current_block.next_block_type

        decision = adapter.check_and_adapt_mode(
            state=state,
            current_mode=current_mode,
            block_observation=RawBlockObservation(
                block_index=block_index,
                current_mode=current_mode,
                evidence=effective_evidence,
            ),
            profile=support_signal_profile,
        )
        adaptation_trace.append(
            ModeAdaptationTraceEntry(
                block_index=block_index,
                mode_before=current_mode,
                mode_after=decision.selected_mode,
                changed=decision.changed,
                trigger_signals=decision.trigger_signals,
                transition_message=decision.transition_message,
                notes=decision.notes,
            )
        )

        state = adapter.advance_state(
            state,
            decision,
            transition_was_consumed=displayed_transition_message is not None,
        )
        state = state.model_copy(update={"last_observation_evidence": effective_evidence})
        current_mode = state.current_mode
        pending_transition_message = state.pending_transition_message
        previous_effective_evidence = set(effective_evidence)

    preview_block, sequence_state = _attach_sequence_decision(
        _build_planned_block(
            block_index=len(runtime_observations) + 1,
            lesson_mode=current_mode,
            objective=objective,
            response_settings=response_settings,
            transition_message=pending_transition_message,
            observed_evidence=[],
            previous_evidence=sorted(previous_effective_evidence or set()),
            block_type_override=last_routed_block_type,
        ),
        response_settings=response_settings,
        sequence_state=sequence_state,
    )
    planned_blocks.append(preview_block)

    return planned_blocks, adaptation_trace, state, sequence_state


def _resolve_resume_state(request: SessionRequest) -> ModeAdaptationState | None:
    if request.mode_adaptation_checkpoint is not None:
        return request.mode_adaptation_checkpoint.mode_adaptation_state
    return request.mode_adaptation_state


def _resolve_resume_source(request: SessionRequest) -> ResumeSource:
    if request.resume_source is not None:
        return request.resume_source
    if request.mode_adaptation_checkpoint is not None:
        return "inline_checkpoint"
    if request.mode_adaptation_state is not None:
        return "inline_state"
    return "fresh_start"


def _used_carried_observation_evidence(
    request: SessionRequest,
    carried_observation_evidence: list[str],
    planned_blocks: list[PlannedTeachingBlock],
) -> bool:
    if not carried_observation_evidence or not planned_blocks:
        return False

    first_block_evidence = set(planned_blocks[0].observed_evidence)
    carried_evidence = set(carried_observation_evidence)

    if not request.runtime_observations:
        return first_block_evidence == carried_evidence

    first_runtime_evidence = set(request.runtime_observations[0].evidence)
    return bool(first_block_evidence & carried_evidence) or (
        first_block_evidence != first_runtime_evidence
    )


def _build_resume_context(
    request: SessionRequest,
    resume_state: ModeAdaptationState | None,
    planned_blocks: list[PlannedTeachingBlock],
    final_state: ModeAdaptationState,
) -> ResumeContext:
    carried_observation_evidence = (
        list(resume_state.last_observation_evidence) if resume_state is not None else []
    )
    pending_transition_message_carried = bool(
        resume_state is not None and resume_state.pending_transition_message is not None
    )
    first_block_transition_message = (
        planned_blocks[0].transition_message if planned_blocks else None
    )

    return ResumeContext(
        resume_source=_resolve_resume_source(request),
        resume_active=resume_state is not None,
        carried_observation_evidence=carried_observation_evidence,
        used_carried_observation_evidence=_used_carried_observation_evidence(
            request=request,
            carried_observation_evidence=carried_observation_evidence,
            planned_blocks=planned_blocks,
        ),
        pending_transition_message_carried=pending_transition_message_carried,
        pending_transition_message_consumed=(
            pending_transition_message_carried
            and first_block_transition_message is not None
            and final_state.pending_transition_message is None
        ),
    )


def build_stack(settings: Settings) -> StackResponse:
    return StackResponse(
        checked_on="2026-04-01",
        primary_choice=settings.primary_reasoner_model,
        assignments=[
            ModelAssignment(
                role="tutor_orchestrator",
                model=settings.primary_reasoner_model,
                why="Best default choice for complex tutoring flows, tool use, and grounded reasoning.",
            ),
            ModelAssignment(
                role="fast_hinting_and_routing",
                model=settings.fast_path_model,
                why="Lower cost and latency for helper tasks inside a teaching session.",
            ),
            ModelAssignment(
                role="offline_corpus_ingestion",
                model=settings.ingestion_model,
                why="Strong long-context fit for books, papers, and large document extraction.",
            ),
            ModelAssignment(
                role="hard_case_verification",
                model=settings.verifier_model,
                why="Useful as an optional second opinion for difficult reasoning or literature checks.",
            ),
            ModelAssignment(
                role="semantic_search",
                model=settings.embeddings_model,
                why="High-quality embeddings for multilingual semantic retrieval over math sources.",
            ),
        ],
        architecture_summary=(
            "Teacher agent plus math knowledge graph plus hybrid retrieval plus learner model."
        ),
    )


def build_teaching_plan(request: SessionRequest) -> TeachingPlan:
    profile: LearnerProfile = request.learner_profile
    resume_state = _resolve_resume_state(request)
    tone, pattern_hint = AUDIENCE_MODES[profile.age_group]
    concept_depth, include_proof = LEVEL_DEPTH[profile.math_level]
    requested_mode = _infer_lesson_mode(request)
    support_signal_profile, response_settings = build_support_response(profile)
    mode_selection: ModeSelection = select_mode(
        requested_mode,
        profile,
        support_signal_profile,
        response_settings,
    )
    lesson_mode = mode_selection.selected_mode
    if resume_state is not None:
        lesson_mode = resume_state.current_mode
    response_arc = _mode_response_arc(lesson_mode)
    include_history, history_mode = _mode_history_strategy(lesson_mode, profile.wants_history)
    if "short_origin_bridge" in mode_selection.constraints or "micro_origin_bridge" in mode_selection.constraints:
        include_history = True
        history_mode = "supporting_only"
    network_focus = _mode_network_focus(lesson_mode)

    teaching_pattern = [
        "Start from the learner objective before introducing formal notation.",
        "Check prerequisites explicitly before pushing ahead.",
        pattern_hint,
    ]

    if profile.wants_visuals:
        teaching_pattern.append("Offer a visual or spatial explanation when possible.")
    if profile.confidence == "low":
        teaching_pattern.append("Reduce shame and normalize mistakes as part of learning.")
    if include_history:
        teaching_pattern.append("Include origin stories when they improve intuition.")
    if lesson_mode == "origin_story_explanation":
        teaching_pattern.append("Treat history as the main entry point, not as a side note.")
    if lesson_mode == "worked_example_tutoring":
        teaching_pattern.append("Keep each algebraic move local, explicit, and checkable.")
    if lesson_mode == "origin_then_example":
        teaching_pattern.append("Bridge from historical motivation into the learner's own example.")
    if requested_mode != lesson_mode:
        teaching_pattern.append("Use a support-sensitive mode override instead of the naive request-only mode.")
    if response_settings.active_supports:
        teaching_pattern.append(
            "Adapt pacing, notation, and scaffolds to the active support profile."
        )
    if response_settings.conflict_pairs:
        teaching_pattern.append(
            "Use explicit conflict-resolution rules when multiple support profiles pull in different directions."
        )
    if response_settings.priority_ladders:
        teaching_pattern.append(
            "Apply explicit priority ladders when three or more support profiles compete."
        )
    if "adhd_aware_support" in response_settings.active_supports:
        teaching_pattern.append("Use short blocks, explicit transitions, and fast feedback.")
    if "dyscalculia_aware_support" in response_settings.active_supports:
        teaching_pattern.append("Keep quantity meaning visible before compressing into symbols.")
    if "dyslexia_aware_support" in response_settings.active_supports:
        teaching_pattern.append("Reduce reading burden before concluding a math misunderstanding.")
    if "autism_spectrum_aware_support" in response_settings.active_supports:
        teaching_pattern.append("Keep structure predictable, explicit, and low in sensory clutter.")
    if "language_sensitive_support" in response_settings.active_supports:
        teaching_pattern.append(
            "Bridge everyday language and math vocabulary before compressing into formal terms."
        )
    if "scarcity_aware_support" in response_settings.active_supports:
        teaching_pattern.append(
            "Make relevance, success criteria, and visible progress explicit from the start."
        )
    if mode_selection.constraints:
        teaching_pattern.append("Respect the active mode constraints instead of treating the mode as unconstrained.")

    retrieval_plan = RetrievalPlan(
        concept_depth=concept_depth,
        include_history=include_history,
        history_mode=history_mode,
        include_proof_sketch=include_proof,
        include_modern_applications=True,
        highlight_misconceptions=True,
        network_focus=network_focus,
        required_source_types=[
            "primary_math_source_or_standard_reference",
            "modern_explanatory_source",
            "worked_example_source",
            "historical_network_source",
        ],
    )

    evaluation_focus = [
        "Did the answer choose the right lesson mode for the learner request?",
        "Did the plan align response settings to the learner support profile?",
        "Is the selected mode ready for later block-level live adaptation?",
        "Did the explanation respect prerequisites?",
        "Was the mathematical claim sourceable?",
        "Was the difficulty level appropriate for the learner?",
        "Did the answer leave a useful next step or self-check question?",
    ]

    next_turn_contract = [
        "State assumptions about the learner openly.",
        "Name the central idea before details.",
        "Keep notation load proportional to the learner level.",
        "Keep support adaptations explicit and non-diagnostic.",
        "Only adapt live mode at block boundaries, never at every small step.",
        "Cite or reference source families for nontrivial claims.",
    ]

    (
        planned_blocks,
        adaptation_trace,
        mode_adaptation_state,
        block_sequence_state,
    ) = _simulate_runtime_blocks(
        objective=request.objective,
        initial_mode=lesson_mode,
        runtime_observations=request.runtime_observations,
        initial_state=resume_state,
        support_signal_profile=support_signal_profile,
        response_settings=response_settings,
    )
    mode_adaptation_checkpoint = ModeAdaptationCheckpoint(
        mode_adaptation_state=mode_adaptation_state
    )
    resume_context = _build_resume_context(
        request=request,
        resume_state=resume_state,
        planned_blocks=planned_blocks,
        final_state=mode_adaptation_state,
    )
    sequence_planning_metadata = SequencePlanningMetadata(
        active_sequence_intent=block_sequence_state.active_sequence_intent,
        next_block_options=(
            planned_blocks[-1].alternative_next_block_types if planned_blocks else []
        ),
        adaptive_transitions_applied=block_sequence_state.adaptive_transitions_applied,
        last_transition_reason=(
            planned_blocks[-1].transition_reason if planned_blocks else None
        ),
        last_routing_confidence=(
            planned_blocks[-1].routing_confidence if planned_blocks else None
        ),
        lookahead_block_types=block_sequence_state.lookahead_block_types,
        candidate_path_count=(
            len(planned_blocks[-1].candidate_paths) if planned_blocks else 0
        ),
        candidate_paths=planned_blocks[-1].candidate_paths if planned_blocks else [],
    )

    return TeachingPlan(
        lesson_mode=lesson_mode,
        audience_mode=profile.age_group,
        tone=tone,
        teaching_pattern=teaching_pattern,
        response_arc=response_arc,
        mode_selection=mode_selection,
        mode_adaptation_state=mode_adaptation_state,
        mode_adaptation_checkpoint=mode_adaptation_checkpoint,
        planned_blocks=planned_blocks,
        block_sequence_state=block_sequence_state,
        sequence_planning_metadata=sequence_planning_metadata,
        mode_adaptation_trace=adaptation_trace,
        resume_context=resume_context,
        support_signal_profile=support_signal_profile,
        response_settings=response_settings,
        retrieval_plan=retrieval_plan,
        evaluation_focus=evaluation_focus,
        next_turn_contract=next_turn_contract,
    )
