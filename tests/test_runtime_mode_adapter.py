from mathteach.models import (
    ModeAdaptationDecision,
    LearnerProfile,
    ModeAdaptationState,
    RawBlockObservation,
)
from mathteach.services.response_engine import build_support_response
from mathteach.services.runtime_mode_adapter import RuntimeModeAdapter


def test_runtime_mode_adapter_simplifies_after_meaningful_confusion() -> None:
    learner = LearnerProfile(
        age_group="teen",
        math_level="middle_school",
        confidence="low",
        preferred_pace="balanced",
        language="de",
        wants_visuals=True,
        wants_history=True,
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

    assert decision.changed is True
    assert decision.selected_mode == "worked_example_tutoring"
    assert decision.transition_family == "simplifying"
    assert "confusion_signal" in decision.trigger_signals


def test_runtime_mode_adapter_blocks_shift_before_minimum_mode_duration() -> None:
    learner = LearnerProfile(
        age_group="teen",
        math_level="middle_school",
        confidence="low",
        preferred_pace="balanced",
        language="de",
        wants_visuals=True,
        wants_history=True,
    )
    signal_profile, _ = build_support_response(learner)
    adapter = RuntimeModeAdapter()
    state = ModeAdaptationState(
        current_mode="origin_then_example",
        blocks_in_current_mode=1,
    )
    observation = RawBlockObservation(
        block_index=1,
        current_mode="origin_then_example",
        evidence=["repeated_concept_error"],
    )

    decision = adapter.check_and_adapt_mode(
        state,
        "origin_then_example",
        observation,
        signal_profile,
    )

    assert decision.changed is False
    assert decision.selected_mode == "origin_then_example"
    assert any("held long enough" in note for note in decision.notes)


def test_runtime_mode_adapter_stretches_after_stable_breakthrough() -> None:
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
        blocks_in_current_mode=3,
    )
    observation = RawBlockObservation(
        block_index=4,
        current_mode="worked_example_tutoring",
        evidence=["pattern_recognized", "transfer_success"],
    )

    decision = adapter.check_and_adapt_mode(
        state,
        "worked_example_tutoring",
        observation,
        signal_profile,
    )

    assert decision.changed is True
    assert decision.selected_mode == "guided_concept_explanation"
    assert decision.transition_family == "stretching"
    assert "breakthrough_signal" in decision.trigger_signals


def test_runtime_mode_adapter_advances_state_and_applies_cooldown() -> None:
    adapter = RuntimeModeAdapter()
    state = ModeAdaptationState(
        current_mode="guided_concept_explanation",
        blocks_in_current_mode=2,
        mode_changes_in_session=1,
    )
    shifted = adapter.advance_state(
        state,
        adapter.check_and_adapt_mode(
            state,
            "guided_concept_explanation",
            RawBlockObservation(
                block_index=3,
                current_mode="guided_concept_explanation",
                evidence=["repeated_concept_error"],
            ),
            build_support_response(
                LearnerProfile(
                    age_group="teen",
                    math_level="middle_school",
                    confidence="low",
                    preferred_pace="balanced",
                    language="de",
                    wants_visuals=True,
                    wants_history=False,
                )
            )[0],
        ),
    )

    assert shifted.current_mode == "worked_example_tutoring"
    assert shifted.blocks_in_current_mode == 0
    assert shifted.mode_changes_in_session == 2
    assert shifted.cooldown_blocks_remaining == 1
    assert shifted.pending_transition_message is not None


def test_runtime_mode_adapter_blocks_shift_when_change_budget_is_exhausted() -> None:
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
        blocks_in_current_mode=3,
        mode_changes_in_session=3,
    )
    observation = RawBlockObservation(
        block_index=4,
        current_mode="origin_then_example",
        evidence=["repeated_concept_error"],
    )

    decision = adapter.check_and_adapt_mode(
        state,
        "origin_then_example",
        observation,
        signal_profile,
    )

    assert decision.changed is False
    assert decision.selected_mode == "origin_then_example"
    assert any("change budget" in note for note in decision.notes)


def test_runtime_mode_adapter_clears_pending_transition_after_consumption() -> None:
    adapter = RuntimeModeAdapter()
    state = ModeAdaptationState(
        current_mode="worked_example_tutoring",
        blocks_in_current_mode=1,
        pending_transition_message=(
            "Das ist eine Stelle, an der viele kurz haengen bleiben. "
            "Ich nehme etwas Last raus. "
            "Wir gehen jetzt in kleineren Schritten weiter."
        ),
    )
    decision = ModeAdaptationDecision(
        selected_mode="worked_example_tutoring",
        changed=False,
    )

    next_state = adapter.advance_state(
        state,
        decision,
        transition_was_consumed=True,
    )

    assert next_state.pending_transition_message is None
