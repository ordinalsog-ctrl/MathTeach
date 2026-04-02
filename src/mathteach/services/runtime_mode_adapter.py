from mathteach.models import (
    ModeAdaptationDecision,
    ModeAdaptationState,
    ObservationSignal,
    ObservationStrength,
    RawBlockObservation,
    SignalInterpretationResult,
    SupportSignalProfile,
    TransitionFamily,
)


STRENGTH_ORDER: dict[ObservationStrength, int] = {
    "weak": 1,
    "meaningful": 2,
    "strong": 3,
}

DOWNWARD_SHIFT_TARGETS = {
    "origin_then_example": "worked_example_tutoring",
    "guided_concept_explanation": "worked_example_tutoring",
    "formal_compact_explanation": "guided_concept_explanation",
}

UPWARD_SHIFT_TARGETS = {
    "worked_example_tutoring": "guided_concept_explanation",
    "guided_concept_explanation": "origin_then_example",
}

TRANSITION_TEMPLATES: dict[TransitionFamily, tuple[str, str, str]] = {
    "simplifying": (
        "Das ist eine Stelle, an der viele kurz haengen bleiben.",
        "Ich nehme etwas Last raus.",
        "Wir gehen jetzt in kleineren Schritten weiter.",
    ),
    "reframing": (
        "Wir bleiben bei derselben Idee.",
        "Ich erklaere sie dir nur auf einem anderen Weg.",
        "Danach pruefen wir sie wieder an einem Beispiel.",
    ),
    "stretching": (
        "Das klappt schon gut.",
        "Du hast das Muster sicherer im Griff.",
        "Ich gebe dir jetzt etwas mehr Eigenraum.",
    ),
}


def _strength_at_least(
    current: ObservationStrength | None,
    threshold: ObservationStrength,
) -> bool:
    if current is None:
        return False
    return STRENGTH_ORDER[current] >= STRENGTH_ORDER[threshold]


def _raise_strength(strength: ObservationStrength) -> ObservationStrength:
    if strength == "weak":
        return "meaningful"
    if strength == "meaningful":
        return "strong"
    return "strong"


def _lower_strength(strength: ObservationStrength) -> ObservationStrength | None:
    if strength == "strong":
        return "meaningful"
    if strength == "meaningful":
        return "weak"
    return None


