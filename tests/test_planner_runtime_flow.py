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
    assert plan.mode_adaptation_trace == []


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
