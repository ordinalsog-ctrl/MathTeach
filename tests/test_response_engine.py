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
