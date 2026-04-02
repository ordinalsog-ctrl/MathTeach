from mathteach.models import LearnerProfile
from mathteach.response_matrix import SupportSignalProfile, TutorResponseSettings


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
            signal_profile.symbolic_processing = "fragile"
        elif need == "autism_spectrum_aware_support":
            signal_profile.autism_spectrum_aware_support = "declared"
            signal_profile.attention_regulation = "supported"
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


def _apply_dyslexia_support(settings: TutorResponseSettings) -> TutorResponseSettings:
    settings.symbolic_vs_verbal_balance = "clear_symbol_spacing_with_supported_language"
    settings.word_budget_per_chunk = "very_short_chunks_with_simple_sentences"
    settings.primary_representation = "visual_plus_audio_ready_before_dense_text"
    settings.error_response_style = "clarify_reading_load_before_math_correction"
    settings.check_frequency = "every_major_step_with_term_check"
    settings.language_support = "glossary_plus_key_terms_plus_simplified_syntax"
    settings.sensory_load_level = "reduced_visual_clutter"
    settings.external_scaffolds = _merge_unique(
        settings.external_scaffolds,
        [
            "key_term_highlighting",
            "step_labels",
            "symbol_reading_support",
            "short_sentence_chunks",
        ],
    )
    settings.active_supports = _merge_unique(settings.active_supports, ["dyslexia_aware_support"])
    settings.rationale_summary = _merge_unique(
        settings.rationale_summary,
        [
            "Reduce reading burden before inferring mathematical misunderstanding.",
            "Keep symbols visible and spaced while language stays short and explicit.",
        ],
    )
    settings.source_anchors = _merge_unique(
        settings.source_anchors,
        [
            "nichd-reading-and-reading-disorders",
            "shaywitz-dyslexia-specific-reading-disability",
        ],
    )
    return settings


def _apply_autism_support(settings: TutorResponseSettings) -> TutorResponseSettings:
    settings.session_duration = "predictable_guided_block"
    settings.break_pattern = "predictable_optional_pause_points"
    settings.transition_buffer = "explicit_transition_cue_before_every_shift"
    settings.conceptual_increment = "small_and_highly_explicit"
    settings.worked_example_ratio = "structured_examples_before_variation"
    settings.symbolic_vs_verbal_balance = "explicit_literal_language_with_clean_symbol_layout"
    settings.word_budget_per_chunk = "short_explicit_chunks"
    settings.primary_representation = "stable_visual_structure_before_format_shifts"
    settings.error_response_style = "explicit_calm_local_correction"
    settings.check_frequency = "predictable_checkpoint_rhythm"
    settings.language_support = "explicit_literal_instructions"
    settings.sensory_load_level = "minimal_and_high_contrast"
    settings.external_scaffolds = _merge_unique(
        settings.external_scaffolds,
        [
            "consistent_session_structure",
            "step_labels",
            "explicit_transition_cues",
            "visible_progress_markers",
            "stable_visual_layout",
        ],
    )
    settings.active_supports = _merge_unique(
        settings.active_supports, ["autism_spectrum_aware_support"]
    )
    settings.rationale_summary = _merge_unique(
        settings.rationale_summary,
        [
            "Use predictable structure, explicit transitions, and low sensory clutter.",
            "Keep language literal and examples stable before introducing variation.",
        ],
    )
    settings.source_anchors = _merge_unique(
        settings.source_anchors,
        [
            "cdc-autism-treatment-and-intervention",
            "rutherford-visual-supports-autism-scoping-review",
            "arthur-kelly-visual-supports-autism-issues",
        ],
    )
    return settings


