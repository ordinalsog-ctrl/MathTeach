from mathteach.config import Settings
from mathteach.models import (
    LearnerProfile,
    ModelAssignment,
    RetrievalPlan,
    SessionRequest,
    StackResponse,
    TeachingPlan,
)


AUDIENCE_MODES = {
    "child": ("concrete and encouraging", "Use stories, objects, and tiny steps."),
    "teen": ("clear and motivating", "Connect rules to intuition and school examples."),
    "adult": ("respectful and practical", "Tie math to goals, utility, and confidence rebuilding."),
    "expert": ("precise and compact", "Prefer formalism, provenance, and alternative derivations."),
}

LEVEL_DEPTH = {
    "early_school": ("foundational", False),
    "middle_school": ("guided", False),
    "high_school": ("layered", True),
    "undergraduate": ("formal", True),
    "graduate": ("advanced", True),
    "research": ("research-grade", True),
}


def build_stack(settings: Settings) -> StackResponse:
    return StackResponse(
        checked_on="2026-04-01",
        primary_choice=settings.primary_reasoner_model,
        assignments=[
            ModelAssignment(
                role="tutor_orchestrator",
                model=settings.primary_reasoner_model,
                why="Best default choice for complex tutoring flows, tool use, and grounded reasoning.",
            ),
            ModelAssignment(
                role="fast_hinting_and_routing",
                model=settings.fast_path_model,
                why="Lower cost and latency for helper tasks inside a teaching session.",
            ),
            ModelAssignment(
                role="offline_corpus_ingestion",
                model=settings.ingestion_model,
                why="Strong long-context fit for books, papers, and large document extraction.",
            ),
            ModelAssignment(
                role="hard_case_verification",
                model=settings.verifier_model,
                why="Useful as an optional second opinion for difficult reasoning or literature checks.",
            ),
            ModelAssignment(
                role="semantic_search",
                model=settings.embeddings_model,
                why="High-quality embeddings for multilingual semantic retrieval over math sources.",
            ),
        ],
        architecture_summary=(
            "Teacher agent plus math knowledge graph plus hybrid retrieval plus learner model."
        ),
    )


def build_teaching_plan(request: SessionRequest) -> TeachingPlan:
    profile: LearnerProfile = request.learner_profile
    tone, pattern_hint = AUDIENCE_MODES[profile.age_group]
    concept_depth, include_proof = LEVEL_DEPTH[profile.math_level]

    teaching_pattern = [
        "Start from the learner objective before introducing formal notation.",
        "Check prerequisites explicitly before pushing ahead.",
        pattern_hint,
    ]

    if profile.wants_visuals:
        teaching_pattern.append("Offer a visual or spatial explanation when possible.")
    if profile.confidence == "low":
        teaching_pattern.append("Reduce shame and normalize mistakes as part of learning.")
    if profile.wants_history:
        teaching_pattern.append("Include origin stories when they improve intuition.")

    retrieval_plan = RetrievalPlan(
        concept_depth=concept_depth,
        include_history=profile.wants_history,
        include_proof_sketch=include_proof,
        include_modern_applications=True,
        highlight_misconceptions=True,
        required_source_types=[
            "primary_math_source_or_standard_reference",
            "modern_explanatory_source",
            "worked_example_source",
        ],
    )

    evaluation_focus = [
        "Did the explanation respect prerequisites?",
        "Was the mathematical claim sourceable?",
        "Was the difficulty level appropriate for the learner?",
        "Did the answer leave a useful next step or self-check question?",
    ]

    next_turn_contract = [
        "State assumptions about the learner openly.",
        "Name the central idea before details.",
        "Keep notation load proportional to the learner level.",
        "Cite or reference source families for nontrivial claims.",
    ]

    return TeachingPlan(
        audience_mode=profile.age_group,
        tone=tone,
        teaching_pattern=teaching_pattern,
        retrieval_plan=retrieval_plan,
        evaluation_focus=evaluation_focus,
        next_turn_contract=next_turn_contract,
    )
