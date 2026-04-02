from dataclasses import dataclass
from itertools import combinations

from mathteach.response_matrix import SupportNeed, TutorResponseSettings


PROFILE_APPLICATION_ORDER: tuple[SupportNeed, ...] = (
    "adhd_aware_support",
    "dyscalculia_aware_support",
    "dyslexia_aware_support",
    "autism_spectrum_aware_support",
    "language_sensitive_support",
    "scarcity_aware_support",
)

PROFILE_COMPATIBILITY: dict[frozenset[SupportNeed], tuple[str, ...]] = {
    frozenset({"adhd_aware_support", "dyscalculia_aware_support"}): (
        "session_duration",
        "break_pattern",
        "worked_example_ratio",
        "fading_speed",
        "primary_representation",
    ),
    frozenset({"adhd_aware_support", "dyslexia_aware_support"}): (),
    frozenset({"adhd_aware_support", "autism_spectrum_aware_support"}): (
        "session_duration",
        "break_pattern",
        "check_frequency",
    ),
    frozenset({"adhd_aware_support", "language_sensitive_support"}): (),
    frozenset({"adhd_aware_support", "scarcity_aware_support"}): (
        "worked_example_ratio",
        "check_frequency",
        "language_support",
    ),
    frozenset({"dyscalculia_aware_support", "dyslexia_aware_support"}): (),
    frozenset({"dyscalculia_aware_support", "autism_spectrum_aware_support"}): (),
    frozenset({"dyscalculia_aware_support", "language_sensitive_support"}): (
        "symbolic_vs_verbal_balance",
        "primary_representation",
        "language_support",
    ),
    frozenset({"dyscalculia_aware_support", "scarcity_aware_support"}): (
        "session_duration",
        "worked_example_ratio",
        "check_frequency",
    ),
    frozenset({"dyslexia_aware_support", "autism_spectrum_aware_support"}): (),
    frozenset({"dyslexia_aware_support", "language_sensitive_support"}): (),
    frozenset({"dyslexia_aware_support", "scarcity_aware_support"}): (),
    frozenset({"autism_spectrum_aware_support", "language_sensitive_support"}): (),
    frozenset({"autism_spectrum_aware_support", "scarcity_aware_support"}): (),
    frozenset({"language_sensitive_support", "scarcity_aware_support"}): (),
}


@dataclass(frozen=True)
class DetectedProfileConflict:
    profiles: tuple[SupportNeed, SupportNeed]
    axes: tuple[str, ...]

    @property
    def slug(self) -> str:
        return f"{self.profiles[0]}__{self.profiles[1]}"


def _merge_unique(existing: list[str], additions: list[str]) -> list[str]:
    merged = list(existing)
    seen = set(existing)
    for item in additions:
        if item not in seen:
            merged.append(item)
            seen.add(item)
    return merged


def ordered_active_supports(active_supports: list[SupportNeed]) -> list[SupportNeed]:
    ordered = [need for need in PROFILE_APPLICATION_ORDER if need in active_supports]
    extras = [need for need in active_supports if need not in ordered]
    return ordered + extras


def detect_profile_conflicts(active_supports: list[SupportNeed]) -> list[DetectedProfileConflict]:
    conflicts: list[DetectedProfileConflict] = []
    ordered = ordered_active_supports(active_supports)
    for left, right in combinations(ordered, 2):
        axes = PROFILE_COMPATIBILITY.get(frozenset({left, right}), ())
        if axes:
            conflicts.append(DetectedProfileConflict(profiles=(left, right), axes=axes))
    return conflicts


def _register_resolution(
    settings: TutorResponseSettings,
    slug: str,
    note: str,
    source_anchors: list[str],
) -> TutorResponseSettings:
    settings.conflict_pairs = _merge_unique(settings.conflict_pairs, [slug])
    settings.conflict_resolution_notes = _merge_unique(
        settings.conflict_resolution_notes, [note]
    )
    settings.rationale_summary = _merge_unique(settings.rationale_summary, [note])
    settings.source_anchors = _merge_unique(settings.source_anchors, source_anchors)
    return settings


def _resolve_adhd_and_dyscalculia(settings: TutorResponseSettings) -> TutorResponseSettings:
    settings.session_duration = "15_to_18_minute_concrete_focus_blocks"
    settings.break_pattern = "ultradian_micro_breaks_within_concrete_work"
    settings.worked_example_ratio = "high_examples_with_varied_contexts"
    settings.fading_speed = "very_gradual_with_novel_variation"
    settings.primary_representation = "manipulative_or_quantity_visual_with_varied_contexts"
    settings.external_scaffolds = _merge_unique(
        settings.external_scaffolds,
        [
            "varied_concrete_materials",
            "ultradian_re_entry_cues",
        ],
    )
    return _register_resolution(
        settings,
        "adhd_aware_support__dyscalculia_aware_support",
        (
            "For ADHD plus dyscalculia, keep the longer concrete path but vary contexts and "
            "insert ultradian regulation breaks."
        ),
        [
            "barkley-executive-functions-adhd",
            "butterworth-varma-laurillard-dyscalculia-science",
        ],
    )


