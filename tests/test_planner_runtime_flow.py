from mathteach.models import (
    BlockSequenceIntent,
    BlockTransitionReason,
    BlockType,
    EvidenceCombinationPattern,
    SessionRequest,
)
from mathteach.services.planner import build_teaching_plan


def test_planner_builds_preview_block_without_runtime_observations() -> None:
    plan = build_teaching_plan(
        SessionRequest(
            objective="Erklaere mir die quadratische Gleichung anschaulich.",
            learner_profile={
                "age_group": "teen",
                "math_level": "high_school",
                "confidence": "low",
                "preferred_pace": "balanced",
                "language": "de",
                "wants_visuals": True,
                "wants_history": True,
            },
        )
    )

    assert len(plan.planned_blocks) == 1
    assert plan.planned_blocks[0].block_index == 1
    assert plan.planned_blocks[0].mode == "guided_concept_explanation"
    assert "insert_frequent_understanding_checks" in plan.planned_blocks[0].support_moves
    assert "clear_step_boundary" in plan.planned_blocks[0].support_scaffolds
    assert plan.mode_adaptation_trace == []
    assert plan.resume_context.resume_source == "fresh_start"
    assert plan.resume_context.resume_active is False


def test_planner_exposes_block_level_support_moves_for_adhd_and_dyscalculia() -> None:
    plan = build_teaching_plan(
        SessionRequest(
            objective="Erklaere mir diese Aufgabe Schritt fuer Schritt mit Beispiel.",
            learner_profile={
                "age_group": "teen",
                "math_level": "middle_school",
                "confidence": "low",
                "preferred_pace": "gentle",
                "language": "de",
                "wants_visuals": True,
                "wants_history": False,
                "declared_support_needs": [
                    "adhd_aware_support",
                    "dyscalculia_aware_support",
                ],
            },
        )
    )

    first_block = plan.planned_blocks[0]

    assert "announce_short_goal_before_block" in first_block.support_moves
    assert "keep_quantity_representation_visible" in first_block.support_moves
    assert "step_labels" in first_block.support_scaffolds
    assert "number_lines" in first_block.support_scaffolds


def test_planner_adapts_block_support_to_confusion_evidence() -> None:
    plan = build_teaching_plan(
        SessionRequest(
            objective="Erklaere mir diese Aufgabe Schritt fuer Schritt mit Beispiel.",
            learner_profile={
                "age_group": "teen",
                "math_level": "middle_school",
                "confidence": "low",
                "preferred_pace": "gentle",
                "language": "de",
                "wants_visuals": True,
                "wants_history": False,
                "declared_support_needs": [
                    "adhd_aware_support",
                    "dyscalculia_aware_support",
                ],
            },
            runtime_observations=[
                {"evidence": ["repeated_concept_error"]},
            ],
        )
    )

    first_block = plan.planned_blocks[0]

    assert "rebuild_last_step_after_confusion" in first_block.support_moves
    assert "return_to_quantity_model_before_symbols" in first_block.support_moves
    assert "number_lines" in first_block.support_scaffolds
    assert "visible_link_between_quantity_and_symbol" in first_block.support_scaffolds


def test_planner_adapts_block_support_to_text_overload_evidence() -> None:
    plan = build_teaching_plan(
        SessionRequest(
            objective="Explain this word problem in small clear steps.",
            learner_profile={
                "age_group": "teen",
                "math_level": "middle_school",
                "confidence": "low",
                "preferred_pace": "balanced",
                "language": "en",
                "wants_visuals": True,
                "wants_history": False,
                "declared_support_needs": ["dyslexia_aware_support"],
            },
            runtime_observations=[
                {"evidence": ["text_overload", "vocabulary_request"]},
            ],
        )
    )

    first_block = plan.planned_blocks[0]

    assert "split_problem_text_into_shorter_chunks" in first_block.support_moves
    assert "clarify_terms_before_retrying_math_step" in first_block.support_moves
    assert "key_term_glossary" in first_block.support_scaffolds
    assert "short_sentence_chunks" in first_block.support_scaffolds


