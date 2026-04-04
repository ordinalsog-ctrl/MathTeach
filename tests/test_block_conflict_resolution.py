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
    assert resolved_moves[0] == "stop_retry_loop_and_reframe_concept"
    assert (
        resolved_moves.index("clarify_terms_before_retrying_math_step")
        < resolved_moves.index("increase_pacing_monitor_only_after_concept_recovery")
    )
