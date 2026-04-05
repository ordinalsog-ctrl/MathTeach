from __future__ import annotations

from datetime import UTC, datetime
from statistics import fmean

from mathteach.models import (
    BlockType,
    CalibrationWeightsSnapshot,
    DecisionRecord,
    EnrichedPathEvaluation,
    EvidenceCombinationPattern,
    OutcomeMetrics,
    RawBlockObservation,
)
from mathteach.services.calibration_store import CalibrationData, CalibrationStore
from mathteach.services.evidence_pattern_detector import build_evidence_combination


def _estimate_mastery_gain(
    observation: RawBlockObservation,
    evidence_patterns: list[EvidenceCombinationPattern],
) -> float:
    evidence = set(observation.evidence)
    mastery_gain = 0.12

    if evidence & {"rapid_success_two_blocks", "rapid_success_three_blocks", "transfer_success"}:
        mastery_gain += 0.18
    if evidence & {"visible_small_success", "error_recovery_with_hint"}:
        mastery_gain += 0.08
    if evidence & {"repeated_concept_error", "repeated_attempt_three_plus", "text_overload"}:
        mastery_gain -= 0.1
    if EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS in evidence_patterns:
        mastery_gain += 0.1
    if EvidenceCombinationPattern.STAGNATION_PATTERN in evidence_patterns:
        mastery_gain -= 0.08
    if EvidenceCombinationPattern.CONCEPT_CONFUSION in evidence_patterns:
        mastery_gain -= 0.06

    return max(0.0, min(1.0, mastery_gain))


def _infer_error_rate_trend(
    observation: RawBlockObservation,
    evidence_patterns: list[EvidenceCombinationPattern],
) -> str:
    evidence = set(observation.evidence)
    if evidence & {
        "repeated_concept_error",
        "repeated_attempt_three_plus",
        "no_progress_two_blocks",
        "no_progress_three_blocks",
    } or EvidenceCombinationPattern.STAGNATION_PATTERN in evidence_patterns:
        return "degrading"
    if evidence & {
        "rapid_success_two_blocks",
        "rapid_success_three_blocks",
        "visible_small_success",
        "transfer_success",
    } or EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS in evidence_patterns:
        return "improving"
    return "stable"


def _infer_accuracy_estimate(
    observation: RawBlockObservation,
    evidence_patterns: list[EvidenceCombinationPattern],
) -> float | None:
    if observation.accuracy_estimate is not None:
        return observation.accuracy_estimate

    evidence = set(observation.evidence)
    if evidence & {"rapid_success_three_blocks", "transfer_success"}:
        return 0.88
    if evidence & {"visible_small_success", "error_recovery_with_hint"}:
        return 0.7
    if evidence & {"repeated_concept_error", "repeated_attempt_three_plus"}:
        return 0.4
    if EvidenceCombinationPattern.VOCABULARY_GAP in evidence_patterns:
        return 0.58
    return 0.6


def infer_outcome_metrics(
    observation: RawBlockObservation,
    confidence_change: float = 0.0,
    engagement_estimate: str | None = None,
) -> OutcomeMetrics:
    evidence_combination = build_evidence_combination(
        current_evidence=observation.evidence,
        block_type=BlockType.REFLECTION,
        block_sequence=max(1, observation.block_index),
        previous_evidence=[],
    )
    inferred_engagement = (
        engagement_estimate
        or observation.engagement_estimate
        or (
            "high"
            if set(observation.evidence)
            & {"rapid_success_two_blocks", "rapid_success_three_blocks", "transfer_success"}
            else "low"
            if set(observation.evidence)
            & {"no_progress_two_blocks", "no_progress_three_blocks", "no_success_visible_two_blocks"}
            else "medium"
        )
    )

    return OutcomeMetrics(
        observed_evidence=observation.evidence,
        observed_evidence_patterns=evidence_combination.patterns,
        duration_seconds=observation.duration_seconds,
        accuracy_estimate=_infer_accuracy_estimate(observation, evidence_combination.patterns),
        confidence_change=confidence_change,
        mastery_gain_estimate=_estimate_mastery_gain(observation, evidence_combination.patterns),
        error_rate_trend=_infer_error_rate_trend(observation, evidence_combination.patterns),
        observed_engagement=inferred_engagement,
    )