def test_planner_applies_worked_example_mode_evidence_coupling_for_triad() -> None:
    plan = build_teaching_plan(
        SessionRequest(
            objective="Explain this word problem with a clear example.",
            learner_profile={
                "age_group": "teen",
                "math_level": "middle_school",
                "confidence": "low",
                "preferred_pace": "balanced",
                "language": "en",
                "wants_visuals": True,
                "wants_history": False,
                "declared_support_needs": [
                    "adhd_aware_support",
                    "dyscalculia_aware_support",
                ],
            },
            mode_adaptation_state={
                "current_mode": "worked_example_tutoring",
                "blocks_in_current_mode": 1,
                "mode_changes_in_session": 0,
                "cooldown_blocks_remaining": 1,
            },
            runtime_observations=[
                {
                    "evidence": [
                        "rapid_success",
                        "repeated_concept_error",
                        "attempt_count_three_plus",
                        "text_overload",
                        "vocabulary_request",
                    ]
                },
            ],
        )
    )

    first_block = plan.planned_blocks[0]

    assert first_block.mode == "worked_example_tutoring"
    assert first_block.conflict_resolution_summary is not None
    assert (
        first_block.conflict_resolution_summary.lesson_mode_applied
        == "worked_example_tutoring"
    )
    assert "worked_example_visual_concept_with_minimal_text" in first_block.support_moves
    assert first_block.conflict_resolution_summary.mode_evidence_adjustments


def test_planner_exposes_worked_example_blocktype_and_patterns() -> None:
    plan = build_teaching_plan(
        SessionRequest(
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
                {"evidence": ["rapid_success", "pattern_recognized", "transfer_success"]},
            ],
        )
    )

    third_block = plan.planned_blocks[2]

    assert third_block.block_type == BlockType.WORKED_EXAMPLE
    assert third_block.evidence_combination is not None
    assert (
        EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS
        in third_block.evidence_combination.patterns
    )
    assert third_block.conflict_resolution_summary is not None
    assert third_block.conflict_resolution_summary.block_type_applied == (
        BlockType.WORKED_EXAMPLE
    )
    assert "worked_example_accelerated_with_pacing_checks" in third_block.support_moves
    assert "use_concrete_example_as_anchor" in third_block.support_moves


def test_planner_exposes_concept_intro_vocabulary_gap_blocktype() -> None:
    plan = build_teaching_plan(
        SessionRequest(
            objective="Warum braucht man Brueche eigentlich?",
            learner_profile={
                "age_group": "teen",
                "math_level": "middle_school",
                "confidence": "low",
                "preferred_pace": "balanced",
                "language": "en",
                "wants_visuals": True,
                "wants_history": True,
                "declared_support_needs": ["dyscalculia_aware_support"],
            },
            mode_adaptation_state={
                "current_mode": "origin_story_explanation",
                "blocks_in_current_mode": 1,
                "mode_changes_in_session": 0,
                "cooldown_blocks_remaining": 1,
            },
            runtime_observations=[
                {"evidence": ["text_overload", "vocabulary_request"]},
            ],
        )
    )

    first_block = plan.planned_blocks[0]

    assert first_block.block_type == BlockType.CONCEPT_INTRODUCTION
    assert first_block.evidence_combination is not None
    assert (
        EvidenceCombinationPattern.VOCABULARY_GAP
        in first_block.evidence_combination.patterns
    )
    assert first_block.conflict_resolution_summary is not None
    assert "visual_concept_intro_minimal_text" in first_block.support_moves


def test_planner_routes_preview_block_type_after_rapid_success() -> None:
    plan = build_teaching_plan(
        SessionRequest(
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
                {"evidence": ["rapid_success", "pattern_recognized", "transfer_success"]},
            ],
        )
    )

    third_block = plan.planned_blocks[2]
    preview_block = plan.planned_blocks[3]

    assert third_block.next_block_type == BlockType.GUIDED_PRACTICE
    assert third_block.transition_reason == BlockTransitionReason.EVIDENCE_PATTERN
    assert third_block.sequence_intent == BlockSequenceIntent.MASTERY_PATH
    assert preview_block.block_type == BlockType.GUIDED_PRACTICE
    assert plan.block_sequence_state is not None
    assert plan.sequence_planning_metadata is not None
    assert plan.sequence_planning_metadata.adaptive_transitions_applied >= 1


