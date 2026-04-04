from __future__ import annotations

import hashlib
import re
import tempfile
from pathlib import Path

from mathteach.models import ModeAdaptationCheckpoint


class SessionStore:
    def __init__(self, base_dir: str | Path | None = None) -> None:
        if base_dir is None:
            self.base_dir = Path(tempfile.gettempdir()) / "mathteach_sessions"
        else:
            self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def save_checkpoint(
        self,
        session_id: str,
        checkpoint: ModeAdaptationCheckpoint,
    ) -> None:
        session_path = self._session_path(session_id)
        session_path.write_text(
            checkpoint.model_dump_json(indent=2),
            encoding="utf-8",
        )

    def load_checkpoint(
        self,
        session_id: str,
    ) -> ModeAdaptationCheckpoint | None:
        session_path = self._session_path(session_id)
        if not session_path.exists():
            return None
        return ModeAdaptationCheckpoint.model_validate_json(
            session_path.read_text(encoding="utf-8")
        )

    def delete_checkpoint(self, session_id: str) -> None:
        session_path = self._session_path(session_id)
        session_path.unlink(missing_ok=True)

    def _session_path(self, session_id: str) -> Path:
        normalized = self._normalize_session_id(session_id)
        readable_prefix = re.sub(r"[^A-Za-z0-9._-]+", "_", normalized).strip("._-")
        if not readable_prefix:
            readable_prefix = "session"
        digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:16]
        return self.base_dir / f"{readable_prefix[:40]}-{digest}.json"

    def _normalize_session_id(self, session_id: str) -> str:
        normalized = session_id.strip()
        if not normalized:
            raise ValueError("session_id must not be empty.")
        return normalized
