from mathteach.models import LearnerProfile, RawBlockObservation
from mathteach.services.response_engine import build_support_response
from mathteach.services.runtime_mode_adapter import SignalInterpreter


def test_signal_interpreter_raises_overload_for_adhd_context_loss() -> None:
    learner = LearnerProfile(
        age_group="teen",
        math_level="middle_school",
        confidence="low",
        preferred_pace="gentle",
        language="de",
        wants_visuals=True,
        wants_history=False,
        declared_support_needs=["adhd_aware_support"],
    )
    signal_profile, _ = build_support_response(learner)
    observation = RawBlockObservation(
        block_index=1,
        current_mode="guided_concept_explanation",
        evidence=["structure_break", "context_loss"],
    )

    result = SignalInterpreter().interpret(observation, signal_profile)
    overload = next(
        signal for signal in result.signals if signal.signal_type == "overload_signal"
    )

    assert overload.strength == "strong"
    assert any("ADHD-aware weighting raised overload" in note for note in result.notes)


def test_signal_interpreter_softens_confusion_for_language_vocabulary_load() -> None:
    learner = LearnerProfile(
        age_group="teen",
        math_level="middle_school",
        confidence="medium",
        preferred_pace="balanced",
        language="en",
        wants_visuals=True,
        wants_history=False,
    )
    signal_profile, _ = build_support_response(learner)
    observation = RawBlockObservation(
        block_index=2,
        current_mode="guided_concept_explanation",
        evidence=["repeated_concept_error", "vocabulary_request"],
    )

    result = SignalInterpreter().interpret(observation, signal_profile)
    confusion = next(
        signal for signal in result.signals if signal.signal_type == "confusion_signal"
    )

    assert confusion.strength == "weak"
    assert any("Language-sensitive weighting softened confusion" in note for note in result.notes)


def test_signal_interpreter_raises_confidence_recovery_for_visible_small_success() -> None:
    learner = LearnerProfile(
        age_group="teen",
        math_level="middle_school",
        confidence="low",
        preferred_pace="balanced",
        language="de",
        wants_visuals=True,
        wants_history=False,
        declared_support_needs=["scarcity_aware_support"],
    )
    signal_profile, _ = build_support_response(learner)
    observation = RawBlockObservation(
        block_index=3,
        current_mode="worked_example_tutoring",
        evidence=["self_correction", "active_continue", "visible_small_success"],
    )

    result = SignalInterpreter().interpret(observation, signal_profile)
    confidence = next(
        signal
        for signal in result.signals
        if signal.signal_type == "confidence_recovery_signal"
    )

    assert confidence.strength == "strong"
    assert any("Scarcity-aware weighting raised confidence recovery" in note for note in result.notes)


def test_signal_interpreter_detects_stagnation_from_missing_success_line() -> None:
    learner = LearnerProfile(
        age_group="teen",
        math_level="middle_school",
        confidence="low",
        preferred_pace="balanced",
        language="de",
        wants_visuals=True,
        wants_history=False,
        declared_support_needs=["scarcity_aware_support"],
    )
    signal_profile, _ = build_support_response(learner)
    observation = RawBlockObservation(
        block_index=4,
        current_mode="guided_concept_explanation",
        evidence=["no_success_visible_two_blocks"],
    )

    result = SignalInterpreter().interpret(observation, signal_profile)
    stagnation = next(
        signal for signal in result.signals if signal.signal_type == "stagnation_signal"
    )

    assert stagnation.strength == "strong"


def test_signal_interpreter_reads_rapid_success_three_blocks_as_breakthrough() -> None:
    learner = LearnerProfile(
        age_group="teen",
        math_level="middle_school",
        confidence="medium",
        preferred_pace="balanced",
        language="de",
        wants_visuals=True,
        wants_history=False,
    )
    signal_profile, _ = build_support_response(learner)
    observation = RawBlockObservation(
        block_index=5,
        current_mode="worked_example_tutoring",
        evidence=["rapid_success_three_blocks", "transfer_success"],
    )

    result = SignalInterpreter().interpret(observation, signal_profile)
    breakthrough = next(
        signal for signal in result.signals if signal.signal_type == "breakthrough_signal"
    )

    assert breakthrough.strength == "strong"
    assert "rapid_success_three_blocks" in breakthrough.evidence


def test_signal_interpreter_reads_error_recovery_with_hint_as_confidence_recovery() -> None:
    learner = LearnerProfile(
        age_group="teen",
        math_level="middle_school",
        confidence="low",
        preferred_pace="balanced",
        language="de",
        wants_visuals=True,
        wants_history=False,
        declared_support_needs=["adhd_aware_support"],
    )
    signal_profile, _ = build_support_response(learner)
    observation = RawBlockObservation(
        block_index=6,
        current_mode="guided_concept_explanation",
        evidence=["error_recovery_with_hint", "self_correction"],
    )

    result = SignalInterpreter().interpret(observation, signal_profile)
    confidence = next(
        signal
        for signal in result.signals
        if signal.signal_type == "confidence_recovery_signal"
    )

    assert confidence.strength == "meaningful"
    assert "error_recovery_with_hint" in confidence.evidence


def test_signal_interpreter_reads_repeated_attempt_three_plus_as_strong_confusion() -> None:
    learner = LearnerProfile(
        age_group="teen",
        math_level="middle_school",
        confidence="low",
        preferred_pace="balanced",
        language="de",
        wants_visuals=True,
        wants_history=False,
        declared_support_needs=["dyscalculia_aware_support"],
    )
    signal_profile, _ = build_support_response(learner)
    observation = RawBlockObservation(
        block_index=7,
        current_mode="guided_concept_explanation",
        evidence=["repeated_attempt_three_plus"],
    )

    result = SignalInterpreter().interpret(observation, signal_profile)
    confusion = next(
        signal for signal in result.signals if signal.signal_type == "confusion_signal"
    )

    assert confusion.strength == "strong"
    assert "repeated_attempt_three_plus" in confusion.evidence
