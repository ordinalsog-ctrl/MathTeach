from mathteach.models import LearnerProfile
from mathteach.services.conflict_resolver import (
    detect_profile_conflicts,
    detect_profile_triads,
)
from mathteach.services.response_engine import build_support_response


def test_detect_profile_conflicts_for_adhd_and_dyscalculia() -> None:
    conflicts = detect_profile_conflicts(
        ["adhd_aware_support", "dyscalculia_aware_support", "dyslexia_aware_support"]
    )

    assert any(
        conflict.slug == "adhd_aware_support__dyscalculia_aware_support" for conflict in conflicts
    )


def test_detect_profile_triads_for_adhd_dyscalculia_and_scarcity() -> None:
    triads = detect_profile_triads(
        [
            "adhd_aware_support",
            "dyscalculia_aware_support",
            "scarcity_aware_support",
        ]
    )

    assert any(
        triad.slug
        == "adhd_aware_support__dyscalculia_aware_support__scarcity_aware_support"
        for triad in triads
    )


def test_mixed_profile_adhd_and_dyscalculia_resolution() -> None:
    profile = LearnerProfile(
        age_group="teen",
        math_level="middle_school",
        confidence="low",
        preferred_pace="gentle",
        language="de",
        wants_visuals=True,
        wants_history=False,
        declared_support_needs=["adhd_aware_support", "dyscalculia_aware_support"],
    )

    _, response_settings = build_support_response(profile)

    assert response_settings.session_duration == "15_to_18_minute_concrete_focus_blocks"
    assert response_settings.break_pattern == "ultradian_micro_breaks_within_concrete_work"
    assert (
        "adhd_aware_support__dyscalculia_aware_support"
        in response_settings.conflict_pairs
    )


def test_mixed_profile_adhd_and_scarcity_resolution() -> None:
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

    _, response_settings = build_support_response(profile)

    assert response_settings.language_support == "plain_goal_and_relevance_framing"
    assert response_settings.check_frequency == "every_two_problems_with_progress_confirmation"
    assert "clear_success_criteria" in response_settings.external_scaffolds


def test_mixed_profile_dyscalculia_and_language_sensitive_resolution() -> None:
    profile = LearnerProfile(
        age_group="teen",
        math_level="middle_school",
        confidence="medium",
        preferred_pace="balanced",
        language="en",
        wants_visuals=True,
        wants_history=False,
        declared_support_needs=["dyscalculia_aware_support"],
    )

    _, response_settings = build_support_response(profile)

    assert response_settings.symbolic_vs_verbal_balance == (
        "quantity_and_everyday_language_before_symbol_compression"
    )
    assert response_settings.language_support == (
        "translated_key_terms_glossary_and_quantity_language_support"
    )
    assert "quantity_word_bridge" in response_settings.external_scaffolds


def test_mixed_profile_adhd_and_autism_resolution() -> None:
    profile = LearnerProfile(
        age_group="teen",
        math_level="middle_school",
        confidence="medium",
        preferred_pace="balanced",
        language="de",
        wants_visuals=True,
        wants_history=False,
        declared_support_needs=["adhd_aware_support", "autism_spectrum_aware_support"],
    )

    _, response_settings = build_support_response(profile)

    assert response_settings.session_duration == "predictable_15_to_18_minute_focus_blocks"
    assert response_settings.break_pattern == "predictable_ultradian_regulation_breaks"
    assert response_settings.sensory_load_level == "minimal_and_high_contrast"


def test_triad_resolution_adhd_dyscalculia_and_scarcity() -> None:
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

    _, response_settings = build_support_response(profile)

    assert response_settings.session_duration == "15_to_18_minute_concrete_success_blocks"
    assert response_settings.break_pattern == "ultradian_micro_breaks_within_concrete_work"
    assert response_settings.check_frequency == (
        "after_each_major_micro_step_with_progress_confirmation"
    )
    assert (
        "adhd_aware_support__dyscalculia_aware_support__scarcity_aware_support"
        in response_settings.triad_groups
    )
    assert "conceptual_grounding_before_speed" in response_settings.priority_ladders


def test_triad_resolution_dyscalculia_language_and_scarcity() -> None:
    profile = LearnerProfile(
        age_group="teen",
        math_level="middle_school",
        confidence="low",
        preferred_pace="balanced",
        language="en",
        wants_visuals=True,
        wants_history=False,
        declared_support_needs=[
            "dyscalculia_aware_support",
            "scarcity_aware_support",
        ],
    )

    _, response_settings = build_support_response(profile)

    assert response_settings.language_support == (
        "translated_key_terms_glossary_quantity_language_and_relevance_support"
    )
    assert (
        "dyscalculia_aware_support__language_sensitive_support__scarcity_aware_support"
        in response_settings.triad_groups
    )
    assert "quantity_meaning_before_symbol_compression" in response_settings.priority_ladders