def test_planner_routes_error_recovery_preview_back_to_worked_example() -> None:
    plan = build_teaching_plan(
        SessionRequest(
            objective="Erklaere mir diese Aufgabe mit Beispiel.",
            learner_profile={
                "age_group": "teen",
                "math_level": "middle_school",
                "confidence": "low",
                "preferred_pace": "gentle",
                "language": "de",
                "wants_visuals": True,
                "wants_history": False,
                "declared_support_needs": ["dyscalculia_aware_support"],
            },
            runtime_observations=[
                {"evidence": ["repeated_concept_error", "attempt_count_three_plus"]},
            ],
        )
    )

    first_block = plan.planned_blocks[0]
    preview_block = plan.planned_blocks[1]

    assert first_block.block_type == BlockType.ERROR_RECOVERY
    assert first_block.next_block_type == BlockType.WORKED_EXAMPLE
    assert first_block.transition_reason == BlockTransitionReason.EVIDENCE_PATTERN
    assert first_block.sequence_intent == BlockSequenceIntent.ERROR_RECOVERY_CYCLE
    assert preview_block.block_type == BlockType.WORKED_EXAMPLE


def test_planner_carries_mode_change_into_next_preview_block() -> None:
    plan = build_teaching_plan(
        SessionRequest(
            objective="Erklaere mir mit Beispiel, warum die quadratische Gleichung so funktioniert.",
            learner_profile={
                "age_group": "teen",
                "math_level": "high_school",
                "confidence": "low",
                "preferred_pace": "balanced",
                "language": "de",
                "wants_visuals": True,
                "wants_history": True,
            },
            runtime_observations=[
                {"evidence": ["repeated_concept_error"]},
                {"evidence": ["repeated_concept_error"]},
                {"evidence": ["repeated_concept_error"]},
            ],
        )
    )

    assert [block.mode for block in plan.planned_blocks[:3]] == [
        "origin_then_example",
        "origin_then_example",
        "origin_then_example",
    ]
    assert plan.mode_adaptation_trace[-1].changed is True
    assert plan.mode_adaptation_trace[-1].mode_after == "worked_example_tutoring"
    assert plan.planned_blocks[-1].mode == "worked_example_tutoring"
    assert plan.mode_adaptation_state.current_mode == "worked_example_tutoring"
    assert plan.mode_adaptation_state.cooldown_blocks_remaining == 1


def test_planner_supports_multiple_mode_changes_across_longer_block_sequence() -> None:
    plan = build_teaching_plan(
        SessionRequest(
            objective="Erklaere mir mit Beispiel, warum die quadratische Gleichung so funktioniert.",
            learner_profile={
                "age_group": "teen",
                "math_level": "high_school",
                "confidence": "low",
                "preferred_pace": "balanced",
                "language": "de",
                "wants_visuals": True,
                "wants_history": True,
            },
            runtime_observations=[
                {"evidence": ["repeated_concept_error"]},
                {"evidence": ["repeated_concept_error"]},
                {"evidence": ["repeated_concept_error"]},
                {"evidence": ["pattern_recognized", "transfer_success"]},
                {"evidence": ["pattern_recognized", "transfer_success"]},
                {"evidence": ["pattern_recognized", "transfer_success"]},
            ],
        )
    )

    changed_entries = [entry for entry in plan.mode_adaptation_trace if entry.changed]

    assert len(changed_entries) == 2
    assert changed_entries[0].mode_after == "worked_example_tutoring"
    assert changed_entries[1].mode_after == "guided_concept_explanation"
    assert plan.planned_blocks[-1].mode == "guided_concept_explanation"
    assert plan.mode_adaptation_state.current_mode == "guided_concept_explanation"
    assert plan.mode_adaptation_state.mode_changes_in_session == 2
    assert "transfer_success_two_blocks" in plan.planned_blocks[4].observed_evidence


