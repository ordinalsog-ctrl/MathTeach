from __future__ import annotations

import re
import shutil
import tempfile
from datetime import UTC, datetime
from pathlib import Path

from pydantic import BaseModel, Field


class SessionQuarantineRecord(BaseModel):
    session_id: str
    reason: str
    detail: str
    original_path: str
    quarantine_path: str
    metadata_path: str
    timestamp: str = Field(
        default_factory=lambda: datetime.now(UTC).isoformat(timespec="seconds")
    )


class SessionQuarantine:
    def __init__(self, base_dir: str | Path | None = None) -> None:
        if base_dir is None:
            self.base_dir = Path(tempfile.gettempdir()) / "mathteach_sessions" / "_quarantine"
        else:
            self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def quarantine_file(
        self,
        session_id: str,
        source_path: str | Path,
        reason: str,
        detail: str,
    ) -> SessionQuarantineRecord | None:
        source = Path(source_path)
        if not source.exists():
            return None

        timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S%fZ")
        reason_slug = re.sub(r"[^A-Za-z0-9._-]+", "-", reason).strip("-") or "quarantine"
        target = self.base_dir / f"{source.stem}-{reason_slug}-{timestamp}{source.suffix}"
        shutil.move(str(source), target)

        metadata_path = target.with_suffix(f"{target.suffix}.meta.json")
        record = SessionQuarantineRecord(
            session_id=session_id,
            reason=reason,
            detail=detail,
            original_path=str(source),
            quarantine_path=str(target),
            metadata_path=str(metadata_path),
        )
        metadata_path.write_text(
            record.model_dump_json(indent=2),
            encoding="utf-8",
        )
        return record

    def list_records(self, session_id: str | None = None) -> list[SessionQuarantineRecord]:
        records = [
            SessionQuarantineRecord.model_validate_json(
                metadata_path.read_text(encoding="utf-8")
            )
            for metadata_path in sorted(self.base_dir.glob("*.meta.json"))
        ]
        if session_id is not None:
            records = [record for record in records if record.session_id == session_id]
        return sorted(records, key=lambda record: record.timestamp, reverse=True)

    def latest_record(self, session_id: str) -> SessionQuarantineRecord | None:
        records = self.list_records(session_id=session_id)
        if not records:
            return None
        return records[0]

    def read_quarantined_text(self, session_id: str) -> tuple[SessionQuarantineRecord, str] | None:
        record = self.latest_record(session_id)
        if record is None:
            return None
        quarantine_path = Path(record.quarantine_path)
        if not quarantine_path.exists():
            return None
        return record, quarantine_path.read_text(encoding="utf-8")

    def restore_latest(
        self,
        session_id: str,
        target_path: str | Path,
    ) -> SessionQuarantineRecord | None:
        record = self.latest_record(session_id)
        if record is None:
            return None
        quarantine_path = Path(record.quarantine_path)
        metadata_path = Path(record.metadata_path)
        if not quarantine_path.exists():
            metadata_path.unlink(missing_ok=True)
            return None

        target = Path(target_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(quarantine_path), target)
        metadata_path.unlink(missing_ok=True)
        return record

    def discard_latest(self, session_id: str) -> SessionQuarantineRecord | None:
        record = self.latest_record(session_id)
        if record is None:
            return None
        Path(record.quarantine_path).unlink(missing_ok=True)
        Path(record.metadata_path).unlink(missing_ok=True)
        return record
