from mathteach.models import LearnerProfile
from mathteach.services.mode_selector import select_mode
from mathteach.services.response_engine import build_support_response


def test_mode_selector_keeps_requested_mode_without_override() -> None:
    profile = LearnerProfile(
        age_group="adult",
        math_level="high_school",
        confidence="medium",
        preferred_pace="balanced",
        language="de",
        wants_visuals=True,
        wants_history=True,
    )

    signal_profile, response_settings = build_support_response(profile)
    selection = select_mode(
        "origin_story_explanation",
        profile,
        signal_profile,
        response_settings,
    )

    assert selection.selected_mode == "origin_story_explanation"
    assert selection.constraints == []


def test_mode_selector_reduces_adhd_scarcity_origin_mode_to_origin_then_example() -> None:
    profile = LearnerProfile(
        age_group="teen",
        math_level="middle_school",
        confidence="low",
        preferred_pace="balanced",
        language="de",
        wants_visuals=True,
        wants_history=False,
        declared_support_needs=["adhd_aware_support", "scarcity_aware_support"],
    )

    signal_profile, response_settings = build_support_response(profile)
    selection = select_mode(
        "origin_story_explanation",
        profile,
        signal_profile,
        response_settings,
    )

    assert selection.selected_mode == "origin_then_example"
    assert "micro_origin_bridge" in selection.constraints
    assert "immediate_relevance_signal" in selection.constraints


def test_mode_selector_uses_origin_then_example_for_dyscalculia_language_scarcity() -> None:
    profile = LearnerProfile(
        age_group="teen",
        math_level="middle_school",
        confidence="low",
        preferred_pace="balanced",
        language="en",
        wants_visuals=True,
        wants_history=False,
        declared_support_needs=["dyscalculia_aware_support", "scarcity_aware_support"],
    )

    signal_profile, response_settings = build_support_response(profile)
    selection = select_mode(
        "guided_concept_explanation",
        profile,
        signal_profile,
        response_settings,
    )

    assert selection.selected_mode == "origin_then_example"
    assert "term_support_first" in selection.constraints


def test_mode_selector_uses_worked_examples_for_adhd_dyscalculia_scarcity() -> None:
    profile = LearnerProfile(
        age_group="teen",
        math_level="middle_school",
        confidence="low",
        preferred_pace="gentle",
        language="de",
        wants_visuals=True,
        wants_history=False,
        declared_support_needs=[
            "adhd_aware_support",
            "dyscalculia_aware_support",
            "scarcity_aware_support",
        ],
    )

    signal_profile, response_settings = build_support_response(profile)
    selection = select_mode(
        "origin_then_example",
        profile,
        signal_profile,
        response_settings,
    )

    assert selection.selected_mode == "worked_example_tutoring"
    assert "micro_success_cycles" in selection.constraints


def test_mode_selector_uses_worked_examples_for_adhd_autism_scarcity() -> None:
    profile = LearnerProfile(
        age_group="teen",
        math_level="middle_school",
        confidence="low",
        preferred_pace="gentle",
        language="de",
        wants_visuals=True,
        wants_history=False,
        declared_support_needs=[
            "adhd_aware_support",
            "autism_spectrum_aware_support",
            "scarcity_aware_support",
        ],
    )

    signal_profile, response_settings = build_support_response(profile)
    selection = select_mode(
        "guided_concept_explanation",
        profile,
        signal_profile,
        response_settings,
    )

    assert selection.selected_mode == "worked_example_tutoring"
    assert "high_structure" in selection.constraints
    assert "minimal_mode_switching" in selection.constraints
