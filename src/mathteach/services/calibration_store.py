from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from threading import RLock
from typing import Any

from pydantic import BaseModel, Field

from mathteach.models import (
    CalibrationProfile,
    CalibrationWeights,
    CalibrationWeightsSnapshot,
    DecisionRecord,
    OutcomeMetrics,
)


class CalibrationData(BaseModel):
    decision_records: list[DecisionRecord] = Field(default_factory=list)
    outcome_metrics: list[OutcomeMetrics] = Field(default_factory=list)
    calibration_weights: CalibrationWeights = Field(default_factory=CalibrationWeights)
    weights_history: list[CalibrationWeightsSnapshot] = Field(default_factory=list)
    calibration_profiles: dict[str, CalibrationProfile] = Field(default_factory=dict)
    last_updated: datetime = Field(default_factory=lambda: datetime.now(UTC))


class CalibrationStore:
    def __init__(self, storage_path: Path | str):
        self.storage_path = Path(storage_path)
        self.lock = RLock()

    def load(self) -> CalibrationData:
        if not self.storage_path.exists():
            return CalibrationData()

        with self.lock:
            payload = json.loads(self.storage_path.read_text(encoding="utf-8"))
            return CalibrationData.model_validate(payload)

    def save(self, data: CalibrationData) -> None:
        with self.lock:
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            temp_path = self.storage_path.with_suffix(f"{self.storage_path.suffix}.tmp")
            serializable = data.model_copy(
                update={"last_updated": datetime.now(UTC)}
            ).model_dump(mode="json")
            temp_path.write_text(
                json.dumps(serializable, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
            temp_path.replace(self.storage_path)

    def get_statistics(self) -> dict[str, Any]:
        data = self.load()
        completed_outcomes = [
            outcome.composite_score() for outcome in data.outcome_metrics[-20:]
        ]
        stability_index = 1.0
        if len(data.weights_history) >= 2:
            latest = data.weights_history[-1].active_weights
            previous = data.weights_history[-2].active_weights
            total_shift = sum(
                abs(latest.get(key, 0.0) - previous.get(key, 0.0))
                for key in set(latest) | set(previous)
            )
            stability_index = max(0.0, min(1.0, 1.0 - total_shift))

        return {
            "total_decisions": len(data.decision_records),
            "total_outcomes": len(data.outcome_metrics),
            "calibration_rounds": data.calibration_weights.calibration_rounds,
            "weights_history_length": len(data.weights_history),
            "profile_count": len(data.calibration_profiles),
            "last_updated": data.last_updated.isoformat(),
            "recent_success_rate": (
                round(sum(completed_outcomes) / len(completed_outcomes), 4)
                if completed_outcomes
                else 0.0
            ),
            "weight_stability_index": round(stability_index, 4),
            "store_path": str(self.storage_path),
        }

    def get_profile(self, profile_id: str) -> CalibrationProfile | None:
        data = self.load()
        return data.calibration_profiles.get(profile_id)

    def list_profiles(self) -> list[CalibrationProfile]:
        data = self.load()
        return sorted(
            data.calibration_profiles.values(),
            key=lambda profile: (
                profile.outcome_count,
                profile.sample_size,
                profile.profile_id,
            ),
            reverse=True,
        )
