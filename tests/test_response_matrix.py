from mathteach.response_matrix import SupportSignalProfile, TutorResponseSettings


def test_support_signal_profile_defaults() -> None:
    profile = SupportSignalProfile()

    assert profile.working_memory_load == "typical"
    assert profile.adhd_aware_support == "none"
    assert profile.active_supports == []


def test_tutor_response_settings_model_roundtrip() -> None:
    settings = TutorResponseSettings(
        session_duration="25_to_35_minute_guided_block",
        break_pattern="as_needed_between_major_steps",
        transition_buffer="brief_explicit_transition",
        conceptual_increment="small_to_medium",
        worked_example_ratio="balanced_examples_then_practice",
        fading_speed="gradual",
        symbolic_vs_verbal_balance="balanced",
        word_budget_per_chunk="short_clear_chunks",
        primary_representation="visual_plus_verbal",
        error_response_style="gentle_normalize_then_strategy",
        check_frequency="every_major_step",
        language_support="standard",
        sensory_load_level="standard",
        external_scaffolds=["clear_step_boundary"],
        active_supports=["language_sensitive_support"],
        rationale_summary=["Keep adaptation explicit and non-diagnostic."],
        source_anchors=["organizing-instruction-and-study"],
    )

    dumped = settings.model_dump()

    assert dumped["active_supports"] == ["language_sensitive_support"]
    assert dumped["source_anchors"] == ["organizing-instruction-and-study"]
