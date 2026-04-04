from __future__ import annotations

import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field


AuditEventType = Literal[
    "checkpoint_migrated",
    "checkpoint_invalid",
    "checkpoint_migration_failed",
    "checkpoint_restored",
    "checkpoint_discarded",
]


class SessionAuditEvent(BaseModel):
    event_type: AuditEventType
    session_id: str
    detail: str
    timestamp: str = Field(
        default_factory=lambda: datetime.now(UTC).isoformat(timespec="seconds")
    )
    source_version: str | None = None
    target_version: str | None = None
    quarantine_path: str | None = None


class SessionAuditLogger:
    def __init__(self, log_path: str | Path | None = None) -> None:
        if log_path is None:
            base_dir = Path(tempfile.gettempdir()) / "mathteach_sessions" / "_audit"
            self.log_path = base_dir / "session_audit.jsonl"
        else:
            self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def record(self, event: SessionAuditEvent) -> None:
        with self.log_path.open("a", encoding="utf-8") as handle:
            handle.write(event.model_dump_json())
            handle.write("\n")

    def read_events(self, session_id: str | None = None) -> list[SessionAuditEvent]:
        if not self.log_path.exists():
            return []
        events = [
            SessionAuditEvent.model_validate_json(line)
            for line in self.log_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        if session_id is None:
            return events
        return [event for event in events if event.session_id == session_id]
