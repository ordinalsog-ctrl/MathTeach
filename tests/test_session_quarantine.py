from pathlib import Path

from mathteach.services.session_quarantine import SessionQuarantine


def test_session_quarantine_moves_file_and_writes_metadata(tmp_path) -> None:
    source = tmp_path / "store" / "session.json"
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_text('{"schema_version":"phase_h1_v1"}', encoding="utf-8")
    quarantine = SessionQuarantine(tmp_path / "quarantine")

    record = quarantine.quarantine_file(
        session_id="session-1",
        source_path=source,
        reason="invalid-checkpoint",
        detail="Checkpoint could not be resumed.",
    )

    assert record is not None
    assert not source.exists()
    assert Path(record.quarantine_path).exists()
    assert Path(record.metadata_path).exists()
