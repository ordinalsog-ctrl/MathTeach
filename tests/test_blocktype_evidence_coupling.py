from mathteach.models import BlockType, EvidenceCombinationPattern
from mathteach.services.conflict_resolver import resolve_block_support_conflicts


def test_blocktype_worked_example_adds_accelerated_example_support() -> None:
    resolved_moves, summary = resolve_block_support_conflicts(
        support_moves=[
            "worked_example_release_after_two_stable_steps",
            "worked_example_rebuild_with_pacing_pause",
        ],
        active_supports=[
            "adhd_aware_support",
            "dyscalculia_aware_support",
        ],
        evidence=["rapid_success_three_blocks", "visible_small_success"],
        lesson_mode="worked_example_tutoring",
        block_type=BlockType.WORKED_EXAMPLE,
        evidence_patterns=[EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS],
    )

    assert summary is not None
    assert summary.block_type_applied == BlockType.WORKED_EXAMPLE
    assert (
        EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS
        in summary.evidence_patterns_applied
    )
    assert summary.blocktype_adjustments_applied
    assert "worked_example_accelerated_with_pacing_checks" in resolved_moves
    assert "use_concrete_example_as_anchor" in resolved_moves


def test_blocktype_worked_example_combines_confusion_and_vocabulary_gap() -> None:
    resolved_moves, summary = resolve_block_support_conflicts(
        support_moves=[
            "worked_example_visual_concept_with_minimal_text",
            "clarify_terms_inside_quantity_rebuild",
        ],
        active_supports=[
            "adhd_aware_support",
            "dyscalculia_aware_support",
            "language_sensitive_support",
        ],
        evidence=[
            "repeated_concept_error",
            "repeated_attempt_three_plus",
            "text_overload",
            "vocabulary_request_again",
        ],
        lesson_mode="worked_example_tutoring",
        block_type=BlockType.WORKED_EXAMPLE,
        evidence_patterns=[
            EvidenceCombinationPattern.CONCEPT_CONFUSION,
            EvidenceCombinationPattern.VOCABULARY_GAP,
        ],
    )

    assert summary is not None
    assert summary.evidence_combination_rules_applied
    assert "preemptively_clarify_key_terms" in resolved_moves
    assert "worked_example_concept_clarification_sequence" in resolved_moves


def test_blocktype_error_recovery_adds_structured_recovery_moves() -> None:
    resolved_moves, summary = resolve_block_support_conflicts(
        support_moves=[
            "stabilize_layout_before_new_quantity_variation",
            "rebuild_errors_from_quantity_model",
        ],
        active_supports=[
            "dyscalculia_aware_support",
            "autism_spectrum_aware_support",
        ],
        evidence=[
            "repeated_attempt_three_plus",
            "no_progress_two_blocks",
        ],
        lesson_mode="guided_concept_explanation",
        block_type=BlockType.ERROR_RECOVERY,
        evidence_patterns=[EvidenceCombinationPattern.STAGNATION_PATTERN],
    )

    assert summary is not None
    assert summary.block_type_applied == BlockType.ERROR_RECOVERY
    assert "structured_error_analysis_with_prediction" in resolved_moves
    assert "error_recovery_with_concept_reframing" in resolved_moves