class SignalInterpreter:
    def interpret(
        self,
        raw_observation: RawBlockObservation,
        profile: SupportSignalProfile,
    ) -> SignalInterpretationResult:
        evidence = set(raw_observation.evidence)
        support_context = list(profile.active_supports)
        signals: list[ObservationSignal] = []
        notes: list[str] = []

        confusion_strength = self._interpret_confusion(evidence)
        confusion_strength, confusion_notes = self._apply_profile_modifiers(
            "confusion_signal",
            confusion_strength,
            evidence,
            profile,
        )
        if confusion_strength is not None:
            signals.append(
                ObservationSignal(
                    signal_type="confusion_signal",
                    strength=confusion_strength,
                    evidence=sorted(
                        evidence
                        & {
                            "single_concept_error",
                            "repeated_concept_error",
                            "repeated_concept_error_across_blocks",
                            "persistent_same_question",
                            "off_target_response",
                            "reading_load_issue",
                            "vocabulary_request",
                        }
                    ),
                    support_context=support_context,
                    block_index=raw_observation.block_index,
                )
            )
            notes.extend(confusion_notes)

        overload_strength = self._interpret_overload(evidence)
        overload_strength, overload_notes = self._apply_profile_modifiers(
            "overload_signal",
            overload_strength,
            evidence,
            profile,
        )
        if overload_strength is not None:
            signals.append(
                ObservationSignal(
                    signal_type="overload_signal",
                    strength=overload_strength,
                    evidence=sorted(
                        evidence
                        & {
                            "structure_break",
                            "symbol_mix",
                            "text_overload",
                            "answer_abandoned",
                            "context_loss",
                            "overload_persisted_after_simplification",
                        }
                    ),
                    support_context=support_context,
                    block_index=raw_observation.block_index,
                )
            )
            notes.extend(overload_notes)

        stagnation_strength = self._interpret_stagnation(evidence)
        stagnation_strength, stagnation_notes = self._apply_profile_modifiers(
            "stagnation_signal",
            stagnation_strength,
            evidence,
            profile,
        )
        if stagnation_strength is not None:
            signals.append(
                ObservationSignal(
                    signal_type="stagnation_signal",
                    strength=stagnation_strength,
                    evidence=sorted(
                        evidence
                        & {
                            "no_progress_block",
                            "no_progress_two_blocks",
                            "no_progress_three_blocks",
                            "no_success_visible_two_blocks",
                        }
                    ),
                    support_context=support_context,
                    block_index=raw_observation.block_index,
                )
            )
            notes.extend(stagnation_notes)

        breakthrough_strength = self._interpret_breakthrough(evidence)
        breakthrough_strength, breakthrough_notes = self._apply_profile_modifiers(
            "breakthrough_signal",
            breakthrough_strength,
            evidence,
            profile,
        )
        if breakthrough_strength is not None:
            signals.append(
                ObservationSignal(
                    signal_type="breakthrough_signal",
                    strength=breakthrough_strength,
                    evidence=sorted(
                        evidence
                        & {
                            "correct_with_guidance",
                            "pattern_recognized",
                            "reduced_prompting",
                            "transfer_success",
                            "transfer_success_two_blocks",
                        }
                    ),
                    support_context=support_context,
                    block_index=raw_observation.block_index,
                )
            )
            notes.extend(breakthrough_notes)

        confidence_strength = self._interpret_confidence_recovery(evidence)
        confidence_strength, confidence_notes = self._apply_profile_modifiers(
            "confidence_recovery_signal",
            confidence_strength,
            evidence,
            profile,
        )
        if confidence_strength is not None:
            signals.append(
                ObservationSignal(
                    signal_type="confidence_recovery_signal",
                    strength=confidence_strength,
                    evidence=sorted(
                        evidence
                        & {
                            "less_withdrawal_language",
                            "self_correction",
                            "active_continue",
                            "explains_next_step",
                            "visible_small_success",
                        }
                    ),
                    support_context=support_context,
                    block_index=raw_observation.block_index,
                )
            )
            notes.extend(confidence_notes)

        return SignalInterpretationResult(
            raw_observation=raw_observation,
            signals=signals,
            notes=notes,
        )

    def _interpret_confusion(self, evidence: set[str]) -> ObservationStrength | None:
        if "repeated_concept_error_across_blocks" in evidence:
            return "strong"
        if "repeated_concept_error" in evidence or "persistent_same_question" in evidence:
            return "meaningful"
        if "single_concept_error" in evidence or "off_target_response" in evidence:
            return "weak"
        return None

    def _interpret_overload(self, evidence: set[str]) -> ObservationStrength | None:
        if "overload_persisted_after_simplification" in evidence:
            return "strong"
        overload_indicators = len(
            evidence
            & {
                "structure_break",
                "symbol_mix",
                "text_overload",
                "answer_abandoned",
                "context_loss",
            }
        )
        if overload_indicators >= 2:
            return "meaningful"
        if overload_indicators == 1:
            return "weak"
        return None

    def _interpret_stagnation(self, evidence: set[str]) -> ObservationStrength | None:
        if "no_progress_three_blocks" in evidence:
            return "strong"
        if "no_progress_two_blocks" in evidence:
            return "meaningful"
        if "no_progress_block" in evidence:
            return "weak"
        return None

    def _interpret_breakthrough(self, evidence: set[str]) -> ObservationStrength | None:
        if "transfer_success_two_blocks" in evidence or (
            "pattern_recognized" in evidence and "transfer_success" in evidence
        ):
            return "strong"
        if (
            "transfer_success" in evidence
            or ("pattern_recognized" in evidence and "reduced_prompting" in evidence)
        ):
            return "meaningful"
        if "correct_with_guidance" in evidence:
            return "weak"
        return None

    def _interpret_confidence_recovery(
        self,
        evidence: set[str],
    ) -> ObservationStrength | None:
        if "explains_next_step" in evidence and "active_continue" in evidence:
            return "strong"
        if (
            "self_correction" in evidence and "active_continue" in evidence
        ) or (
            "less_withdrawal_language" in evidence and "self_correction" in evidence
        ):
            return "meaningful"
        if evidence & {
            "less_withdrawal_language",
            "self_correction",
            "active_continue",
        }:
            return "weak"
        return None

    def _apply_profile_modifiers(
        self,
        signal_type: str,
        strength: ObservationStrength | None,
        evidence: set[str],
        profile: SupportSignalProfile,
    ) -> tuple[ObservationStrength | None, list[str]]:
        if strength is None:
            return None, []

        notes: list[str] = []
        active_supports = set(profile.active_supports)

        if (
            signal_type == "overload_signal"
            and "adhd_aware_support" in active_supports
            and "context_loss" in evidence
        ):
            strength = _raise_strength(strength)
            notes.append("ADHD-aware weighting raised overload because context loss was visible.")

        if (
            signal_type == "stagnation_signal"
            and "adhd_aware_support" in active_supports
            and evidence == {"slow_response"}
        ):
            lowered = _lower_strength(strength)
            if lowered is None:
                return None, notes + [
                    "ADHD-aware weighting suppressed stagnation from slow response alone."
                ]
            strength = lowered
            notes.append("ADHD-aware weighting softened stagnation from slow response alone.")

        if (
            signal_type == "stagnation_signal"
            and "dyscalculia_aware_support" in active_supports
            and evidence & {"careful_counting", "slow_response"}
            and not evidence
            & {
                "no_progress_two_blocks",
                "no_progress_three_blocks",
            }
        ):
            lowered = _lower_strength(strength)
            if lowered is None:
                return None, notes + [
                    "Dyscalculia-aware weighting suppressed stagnation from careful slow concrete work."
                ]
            strength = lowered
            notes.append("Dyscalculia-aware weighting softened stagnation during careful concrete work.")

        if (
            signal_type == "confusion_signal"
            and "dyslexia_aware_support" in active_supports
            and "reading_load_issue" in evidence
        ):
            lowered = _lower_strength(strength)
            if lowered is None:
                return None, notes + [
                    "Dyslexia-aware weighting suppressed confusion because reading load dominated."
                ]
            strength = lowered
            notes.append("Dyslexia-aware weighting softened confusion because reading load dominated.")

        if (
            signal_type == "overload_signal"
            and "autism_spectrum_aware_support" in active_supports
            and "structure_break" in evidence
        ):
            strength = _raise_strength(strength)
            notes.append("Autism-aware weighting raised overload after a visible structure break.")

        if (
            signal_type == "confusion_signal"
            and "language_sensitive_support" in active_supports
            and "vocabulary_request" in evidence
        ):
            lowered = _lower_strength(strength)
            if lowered is None:
                return None, notes + [
                    "Language-sensitive weighting suppressed confusion because vocabulary load dominated."
                ]
            strength = lowered
            notes.append("Language-sensitive weighting softened confusion because vocabulary load dominated.")

        if (
            signal_type == "stagnation_signal"
            and "scarcity_aware_support" in active_supports
            and "no_success_visible_two_blocks" in evidence
        ):
            strength = _raise_strength(strength)
            notes.append("Scarcity-aware weighting raised stagnation because success stayed invisible.")

        if (
            signal_type == "confidence_recovery_signal"
            and "scarcity_aware_support" in active_supports
            and "visible_small_success" in evidence
        ):
            strength = _raise_strength(strength)
            notes.append(
                "Scarcity-aware weighting raised confidence recovery because a visible small success occurred."
            )

        return strength, notes


