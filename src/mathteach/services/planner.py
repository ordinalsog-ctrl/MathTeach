from mathteach.config import Settings
from mathteach.models import (
    LearnerProfile,
    ModelAssignment,
    RetrievalPlan,
    SessionRequest,
    StackResponse,
    TeachingPlan,
)
from mathteach.services.response_engine import build_support_response


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

ORIGIN_HINTS = (
    "laie",
    "einfach",
    "ursprung",
    "notwendig",
    "angewandt",
    "geschichte",
    "grundidee",
    "wozu",
    "warum",
)

EXAMPLE_HINTS = (
    "beispiel",
    "zahlenbeispiel",
    "anhand",
    "aufgabe",
    "rechne",
    "loese",
    "loesen",
    "gegeben",
)


def _normalize_text(value: str) -> str:
    return (
        value.casefold()
        .replace("\u00e4", "ae")
        .replace("\u00f6", "oe")
        .replace("\u00fc", "ue")
        .replace("\u00df", "ss")
    )


def _infer_lesson_mode(request: SessionRequest) -> str:
    objective = _normalize_text(request.objective)
    has_origin = any(hint in objective for hint in ORIGIN_HINTS)
    has_example = any(hint in objective for hint in EXAMPLE_HINTS)

    if has_origin and has_example:
        return "origin_then_example"
    if has_origin:
        return "origin_story_explanation"
    if has_example:
        return "worked_example_tutoring"
    if request.learner_profile.age_group == "expert":
        return "formal_compact_explanation"
    return "guided_concept_explanation"


def _mode_response_arc(lesson_mode: str) -> list[str]:
    if lesson_mode == "origin_story_explanation":
        return [
            "Start with the motivating problem before formal notation.",
            "Explain why the concept became necessary.",
            "Use plain language before symbols.",
            "Connect the concept to one simple example.",
            "Close with a present-day application.",
        ]
    if lesson_mode == "origin_then_example":
        return [
            "Start with the historical or intuitive need for the concept.",
            "Name the core mathematical idea in simple language.",
            "Work through the learner example step by step.",
            "Check the result against the original problem.",
            "End with a transfer pattern for similar tasks.",
        ]
    if lesson_mode == "worked_example_tutoring":
        return [
            "Restate the learner problem in simple words.",
            "Classify the problem type before solving.",
            "Solve one step at a time with local justification.",
            "Check the answer against the original statement.",
            "End with a reusable pattern summary.",
        ]
    if lesson_mode == "formal_compact_explanation":
        return [
            "State the formal object first.",
            "Name assumptions and notation explicitly.",
            "Give the shortest valid derivation path.",
            "Point to one alternative formulation or proof route.",
            "Close with source-aware next steps.",
        ]
    return [
        "Start from intuition before notation.",
        "Name the core mathematical object clearly.",
        "Give one small worked example.",
        "State the main rule or pattern explicitly.",
        "End with a quick self-check question.",
    ]


def _mode_history_strategy(lesson_mode: str, wants_history: bool) -> tuple[bool, str]:
    if lesson_mode == "origin_story_explanation":
        return True, "origin_first"
    if lesson_mode == "origin_then_example":
        return True, "origin_then_example"
    if lesson_mode == "worked_example_tutoring":
        return wants_history, "supporting_only" if wants_history else "minimal"
    if lesson_mode == "formal_compact_explanation":
        return wants_history, "minimal"
    return wants_history, "supporting_only" if wants_history else "minimal"


def _mode_network_focus(lesson_mode: str) -> list[str]:
    if lesson_mode == "origin_story_explanation":
        return [
            "transmission_path",
            "domain_line",
            "application_bridge",
        ]
    if lesson_mode == "origin_then_example":
        return [
            "domain_line",
            "equation_line",
            "application_bridge",
        ]
    if lesson_mode == "worked_example_tutoring":
        return [
            "equation_line",
            "proof_line",
        ]
    if lesson_mode == "formal_compact_explanation":
        return [
            "proof_line",
            "domain_line",
        ]
    return [
        "domain_line",
        "equation_line",
    ]


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
    lesson_mode = _infer_lesson_mode(request)
    response_arc = _mode_response_arc(lesson_mode)
    include_history, history_mode = _mode_history_strategy(lesson_mode, profile.wants_history)
    network_focus = _mode_network_focus(lesson_mode)
    support_signal_profile, response_settings = build_support_response(profile)

    teaching_pattern = [
        "Start from the learner objective before introducing formal notation.",
        "Check prerequisites explicitly before pushing ahead.",
        pattern_hint,
    ]

    if profile.wants_visuals:
        teaching_pattern.append("Offer a visual or spatial explanation when possible.")
    if profile.confidence == "low":
        teaching_pattern.append("Reduce shame and normalize mistakes as part of learning.")
    if include_history:
        teaching_pattern.append("Include origin stories when they improve intuition.")
    if lesson_mode == "origin_story_explanation":
        teaching_pattern.append("Treat history as the main entry point, not as a side note.")
    if lesson_mode == "worked_example_tutoring":
        teaching_pattern.append("Keep each algebraic move local, explicit, and checkable.")
    if lesson_mode == "origin_then_example":
        teaching_pattern.append("Bridge from historical motivation into the learner's own example.")
    if response_settings.active_supports:
        teaching_pattern.append(
            "Adapt pacing, notation, and scaffolds to the active support profile."
        )
    if "adhd_aware_support" in response_settings.active_supports:
        teaching_pattern.append("Use short blocks, explicit transitions, and fast feedback.")
    if "dyscalculia_aware_support" in response_settings.active_supports:
        teaching_pattern.append("Keep quantity meaning visible before compressing into symbols.")
    if "dyslexia_aware_support" in response_settings.active_supports:
        teaching_pattern.append("Reduce reading burden before concluding a math misunderstanding.")
    if "autism_spectrum_aware_support" in response_settings.active_supports:
        teaching_pattern.append("Keep structure predictable, explicit, and low in sensory clutter.")
    if "language_sensitive_support" in response_settings.active_supports:
        teaching_pattern.append(
            "Bridge everyday language and math vocabulary before compressing into formal terms."
        )

    retrieval_plan = RetrievalPlan(
        concept_depth=concept_depth,
        include_history=include_history,
        history_mode=history_mode,
        include_proof_sketch=include_proof,
        include_modern_applications=True,
        highlight_misconceptions=True,
        network_focus=network_focus,
        required_source_types=[
            "primary_math_source_or_standard_reference",
            "modern_explanatory_source",
            "worked_example_source",
            "historical_network_source",
        ],
    )

    evaluation_focus = [
        "Did the answer choose the right lesson mode for the learner request?",
        "Did the plan align response settings to the learner support profile?",
        "Did the explanation respect prerequisites?",
        "Was the mathematical claim sourceable?",
        "Was the difficulty level appropriate for the learner?",
        "Did the answer leave a useful next step or self-check question?",
    ]

    next_turn_contract = [
        "State assumptions about the learner openly.",
        "Name the central idea before details.",
        "Keep notation load proportional to the learner level.",
        "Keep support adaptations explicit and non-diagnostic.",
        "Cite or reference source families for nontrivial claims.",
    ]

    return TeachingPlan(
        lesson_mode=lesson_mode,
        audience_mode=profile.age_group,
        tone=tone,
        teaching_pattern=teaching_pattern,
        response_arc=response_arc,
        support_signal_profile=support_signal_profile,
        response_settings=response_settings,
        retrieval_plan=retrieval_plan,
        evaluation_focus=evaluation_focus,
        next_turn_contract=next_turn_contract,
    )
