from mathteach.services.conflict_resolver import resolve_block_support_conflicts


def test_worked_example_pair_uses_mode_specific_release_and_rebuild() -> None:
    resolved_moves, summary = resolve_block_support_conflicts(
        support_moves=[
            "increase_pacing_monitor_only_after_concept_recovery",
            "stop_retry_loop_and_reframe_concept",
        ],
        active_supports=[
            "adhd_aware_support",
            "dyscalculia_aware_support",
        ],
        evidence=[
            "rapid_success_three_blocks",
            "repeated_attempt_three_plus",
        ],
        lesson_mode="worked_example_tutoring",
    )

    assert summary is not None
    assert summary.lesson_mode_applied == "worked_example_tutoring"
    assert "worked_example_rebuild_with_pacing_pause" in resolved_moves
    assert "worked_example_release_after_two_stable_steps" in resolved_moves
    assert summary.mode_evidence_adjustments


def test_worked_example_triad_uses_mode_specific_visual_concept_rule() -> None:
    resolved_moves, summary = resolve_block_support_conflicts(
        support_moves=[
            "reframe_concept_with_simple_language_and_quantity_support",
            "increase_pacing_after_concept_and_language_stabilize",
        ],
        active_supports=[
            "adhd_aware_support",
            "dyscalculia_aware_support",
            "language_sensitive_support",
        ],
        evidence=[
            "rapid_success_three_blocks",
            "repeated_attempt_three_plus",
            "text_overload",
            "vocabulary_request_again",
        ],
        lesson_mode="worked_example_tutoring",
    )

    assert summary is not None
    assert summary.lesson_mode_applied == "worked_example_tutoring"
    assert "worked_example_visual_concept_with_minimal_text" in resolved_moves
    assert "worked_example_release_after_concept_check" in resolved_moves
    assert "worked_example_check_after_each_micro_step" in resolved_moves
    assert any(
        "worked_example_tutoring" in item for item in summary.mode_evidence_adjustments
    )


def test_guided_concept_triad_uses_mode_specific_rebuild_rule() -> None:
    resolved_moves, summary = resolve_block_support_conflicts(
        support_moves=[
            "reframe_concept_with_simple_language_and_quantity_support",
            "keep_quantity_representation_visible",
        ],
        active_supports=[
            "adhd_aware_support",
            "dyscalculia_aware_support",
            "language_sensitive_support",
        ],
        evidence=[
            "repeated_attempt_three_plus",
            "text_overload",
            "vocabulary_request_again",
        ],
        lesson_mode="guided_concept_explanation",
    )

    assert summary is not None
    assert "guided_concept_rebuild_with_simple_language" in resolved_moves
    assert "guided_concept_single_check_after_rebuild" in resolved_moves
    assert summary.generated_moves


def test_origin_story_triad_delays_pacing_until_bridge_lands() -> None:
    resolved_moves, summary = resolve_block_support_conflicts(
        support_moves=[
            "reframe_concept_with_simple_language_and_quantity_support",
            "increase_pacing_after_concept_and_language_stabilize",
        ],
        active_supports=[
            "adhd_aware_support",
            "dyscalculia_aware_support",
            "language_sensitive_support",
        ],
        evidence=[
            "repeated_attempt_three_plus",
            "text_overload",
            "vocabulary_request_again",
        ],
        lesson_mode="origin_story_explanation",
    )

    assert summary is not None
    assert "origin_story_bridge_with_concise_math_language" in resolved_moves
    assert "delay_pacing_until_story_bridge_lands" in resolved_moves