class RuntimeModeAdapter:
    def __init__(
        self,
        signal_interpreter: SignalInterpreter | None = None,
        min_blocks_in_mode: int = 2,
        minimum_signal_strength_for_shift: ObservationStrength = "meaningful",
        max_mode_changes_per_session: int = 3,
        cooldown_blocks_after_change: int = 1,
    ) -> None:
        self.signal_interpreter = signal_interpreter or SignalInterpreter()
        self.min_blocks_in_mode = min_blocks_in_mode
        self.minimum_signal_strength_for_shift = minimum_signal_strength_for_shift
        self.max_mode_changes_per_session = max_mode_changes_per_session
        self.cooldown_blocks_after_change = cooldown_blocks_after_change

    def check_and_adapt_mode(
        self,
        state: ModeAdaptationState,
        current_mode: str,
        block_observation: RawBlockObservation,
        profile: SupportSignalProfile,
    ) -> ModeAdaptationDecision:
        interpretation = self.signal_interpreter.interpret(block_observation, profile)
        by_type = {signal.signal_type: signal for signal in interpretation.signals}
        notes = list(interpretation.notes)

        if state.current_mode != current_mode:
            notes.append("Runtime state and current planner mode differed; current planner mode was used.")

        suggested_mode = current_mode
        trigger_signals: list[str] = []
        transition_family: TransitionFamily | None = None

        overload = by_type.get("overload_signal")
        confusion = by_type.get("confusion_signal")
        stagnation = by_type.get("stagnation_signal")
        breakthrough = by_type.get("breakthrough_signal")
        confidence = by_type.get("confidence_recovery_signal")

        if current_mode == "origin_then_example" and (
            _strength_at_least(confusion.strength if confusion else None, "meaningful")
            or _strength_at_least(overload.strength if overload else None, "meaningful")
        ):
            suggested_mode = DOWNWARD_SHIFT_TARGETS[current_mode]
            transition_family = "simplifying"
            trigger_signals = [
                signal.signal_type
                for signal in (confusion, overload)
                if signal is not None
                and _strength_at_least(signal.strength, self.minimum_signal_strength_for_shift)
            ]
        elif current_mode == "guided_concept_explanation" and (
            _strength_at_least(confusion.strength if confusion else None, "meaningful")
            or _strength_at_least(stagnation.strength if stagnation else None, "meaningful")
        ):
            suggested_mode = DOWNWARD_SHIFT_TARGETS[current_mode]
            transition_family = (
                "reframing"
                if _strength_at_least(stagnation.strength if stagnation else None, "meaningful")
                else "simplifying"
            )
            trigger_signals = [
                signal.signal_type
                for signal in (confusion, stagnation)
                if signal is not None
                and _strength_at_least(signal.strength, self.minimum_signal_strength_for_shift)
            ]
        elif current_mode == "formal_compact_explanation" and _strength_at_least(
            overload.strength if overload else None,
            "meaningful",
        ):
            suggested_mode = DOWNWARD_SHIFT_TARGETS[current_mode]
            transition_family = "simplifying"
            trigger_signals = ["overload_signal"]
        elif current_mode == "worked_example_tutoring" and _strength_at_least(
            breakthrough.strength if breakthrough else None,
            "strong",
        ):
            suggested_mode = UPWARD_SHIFT_TARGETS[current_mode]
            transition_family = "stretching"
            trigger_signals = ["breakthrough_signal"]
        elif (
            current_mode == "guided_concept_explanation"
            and _strength_at_least(breakthrough.strength if breakthrough else None, "strong")
            and _strength_at_least(confidence.strength if confidence else None, "strong")
        ):
            suggested_mode = UPWARD_SHIFT_TARGETS[current_mode]
            transition_family = "stretching"
            trigger_signals = [
                "breakthrough_signal",
                "confidence_recovery_signal",
            ]

        if suggested_mode == current_mode:
            notes.append("No supported live mode shift was triggered for this block.")
            return ModeAdaptationDecision(
                selected_mode=current_mode,
                changed=False,
                trigger_signals=[],
                transition_family=None,
                transition_message=None,
                notes=notes,
            )

        if state.cooldown_blocks_remaining > 0:
            notes.append("Mode shift blocked by cooldown.")
            return ModeAdaptationDecision(
                selected_mode=current_mode,
                changed=False,
                trigger_signals=trigger_signals,
                transition_family=None,
                transition_message=None,
                notes=notes,
            )

        if state.blocks_in_current_mode < self.min_blocks_in_mode:
            notes.append("Mode shift blocked because the current mode has not been held long enough.")
            return ModeAdaptationDecision(
                selected_mode=current_mode,
                changed=False,
                trigger_signals=trigger_signals,
                transition_family=None,
                transition_message=None,
                notes=notes,
            )

        if state.mode_changes_in_session >= self.max_mode_changes_per_session:
            notes.append("Mode shift blocked because the session already used its change budget.")
            return ModeAdaptationDecision(
                selected_mode=current_mode,
                changed=False,
                trigger_signals=trigger_signals,
                transition_family=None,
                transition_message=None,
                notes=notes,
            )

        notes.append(f"Mode shift accepted from {current_mode} to {suggested_mode}.")
        return ModeAdaptationDecision(
            selected_mode=suggested_mode,
            changed=True,
            trigger_signals=trigger_signals,
            transition_family=transition_family,
            transition_message=self.build_transition_message(transition_family),
            notes=notes,
        )

    def advance_state(
        self,
        state: ModeAdaptationState,
        decision: ModeAdaptationDecision,
    ) -> ModeAdaptationState:
        if decision.changed:
            return ModeAdaptationState(
                current_mode=decision.selected_mode,
                blocks_in_current_mode=0,
                mode_changes_in_session=state.mode_changes_in_session + 1,
                last_change_reason=", ".join(decision.trigger_signals) or None,
                cooldown_blocks_remaining=self.cooldown_blocks_after_change,
            )

        return ModeAdaptationState(
            current_mode=decision.selected_mode,
            blocks_in_current_mode=state.blocks_in_current_mode + 1,
            mode_changes_in_session=state.mode_changes_in_session,
            last_change_reason=state.last_change_reason,
            cooldown_blocks_remaining=max(state.cooldown_blocks_remaining - 1, 0),
        )

    def build_transition_message(self, family: TransitionFamily | None) -> str | None:
        if family is None:
            return None
        stabilize, reason, next_step = TRANSITION_TEMPLATES[family]
        return " ".join([stabilize, reason, next_step])
