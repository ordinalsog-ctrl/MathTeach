from mathteach.models import LearnerProfile, SupportSignalProfile, TutorResponseSettings


def _merge_unique(existing: list[str], additions: list[str]) -> list[str]:
    merged = list(existing)
    seen = set(existing)
    for item in additions:
        if item not in seen:
            merged.append(item)
            seen.add(item)
    return merged


def derive_support_signal_profile(profile: LearnerProfile) -> SupportSignalProfile:
    signal_profile = SupportSignalProfile()

    if profile.confidence == "low":
        signal_profile.math_anxiety = "moderate"

    for need in profile.declared_support_needs:
        if need == "adhd_aware_support":
            signal_profile.adhd_aware_support = "declared"
            signal_profile.working_memory_load = "fragile"
            signal_profile.attention_regulation = "fragile"
        elif need == "dyscalculia_aware_support":
            signal_profile.dyscalculia_aware_support = "declared"
            signal_profile.symbolic_processing = "fragile"
        elif need == "dyslexia_aware_support":
            signal_profile.dyslexia_aware_support = "declared"
        elif need == "autism_spectrum_aware_support":
            signal_profile.autism_spectrum_aware_support = "declared"
        elif need == "language_sensitive_support":
            signal_profile.language_sensitive_support = "declared"
        elif need == "scarcity_aware_support":
            signal_profile.scarcity_aware_support = "declared"

    if profile.language != "de" and signal_profile.language_sensitive_support == "none":
        signal_profile.language_sensitive_support = "possible"

    signal_profile.active_supports = [
        need
        for need in (
            "adhd_aware_support",
            "dyscalculia_aware_support",
            "dyslexia_aware_support",
            "autism_spectrum_aware_support",
            "language_sensitive_support",
            "scarcity_aware_support",
        )
        if getattr(signal_profile, need) != "none"
    ]
    return signal_profile


def _default_response_settings(profile: LearnerProfile) -> TutorResponseSettings:
    session_duration = {
        "gentle": "20_to_30_minute_guided_block",
        "balanced": "25_to_35_minute_guided_block",
        "intensive": "30_to_40_minute_guided_block",
    }[profile.preferred_pace]
    primary_representation = "visual_plus_verbal" if profile.wants_visuals else "verbal_then_symbolic"
    error_response_style = (
        "gentle_normalize_then_strategy"
        if profile.confidence == "low"
        else "direct_with_local_justification"
    )
    check_frequency = "every_major_step" if profile.confidence == "low" else "every_few_steps"
    external_scaffolds = ["clear_step_boundary"]
    if profile.wants_visuals:
        external_scaffolds.append("visual_hint")
    if profile.confidence == "low":
        external_scaffolds.append("confidence_preserving_check")

    return TutorResponseSettings(
        session_duration=session_duration,
        break_pattern="as_needed_between_major_steps",
        transition_buffer="brief_explicit_transition",
        conceptual_increment="small_to_medium",
        worked_example_ratio="balanced_examples_then_practice",
        fading_speed="gradual",
        symbolic_vs_verbal_balance="balanced",
        word_budget_per_chunk="short_clear_chunks",
        primary_representation=primary_representation,
        error_response_style=error_response_style,
        check_frequency=check_frequency,
        language_support="standard",
        sensory_load_level="standard",
        external_scaffolds=external_scaffolds,
        active_supports=[],
        rationale_summary=[
            "Start from a low-load explanation structure matched to the learner pace.",
            "Keep adaptation explicit and non-diagnostic.",
        ],
        source_anchors=[
            "organizing-instruction-and-study",
            "rosenshine-principles-of-instruction",
            "the-power-of-feedback",
        ],
    )