def test_planner_can_resume_from_existing_mode_adaptation_state() -> None:
    plan = build_teaching_plan(
        SessionRequest(
            objective="Erklaere mir mit Beispiel, warum die quadratische Gleichung so funktioniert.",
            learner_profile={
                "age_group": "teen",
                "math_level": "high_school",
                "confidence": "low",
                "preferred_pace": "balanced",
                "language": "de",
                "wants_visuals": True,
                "wants_history": True,
            },
            mode_adaptation_state={
                "current_mode": "worked_example_tutoring",
                "blocks_in_current_mode": 2,
                "mode_changes_in_session": 1,
                "cooldown_blocks_remaining": 0,
            },
            runtime_observations=[
                {"evidence": ["pattern_recognized", "transfer_success"]},
            ],
        )
    )

    assert plan.lesson_mode == "worked_example_tutoring"
    assert plan.planned_blocks[0].mode == "worked_example_tutoring"
    assert plan.mode_adaptation_trace[0].changed is True
    assert plan.mode_adaptation_trace[0].mode_after == "guided_concept_explanation"
    assert plan.mode_adaptation_state.current_mode == "guided_concept_explanation"
    assert plan.mode_adaptation_checkpoint.mode_adaptation_state.current_mode == (
        "guided_concept_explanation"
    )
    assert plan.resume_context.resume_source == "inline_state"
    assert plan.resume_context.resume_active is True


def test_planner_can_resume_from_mode_adaptation_checkpoint() -> None:
    plan = build_teaching_plan(
        SessionRequest(
            objective="Erklaere mir mit Beispiel, warum die quadratische Gleichung so funktioniert.",
            learner_profile={
                "age_group": "teen",
                "math_level": "high_school",
                "confidence": "low",
                "preferred_pace": "balanced",
                "language": "de",
                "wants_visuals": True,
                "wants_history": True,
            },
            mode_adaptation_checkpoint={
                "schema_version": "phase_h1_v1",
                "mode_adaptation_state": {
                    "current_mode": "worked_example_tutoring",
                    "blocks_in_current_mode": 2,
                    "mode_changes_in_session": 1,
                    "cooldown_blocks_remaining": 0,
                },
            },
            runtime_observations=[
                {"evidence": ["pattern_recognized", "transfer_success"]},
            ],
        )
    )

    assert plan.lesson_mode == "worked_example_tutoring"
    assert plan.planned_blocks[0].mode == "worked_example_tutoring"
    assert plan.mode_adaptation_trace[0].changed is True
    assert plan.mode_adaptation_trace[0].mode_after == "guided_concept_explanation"
    assert plan.mode_adaptation_checkpoint.schema_version == "phase_h1_v1"
    assert plan.resume_context.resume_source == "inline_checkpoint"
    assert plan.resume_context.resume_active is True


def test_planner_preserves_pending_transition_message_across_resume() -> None:
    plan = build_teaching_plan(
        SessionRequest(
            objective="Erklaere mir mit Beispiel, warum die quadratische Gleichung so funktioniert.",
            learner_profile={
                "age_group": "teen",
                "math_level": "high_school",
                "confidence": "low",
                "preferred_pace": "balanced",
                "language": "de",
                "wants_visuals": True,
                "wants_history": True,
            },
            mode_adaptation_state={
                "current_mode": "worked_example_tutoring",
                "blocks_in_current_mode": 0,
                "mode_changes_in_session": 1,
                "cooldown_blocks_remaining": 1,
                "pending_transition_message": (
                    "Das ist eine Stelle, an der viele kurz haengen bleiben. "
                    "Ich nehme etwas Last raus. "
                    "Wir gehen jetzt in kleineren Schritten weiter."
                ),
            },
        )
    )

    assert plan.planned_blocks[0].mode == "worked_example_tutoring"
    assert plan.planned_blocks[0].transition_message is not None
    assert "kleineren Schritten" in plan.planned_blocks[0].transition_message
    assert plan.mode_adaptation_state.pending_transition_message is None
    assert plan.resume_context.pending_transition_message_carried is True
    assert plan.resume_context.pending_transition_message_consumed is True


