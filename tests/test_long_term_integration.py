from mathteach.models import (
    BlockSequencePathOption,
    BlockType,
    EvidenceCombination,
    EvidenceCombinationPattern,
    PlannedTeachingBlock,
)
from mathteach.services.block_sequence_planner import enrich_candidate_paths
from mathteach.services.learner_progress_model import (
    build_session_progress_tracker,
    infer_learning_goals,
)


def test_session_progress_tracker_builds_mastery_from_success_history() -> None:
    tracker = build_session_progress_tracker(
        session_id="session-1",
        objective="Explain quadratic equations with examples.",
        lesson_mode="worked_example_tutoring",
        math_level="high_school",
        planned_blocks=[
            PlannedTeachingBlock(
                block_index=1,
                mode="worked_example_tutoring",
                block_type=BlockType.WORKED_EXAMPLE,
                goal="goal",
                evidence_combination=EvidenceCombination(
                    patterns=[EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS],
                    current_evidence=["rapid_success_three_blocks"],
                    previous_evidence=[],
                    block_type=BlockType.WORKED_EXAMPLE,
                    block_sequence=1,
                ),
                observed_evidence=["rapid_success_three_blocks", "transfer_success"],
            )
        ],
    )

    assert tracker.current_concept == "quadratic_equations"
    assert tracker.learning_goals
    assert tracker.history_entries
    assert tracker.concept_mastery_tracking["quadratic_equations"] > 0.2


def test_enrich_candidate_paths_prefers_goal_and_language_aligned_path() -> None:
    tracker = build_session_progress_tracker(
        session_id="session-2",
        objective="Warum braucht man Brueche eigentlich?",
        lesson_mode="origin_story_explanation",
        math_level="middle_school",
        planned_blocks=[
            PlannedTeachingBlock(
                block_index=1,
                mode="origin_story_explanation",
                block_type=BlockType.CONCEPT_INTRODUCTION,
                goal="goal",
                evidence_combination=EvidenceCombination(
                    patterns=[EvidenceCombinationPattern.VOCABULARY_GAP],
                    current_evidence=["text_overload", "vocabulary_request"],
                    previous_evidence=[],
                    block_type=BlockType.CONCEPT_INTRODUCTION,
                    block_sequence=1,
                ),
                observed_evidence=["text_overload", "vocabulary_request"],
            )
        ],
    )
    goals = infer_learning_goals(
        "Warum braucht man Brueche eigentlich?",
        "origin_story_explanation",
        "middle_school",
    )

    enriched_paths = enrich_candidate_paths(
        candidate_paths=[
            BlockSequencePathOption(
                block_types=[
                    BlockType.CONCEPT_INTRODUCTION,
                    BlockType.WORKED_EXAMPLE,
                    BlockType.GUIDED_PRACTICE,
                ],
                score=0.62,
                rationale=["Concept-first path."],
            ),
            BlockSequencePathOption(
                block_types=[
                    BlockType.BRIDGE_TO_APPLICATION,
                    BlockType.REFLECTION,
                    BlockType.CONCEPT_CHECK,
                ],
                score=0.62,
                rationale=["Transfer-first path."],
            ),
        ],
        learning_goals=goals,
        session_tracker=tracker,
        active_supports=["language_sensitive_support"],
        active_patterns=[EvidenceCombinationPattern.VOCABULARY_GAP],
    )

    assert len(enriched_paths) == 2
    assert enriched_paths[0].total_score >= enriched_paths[1].total_score
    assert enriched_paths[0].goal_alignment_explanation
    assert enriched_paths[0].pilot_data_references
