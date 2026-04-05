from __future__ import annotations

from datetime import UTC, datetime
from statistics import fmean

from mathteach.models import (
    BlockSequenceIntent,
    BlockType,
    CalibrationProfile,
    CalibrationWeightsSnapshot,
    DecisionRecord,
    EnrichedPathEvaluation,
    EvidenceCombinationPattern,
    OutcomeMetrics,
    RawBlockObservation,
)
from mathteach.response_matrix import SupportNeed
from mathteach.services.calibration_store import CalibrationData, CalibrationStore
from mathteach.services.evidence_pattern_detector import build_evidence_combination

GLOBAL_CALIBRATION_PROFILE_ID = "global"
PROFILE_PARTIAL_INHERITANCE_THRESHOLD = 10
PROFILE_FULL_INDEPENDENCE_THRESHOLD = 50
PROFILE_MIN_OUTCOMES_FOR_CALIBRATION = 3


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


def _sorted_support_key(active_supports: list[SupportNeed] | None) -> str | None:
    if not active_supports:
        return None
    return "+".join(sorted(active_supports))


def _dominant_evidence_key(
    evidence_patterns: list[EvidenceCombinationPattern] | None,
) -> str | None:
    if not evidence_patterns:
        return None
    return evidence_patterns[0].value


def _profile_id_from_dimensions(dimensions: dict[str, str]) -> str:
    parts = [
        f"{key}__{value}"
        for key, value in sorted(dimensions.items())
        if value
    ]
    return "__".join(parts) if parts else GLOBAL_CALIBRATION_PROFILE_ID


def _ordered_profile_dimensions(
    active_supports: list[SupportNeed] | None = None,
    sequence_intent: BlockSequenceIntent | None = None,
    evidence_patterns: list[EvidenceCombinationPattern] | None = None,
    current_block_type: BlockType | None = None,
) -> list[dict[str, str]]:
    support_key = _sorted_support_key(active_supports)
    evidence_key = _dominant_evidence_key(evidence_patterns)
    intent_key = sequence_intent.value if sequence_intent is not None else None
    block_key = current_block_type.value if current_block_type is not None else None

    candidates = [
        {
            "support_profile": support_key,
            "sequence_intent": intent_key,
            "evidence_pattern": evidence_key,
            "block_type": block_key,
        },
        {
            "support_profile": support_key,
            "sequence_intent": intent_key,
            "evidence_pattern": evidence_key,
        },
        {
            "support_profile": support_key,
            "sequence_intent": intent_key,
        },
        {
            "support_profile": support_key,
            "evidence_pattern": evidence_key,
        },
        {
            "support_profile": support_key,
        },
        {
            "sequence_intent": intent_key,
            "evidence_pattern": evidence_key,
        },
        {
            "sequence_intent": intent_key,
        },
        {
            "evidence_pattern": evidence_key,
        },
        {
            "block_type": block_key,
        },
    ]

    seen: set[tuple[tuple[str, str], ...]] = set()
    ordered: list[dict[str, str]] = []
    for candidate in candidates:
        normalized = {
            key: value
            for key, value in candidate.items()
            if value is not None
        }
        if not normalized:
            continue
        signature = tuple(sorted(normalized.items()))
        if signature in seen:
            continue
        seen.add(signature)
        ordered.append(normalized)
    return ordered


