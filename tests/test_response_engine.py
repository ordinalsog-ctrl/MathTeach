from mathteach.models import LearnerProfile
from mathteach.services.response_engine import build_support_response


def test_response_engine_adhd_profile() -> None:
    profile = LearnerProfile(
        age_group="teen",
        math_level="high_school",
        confidence="low",
        preferred_pace="gentle",
        language="de",
        wants_visuals=True,
        wants_history=True,
        declared_support_needs=["adhd_aware_support"],
    )

    signal_profile, response_settings = build_support_response(profile)

    assert signal_profile.adhd_aware_support == "declared"
    assert signal_profile.attention_regulation == "fragile"
    assert response_settings.session_duration == "12_to_15_minute_focus_blocks"
    assert response_settings.break_pattern == "short_structured_break_after_focus_block"
    assert "step_labels" in response_settings.external_scaffolds
    assert "barkley-executive-functions-adhd" in response_settings.source_anchors


def test_response_engine_dyscalculia_profile() -> None:
    profile = LearnerProfile(
        age_group="child",
        math_level="early_school",
        confidence="low",
        preferred_pace="gentle",
        language="de",
        wants_visuals=True,
        wants_history=False,
        declared_support_needs=["dyscalculia_aware_support"],
    )

    signal_profile, response_settings = build_support_response(profile)

    assert signal_profile.dyscalculia_aware_support == "declared"
    assert signal_profile.symbolic_processing == "fragile"
    assert response_settings.primary_representation == "manipulative_or_quantity_visual_first"
    assert response_settings.conceptual_increment == "very_small"
    assert response_settings.error_response_style == "explicit_reconstruction"
    assert "number_lines" in response_settings.external_scaffolds
    assert "visible_link_between_quantity_and_symbol" in response_settings.external_scaffolds


def test_response_engine_dyslexia_profile() -> None:
    profile = LearnerProfile(
        age_group="teen",
        math_level="middle_school",
        confidence="low",
        preferred_pace="balanced",
        language="de",
        wants_visuals=True,
        wants_history=False,
        declared_support_needs=["dyslexia_aware_support"],
    )

    signal_profile, response_settings = build_support_response(profile)

    assert signal_profile.dyslexia_aware_support == "declared"
    assert signal_profile.symbolic_processing == "fragile"
    assert response_settings.language_support == "glossary_plus_key_terms_plus_simplified_syntax"
    assert response_settings.error_response_style == "clarify_reading_load_before_math_correction"
    assert "key_term_highlighting" in response_settings.external_scaffolds
    assert "shaywitz-dyslexia-specific-reading-disability" in response_settings.source_anchors


def test_response_engine_autism_profile() -> None:
    profile = LearnerProfile(
        age_group="teen",
        math_level="middle_school",
        confidence="medium",
        preferred_pace="balanced",
        language="de",
        wants_visuals=True,
        wants_history=False,
        declared_support_needs=["autism_spectrum_aware_support"],
    )

    signal_profile, response_settings = build_support_response(profile)

    assert signal_profile.autism_spectrum_aware_support == "declared"
    assert signal_profile.attention_regulation == "supported"
    assert response_settings.sensory_load_level == "minimal_and_high_contrast"
    assert response_settings.language_support == "explicit_literal_instructions"
    assert "consistent_session_structure" in response_settings.external_scaffolds
    assert "rutherford-visual-supports-autism-scoping-review" in response_settings.source_anchors


def test_response_engine_language_sensitive_profile() -> None:
    profile = LearnerProfile(
        age_group="teen",
        math_level="middle_school",
        confidence="medium",
        preferred_pace="balanced",
        language="en",
        wants_visuals=True,
        wants_history=False,
    )

    signal_profile, response_settings = build_support_response(profile)

    assert signal_profile.language_sensitive_support == "possible"
    assert response_settings.language_support == (
        "translated_key_terms_glossary_and_simplified_syntax"
    )
    assert response_settings.symbolic_vs_verbal_balance == (
        "everyday_language_bridge_before_compact_symbolic"
    )
    assert "key_term_glossary" in response_settings.external_scaffolds
    assert "sharma-sharma-multilingual-math-meta-analysis" in response_settings.source_anchors


def test_response_engine_scarcity_profile() -> None:
    profile = LearnerProfile(
        age_group="teen",
        math_level="middle_school",
        confidence="low",
        preferred_pace="balanced",
        language="de",
        wants_visuals=True,
        wants_history=False,
        declared_support_needs=["scarcity_aware_support"],
    )

    signal_profile, response_settings = build_support_response(profile)

    assert signal_profile.scarcity_aware_support == "declared"
    assert response_settings.transition_buffer == "brief_explicit_transition_with_goal_reminder"
    assert response_settings.language_support == "plain_goal_and_relevance_framing"
    assert "clear_success_criteria" in response_settings.external_scaffolds
    assert "mani-mullainathan-shafir-zhao-poverty-cognition" in response_settings.source_anchors
