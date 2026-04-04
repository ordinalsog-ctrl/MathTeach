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
