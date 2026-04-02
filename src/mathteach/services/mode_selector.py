from mathteach.models import LearnerProfile, ModeSelection
from mathteach.response_matrix import SupportSignalProfile, TutorResponseSettings


def _merge_unique(existing: list[str], additions: list[str]) -> list[str]:
    merged = list(existing)
    seen = set(existing)
    for item in additions:
        if item not in seen:
            merged.append(item)
            seen.add(item)
    return merged


def select_mode(
    requested_mode: str,
    profile: LearnerProfile,
    signal_profile: SupportSignalProfile,
    response_settings: TutorResponseSettings,
) -> ModeSelection:
    selected_mode = requested_mode
    rationale: list[str] = []
    constraints: list[str] = []

    triads = set(response_settings.triad_groups)
    conflicts = set(response_settings.conflict_pairs)
    active_supports = set(response_settings.active_supports)

    if (
        "adhd_aware_support__dyscalculia_aware_support__scarcity_aware_support"
        in triads
    ):
        selected_mode = "worked_example_tutoring"
        rationale = _merge_unique(
            rationale,
            [
                "This triad needs concrete worked structure before any larger narrative ramp-up.",
                "Visible progress and short regulated blocks matter more here than a long origin lead-in.",
            ],
        )
        constraints = _merge_unique(
            constraints,
            [
                "immediate_relevance_signal",
                "high_visual_and_concrete_support",
                "low_notation_density",
                "micro_success_cycles",
            ],
        )
    elif (
        "adhd_aware_support__autism_spectrum_aware_support__scarcity_aware_support"
        in triads
    ):
        selected_mode = "worked_example_tutoring"
        rationale = _merge_unique(
            rationale,
            [
                "Predictable structured examples are safer here than a mode with longer open-ended setup.",
                "Relevance must stay visible, but inside a stable low-clutter session format.",
            ],
        )
        constraints = _merge_unique(
            constraints,
            [
                "high_structure",
                "minimal_mode_switching",
                "predictable_checkpoint_structure",
                "immediate_relevance_signal",
            ],
        )
    elif (
        "dyscalculia_aware_support__language_sensitive_support__scarcity_aware_support"
        in triads
    ):
        selected_mode = "origin_then_example"
        rationale = _merge_unique(
            rationale,
            [
                "This triad benefits from a short meaning bridge before the worked example starts.",
                "Language and quantity grounding need a brief origin-style opening, but not a long pure history block.",
            ],
        )
        constraints = _merge_unique(
            constraints,
            [
                "short_origin_bridge",
                "visual_heavy",
                "term_support_first",
                "quantity_before_symbols",
            ],
        )
    elif "adhd_aware_support__scarcity_aware_support" in conflicts:
        if requested_mode == "origin_story_explanation":
            selected_mode = "origin_then_example"
        else:
            selected_mode = "worked_example_tutoring"
        rationale = _merge_unique(
            rationale,
            [
                "ADHD plus scarcity support needs fast traction, so long setup should collapse into short relevance plus action.",
            ],
        )
        constraints = _merge_unique(
            constraints,
            [
                "micro_origin_bridge",
                "immediate_relevance_signal",
                "micro_success_cycles",
            ],
        )
    elif "adhd_aware_support__dyscalculia_aware_support" in conflicts:
        selected_mode = "worked_example_tutoring"
        rationale = _merge_unique(
            rationale,
            [
                "ADHD plus dyscalculia benefits most from explicit worked structure with concrete variation.",
            ],
        )
        constraints = _merge_unique(
            constraints,
            [
                "high_visual_and_concrete_support",
                "low_notation_density",
            ],
        )
    elif "dyscalculia_aware_support__language_sensitive_support" in conflicts:
        selected_mode = "origin_then_example"
        rationale = _merge_unique(
            rationale,
            [
                "A short meaning bridge helps this pair before symbols and text density rise.",
            ],
        )
        constraints = _merge_unique(
            constraints,
            [
                "short_origin_bridge",
                "term_support_first",
                "quantity_before_symbols",
            ],
        )

    if (
        selected_mode == "origin_story_explanation"
        and active_supports
        & {
            "adhd_aware_support",
            "autism_spectrum_aware_support",
            "scarcity_aware_support",
        }
    ):
        selected_mode = "origin_then_example"
        rationale = _merge_unique(
            rationale,
            [
                "A pure origin-first mode is too costly here; keep the origin signal, but shorten it and move to action sooner.",
            ],
        )
        constraints = _merge_unique(constraints, ["short_origin_bridge"])

    if (
        selected_mode == "formal_compact_explanation"
        and profile.math_level != "research"
        and response_settings.active_supports
    ):
        selected_mode = "guided_concept_explanation"
        rationale = _merge_unique(
            rationale,
            [
                "Support-heavy sessions below research level should avoid a compact formal-first mode.",
            ],
        )
        constraints = _merge_unique(constraints, ["support_before_formal_compaction"])

    if not rationale:
        rationale = [
            "No mixed-profile mode override was needed; keep the requested tutoring mode."
        ]
    if not constraints and signal_profile.active_supports:
        constraints = ["keep_mode_consistent_with_active_support_profile"]

    return ModeSelection(
        requested_mode=requested_mode,
        selected_mode=selected_mode,
        rationale=rationale,
        constraints=constraints,
    )