class CalibrationEngine:
    def __init__(
        self,
        min_samples_for_calibration: int = 8,
        store: CalibrationStore | None = None,
        autosave_threshold: int = 10,
    ):
        self.min_samples_for_calibration = min_samples_for_calibration
        self.store = store
        self.autosave_threshold = max(1, autosave_threshold)
        self._pending_updates = 0

        data = self.store.load() if self.store is not None else CalibrationData()
        self.decision_log: list[DecisionRecord] = list(data.decision_records)
        self.outcome_metrics: list[OutcomeMetrics] = list(data.outcome_metrics)
        self.current_weights = data.calibration_weights
        self.weights_history: list[CalibrationWeightsSnapshot] = list(data.weights_history)

    def _snapshot(self) -> CalibrationData:
        return CalibrationData(
            decision_records=self.decision_log,
            outcome_metrics=self.outcome_metrics,
            calibration_weights=self.current_weights,
            weights_history=self.weights_history,
            last_updated=datetime.now(UTC),
        )

    @property
    def store_path(self) -> str | None:
        return str(self.store.storage_path) if self.store is not None else None

    def get_recent_success_rate(self, limit: int = 20) -> float | None:
        recent = [outcome.composite_score() for outcome in self.outcome_metrics[-limit:]]
        if not recent:
            return None
        return max(0.0, min(1.0, sum(recent) / len(recent)))

    def get_weight_stability_index(self) -> float | None:
        if len(self.weights_history) < 2:
            return None
        latest = self.weights_history[-1].active_weights
        previous = self.weights_history[-2].active_weights
        total_shift = sum(
            abs(latest.get(key, 0.0) - previous.get(key, 0.0))
            for key in set(latest) | set(previous)
        )
        return max(0.0, min(1.0, 1.0 - total_shift))

    def get_statistics(self) -> dict[str, object]:
        return {
            "total_decisions": len(self.decision_log),
            "total_outcomes": len(self.outcome_metrics),
            "calibration_rounds": self.current_weights.calibration_rounds,
            "weights_history_length": len(self.weights_history),
            "recent_success_rate": self.get_recent_success_rate() or 0.0,
            "weight_stability_index": self.get_weight_stability_index() or 1.0,
            "store_path": self.store_path,
            "last_calibration": (
                self.current_weights.last_calibration.isoformat()
                if self.current_weights.last_calibration is not None
                else None
            ),
        }

    def _mark_dirty(self) -> None:
        self._pending_updates += 1
        if self.store is not None and self._pending_updates >= self.autosave_threshold:
            self.force_save()

    def force_save(self) -> None:
        if self.store is None:
            return
        self.store.save(self._snapshot())
        self._pending_updates = 0

    def log_decision(self, record: DecisionRecord) -> DecisionRecord:
        self.decision_log.append(record)
        self._mark_dirty()
        return record

    def update_outcome(self, decision_id: str, outcome: OutcomeMetrics) -> bool:
        updated = False
        for index, record in enumerate(self.decision_log):
            if record.decision_id != decision_id:
                continue
            self.decision_log[index] = record.model_copy(
                update={
                    "observed_outcome": outcome,
                    "outcome_timestamp": datetime.now(UTC),
                }
            )
            updated = True
            break

        if updated:
            self.outcome_metrics.append(outcome)
            self._attempt_calibration()
            self._mark_dirty()
        return updated

    def get_calibrated_score(self, score_breakdown: dict[str, float]) -> float:
        weights = self.current_weights.get_current_weights()
        score = 0.0
        for component, weight in weights.items():
            score += score_breakdown.get(component, 0.0) * weight
        return max(0.0, min(1.0, score))

    def apply_to_enriched_paths(
        self,
        enriched_paths: list[EnrichedPathEvaluation],
    ) -> list[EnrichedPathEvaluation]:
        calibrated_paths: list[EnrichedPathEvaluation] = []

        for path in enriched_paths:
            calibrated_score = self.get_calibrated_score(path.score_breakdown)
            calibrated_paths.append(
                path.model_copy(
                    update={
                        "uncalibrated_total_score": path.total_score,
                        "total_score": calibrated_score,
                        "calibration_applied": True,
                        "score_breakdown": {
                            **path.score_breakdown,
                            "calibrated_total": round(calibrated_score, 4),
                            "uncalibrated_total": round(path.total_score, 4),
                        },
                    }
                )
            )

        calibrated_paths.sort(key=lambda item: item.total_score, reverse=True)
        return calibrated_paths

    def _compute_outcome_score(self, outcome: OutcomeMetrics) -> float:
        return outcome.composite_score()

    def _attempt_calibration(self) -> dict[str, float] | None:
        eligible_records = [
            record
            for record in self.decision_log
            if record.observed_outcome is not None and not record.used_for_calibration
        ]
        if len(eligible_records) < self.min_samples_for_calibration:
            return None

        baseline = self.current_weights.baseline_weights
        raw_strengths: dict[str, float] = {}

        for component, default_weight in baseline.items():
            component_scores = [
                record.chosen_path_score_breakdown.get(component, 0.0)
                * self._compute_outcome_score(record.observed_outcome)
                for record in eligible_records
                if record.observed_outcome is not None
            ]
            strength = fmean(component_scores) if component_scores else default_weight
            raw_strengths[component] = max(0.001, strength)

        total_strength = sum(raw_strengths.values())
        adjusted_weights = {
            component: value / total_strength
            for component, value in raw_strengths.items()
        }

        mse = fmean(
            (
                self.get_calibrated_score(record.chosen_path_score_breakdown)
                - self._compute_outcome_score(record.observed_outcome)
            )
            ** 2
            for record in eligible_records
            if record.observed_outcome is not None
        )

        self.current_weights = self.current_weights.model_copy(
            update={
                "adjusted_weights": adjusted_weights,
                "calibration_rounds": self.current_weights.calibration_rounds + 1,
                "last_calibration": datetime.now(UTC),
                "mean_squared_error_history": [
                    *self.current_weights.mean_squared_error_history,
                    mse,
                ],
            }
        )
        trigger_record = max(
            eligible_records,
            key=lambda record: self._compute_outcome_score(record.observed_outcome),
        )
        self.weights_history.append(
            CalibrationWeightsSnapshot(
                timestamp=datetime.now(UTC),
                active_weights=self.current_weights.get_current_weights(),
                trigger_decision_id=trigger_record.decision_id,
                outcome_score=self._compute_outcome_score(trigger_record.observed_outcome),
                adjustment_reason="Outcome-driven calibration round completed.",
            )
        )

        updated_records: list[DecisionRecord] = []
        eligible_ids = {record.decision_id for record in eligible_records}
        for record in self.decision_log:
            if record.decision_id in eligible_ids:
                updated_records.append(
                    record.model_copy(
                        update={
                            "used_for_calibration": True,
                            "calibration_weight_updates": adjusted_weights,
                        }
                    )
                )
            else:
                updated_records.append(record)
        self.decision_log = updated_records
        return adjusted_weights
