from mathteach.models import (
    BlockType,
    ConceptComplexityLevel,
    LearningGoalCategory,
    LongTermLearningGoal,
    PlannedTeachingBlock,
    SessionProgressTracker,
    SessionHistoryEntry,
)


def _normalize_text(value: str) -> str:
    return (
        value.casefold()
        .replace("\u00e4", "ae")
        .replace("\u00f6", "oe")
        .replace("\u00fc", "ue")
        .replace("\u00df", "ss")
    )


def infer_concept_slug(objective: str) -> str:
    normalized = _normalize_text(objective)
    if "bruch" in normalized or "fraction" in normalized:
        return "fractions"
    if "quadrat" in normalized:
        return "quadratic_equations"
    if "gleichung" in normalized or "equation" in normalized:
        return "equations"
    if "ableitung" in normalized or "differential" in normalized:
        return "calculus_change"

    tokens = [
        token
        for token in "".join(
            ch if ch.isalnum() or ch == " " else " " for ch in normalized
        ).split()
        if len(token) > 2
    ]
    return "_".join(tokens[:3]) or "math_concept"


def _infer_complexity_level(math_level: str) -> ConceptComplexityLevel:
    if math_level in {"early_school", "middle_school"}:
        return ConceptComplexityLevel.FOUNDATIONAL
    if math_level in {"high_school", "undergraduate"}:
        return ConceptComplexityLevel.INTERMEDIATE
    return ConceptComplexityLevel.ADVANCED


def infer_learning_goals(
    objective: str,
    lesson_mode: str,
    math_level: str,
) -> list[LongTermLearningGoal]:
    concept = infer_concept_slug(objective)
    complexity = _infer_complexity_level(math_level)

    goals = [
        LongTermLearningGoal(
            goal_id=f"{concept}_mastery",
            category=LearningGoalCategory.CONCEPT_MASTERY,
            concept=concept,
            description=f"Build stable mastery for {concept}.",
            complexity_level=complexity,
            target_mastery_threshold=0.85,
            estimated_blocks_needed=5 if complexity == ConceptComplexityLevel.INTERMEDIATE else 4,
        )
    ]

    if lesson_mode in {
        "origin_story_explanation",
        "guided_concept_explanation",
        "origin_then_example",
    }:
        goals.append(
            LongTermLearningGoal(
                goal_id=f"{concept}_understanding",
                category=LearningGoalCategory.CONCEPTUAL_UNDERSTANDING,
                concept=concept,
                description=f"Strengthen conceptual understanding for {concept}.",
                complexity_level=complexity,
                target_mastery_threshold=0.75,
                estimated_blocks_needed=4,
            )
        )

    if lesson_mode in {"worked_example_tutoring", "origin_then_example"}:
        goals.append(
            LongTermLearningGoal(
                goal_id=f"{concept}_transfer",
                category=LearningGoalCategory.TRANSFER_ABILITY,
                concept=concept,
                description=f"Reach transfer-ready application for {concept}.",
                complexity_level=complexity,
                target_mastery_threshold=0.7,
                estimated_blocks_needed=3,
            )
        )

    return goals


def _difficulty_rating_for_block(block_type: BlockType | None) -> float:
    mapping = {
        BlockType.CONCEPT_INTRODUCTION: 0.35,
        BlockType.WORKED_EXAMPLE: 0.5,
        BlockType.GUIDED_PRACTICE: 0.6,
        BlockType.ERROR_RECOVERY: 0.7,
        BlockType.CONCEPT_CHECK: 0.45,
        BlockType.BRIDGE_TO_APPLICATION: 0.75,
        BlockType.REFLECTION: 0.25,
    }
    return mapping.get(block_type or BlockType.REFLECTION, 0.5)


def _success_indicators_for_block(block: PlannedTeachingBlock) -> list[str]:
    evidence = set(block.observed_evidence)
    indicators = ["completed"]

    if evidence & {
        "rapid_success_two_blocks",
        "rapid_success_three_blocks",
        "transfer_success",
        "transfer_success_two_blocks",
    }:
        indicators.append("high_accuracy")

    if evidence & {
        "visible_small_success",
        "error_recovery_with_hint",
        "self_correction",
    }:
        indicators.append("confident")

    if evidence & {
        "text_overload",
        "repeated_concept_error",
        "repeated_attempt_three_plus",
        "no_progress_two_blocks",
        "no_progress_three_blocks",
    }:
        indicators.append("needs_support")

    return indicators


def build_session_progress_tracker(
    session_id: str | None,
    objective: str,
    lesson_mode: str,
    math_level: str,
    planned_blocks: list[PlannedTeachingBlock],
) -> SessionProgressTracker:
    concept = infer_concept_slug(objective)
    goals = infer_learning_goals(objective, lesson_mode, math_level)
    history_entries: list[SessionHistoryEntry] = []
    mastery = 0.0

    for block in planned_blocks:
        if not block.observed_evidence:
            continue
        entry = SessionHistoryEntry(
            block_index=block.block_index,
            block_type=block.block_type or BlockType.REFLECTION,
            evidence_patterns=(
                block.evidence_combination.patterns if block.evidence_combination else []
            ),
            observed_evidence=block.observed_evidence,
            success_indicators=_success_indicators_for_block(block),
            difficulty_rating=_difficulty_rating_for_block(block.block_type),
            concept_target=concept,
        )
        history_entries.append(entry)

        contribution = 0.2
        if "high_accuracy" in entry.success_indicators:
            contribution += 0.25
        if "confident" in entry.success_indicators:
            contribution += 0.15
        if "needs_support" in entry.success_indicators:
            contribution -= 0.1
        if any(pattern.value == "rapid_consecutive_success" for pattern in entry.evidence_patterns):
            contribution += 0.1
        if any(pattern.value == "stagnation_pattern" for pattern in entry.evidence_patterns):
            contribution -= 0.1
        mastery = max(0.0, min(1.0, mastery + (contribution - mastery) * 0.4))

    return SessionProgressTracker(
        session_id=session_id,
        current_concept=concept,
        learning_goals=goals,
        history_entries=history_entries,
        concept_mastery_tracking={concept: mastery},
    )