def test_planner_resume_preview_reuses_last_observation_evidence_for_support() -> None:
    plan = build_teaching_plan(
        SessionRequest(
            objective="Explain this word problem in small clear steps.",
            learner_profile={
                "age_group": "teen",
                "math_level": "middle_school",
                "confidence": "low",
                "preferred_pace": "balanced",
                "language": "en",
                "wants_visuals": True,
                "wants_history": False,
                "declared_support_needs": ["dyslexia_aware_support"],
            },
            mode_adaptation_state={
                "current_mode": "guided_concept_explanation",
                "blocks_in_current_mode": 1,
                "mode_changes_in_session": 0,
                "cooldown_blocks_remaining": 0,
                "last_observation_evidence": ["text_overload", "vocabulary_request"],
            },
        )
    )

    first_block = plan.planned_blocks[0]

    assert "text_overload" in first_block.observed_evidence
    assert "vocabulary_request" in first_block.observed_evidence
    assert "split_problem_text_into_shorter_chunks" in first_block.support_moves
    assert "clarify_terms_before_retrying_math_step" in first_block.support_moves
    assert "key_term_glossary" in first_block.support_scaffolds
    assert plan.resume_context.resume_source == "inline_state"
    assert plan.resume_context.resume_active is True
    assert plan.resume_context.carried_observation_evidence == [
        "text_overload",
        "vocabulary_request",
    ]
    assert plan.resume_context.used_carried_observation_evidence is True


def test_planner_blocks_fourth_change_when_budget_is_exhausted() -> None:
    plan = build_teaching_plan(
        SessionRequest(
            objective="Erklaere mir mit Beispiel, warum die quadratische Gleichung so funktioniert.",
            learner_profile={
                "age_group": "teen",
                "math_level": "high_school",
                "confidence": "low",
                "preferred_pace": "balanced",
                "language": "de",
                "wants_visuals": True,
                "wants_history": True,
            },
            runtime_observations=[
                {"evidence": ["repeated_concept_error"]},
                {"evidence": ["repeated_concept_error"]},
                {"evidence": ["repeated_concept_error"]},
                {"evidence": ["pattern_recognized", "transfer_success"]},
                {"evidence": ["pattern_recognized", "transfer_success"]},
                {"evidence": ["pattern_recognized", "transfer_success"]},
                {"evidence": ["pattern_recognized", "transfer_success", "explains_next_step", "active_continue"]},
                {"evidence": ["pattern_recognized", "transfer_success", "explains_next_step", "active_continue"]},
                {"evidence": ["pattern_recognized", "transfer_success", "explains_next_step", "active_continue"]},
                {"evidence": ["repeated_concept_error"]},
                {"evidence": ["repeated_concept_error"]},
                {"evidence": ["repeated_concept_error"]},
            ],
        )
    )

    changed_entries = [entry for entry in plan.mode_adaptation_trace if entry.changed]

    assert len(changed_entries) == 3
    assert changed_entries[0].mode_after == "worked_example_tutoring"
    assert changed_entries[1].mode_after == "guided_concept_explanation"
    assert changed_entries[2].mode_after == "origin_then_example"
    assert plan.mode_adaptation_trace[-1].changed is False
    assert any("change budget" in note for note in plan.mode_adaptation_trace[-1].notes)
    assert plan.mode_adaptation_state.mode_changes_in_session == 3
    assert plan.mode_adaptation_state.current_mode == "origin_then_example"


def test_planner_derives_cross_block_stagnation_from_simple_progress_signals() -> None:
    plan = build_teaching_plan(
        SessionRequest(
            objective="Erklaere mir die quadratische Gleichung anschaulich.",
            learner_profile={
                "age_group": "teen",
                "math_level": "high_school",
                "confidence": "low",
                "preferred_pace": "balanced",
                "language": "de",
                "wants_visuals": True,
                "wants_history": True,
            },
            runtime_observations=[
                {"evidence": ["no_progress_block"]},
                {"evidence": ["no_progress_block"]},
                {"evidence": ["no_progress_block"]},
            ],
        )
    )

    assert "no_progress_two_blocks" in plan.planned_blocks[1].observed_evidence
    assert "no_progress_three_blocks" in plan.planned_blocks[2].observed_evidence
    assert plan.mode_adaptation_trace[1].changed is False
    assert plan.mode_adaptation_trace[2].changed is True
    assert plan.mode_adaptation_trace[2].mode_after == "worked_example_tutoring"
    assert plan.planned_blocks[-1].mode == "worked_example_tutoring"