def _apply_language_sensitive_support(settings: TutorResponseSettings) -> TutorResponseSettings:
    settings.symbolic_vs_verbal_balance = "everyday_language_bridge_before_compact_symbolic"
    settings.word_budget_per_chunk = "short_chunks_with_controlled_vocabulary"
    if settings.primary_representation in {"verbal_then_symbolic", "visual_plus_verbal"}:
        settings.primary_representation = "visual_plus_term_support_before_dense_language"
    if settings.error_response_style in {
        "gentle_normalize_then_strategy",
        "direct_with_local_justification",
        "normalize_then_strategy",
    }:
        settings.error_response_style = "clarify_term_meaning_then_math_correction"
    if settings.check_frequency in {"every_few_steps", "every_major_step"}:
        settings.check_frequency = "every_major_step_with_term_confirmation"
    if settings.language_support == "explicit_literal_instructions":
        settings.language_support = "explicit_literal_instructions_with_key_terms_and_syntax_support"
    elif settings.language_support == "standard":
        settings.language_support = "translated_key_terms_glossary_and_simplified_syntax"
    settings.external_scaffolds = _merge_unique(
        settings.external_scaffolds,
        [
            "key_term_glossary",
            "everyday_to_math_language_bridge",
            "translated_key_terms_when_needed",
            "term_confirmation_checks",
        ],
    )
    settings.active_supports = _merge_unique(
        settings.active_supports, ["language_sensitive_support"]
    )
    settings.rationale_summary = _merge_unique(
        settings.rationale_summary,
        [
            "Bridge everyday language and mathematical terminology before increasing formal density.",
            "Check whether term meaning, not only calculation, is blocking the next step.",
        ],
    )
    settings.source_anchors = _merge_unique(
        settings.source_anchors,
        [
            "ies-english-learners-practice-guide",
            "sharma-sharma-multilingual-math-meta-analysis",
        ],
    )
    return settings


def _apply_scarcity_support(settings: TutorResponseSettings) -> TutorResponseSettings:
    settings.transition_buffer = "brief_explicit_transition_with_goal_reminder"
    if settings.worked_example_ratio == "balanced_examples_then_practice":
        settings.worked_example_ratio = "examples_then_quick_success_practice"
    if settings.symbolic_vs_verbal_balance == "balanced":
        settings.symbolic_vs_verbal_balance = "meaning_and_relevance_before_dense_formalism"
    if settings.word_budget_per_chunk == "short_clear_chunks":
        settings.word_budget_per_chunk = "short_clear_chunks_with_immediate_relevance"
    if settings.primary_representation in {"verbal_then_symbolic", "visual_plus_verbal"}:
        settings.primary_representation = "everyday_relevance_then_visual_or_symbolic"
    if settings.error_response_style in {
        "gentle_normalize_then_strategy",
        "direct_with_local_justification",
    }:
        settings.error_response_style = "stabilize_then_strategy_with_progress_marker"
    if settings.check_frequency in {"every_few_steps", "every_major_step"}:
        settings.check_frequency = "every_major_step_with_progress_confirmation"
    if settings.language_support == "standard":
        settings.language_support = "plain_goal_and_relevance_framing"
    settings.external_scaffolds = _merge_unique(
        settings.external_scaffolds,
        [
            "clear_success_criteria",
            "visible_progress_markers",
            "why_this_matters_now",
            "small_wins_sequence",
            "re_entry_summary_after_interruption",
        ],
    )
    settings.active_supports = _merge_unique(settings.active_supports, ["scarcity_aware_support"])
    settings.rationale_summary = _merge_unique(
        settings.rationale_summary,
        [
            "Reduce unnecessary friction and make immediate value visible under constrained bandwidth.",
            "Use explicit success criteria and small visible wins to protect persistence and dignity.",
        ],
    )
    settings.source_anchors = _merge_unique(
        settings.source_anchors,
        [
            "mani-mullainathan-shafir-zhao-poverty-cognition",
            "steele-aronson-stereotype-threat",
            "unesco-gem-inclusion-and-education",
            "ryan-deci-self-determination-theory",
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
    if signal_profile.dyslexia_aware_support in {"declared", "highly_relevant"}:
        settings = _apply_dyslexia_support(settings)
    if signal_profile.autism_spectrum_aware_support in {"declared", "highly_relevant"}:
        settings = _apply_autism_support(settings)
    if signal_profile.language_sensitive_support in {"possible", "declared", "highly_relevant"}:
        settings = _apply_language_sensitive_support(settings)
    if signal_profile.scarcity_aware_support in {"declared", "highly_relevant"}:
        settings = _apply_scarcity_support(settings)

    return settings


def build_support_response(
    profile: LearnerProfile,
) -> tuple[SupportSignalProfile, TutorResponseSettings]:
    signal_profile = derive_support_signal_profile(profile)
    response_settings = derive_response_settings(profile, signal_profile)
    return signal_profile, response_settings
