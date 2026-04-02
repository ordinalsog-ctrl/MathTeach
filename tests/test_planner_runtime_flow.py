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
