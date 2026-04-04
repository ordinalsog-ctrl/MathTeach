from mathteach.services.session_audit import SessionAuditEvent, SessionAuditLogger


def test_session_audit_logger_records_and_reads_events(tmp_path) -> None:
    logger = SessionAuditLogger(tmp_path / "audit" / "events.jsonl")
    event = SessionAuditEvent(
        event_type="checkpoint_migrated",
        session_id="session-1",
        detail="Checkpoint migrated successfully.",
        source_version="phase_h0_v1",
        target_version="phase_h1_v1",
    )

    logger.record(event)
    restored = logger.read_events()

    assert restored == [event]
