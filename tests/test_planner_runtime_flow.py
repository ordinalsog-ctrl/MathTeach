from mathteach.models import SessionRequest
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