def _resolve_adhd_and_autism(settings: TutorResponseSettings) -> TutorResponseSettings:
    settings.session_duration = "predictable_15_to_18_minute_focus_blocks"
    settings.break_pattern = "predictable_ultradian_regulation_breaks"
    settings.transition_buffer = "explicit_transition_cue_before_every_shift"
    settings.check_frequency = "predictable_checkpoint_rhythm"
    settings.sensory_load_level = "minimal_and_high_contrast"
    settings.external_scaffolds = _merge_unique(
        settings.external_scaffolds,
        [
            "predictable_movement_breaks",
            "stable_visual_layout",
        ],
    )
    return _register_resolution(
        settings,
        "adhd_aware_support__autism_spectrum_aware_support",
        (
            "For ADHD plus autism-spectrum support, preserve predictable structure while keeping "
            "ultradian regulation breaks explicit and low in sensory clutter."
        ),
        [
            "barkley-executive-functions-adhd",
            "rutherford-visual-supports-autism-scoping-review",
        ],
    )


def _resolve_adhd_and_scarcity(settings: TutorResponseSettings) -> TutorResponseSettings:
    settings.worked_example_ratio = "examples_then_quick_success_practice_with_varied_contexts"
    settings.check_frequency = "every_two_problems_with_progress_confirmation"
    settings.language_support = "plain_goal_and_relevance_framing"
    settings.word_budget_per_chunk = "short_clear_chunks_with_immediate_relevance"
    settings.external_scaffolds = _merge_unique(
        settings.external_scaffolds,
        [
            "why_this_matters_now",
            "small_wins_sequence",
            "clear_success_criteria",
        ],
    )
    return _register_resolution(
        settings,
        "adhd_aware_support__scarcity_aware_support",
        (
            "For ADHD plus scarcity-aware support, combine novelty with immediate relevance and "
            "make progress visible after very short cycles."
        ),
        [
            "barkley-executive-functions-adhd",
            "mani-mullainathan-shafir-zhao-poverty-cognition",
            "ryan-deci-self-determination-theory",
        ],
    )


def _resolve_dyscalculia_and_language_sensitive(
    settings: TutorResponseSettings,
) -> TutorResponseSettings:
    settings.symbolic_vs_verbal_balance = (
        "quantity_and_everyday_language_before_symbol_compression"
    )
    settings.primary_representation = "manipulative_or_quantity_visual_with_term_support"
    settings.language_support = "translated_key_terms_glossary_and_quantity_language_support"
    settings.word_budget_per_chunk = "short_chunks_with_controlled_vocabulary"
    settings.external_scaffolds = _merge_unique(
        settings.external_scaffolds,
        [
            "quantity_word_bridge",
            "key_term_glossary",
        ],
    )
    return _register_resolution(
        settings,
        "dyscalculia_aware_support__language_sensitive_support",
        (
            "For dyscalculia plus language-sensitive support, keep quantity meaning visible and "
            "anchor each symbol in everyday mathematical language."
        ),
        [
            "butterworth-varma-laurillard-dyscalculia-science",
            "ies-english-learners-practice-guide",
            "sharma-sharma-multilingual-math-meta-analysis",
        ],
    )


def _resolve_dyscalculia_and_scarcity(settings: TutorResponseSettings) -> TutorResponseSettings:
    settings.session_duration = "18_to_22_minute_concrete_success_blocks"
    settings.worked_example_ratio = "high_examples_with_small_success_cycles"
    settings.check_frequency = "after_each_major_micro_step_with_progress_confirmation"
    settings.transition_buffer = "brief_explicit_transition_with_goal_reminder"
    settings.language_support = "plain_goal_and_relevance_framing"
    settings.external_scaffolds = _merge_unique(
        settings.external_scaffolds,
        [
            "clear_success_criteria",
            "small_wins_sequence",
            "re_entry_summary_after_interruption",
        ],
    )
    return _register_resolution(
        settings,
        "dyscalculia_aware_support__scarcity_aware_support",
        (
            "For dyscalculia plus scarcity-aware support, slow the pace just enough for concrete "
            "understanding while ending each block with visible success."
        ),
        [
            "butterworth-varma-laurillard-dyscalculia-science",
            "mani-mullainathan-shafir-zhao-poverty-cognition",
            "ryan-deci-self-determination-theory",
        ],
    )


def resolve_mixed_profile_settings(
    settings: TutorResponseSettings,
    active_supports: list[SupportNeed],
) -> TutorResponseSettings:
    for conflict in detect_profile_conflicts(active_supports):
        pair = frozenset(conflict.profiles)
        if pair == frozenset({"adhd_aware_support", "dyscalculia_aware_support"}):
            settings = _resolve_adhd_and_dyscalculia(settings)
        elif pair == frozenset({"adhd_aware_support", "autism_spectrum_aware_support"}):
            settings = _resolve_adhd_and_autism(settings)
        elif pair == frozenset({"adhd_aware_support", "scarcity_aware_support"}):
            settings = _resolve_adhd_and_scarcity(settings)
        elif pair == frozenset({"dyscalculia_aware_support", "language_sensitive_support"}):
            settings = _resolve_dyscalculia_and_language_sensitive(settings)
        elif pair == frozenset({"dyscalculia_aware_support", "scarcity_aware_support"}):
            settings = _resolve_dyscalculia_and_scarcity(settings)
    return settings
