from mathteach.models import LearnerProfile, ModeAdaptationState, RawBlockObservation
from mathteach.services.response_engine import build_support_response
from mathteach.services.runtime_mode_adapter import RuntimeModeAdapter


def test_transition_language_stays_non_technical_for_simplifying_shift() -> None:
    learner = LearnerProfile(
        age_group="teen",
        math_level="middle_school",
        confidence="low",
        preferred_pace="balanced",
        language="de",
        wants_visuals=True,
        wants_history=False,
    )
    signal_profile, _ = build_support_response(learner)
    adapter = RuntimeModeAdapter()
    state = ModeAdaptationState(
        current_mode="origin_then_example",
        blocks_in_current_mode=2,
    )
    observation = RawBlockObservation(
        block_index=2,
        current_mode="origin_then_example",
        evidence=["repeated_concept_error"],
    )

    decision = adapter.check_and_adapt_mode(
        state,
        "origin_then_example",
        observation,
        signal_profile,
    )

    assert decision.transition_message is not None
    assert "Modus" not in decision.transition_message
    assert "worked_example_tutoring" not in decision.transition_message
    assert "kleineren Schritten" in decision.transition_message


def test_transition_language_uses_stretch_template() -> None:
    learner = LearnerProfile(
        age_group="adult",
        math_level="high_school",
        confidence="medium",
        preferred_pace="balanced",
        language="de",
        wants_visuals=True,
        wants_history=True,
    )
    signal_profile, _ = build_support_response(learner)
    adapter = RuntimeModeAdapter()
    state = ModeAdaptationState(
        current_mode="worked_example_tutoring",
        blocks_in_current_mode=2,
    )
    observation = RawBlockObservation(
        block_index=3,
        current_mode="worked_example_tutoring",
        evidence=["pattern_recognized", "transfer_success"],
    )

    decision = adapter.check_and_adapt_mode(
        state,
        "worked_example_tutoring",
        observation,
        signal_profile,
    )

    assert decision.transition_message is not None
    assert "Das klappt schon gut." in decision.transition_message
    assert "mehr Eigenraum" in decision.transition_message
