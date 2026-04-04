from mathteach.services.conflict_resolver import resolve_block_support_conflicts


def test_block_conflict_resolution_adapts_pacing_for_adhd_dyscalculia() -> None:
    resolved_moves, summary = resolve_block_support_conflicts(
        support_moves=[
            "increase_pacing_after_stable_success",
            "offer_more_independent_challenge",
            "stop_retry_loop_and_reframe_concept",
            "switch_from_attempt_counting_to_model_rebuild",
        ],
        active_supports=[
            "adhd_aware_support",
            "dyscalculia_aware_support",
        ],
        evidence=[
            "rapid_success_three_blocks",
            "repeated_attempt_three_plus",
        ],
    )

    assert summary is not None
    assert "adhd_aware_support__dyscalculia_aware_support" in summary.pair_conflicts
    assert summary.priority_ladder == [
        "dyscalculia_aware_support",
        "adhd_aware_support",
    ]
    assert "offer_more_independent_challenge" in summary.suppressed_moves
    assert (
        "increase_pacing_after_stable_success -> "
        "increase_pacing_monitor_only_after_concept_recovery"
    ) in summary.adapted_moves
    assert "increase_pacing_after_stable_success" not in resolved_moves
    assert (
        resolved_moves.index("stop_retry_loop_and_reframe_concept")
        < resolved_moves.index("increase_pacing_monitor_only_after_concept_recovery")
    )


def test_block_conflict_resolution_uses_triad_priority_ladder() -> None:
    resolved_moves, summary = resolve_block_support_conflicts(
        support_moves=[
            "increase_pacing_after_stable_success",
            "stop_retry_loop_and_reframe_concept",
            "clarify_terms_before_retrying_math_step",
            "offer_more_independent_challenge",
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
        ],
    )

    assert summary is not None
    assert (
        summary.triad_group
        == "dyscalculia_aware_support__language_sensitive_support__adhd_aware_support"
    )
    assert summary.priority_ladder == [
        "dyscalculia_aware_support",
        "language_sensitive_support",
        "adhd_aware_support",
    ]
    assert (
        resolved_moves[0]
        == "reframe_concept_with_simple_language_and_quantity_support"
    )
    assert (
        resolved_moves.index("clarify_terms_inside_quantity_rebuild")
        < resolved_moves.index("increase_pacing_after_concept_and_language_stabilize")
    )


def test_block_conflict_resolution_adapts_adhd_and_dyslexia_moves() -> None:
    resolved_moves, summary = resolve_block_support_conflicts(
        support_moves=[
            "increase_pacing_after_stable_success",
            "offer_more_independent_challenge",
            "reduce_text_load_before_problem_solving",
            "use_step_labels_and_micro_checkpoints",
        ],
        active_supports=[
            "adhd_aware_support",
            "dyslexia_aware_support",
        ],
        evidence=[
            "rapid_success_three_blocks",
            "text_overload",
        ],
    )

    assert summary is not None
    assert summary.priority_ladder == [
        "dyslexia_aware_support",
        "adhd_aware_support",
    ]
    assert "offer_more_independent_challenge" in summary.suppressed_moves
    assert (
        "increase_pacing_after_stable_success -> increase_pacing_after_text_clarity"
        in summary.adapted_moves
    )
    assert (
        "reduce_text_load_before_problem_solving -> "
        "reduce_text_load_with_readaloud_anchor"
    ) in summary.adapted_moves
    assert "pair_shorter_text_with_clear_reading_path" in summary.generated_moves
    assert any(
        "pair_shorter_text_with_clear_reading_path" in item
        for item in summary.move_dependencies_applied
    )
    assert "increase_pacing_after_text_clarity" in resolved_moves
    assert "reduce_text_load_with_readaloud_anchor" in resolved_moves
    assert "pair_shorter_text_with_clear_reading_path" in resolved_moves


def test_block_conflict_resolution_generates_dyscalculia_language_combo_move() -> None:
    resolved_moves, summary = resolve_block_support_conflicts(
        support_moves=[
            "keep_quantity_representation_visible",
            "stop_retry_loop_and_reframe_concept",
            "clarify_terms_before_retrying_math_step",
        ],
        active_supports=[
            "dyscalculia_aware_support",
            "language_sensitive_support",
        ],
        evidence=[
            "repeated_attempt_three_plus",
            "text_overload",
        ],
    )

    assert summary is not None
    assert summary.priority_ladder == [
        "dyscalculia_aware_support",
        "language_sensitive_support",
    ]
    assert (
        "stop_retry_loop_and_reframe_concept -> "
        "reframe_concept_with_everyday_language_bridge"
    ) in summary.adapted_moves
    assert (
        "clarify_terms_before_retrying_math_step -> "
        "clarify_terms_inside_quantity_rebuild"
    ) in summary.adapted_moves
    assert "pair_visual_explanation_with_simple_language" in summary.generated_moves
    assert "pair_visual_explanation_with_simple_language" in resolved_moves
    assert (
        resolved_moves.index("reframe_concept_with_everyday_language_bridge")
        < resolved_moves.index("clarify_terms_inside_quantity_rebuild")
    )


def test_block_conflict_resolution_extends_adhd_dyslexia_autism_triad() -> None:
    resolved_moves, summary = resolve_block_support_conflicts(
        support_moves=[
            "increase_pacing_after_stable_success",
            "offer_more_independent_challenge",
            "split_problem_text_into_shorter_chunks",
            "keep_structure_predictable_and_literal",
        ],
        active_supports=[
            "adhd_aware_support",
            "dyslexia_aware_support",
            "autism_spectrum_aware_support",
        ],
        evidence=[
            "rapid_success_three_blocks",
            "text_overload",
            "structure_break",
        ],
    )

    assert summary is not None
    assert (
        summary.triad_group
        == "dyslexia_aware_support__autism_spectrum_aware_support__adhd_aware_support"
    )
    assert summary.priority_ladder == [
        "dyslexia_aware_support",
        "autism_spectrum_aware_support",
        "adhd_aware_support",
    ]
    assert "split_problem_text_into_shorter_predictable_chunks" in resolved_moves
    assert "keep_structure_predictable_with_visual_reading_anchors" in resolved_moves
    assert "use_predictable_visual_reading_sequence" in resolved_moves
    assert "increase_pacing_only_with_predictable_sequence" in resolved_moves
    assert "use_predictable_visual_reading_sequence" in summary.generated_moves


def test_block_conflict_resolution_extends_dyscalculia_language_scarcity_triad() -> None:
    resolved_moves, summary = resolve_block_support_conflicts(
        support_moves=[
            "stop_retry_loop_and_reframe_concept",
            "state_success_criteria_up_front",
            "keep_quantity_representation_visible",
            "clarify_terms_before_retrying_math_step",
        ],
        active_supports=[
            "dyscalculia_aware_support",
            "language_sensitive_support",
            "scarcity_aware_support",
        ],
        evidence=[
            "repeated_attempt_three_plus",
            "text_overload",
            "no_progress_two_blocks",
        ],
    )

    assert summary is not None
    assert (
        summary.triad_group
        == "dyscalculia_aware_support__language_sensitive_support__scarcity_aware_support"
    )
    assert summary.priority_ladder == [
        "dyscalculia_aware_support",
        "language_sensitive_support",
        "scarcity_aware_support",
    ]
    assert "reframe_concept_with_minimal_language_overhead" in resolved_moves
    assert "state_tiny_success_criteria_before_concept_repair" in resolved_moves
    assert "keep_concept_repair_within_visible_resource_limits" in resolved_moves
    assert "keep_concept_repair_within_visible_resource_limits" in summary.generated_moves