def test_planner_derives_cross_block_breakthrough_on_resume() -> None:
    plan = build_teaching_plan(
        SessionRequest(
            objective="Erklaere mir diese Aufgabe mit Beispiel.",
            learner_profile={
                "age_group": "teen",
                "math_level": "high_school",
                "confidence": "medium",
                "preferred_pace": "balanced",
                "language": "de",
                "wants_visuals": True,
                "wants_history": False,
            },
            mode_adaptation_state={
                "current_mode": "worked_example_tutoring",
                "blocks_in_current_mode": 2,
                "mode_changes_in_session": 0,
                "cooldown_blocks_remaining": 0,
                "last_observation_evidence": ["transfer_success"],
            },
            runtime_observations=[
                {"evidence": ["transfer_success"]},
            ],
        )
    )

    assert "transfer_success_two_blocks" in plan.planned_blocks[0].observed_evidence
    assert plan.mode_adaptation_trace[0].changed is True
    assert plan.mode_adaptation_trace[0].mode_after == "guided_concept_explanation"


def test_planner_derives_rapid_success_signals_across_multiple_blocks() -> None:
    plan = build_teaching_plan(
        SessionRequest(
            objective="Erklaere mir diese Aufgabe mit Beispiel.",
            learner_profile={
                "age_group": "teen",
                "math_level": "high_school",
                "confidence": "medium",
                "preferred_pace": "balanced",
                "language": "de",
                "wants_visuals": True,
                "wants_history": False,
            },
            runtime_observations=[
                {"evidence": ["rapid_success", "pattern_recognized", "transfer_success"]},
                {"evidence": ["rapid_success", "pattern_recognized", "transfer_success"]},
                {"evidence": ["rapid_success", "pattern_recognized", "transfer_success"]},
            ],
        )
    )

    assert "rapid_success_two_blocks" in plan.planned_blocks[1].observed_evidence
    assert "rapid_success_three_blocks" in plan.planned_blocks[2].observed_evidence
    assert "increase_pacing_after_stable_success" in plan.planned_blocks[2].support_moves
    assert "fade_one_scaffold_after_stable_success" in plan.planned_blocks[2].support_moves
    assert "offer_more_independent_challenge" in plan.planned_blocks[2].support_moves


def test_planner_emits_conflict_resolution_summary_for_pair_conflict() -> None:
    plan = build_teaching_plan(
        SessionRequest(
            objective="Erklaere mir diese Aufgabe mit Beispiel.",
            learner_profile={
                "age_group": "teen",
                "math_level": "middle_school",
                "confidence": "low",
                "preferred_pace": "gentle",
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
                {
                    "evidence": [
                        "rapid_success",
                        "transfer_success",
                        "repeated_concept_error",
                        "attempt_count_three_plus",
                    ]
                },
            ],
        )
    )

    second_block = plan.planned_blocks[2]

    assert second_block.conflict_resolution_summary is not None
    assert (
        "adhd_aware_support__dyscalculia_aware_support"
        in second_block.conflict_resolution_summary.pair_conflicts
    )
    assert second_block.conflict_resolution_summary.priority_ladder == [
        "dyscalculia_aware_support",
        "adhd_aware_support",
    ]
    assert "offer_more_independent_challenge" in (
        second_block.conflict_resolution_summary.suppressed_moves
    )
    assert any(
        "increase_pacing_after_stable_success" in item
        for item in second_block.conflict_resolution_summary.adapted_moves
    )
    assert "worked_example_rebuild_with_pacing_pause" in second_block.support_moves
    assert "worked_example_release_after_two_stable_steps" in second_block.support_moves
    assert "offer_more_independent_challenge" not in second_block.support_moves
    assert (
        second_block.support_moves.index("worked_example_rebuild_with_pacing_pause")
        < second_block.support_moves.index("worked_example_release_after_two_stable_steps")
    )


