from mathteach.models import ModeAdaptationCheckpoint, ModeAdaptationState
from mathteach.services.session_store import SessionStore


def test_session_store_saves_and_loads_checkpoint_identically(tmp_path) -> None:
    store = SessionStore(tmp_path)
    checkpoint = ModeAdaptationCheckpoint(
        mode_adaptation_state=ModeAdaptationState(
            current_mode="worked_example_tutoring",
            blocks_in_current_mode=2,
            mode_changes_in_session=1,
            cooldown_blocks_remaining=1,
            pending_transition_message="Wir gehen jetzt in kleineren Schritten weiter.",
            last_observation_evidence=["transfer_success_two_blocks"],
        )
    )

    store.save_checkpoint("session-alpha", checkpoint)
    restored = store.load_checkpoint("session-alpha")

    assert restored == checkpoint


def test_session_store_returns_none_for_unknown_session_id(tmp_path) -> None:
    store = SessionStore(tmp_path)

    assert store.load_checkpoint("unknown-session") is None


def test_session_store_persists_pending_transition_and_cooldown(tmp_path) -> None:
    store = SessionStore(tmp_path)
    checkpoint = ModeAdaptationCheckpoint(
        mode_adaptation_state=ModeAdaptationState(
            current_mode="guided_concept_explanation",
            blocks_in_current_mode=0,
            mode_changes_in_session=2,
            cooldown_blocks_remaining=1,
            pending_transition_message=(
                "Das ist eine Stelle, an der viele kurz haengen bleiben. "
                "Ich nehme etwas Last raus. "
                "Wir gehen jetzt in kleineren Schritten weiter."
            ),
            last_observation_evidence=["no_progress_three_blocks"],
        )
    )

    store.save_checkpoint("session-beta", checkpoint)
    restored = store.load_checkpoint("session-beta")

    assert restored is not None
    assert restored.mode_adaptation_state.cooldown_blocks_remaining == 1
    assert restored.mode_adaptation_state.pending_transition_message is not None
    assert restored.mode_adaptation_state.last_observation_evidence == [
        "no_progress_three_blocks"
    ]


def test_session_store_loads_partial_checkpoint_with_defaults(tmp_path) -> None:
    store = SessionStore(tmp_path)
    store.session_path("session-gamma").write_text(
        '{\n'
        '  "schema_version": "phase_h1_v1",\n'
        '  "mode_adaptation_state": {\n'
        '    "current_mode": "guided_concept_explanation",\n'
        '    "blocks_in_current_mode": 1,\n'
        '    "mode_changes_in_session": 0\n'
        "  }\n"
        "}\n",
        encoding="utf-8",
    )

    restored = store.load_checkpoint("session-gamma")

    assert restored is not None
    assert restored.mode_adaptation_state.cooldown_blocks_remaining == 0
    assert restored.mode_adaptation_state.pending_transition_message is None
    assert restored.mode_adaptation_state.last_observation_evidence == []