def _normalize_weight_map(weights: dict[str, float]) -> dict[str, float]:
    total = sum(max(0.0, value) for value in weights.values())
    if total <= 0:
        fallback = 1.0 / max(1, len(weights))
        return {key: fallback for key in weights}
    return {
        key: max(0.0, value) / total
        for key, value in weights.items()
    }


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
        self.calibration_profiles: dict[str, CalibrationProfile] = {
            profile_id: profile.model_copy()
            for profile_id, profile in data.calibration_profiles.items()
        }

    def _snapshot(self) -> CalibrationData:
        return CalibrationData(
            decision_records=self.decision_log,
            outcome_metrics=self.outcome_metrics,
            calibration_weights=self.current_weights,
            weights_history=self.weights_history,
            calibration_profiles=self.calibration_profiles,
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
            "profile_count": len(self.calibration_profiles),
            "recent_success_rate": self.get_recent_success_rate() or 0.0,
            "weight_stability_index": self.get_weight_stability_index() or 1.0,
            "store_path": self.store_path,
            "last_calibration": (
                self.current_weights.last_calibration.isoformat()
                if self.current_weights.last_calibration is not None
                else None
            ),
        }

    def get_decision(self, decision_id: str) -> DecisionRecord | None:
        for record in self.decision_log:
            if record.decision_id == decision_id:
                return record
        return None

    def get_profile(self, profile_id: str | None) -> CalibrationProfile | None:
        if profile_id in (None, GLOBAL_CALIBRATION_PROFILE_ID):
            return None
        return self.calibration_profiles.get(profile_id)

    def list_profiles(self) -> list[dict[str, object]]:
        profiles = sorted(
            self.calibration_profiles.values(),
            key=lambda profile: (
                profile.outcome_count,
                profile.sample_size,
                len(profile.stratification_dimensions),
                profile.profile_id,
            ),
            reverse=True,
        )
        return [self._profile_summary(profile) for profile in profiles]

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
        self._register_profiles_for_record(record)
        self._mark_dirty()
        return record

    def update_outcome(self, decision_id: str, outcome: OutcomeMetrics) -> bool:
        updated = False
        matched_record: DecisionRecord | None = None
        for index, record in enumerate(self.decision_log):
            if record.decision_id != decision_id:
                continue
            matched_record = record.model_copy(
                update={
                    "observed_outcome": outcome,
                    "outcome_timestamp": datetime.now(UTC),
                }
            )
            self.decision_log[index] = matched_record
            updated = True
            break

        if updated and matched_record is not None:
            self.outcome_metrics.append(outcome)
            self._attempt_calibration()
            self._register_outcome_for_profiles(matched_record)
            self._mark_dirty()
        return updated

    def get_calibrated_score(
        self,
        score_breakdown: dict[str, float],
        weights: dict[str, float] | None = None,
    ) -> float:
        weights = weights or self.current_weights.get_current_weights()
        score = 0.0
        for component, weight in weights.items():
            score += score_breakdown.get(component, 0.0) * weight
        return max(0.0, min(1.0, score))

    def apply_to_enriched_paths(
        self,
        enriched_paths: list[EnrichedPathEvaluation],
        *,
        active_supports: list[SupportNeed] | None = None,
        sequence_intent: BlockSequenceIntent | None = None,
        evidence_patterns: list[EvidenceCombinationPattern] | None = None,
        current_block_type: BlockType | None = None,
    ) -> list[EnrichedPathEvaluation]:
        calibrated_paths: list[EnrichedPathEvaluation] = []

        for path in enriched_paths:
            candidate_block_type = (
                path.block_types[0]
                if path.block_types
                else current_block_type
            )
            profile_chain = self._profile_chain_for_context(
                active_supports=active_supports,
                sequence_intent=sequence_intent,
                evidence_patterns=evidence_patterns,
                current_block_type=candidate_block_type,
            )
            selected_profile = profile_chain[0] if profile_chain else None
            effective_weights, blend_ratio = self._effective_weights_for_profile_chain(
                profile_chain
            )
            calibrated_score = self.get_calibrated_score(
                path.score_breakdown,
                effective_weights,
            )
            calibrated_paths.append(
                path.model_copy(
                    update={
                        "uncalibrated_total_score": path.total_score,
                        "total_score": calibrated_score,
                        "calibration_applied": True,
                        "calibration_profile_id": (
                            selected_profile.profile_id
                            if selected_profile is not None
                            else GLOBAL_CALIBRATION_PROFILE_ID
                        ),
                        "calibration_profile_confidence": (
                            selected_profile.confidence_score
                            if selected_profile is not None
                            else 1.0
                        ),
                        "calibration_profile_sample_size": (
                            selected_profile.outcome_count
                            if selected_profile is not None
                            else len(self.outcome_metrics)
                        ),
                        "profile_weight_blend_ratio": blend_ratio,
                        "calibration_weights_used": {
                            key: round(value, 4)
                            for key, value in effective_weights.items()
                        },
                        "score_breakdown": {
                            **path.score_breakdown,
                            "calibrated_total": round(calibrated_score, 4),
                            "uncalibrated_total": round(path.total_score, 4),
                            "profile_weight_blend_ratio": round(blend_ratio, 4),
                        },
                    }
                )
            )

        calibrated_paths.sort(key=lambda item: item.total_score, reverse=True)
        return calibrated_paths

    def _compute_outcome_score(self, outcome: OutcomeMetrics) -> float:
        return outcome.composite_score()

    def _weights_from_records(
        self,
        records: list[DecisionRecord],
        baseline_weights: dict[str, float],
    ) -> tuple[dict[str, float], float]:
        raw_strengths: dict[str, float] = {}

        for component, default_weight in baseline_weights.items():
            component_scores = [
                record.chosen_path_score_breakdown.get(component, 0.0)
                * self._compute_outcome_score(record.observed_outcome)
                for record in records
                if record.observed_outcome is not None
            ]
            strength = fmean(component_scores) if component_scores else default_weight
            raw_strengths[component] = max(0.001, strength)

        adjusted_weights = _normalize_weight_map(raw_strengths)
        mse = fmean(
            (
                self.get_calibrated_score(
                    record.chosen_path_score_breakdown,
                    adjusted_weights,
                )
                - self._compute_outcome_score(record.observed_outcome)
            )
            ** 2
            for record in records
            if record.observed_outcome is not None
        )
        return adjusted_weights, mse

    def _profile_summary(self, profile: CalibrationProfile) -> dict[str, object]:
        return {
            "profile_id": profile.profile_id,
            "stratification_dimensions": profile.stratification_dimensions,
            "sample_size": profile.sample_size,
            "outcome_count": profile.outcome_count,
            "confidence_score": profile.confidence_score,
            "current_weights": profile.weight_summary(),
            "last_calibration": (
                profile.last_calibration.isoformat()
                if profile.last_calibration is not None
                else None
            ),
            "weights_history_length": len(profile.weights_history),
        }

    def get_profile_summary(self, profile_id: str) -> dict[str, object] | None:
        profile = self.get_profile(profile_id)
        if profile is None:
            return None
        return self._profile_summary(profile)

    def _get_or_create_profile(
        self,
        dimensions: dict[str, str],
    ) -> CalibrationProfile:
        profile_id = _profile_id_from_dimensions(dimensions)
        existing = self.calibration_profiles.get(profile_id)
        if existing is not None:
            return existing

        profile = CalibrationProfile(
            profile_id=profile_id,
            stratification_dimensions=dimensions,
        )
        self.calibration_profiles[profile_id] = profile
        return profile

    def _profile_variants_for_record(
        self,
        record: DecisionRecord,
    ) -> list[CalibrationProfile]:
        calibration_block_type = record.selected_block_type or record.current_block_type
        return [
            self._get_or_create_profile(dimensions)
            for dimensions in _ordered_profile_dimensions(
                active_supports=record.active_supports,
                sequence_intent=record.sequence_intent,
                evidence_patterns=record.evidence_patterns,
                current_block_type=calibration_block_type,
            )
        ]

    def _register_profiles_for_record(self, record: DecisionRecord) -> None:
        for profile in self._profile_variants_for_record(record):
            if record.decision_id not in profile.decision_ids:
                profile.decision_ids.append(record.decision_id)
                profile.refresh_counts()

    def _register_outcome_for_profiles(self, record: DecisionRecord) -> None:
        for profile in self._profile_variants_for_record(record):
            if record.decision_id not in profile.outcome_decision_ids:
                profile.outcome_decision_ids.append(record.decision_id)
            profile.refresh_counts()
            profile.confidence_score = self._profile_confidence(profile.outcome_count)
            self._recalibrate_profile(profile)

    def _profile_confidence(self, outcome_count: int) -> float:
        if outcome_count < PROFILE_PARTIAL_INHERITANCE_THRESHOLD:
            return 0.0
        if outcome_count >= PROFILE_FULL_INDEPENDENCE_THRESHOLD:
            return 1.0
        return (
            outcome_count - PROFILE_PARTIAL_INHERITANCE_THRESHOLD
        ) / (
            PROFILE_FULL_INDEPENDENCE_THRESHOLD
            - PROFILE_PARTIAL_INHERITANCE_THRESHOLD
        )

    def _select_profile(
        self,
        *,
        active_supports: list[SupportNeed] | None = None,
        sequence_intent: BlockSequenceIntent | None = None,
        evidence_patterns: list[EvidenceCombinationPattern] | None = None,
        current_block_type: BlockType | None = None,
    ) -> CalibrationProfile | None:
        profile_chain = self._profile_chain_for_context(
            active_supports=active_supports,
            sequence_intent=sequence_intent,
            evidence_patterns=evidence_patterns,
            current_block_type=current_block_type,
        )
        return profile_chain[0] if profile_chain else None

    def _profile_chain_for_context(
        self,
        *,
        active_supports: list[SupportNeed] | None = None,
        sequence_intent: BlockSequenceIntent | None = None,
        evidence_patterns: list[EvidenceCombinationPattern] | None = None,
        current_block_type: BlockType | None = None,
    ) -> list[CalibrationProfile]:
        dimensions_list = _ordered_profile_dimensions(
            active_supports=active_supports,
            sequence_intent=sequence_intent,
            evidence_patterns=evidence_patterns,
            current_block_type=current_block_type,
        )
        if not dimensions_list:
            return []

        exact_dimensions = dimensions_list[0]
        exact_profile_id = _profile_id_from_dimensions(exact_dimensions)
        exact_profile = self.calibration_profiles.get(exact_profile_id)

        ordered_profiles: list[CalibrationProfile] = []
        if exact_profile is not None:
            ordered_profiles.append(exact_profile)

        for dimensions in dimensions_list[1:]:
            profile = self.calibration_profiles.get(_profile_id_from_dimensions(dimensions))
            if profile is not None:
                ordered_profiles.append(profile)

        if ordered_profiles:
            return ordered_profiles

        return [self._get_or_create_profile(exact_dimensions)]

    def _effective_weights_for_profile(
        self,
        profile: CalibrationProfile | None,
        fallback_weights: dict[str, float] | None = None,
    ) -> tuple[dict[str, float], float]:
        root_weights = fallback_weights or self.current_weights.get_current_weights()
        if profile is None:
            return root_weights, 0.0

        profile_weights = profile.current_weights.get_current_weights()
        blend_ratio = profile.confidence_score
        combined: dict[str, float] = {}
        for component in set(root_weights) | set(profile_weights):
            combined[component] = (
                profile_weights.get(component, 0.0) * blend_ratio
                + root_weights.get(component, 0.0) * (1.0 - blend_ratio)
            )
        return _normalize_weight_map(combined), blend_ratio

    def _effective_weights_for_profile_chain(
        self,
        profiles: list[CalibrationProfile],
    ) -> tuple[dict[str, float], float]:
        if not profiles:
            return self.current_weights.get_current_weights(), 0.0

        base_weights = self.current_weights.get_current_weights()
        for profile in reversed(profiles):
            base_weights, _ = self._effective_weights_for_profile(
                profile,
                base_weights,
            )
        return base_weights, profiles[0].confidence_score

    def _record_matches_profile(
        self,
        record: DecisionRecord,
        dimensions: dict[str, str],
    ) -> bool:
        support_key = _sorted_support_key(record.active_supports)
        evidence_key = _dominant_evidence_key(record.evidence_patterns)
        intent_key = record.sequence_intent.value if record.sequence_intent else None
        block_type = record.selected_block_type or record.current_block_type
        block_key = block_type.value

        for key, expected in dimensions.items():
            if key == "support_profile" and support_key != expected:
                return False
            if key == "sequence_intent" and intent_key != expected:
                return False
            if key == "evidence_pattern" and evidence_key != expected:
                return False
            if key == "block_type" and block_key != expected:
                return False
        return True

    def _recalibrate_profile(self, profile: CalibrationProfile) -> None:
        matched_records = [
            record
            for record in self.decision_log
            if record.observed_outcome is not None
            and self._record_matches_profile(record, profile.stratification_dimensions)
        ]
        profile.sample_size = len(
            [
                record
                for record in self.decision_log
                if self._record_matches_profile(record, profile.stratification_dimensions)
            ]
        )
        profile.outcome_count = len(matched_records)
        profile.confidence_score = self._profile_confidence(profile.outcome_count)

        if len(matched_records) < PROFILE_MIN_OUTCOMES_FOR_CALIBRATION:
            return

        adjusted_weights, mse = self._weights_from_records(
            matched_records,
            profile.current_weights.baseline_weights,
        )
        best_record = max(
            matched_records,
            key=lambda record: self._compute_outcome_score(record.observed_outcome),
        )
        profile.current_weights = profile.current_weights.model_copy(
            update={
                "adjusted_weights": adjusted_weights,
                "calibration_rounds": profile.current_weights.calibration_rounds + 1,
                "last_calibration": datetime.now(UTC),
                "mean_squared_error_history": [
                    *profile.current_weights.mean_squared_error_history,
                    mse,
                ],
            }
        )
        profile.last_calibration = profile.current_weights.last_calibration
        profile.weights_history.append(
            CalibrationWeightsSnapshot(
                timestamp=datetime.now(UTC),
                active_weights=profile.current_weights.get_current_weights(),
                profile_id=profile.profile_id,
                trigger_decision_id=best_record.decision_id,
                outcome_score=self._compute_outcome_score(best_record.observed_outcome),
                adjustment_reason="Profile-aware calibration round completed.",
            )
        )

    def _attempt_calibration(self) -> dict[str, float] | None:
        eligible_records = [
            record
            for record in self.decision_log
            if record.observed_outcome is not None and not record.used_for_calibration
        ]
        if len(eligible_records) < self.min_samples_for_calibration:
            return None

        adjusted_weights, mse = self._weights_from_records(
            eligible_records,
            self.current_weights.baseline_weights,
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
                profile_id=GLOBAL_CALIBRATION_PROFILE_ID,
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