def test_planner_emits_conflict_resolution_summary_for_triad_conflict() -> None:
    plan = build_teaching_plan(
        SessionRequest(
            objective="Explain this word problem with clear examples.",
            learner_profile={
                "age_group": "teen",
                "math_level": "middle_school",
                "confidence": "low",
                "preferred_pace": "balanced",
                "language": "en",
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
                {
                    "evidence": [
                        "rapid_success",
                        "transfer_success",
                        "repeated_concept_error",
                        "attempt_count_three_plus",
                        "text_overload",
                    ]
                },
            ],
        )
    )

    second_block = plan.planned_blocks[2]

    assert second_block.conflict_resolution_summary is not None
    assert (
        second_block.conflict_resolution_summary.triad_group
        == "dyscalculia_aware_support__language_sensitive_support__adhd_aware_support"
    )
    assert second_block.conflict_resolution_summary.priority_ladder == [
        "dyscalculia_aware_support",
        "language_sensitive_support",
        "adhd_aware_support",
    ]
    assert (
        second_block.support_moves.index(
            "worked_example_visual_concept_with_minimal_text"
        )
        < second_block.support_moves.index("clarify_terms_inside_quantity_rebuild")
        < second_block.support_moves.index(
            "worked_example_release_after_concept_check"
        )
    )


def test_planner_emits_adapted_moves_not_only_reordered_for_h2e_triad() -> None:
    plan = build_teaching_plan(
        SessionRequest(
            objective="Explain this word problem with clear examples.",
            learner_profile={
                "age_group": "teen",
                "math_level": "middle_school",
                "confidence": "low",
                "preferred_pace": "balanced",
                "language": "en",
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
                {
                    "evidence": [
                        "rapid_success",
                        "transfer_success",
                        "repeated_concept_error",
                        "attempt_count_three_plus",
                        "text_overload",
                        "vocabulary_request",
                    ]
                },
            ],
        )
    )

    second_block = plan.planned_blocks[2]

    assert second_block.conflict_resolution_summary is not None
    assert "worked_example_visual_concept_with_minimal_text" in second_block.support_moves
    assert "pair_visual_explanation_with_simple_language" in second_block.support_moves
    assert "worked_example_release_after_concept_check" in second_block.support_moves
    assert "pair_visual_explanation_with_simple_language" in (
        second_block.conflict_resolution_summary.generated_moves
    )
    assert second_block.conflict_resolution_summary.move_dependencies_applied
    assert (
        second_block.support_moves.index(
            "worked_example_visual_concept_with_minimal_text"
        )
        < second_block.support_moves.index("pair_visual_explanation_with_simple_language")
        < second_block.support_moves.index("worked_example_release_after_concept_check")
    )


def test_planner_derives_repeated_vocabulary_need_across_blocks() -> None:
    plan = build_teaching_plan(
        SessionRequest(
            objective="Explain this word problem in small clear steps.",
            learner_profile={
                "age_group": "teen",
                "math_level": "middle_school",
                "confidence": "low",
                "preferred_pace": "balanced",
                "language": "en",
                "wants_visuals": True,
                "wants_history": False,
            },
            runtime_observations=[
                {"evidence": ["vocabulary_request"]},
                {"evidence": ["vocabulary_request"]},
            ],
        )
    )

    second_block = plan.planned_blocks[1]

    assert "vocabulary_request_again" in second_block.observed_evidence
    assert "keep_glossary_visible_across_blocks" in second_block.support_moves
    assert "restate_key_term_before_new_symbolic_step" in second_block.support_moves
    assert "key_term_glossary" in second_block.support_scaffolds
    assert "term_confirmation_checks" in second_block.support_scaffolds


def test_planner_derives_error_recovery_with_hint_after_struggle() -> None:
    plan = build_teaching_plan(
        SessionRequest(
            objective="Erklaere mir diese Aufgabe Schritt fuer Schritt.",
            learner_profile={
                "age_group": "teen",
                "math_level": "middle_school",
                "confidence": "low",
                "preferred_pace": "gentle",
                "language": "de",
                "wants_visuals": True,
                "wants_history": False,
                "declared_support_needs": ["adhd_aware_support"],
            },
            runtime_observations=[
                {"evidence": ["repeated_concept_error"]},
                {"evidence": ["hint_used", "correct_with_guidance", "self_correction"]},
            ],
        )
    )

    second_block = plan.planned_blocks[1]

    assert "error_recovery_with_hint" in second_block.observed_evidence
    assert "name_why_the_hint_worked" in second_block.support_moves
    assert "keep_hint_path_available_for_next_attempt" in second_block.support_moves
    assert "micro_checkpoints" in second_block.support_scaffolds