def _apply_adhd_support(settings: TutorResponseSettings) -> TutorResponseSettings:
    settings.session_duration = "12_to_15_minute_focus_blocks"
    settings.break_pattern = "short_structured_break_after_focus_block"
    settings.transition_buffer = "explicit_transition_cue_before_new_step"
    settings.conceptual_increment = "very_small_to_small"
    settings.worked_example_ratio = "high_initial_examples"
    settings.fading_speed = "gradual_when_stable"
    settings.symbolic_vs_verbal_balance = "verbal_plus_visual_before_dense_symbolic"
    settings.word_budget_per_chunk = "short_chunks_under_100_words"
    settings.primary_representation = "concrete_or_light_visual_then_symbolic"
    settings.error_response_style = "normalize_then_strategy"
    settings.check_frequency = "every_two_problems_or_major_step"
    settings.external_scaffolds = _merge_unique(
        settings.external_scaffolds,
        [
            "step_labels",
            "micro_checkpoints",
            "visible_progress_markers",
            "short_goal_for_this_block",
        ],
    )
    settings.active_supports = _merge_unique(settings.active_supports, ["adhd_aware_support"])
    settings.rationale_summary = _merge_unique(
        settings.rationale_summary,
        [
            "Use shorter focus blocks, explicit transitions, and fast feedback.",
            "Treat external structure as functional support rather than extra decoration.",
        ],
    )
    settings.source_anchors = _merge_unique(
        settings.source_anchors,
        [
            "cdc-adhd-classroom-support",
            "richardson-school-interventions-adhd",
            "barkley-executive-functions-adhd",
        ],
    )
    return settings


def _apply_dyscalculia_support(settings: TutorResponseSettings) -> TutorResponseSettings:
    settings.conceptual_increment = "very_small"
    settings.worked_example_ratio = "high_with_explicit_self_explanation"
    settings.fading_speed = "very_gradual"
    settings.symbolic_vs_verbal_balance = "quantity_plus_language_before_symbol_compression"
    settings.word_budget_per_chunk = "short_clear_chunks"
    settings.primary_representation = "manipulative_or_quantity_visual_first"
    settings.error_response_style = "explicit_reconstruction"
    settings.check_frequency = "after_each_major_micro_step"
    settings.external_scaffolds = _merge_unique(
        settings.external_scaffolds,
        [
            "number_lines",
            "ten_frames_or_quantity_grids",
            "counters_or_token_like_objects",
            "explicit_step_labels",
        ],
    )
    settings.active_supports = _merge_unique(settings.active_supports, ["dyscalculia_aware_support"])
    settings.rationale_summary = _merge_unique(
        settings.rationale_summary,
        [
            "Keep quantity meaning visible before compressing into symbols.",
            "Return to manipulatives or quantity visuals when repeated number errors appear.",
        ],
    )
    settings.source_anchors = _merge_unique(
        settings.source_anchors,
        [
            "butterworth-varma-laurillard-dyscalculia-science",
            "landerl-bevan-butterworth-developmental-dyscalculia",
            "nichd-dyscalculia-overview",
        ],
    )
    return settings


def derive_response_settings(
    profile: LearnerProfile, signal_profile: SupportSignalProfile
) -> TutorResponseSettings:
    settings = _default_response_settings(profile)

    if signal_profile.adhd_aware_support in {"declared", "highly_relevant"}:
        settings = _apply_adhd_support(settings)
    if signal_profile.dyscalculia_aware_support in {"declared", "highly_relevant"}:
        settings = _apply_dyscalculia_support(settings)
    if signal_profile.language_sensitive_support in {"possible", "declared", "highly_relevant"}:
        settings.language_support = "key_terms_and_syntax_support"
        settings.source_anchors = _merge_unique(
            settings.source_anchors,
            ["ies-english-learners-practice-guide"],
        )

    return settings


def build_support_response(
    profile: LearnerProfile,
) -> tuple[SupportSignalProfile, TutorResponseSettings]:
    signal_profile = derive_support_signal_profile(profile)
    response_settings = derive_response_settings(profile, signal_profile)
    return signal_profile, response_settings
