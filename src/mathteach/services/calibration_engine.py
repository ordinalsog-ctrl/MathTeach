from __future__ import annotations

from datetime import UTC, datetime
from statistics import fmean

from mathteach.models import (
    BlockType,
    CalibrationWeights,
    DecisionRecord,
    EnrichedPathEvaluation,
    EvidenceCombinationPattern,
    OutcomeMetrics,
    RawBlockObservation,
)
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
    def __init__(self, min_samples_for_calibration: int = 8):
        self.min_samples_for_calibration = min_samples_for_calibration
        self.decision_log: list[DecisionRecord] = []
        self.current_weights = CalibrationWeights()

    def log_decision(self, record: DecisionRecord) -> DecisionRecord:
        self.decision_log.append(record)
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
            self._attempt_calibration()
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
        score = 0.0
        score += outcome.mastery_gain_estimate * 0.45

        if outcome.error_rate_trend == "improving":
            score += 0.2
        elif outcome.error_rate_trend == "stable":
            score += 0.1

        if outcome.observed_engagement == "high":
            score += 0.2
        elif outcome.observed_engagement == "medium":
            score += 0.1

        if outcome.accuracy_estimate is not None:
            score += outcome.accuracy_estimate * 0.1

        score += max(0.0, min(0.05, outcome.confidence_change))
        return max(0.0, min(1.0, score))

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