def test_planner_derives_repeated_attempt_three_plus_from_retry_loop() -> None:
    plan = build_teaching_plan(
        SessionRequest(
            objective="Erklaere mir diese Aufgabe Schritt fuer Schritt mit Beispiel.",
            learner_profile={
                "age_group": "teen",
                "math_level": "middle_school",
                "confidence": "low",
                "preferred_pace": "gentle",
                "language": "de",
                "wants_visuals": True,
                "wants_history": False,
                "declared_support_needs": ["dyscalculia_aware_support"],
            },
            runtime_observations=[
                {"evidence": ["repeated_concept_error", "attempt_count_three_plus"]},
            ],
        )
    )

    first_block = plan.planned_blocks[0]

    assert "repeated_attempt_three_plus" in first_block.observed_evidence
    assert "stop_retry_loop_and_reframe_concept" in first_block.support_moves
    assert "switch_from_attempt_counting_to_model_rebuild" in first_block.support_moves
    assert "number_lines" in first_block.support_scaffolds


def test_planner_marks_mixed_success_as_inconsistent_pattern() -> None:
    plan = build_teaching_plan(
        SessionRequest(
            objective="Erklaere mir diese Aufgabe Schritt fuer Schritt.",
            learner_profile={
                "age_group": "teen",
                "math_level": "middle_school",
                "confidence": "low",
                "preferred_pace": "balanced",
                "language": "de",
                "wants_visuals": True,
                "wants_history": False,
                "declared_support_needs": ["scarcity_aware_support"],
            },
            runtime_observations=[
                {"evidence": ["pattern_recognized", "transfer_success"]},
                {"evidence": ["single_concept_error"]},
            ],
        )
    )

    second_block = plan.planned_blocks[1]

    assert "mixed_success_inconsistent" in second_block.observed_evidence
    assert "stabilize_pattern_before_new_variation" in second_block.support_moves
    assert "contrast_why_this_problem_changed" in second_block.support_moves
    assert "clear_success_criteria" in second_block.support_scaffolds


def test_planner_derives_visible_small_success_from_local_progress() -> None:
    plan = build_teaching_plan(
        SessionRequest(
            objective="Erklaere mir diese Aufgabe Schritt fuer Schritt.",
            learner_profile={
                "age_group": "teen",
                "math_level": "middle_school",
                "confidence": "low",
                "preferred_pace": "balanced",
                "language": "de",
                "wants_visuals": True,
                "wants_history": False,
                "declared_support_needs": ["scarcity_aware_support"],
            },
            runtime_observations=[
                {"evidence": ["correct_with_guidance"]},
            ],
        )
    )

    assert "visible_small_success" in plan.planned_blocks[0].observed_evidence
    assert plan.mode_adaptation_trace[0].changed is False


def test_planner_derives_missing_success_line_across_blocks() -> None:
    plan = build_teaching_plan(
        SessionRequest(
            objective="Erklaere mir die quadratische Gleichung anschaulich.",
            learner_profile={
                "age_group": "teen",
                "math_level": "high_school",
                "confidence": "low",
                "preferred_pace": "balanced",
                "language": "de",
                "wants_visuals": True,
                "wants_history": False,
                "declared_support_needs": ["scarcity_aware_support"],
            },
            runtime_observations=[
                {"evidence": ["single_concept_error"]},
                {"evidence": ["single_concept_error"]},
                {"evidence": ["single_concept_error"]},
            ],
        )
    )

    assert "no_success_visible_two_blocks" in plan.planned_blocks[1].observed_evidence
    assert plan.mode_adaptation_trace[1].changed is False
    assert plan.mode_adaptation_trace[2].changed is True
    assert plan.mode_adaptation_trace[2].mode_after == "worked_example_tutoring"
