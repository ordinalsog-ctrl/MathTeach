from mathteach.models import ModeAdaptationCheckpoint, ModeAdaptationState, SessionRequest


def test_mode_adaptation_checkpoint_roundtrip_json() -> None:
    checkpoint = ModeAdaptationCheckpoint(
        mode_adaptation_state=ModeAdaptationState(
            current_mode="worked_example_tutoring",
            blocks_in_current_mode=2,
            mode_changes_in_session=1,
            last_change_reason="breakthrough_signal",
            cooldown_blocks_remaining=1,
            pending_transition_message="Wir gehen jetzt in kleineren Schritten weiter.",
            last_observation_evidence=["transfer_success_two_blocks"],
        )
    )

    restored = ModeAdaptationCheckpoint.model_validate_json(checkpoint.model_dump_json())

    assert restored == checkpoint
    assert restored.schema_version == "phase_h1_v1"
    assert restored.mode_adaptation_state.last_observation_evidence == [
        "transfer_success_two_blocks"
    ]


def test_mode_adaptation_checkpoint_partial_json_backfills_defaults() -> None:
    restored = ModeAdaptationCheckpoint.model_validate_json(
        """
        {
          "schema_version": "phase_h1_v1",
          "mode_adaptation_state": {
            "current_mode": "guided_concept_explanation",
            "blocks_in_current_mode": 1,
            "mode_changes_in_session": 0
          }
        }
        """
    )

    assert restored.schema_version == "phase_h1_v1"
    assert restored.mode_adaptation_state.current_mode == "guided_concept_explanation"
    assert restored.mode_adaptation_state.blocks_in_current_mode == 1
    assert restored.mode_adaptation_state.mode_changes_in_session == 0
    assert restored.mode_adaptation_state.last_change_reason is None
    assert restored.mode_adaptation_state.cooldown_blocks_remaining == 0
    assert restored.mode_adaptation_state.pending_transition_message is None
    assert restored.mode_adaptation_state.last_observation_evidence == []


def test_session_request_rejects_state_and_checkpoint_together() -> None:
    try:
        SessionRequest.model_validate(
            {
                "objective": "Erklaere mir die quadratische Gleichung anschaulich.",
                "learner_profile": {
                    "age_group": "teen",
                    "math_level": "high_school",
                    "confidence": "low",
                    "preferred_pace": "balanced",
                    "language": "de",
                    "wants_visuals": True,
                    "wants_history": True,
                },
                "mode_adaptation_state": {
                    "current_mode": "guided_concept_explanation",
                    "blocks_in_current_mode": 1,
                    "mode_changes_in_session": 0,
                },
                "mode_adaptation_checkpoint": {
                    "schema_version": "phase_h1_v1",
                    "mode_adaptation_state": {
                        "current_mode": "guided_concept_explanation",
                        "blocks_in_current_mode": 1,
                        "mode_changes_in_session": 0,
                    },
                },
            }
        )
    except ValueError as exc:
        assert "either mode_adaptation_state or mode_adaptation_checkpoint" in str(exc)
    else:
        raise AssertionError("Expected SessionRequest validation to reject duplicate runtime inputs.")
