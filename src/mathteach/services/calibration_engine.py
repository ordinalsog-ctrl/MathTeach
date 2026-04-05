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
    MetaTransferHistoryEntry,
    MetaTransferLink,
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
META_TRANSFER_MAX_BLEND = 0.35
META_TRANSFER_MAX_SOURCES = 3
META_TRANSFER_HISTORY_LIMIT = 50
META_TRANSFER_EFFECTIVE_EPSILON = 1e-6


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


def _support_overlap_score(
    left_support_key: str | None,
    right_support_key: str | None,
) -> float:
    if left_support_key is None or right_support_key is None:
        return 0.0
    left = {item for item in left_support_key.split("+") if item}
    right = {item for item in right_support_key.split("+") if item}
    if not left or not right:
        return 0.0
    union = left | right
    if not union:
        return 0.0
    return len(left & right) / len(union)


def _merge_blend_ratios(existing_ratio: float, additional_ratio: float) -> float:
    return 1.0 - ((1.0 - existing_ratio) * (1.0 - additional_ratio))


def _normalize_source_shares(
    source_profiles: list[str],
    source_shares: dict[str, float] | None = None,
) -> dict[str, float]:
    if not source_profiles:
        return {}

    raw_shares = {
        source_id: max(0.0, (source_shares or {}).get(source_id, 0.0))
        for source_id in source_profiles
    }
    total = sum(raw_shares.values())
    if total <= 0.0:
        equal_share = 1.0 / len(source_profiles)
        return {
            source_id: equal_share
            for source_id in source_profiles
        }
    return {
        source_id: raw_shares[source_id] / total
        for source_id in source_profiles
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

    def _effective_transfer_history_entries(
        self,
        profile: CalibrationProfile,
    ) -> list[MetaTransferHistoryEntry]:
        return [
            entry
            for entry in sorted(
                profile.meta_transfer_history,
                key=lambda item: item.timestamp,
            )
            if entry.effective_weight_delta > META_TRANSFER_EFFECTIVE_EPSILON
        ]

    def _history_based_transfer_links(
        self,
        profile: CalibrationProfile,
    ) -> dict[str, MetaTransferLink]:
        links: dict[str, MetaTransferLink] = {}

        for entry in self._effective_transfer_history_entries(profile):
            for source_profile_id in entry.source_profile_ids:
                share = entry.source_shares.get(source_profile_id, 0.0)
                if share <= 0.0:
                    continue
                link = links.get(source_profile_id)
                if link is None:
                    link = MetaTransferLink(source_profile_id=source_profile_id)
                link.record_outcome(
                    outcome_score=entry.outcome_score * share,
                    similarity_score=entry.similarity_by_source.get(source_profile_id, 0.0),
                    transfer_strength=entry.transfer_strength * share,
                    timestamp=entry.timestamp,
                )
                links[source_profile_id] = link

        return links

    def _edge_metrics(self) -> list[dict[str, object]]:
        edge_index: dict[tuple[str, str], dict[str, object]] = {}

        for target_profile in self.calibration_profiles.values():
            for entry in self._effective_transfer_history_entries(target_profile):
                for source_profile_id in entry.source_profile_ids:
                    share = entry.source_shares.get(source_profile_id, 0.0)
                    if share <= 0.0:
                        continue
                    key = (source_profile_id, target_profile.profile_id)
                    edge = edge_index.setdefault(
                        key,
                        {
                            "source_profile_id": source_profile_id,
                            "target_profile_id": target_profile.profile_id,
                            "use_count": 0,
                            "cumulative_outcome_score": 0.0,
                            "cumulative_effective_weight_delta": 0.0,
                            "cumulative_transfer_strength": 0.0,
                            "cumulative_source_share": 0.0,
                            "last_used": None,
                        },
                    )
                    edge["use_count"] += 1
                    edge["cumulative_outcome_score"] += entry.outcome_score * share
                    edge["cumulative_effective_weight_delta"] += (
                        entry.effective_weight_delta * share
                    )
                    edge["cumulative_transfer_strength"] += entry.transfer_strength * share
                    edge["cumulative_source_share"] += share
                    if (
                        edge["last_used"] is None
                        or entry.timestamp > edge["last_used"]
                    ):
                        edge["last_used"] = entry.timestamp

        finalized_edges: list[dict[str, object]] = []
        for edge in edge_index.values():
            use_count = max(1, int(edge["use_count"]))
            average_outcome_score = edge["cumulative_outcome_score"] / use_count
            average_effective_weight_delta = (
                edge["cumulative_effective_weight_delta"] / use_count
            )
            average_transfer_strength = edge["cumulative_transfer_strength"] / use_count
            average_source_share = edge["cumulative_source_share"] / use_count
            effectiveness_ratio = (
                average_outcome_score / average_effective_weight_delta
                if average_effective_weight_delta > META_TRANSFER_EFFECTIVE_EPSILON
                else 0.0
            )
            finalized_edges.append(
                {
                    "source_profile_id": edge["source_profile_id"],
                    "target_profile_id": edge["target_profile_id"],
                    "use_count": use_count,
                    "average_outcome_score": round(average_outcome_score, 4),
                    "average_effective_weight_delta": round(
                        average_effective_weight_delta,
                        4,
                    ),
                    "average_transfer_strength": round(average_transfer_strength, 4),
                    "average_source_share": round(average_source_share, 4),
                    "transfer_effectiveness": round(effectiveness_ratio, 4),
                    "last_used": (
                        edge["last_used"].isoformat()
                        if edge["last_used"] is not None
                        else None
                    ),
                }
            )

        finalized_edges.sort(
            key=lambda edge: (
                edge["use_count"],
                edge["average_outcome_score"],
                edge["source_profile_id"],
                edge["target_profile_id"],
            ),
            reverse=True,
        )
        return finalized_edges

    def compute_weak_transfers(
        self,
        *,
        min_average_strength: float = 0.05,
        max_average_outcome: float = 0.12,
    ) -> list[dict[str, object]]:
        return [
            edge
            for edge in self._edge_metrics()
            if edge["average_transfer_strength"] >= min_average_strength
            and edge["average_outcome_score"] <= max_average_outcome
        ]

    def profile_transfer_candidates(
        self,
        profile_id: str,
        *,
        limit: int = 5,
    ) -> list[dict[str, object]]:
        profile = self.get_profile(profile_id)
        if profile is None:
            return []

        candidates = self._meta_transfer_candidates(
            profile,
            excluded_profile_ids={profile.profile_id},
        )[:limit]
        if not candidates:
            return []

        candidate_strengths = [
            (similarity_score * candidate.confidence_score)
            + (0.25 * historical_effectiveness)
            for candidate, similarity_score, historical_effectiveness in candidates
        ]
        total_strength = sum(candidate_strengths)
        source_shares = _normalize_source_shares(
            [candidate.profile_id for candidate, _, _ in candidates],
            (
                {
                    candidate.profile_id: strength / total_strength
                    for (candidate, _, _), strength in zip(
                        candidates,
                        candidate_strengths,
                        strict=True,
                    )
                }
                if total_strength > 0.0
                else None
            ),
        )

        return [
            {
                "profile_id": candidate.profile_id,
                "similarity_score": round(similarity_score, 4),
                "historical_effectiveness": round(historical_effectiveness, 4),
                "confidence_score": round(candidate.confidence_score, 4),
                "outcome_count": candidate.outcome_count,
                "recommended_share": round(source_shares.get(candidate.profile_id, 0.0), 4),
            }
            for candidate, similarity_score, historical_effectiveness in candidates
        ]

    def get_profile_transfer_history(
        self,
        profile_id: str,
        *,
        limit: int = 10,
    ) -> dict[str, object] | None:
        profile = self.get_profile(profile_id)
        if profile is None:
            return None

        transfer_decisions = [
            record
            for record in self.decision_log
            if record.calibration_profile_id == profile_id
            and (record.meta_transfer_strength or 0.0) > 0.0
        ]
        effective_transfers = [
            record
            for record in transfer_decisions
            if record.meta_transfer_was_effective
        ]
        phantom_filters = len(transfer_decisions) - len(effective_transfers)
        effective_history = self._effective_transfer_history_entries(profile)

        top_donors = sorted(
            self._history_based_transfer_links(profile).values(),
            key=lambda link: (
                link.average_outcome_score,
                link.use_count,
                link.source_profile_id,
            ),
            reverse=True,
        )

        return {
            "profile_id": profile_id,
            "total_decisions_using_transfer": len(transfer_decisions),
            "effective_transfers": len(effective_transfers),
            "phantom_filters": phantom_filters,
            "top_donors": [
                {
                    "donor_id": link.source_profile_id,
                    "use_count": link.use_count,
                    "average_outcome_score": round(link.average_outcome_score, 4),
                    "last_transfer_strength": (
                        round(link.last_transfer_strength, 4)
                        if link.last_transfer_strength is not None
                        else None
                    ),
                    "last_used": (
                        link.last_used.isoformat()
                        if link.last_used is not None
                        else None
                    ),
                }
                for link in top_donors[:limit]
            ],
            "recent_transfer_sequence": [
                {
                    "decision_id": entry.decision_id,
                    "timestamp": entry.timestamp.isoformat(),
                    "transfer_strength": round(entry.transfer_strength, 4),
                    "effective_weight_delta": round(entry.effective_weight_delta, 4),
                    "source_shares": {
                        source_id: round(share, 4)
                        for source_id, share in entry.source_shares.items()
                    },
                    "outcome_score": round(entry.outcome_score, 4),
                    "attributed_outcome_by_source": {
                        source_id: round(entry.outcome_score * share, 4)
                        for source_id, share in entry.source_shares.items()
                    },
                }
                for entry in effective_history[-limit:]
            ],
            "transfer_candidates": self.profile_transfer_candidates(profile_id, limit=limit),
        }

    def profile_density_summary(self) -> dict[str, object]:
        def _bucket_summary(bucket_fn: callable) -> dict[str, dict[str, object]]:
            buckets: dict[str, dict[str, float | int]] = {}
            for profile in self.calibration_profiles.values():
                bucket = bucket_fn(profile)
                if bucket is None:
                    continue
                stats = buckets.setdefault(
                    bucket,
                    {
                        "profile_count": 0,
                        "total_outcomes": 0,
                        "total_confidence": 0.0,
                        "sparse_profiles": 0,
                    },
                )
                stats["profile_count"] += 1
                stats["total_outcomes"] += profile.outcome_count
                stats["total_confidence"] += profile.confidence_score
                if profile.outcome_count < PROFILE_PARTIAL_INHERITANCE_THRESHOLD:
                    stats["sparse_profiles"] += 1

            summary: dict[str, dict[str, object]] = {}
            for bucket, stats in buckets.items():
                profile_count = int(stats["profile_count"])
                summary[bucket] = {
                    "profile_count": profile_count,
                    "average_outcome_count": round(
                        float(stats["total_outcomes"]) / profile_count,
                        4,
                    ),
                    "average_confidence_score": round(
                        float(stats["total_confidence"]) / profile_count,
                        4,
                    ),
                    "sparse_profiles": int(stats["sparse_profiles"]),
                }
            return summary

        isolated_profiles = []
        for profile in self.calibration_profiles.values():
            if profile.outcome_count >= PROFILE_PARTIAL_INHERITANCE_THRESHOLD:
                continue
            candidates = self.profile_transfer_candidates(profile.profile_id, limit=3)
            if not candidates:
                continue
            isolated_profiles.append(
                {
                    "profile_id": profile.profile_id,
                    "outcome_count": profile.outcome_count,
                    "confidence_score": round(profile.confidence_score, 4),
                    "possible_donors": candidates,
                }
            )

        isolated_profiles.sort(
            key=lambda item: (
                item["outcome_count"],
                item["confidence_score"],
                item["profile_id"],
            )
        )

        return {
            "total_profiles": len(self.calibration_profiles),
            "with_outcomes": sum(
                1
                for profile in self.calibration_profiles.values()
                if profile.outcome_count > 0
            ),
            "sparse_profiles": sum(
                1
                for profile in self.calibration_profiles.values()
                if profile.outcome_count < PROFILE_PARTIAL_INHERITANCE_THRESHOLD
            ),
            "independent_profiles": sum(
                1
                for profile in self.calibration_profiles.values()
                if profile.outcome_count >= PROFILE_FULL_INDEPENDENCE_THRESHOLD
            ),
            "by_support_profile": _bucket_summary(
                lambda profile: profile.stratification_dimensions.get("support_profile")
            ),
            "by_evidence_pattern": _bucket_summary(
                lambda profile: profile.stratification_dimensions.get("evidence_pattern")
            ),
            "by_block_type": _bucket_summary(
                lambda profile: profile.stratification_dimensions.get("block_type")
            ),
            "isolated_profiles": isolated_profiles[:10],
        }

    def compute_transfer_network_summary(self) -> dict[str, object]:
        edges = self._edge_metrics()
        inbound_counts: dict[str, int] = {}
        outbound_counts: dict[str, int] = {}

        for edge in edges:
            inbound_counts[edge["target_profile_id"]] = (
                inbound_counts.get(edge["target_profile_id"], 0) + 1
            )
            outbound_counts[edge["source_profile_id"]] = (
                outbound_counts.get(edge["source_profile_id"], 0) + 1
            )

        nodes = [
            {
                "profile_id": profile.profile_id,
                "outcome_count": profile.outcome_count,
                "confidence_score": round(profile.confidence_score, 4),
                "inbound_transfers": inbound_counts.get(profile.profile_id, 0),
                "outbound_transfers": outbound_counts.get(profile.profile_id, 0),
            }
            for profile in sorted(
                self.calibration_profiles.values(),
                key=lambda profile: (
                    profile.outcome_count,
                    profile.confidence_score,
                    profile.profile_id,
                ),
                reverse=True,
            )
        ]

        return {
            "total_profiles": len(self.calibration_profiles),
            "profiles_with_transfer": sum(
                1
                for profile in self.calibration_profiles.values()
                if self._effective_transfer_history_entries(profile)
            ),
            "effective_transfer_decisions": sum(
                1
                for record in self.decision_log
                if record.meta_transfer_was_effective
            ),
            "nodes": nodes,
            "edges": edges,
            "weak_edges": self.compute_weak_transfers(),
            "isolated_profiles": self.profile_density_summary()["isolated_profiles"],
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
            self._record_meta_transfer_outcome(matched_record)
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
            (
                effective_weights,
                blend_ratio,
                meta_transfer_strength,
                meta_transfer_source_profiles,
                meta_transfer_source_shares,
                meta_transfer_weight_delta,
                meta_transfer_was_effective,
            ) = self._effective_weights_for_profile_chain(
                profile_chain,
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
                        "meta_transfer_strength": meta_transfer_strength,
                        "meta_transfer_source_profiles": meta_transfer_source_profiles,
                        "meta_transfer_source_shares": meta_transfer_source_shares,
                        "meta_transfer_weight_delta": meta_transfer_weight_delta,
                        "meta_transfer_was_effective": meta_transfer_was_effective,
                        "calibration_weights_used": {
                            key: round(value, 4)
                            for key, value in effective_weights.items()
                        },
                        "score_breakdown": {
                            **path.score_breakdown,
                            "calibrated_total": round(calibrated_score, 4),
                            "uncalibrated_total": round(path.total_score, 4),
                            "profile_weight_blend_ratio": round(blend_ratio, 4),
                            "meta_transfer_strength": round(meta_transfer_strength, 4),
                            "meta_transfer_weight_delta": round(meta_transfer_weight_delta, 4),
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
        meta_candidates = self._meta_transfer_candidates(
            profile,
            excluded_profile_ids={profile.profile_id},
        )
        effective_history = self._effective_transfer_history_entries(profile)
        meta_transfer_links = sorted(
            self._history_based_transfer_links(profile).values(),
            key=lambda link: (
                link.average_outcome_score,
                link.use_count,
                link.source_profile_id,
            ),
            reverse=True,
        )
        return {
            "profile_id": profile.profile_id,
            "stratification_dimensions": profile.stratification_dimensions,
            "sample_size": profile.sample_size,
            "outcome_count": profile.outcome_count,
            "confidence_score": profile.confidence_score,
            "current_weights": profile.weight_summary(),
            "meta_transfer_links": [
                {
                    "source_profile_id": link.source_profile_id,
                    "use_count": link.use_count,
                    "average_outcome_score": round(link.average_outcome_score, 4),
                    "last_similarity_score": (
                        round(link.last_similarity_score, 4)
                        if link.last_similarity_score is not None
                        else None
                    ),
                    "last_transfer_strength": (
                        round(link.last_transfer_strength, 4)
                        if link.last_transfer_strength is not None
                        else None
                    ),
                    "last_outcome_score": (
                        round(link.last_outcome_score, 4)
                        if link.last_outcome_score is not None
                        else None
                    ),
                    "last_used": (
                        link.last_used.isoformat()
                        if link.last_used is not None
                        else None
                    ),
                }
                for link in meta_transfer_links
            ],
            "meta_transfer_history_recent": [
                {
                    "timestamp": entry.timestamp.isoformat(),
                    "decision_id": entry.decision_id,
                    "source_profile_ids": entry.source_profile_ids,
                    "transfer_strength": round(entry.transfer_strength, 4),
                    "outcome_score": round(entry.outcome_score, 4),
                    "similarity_by_source": {
                        source_id: round(score, 4)
                        for source_id, score in entry.similarity_by_source.items()
                    },
                    "source_shares": {
                        source_id: round(score, 4)
                        for source_id, score in entry.source_shares.items()
                    },
                    "effective_weight_delta": round(entry.effective_weight_delta, 4),
                }
                for entry in effective_history[-5:]
            ],
            "meta_transfer_candidates": [
                {
                    "profile_id": candidate.profile_id,
                    "similarity_score": round(similarity_score, 4),
                    "historical_effectiveness": round(historical_effectiveness, 4),
                    "confidence_score": candidate.confidence_score,
                    "outcome_count": candidate.outcome_count,
                }
                for candidate, similarity_score, historical_effectiveness in meta_candidates
            ],
            "last_calibration": (
                profile.last_calibration.isoformat()
                if profile.last_calibration is not None
                else None
            ),
            "weights_history_length": len(profile.weights_history),
            "meta_transfer_history_length": len(effective_history),
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

    def _record_meta_transfer_outcome(self, record: DecisionRecord) -> None:
        if (
            record.observed_outcome is None
            or record.calibration_profile_id in (None, GLOBAL_CALIBRATION_PROFILE_ID)
            or not record.meta_transfer_source_profiles
            or not record.meta_transfer_strength
            or not record.meta_transfer_was_effective
            or (record.meta_transfer_weight_delta or 0.0) <= META_TRANSFER_EFFECTIVE_EPSILON
        ):
            return

        target_profile = self.get_profile(record.calibration_profile_id)
        if target_profile is None:
            return

        outcome_score = self._compute_outcome_score(record.observed_outcome)
        timestamp = record.outcome_timestamp or datetime.now(UTC)
        similarity_by_source: dict[str, float] = {}
        normalized_source_shares = _normalize_source_shares(
            record.meta_transfer_source_profiles,
            record.meta_transfer_source_shares,
        )

        for source_profile_id in record.meta_transfer_source_profiles:
            share = normalized_source_shares.get(source_profile_id, 0.0)
            if share <= 0.0:
                continue
            source_profile = self.get_profile(source_profile_id)
            if source_profile is None:
                continue
            similarity_score = self._profile_similarity_score(
                target_profile.stratification_dimensions,
                source_profile.stratification_dimensions,
            )
            link = target_profile.meta_transfer_links.get(source_profile_id)
            if link is None:
                link = MetaTransferLink(source_profile_id=source_profile_id)
            link.record_outcome(
                outcome_score=outcome_score * share,
                similarity_score=similarity_score,
                transfer_strength=record.meta_transfer_strength * share,
                timestamp=timestamp,
            )
            target_profile.meta_transfer_links[source_profile_id] = link
            similarity_by_source[source_profile_id] = similarity_score

        if similarity_by_source:
            target_profile.meta_transfer_history.append(
                MetaTransferHistoryEntry(
                    timestamp=timestamp,
                    target_profile_id=target_profile.profile_id,
                    source_profile_ids=list(similarity_by_source),
                    decision_id=record.decision_id,
                    transfer_strength=record.meta_transfer_strength,
                    outcome_score=outcome_score,
                    similarity_by_source=similarity_by_source,
                    source_shares={
                        source_id: normalized_source_shares[source_id]
                        for source_id in similarity_by_source
                    },
                    effective_weight_delta=record.meta_transfer_weight_delta or 0.0,
                )
            )
            target_profile.meta_transfer_history = target_profile.meta_transfer_history[
                -META_TRANSFER_HISTORY_LIMIT:
            ]

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
        return self._blend_weight_maps(
            root_weights,
            profile_weights,
            blend_ratio,
        ), blend_ratio

    def _blend_weight_maps(
        self,
        fallback_weights: dict[str, float],
        overlay_weights: dict[str, float],
        overlay_ratio: float,
    ) -> dict[str, float]:
        combined: dict[str, float] = {}
        for component in set(fallback_weights) | set(overlay_weights):
            combined[component] = (
                overlay_weights.get(component, 0.0) * overlay_ratio
                + fallback_weights.get(component, 0.0) * (1.0 - overlay_ratio)
            )
        return _normalize_weight_map(combined)

    def _profile_similarity_score(
        self,
        target_dimensions: dict[str, str],
        candidate_dimensions: dict[str, str],
    ) -> float:
        target_support = target_dimensions.get("support_profile")
        candidate_support = candidate_dimensions.get("support_profile")
        if target_support is not None and candidate_support is not None:
            support_similarity = _support_overlap_score(
                target_support,
                candidate_support,
            )
            if support_similarity <= 0.0:
                return 0.0
        elif target_support is not None or candidate_support is not None:
            return 0.0
        else:
            support_similarity = 0.0

        similarity_score = 0.5 * support_similarity
        if (
            target_dimensions.get("sequence_intent") is not None
            and target_dimensions.get("sequence_intent")
            == candidate_dimensions.get("sequence_intent")
        ):
            similarity_score += 0.2
        if (
            target_dimensions.get("evidence_pattern") is not None
            and target_dimensions.get("evidence_pattern")
            == candidate_dimensions.get("evidence_pattern")
        ):
            similarity_score += 0.15
        if (
            target_dimensions.get("block_type") is not None
            and target_dimensions.get("block_type")
            == candidate_dimensions.get("block_type")
        ):
            similarity_score += 0.15
        return max(0.0, min(1.0, similarity_score))

    def _historical_transfer_effectiveness(
        self,
        target_profile: CalibrationProfile,
        source_profile_id: str,
    ) -> float:
        link = self._history_based_transfer_links(target_profile).get(source_profile_id)
        if link is None or link.use_count <= 0:
            return 0.0
        return min(1.0, link.use_count / 5) * link.average_outcome_score

    def _meta_transfer_candidates(
        self,
        target_profile: CalibrationProfile,
        *,
        excluded_profile_ids: set[str],
    ) -> list[tuple[CalibrationProfile, float, float]]:
        ranked_candidates: list[tuple[CalibrationProfile, float, float]] = []
        for candidate in self.calibration_profiles.values():
            if candidate.profile_id in excluded_profile_ids:
                continue
            if candidate.outcome_count < PROFILE_MIN_OUTCOMES_FOR_CALIBRATION:
                continue
            if candidate.confidence_score <= 0.0:
                continue
            similarity_score = self._profile_similarity_score(
                target_profile.stratification_dimensions,
                candidate.stratification_dimensions,
            )
            if similarity_score <= 0.0:
                continue
            historical_effectiveness = self._historical_transfer_effectiveness(
                target_profile,
                candidate.profile_id,
            )
            ranked_candidates.append(
                (candidate, similarity_score, historical_effectiveness)
            )

        ranked_candidates.sort(
            key=lambda item: (
                (item[1] * item[0].confidence_score) + (0.25 * item[2]),
                item[0].outcome_count,
                len(item[0].stratification_dimensions),
                item[0].profile_id,
            ),
            reverse=True,
        )
        return ranked_candidates[:META_TRANSFER_MAX_SOURCES]

    def _meta_transfer_prior(
        self,
        selected_profile: CalibrationProfile,
        *,
        excluded_profile_ids: set[str],
    ) -> tuple[dict[str, float] | None, float, list[str], dict[str, float]]:
        candidates = self._meta_transfer_candidates(
            selected_profile,
            excluded_profile_ids=excluded_profile_ids,
        )
        if not candidates:
            return None, 0.0, [], {}

        candidate_strengths = [
            (similarity_score * candidate.confidence_score)
            + (0.25 * historical_effectiveness)
            for candidate, similarity_score, historical_effectiveness in candidates
        ]
        total_strength = sum(candidate_strengths)
        if total_strength <= 0.0:
            return None, 0.0, [], {}

        transfer_weights: dict[str, float] = {}
        all_components = {
            component
            for candidate, _, _ in candidates
            for component in candidate.current_weights.get_current_weights()
        }
        for component in all_components:
            transfer_weights[component] = sum(
                candidate.current_weights.get_current_weights().get(component, 0.0)
                * strength
                for (candidate, _, _), strength in zip(
                    candidates,
                    candidate_strengths,
                    strict=True,
                )
            ) / total_strength

        transfer_strength = min(
            META_TRANSFER_MAX_BLEND,
            total_strength / len(candidate_strengths),
        )
        source_profiles = [candidate.profile_id for candidate, _, _ in candidates]
        source_shares = _normalize_source_shares(
            source_profiles,
            {
                candidate.profile_id: strength / total_strength
                for (candidate, _, _), strength in zip(
                    candidates,
                    candidate_strengths,
                    strict=True,
                )
            },
        )
        return (
            _normalize_weight_map(transfer_weights),
            transfer_strength,
            source_profiles,
            source_shares,
        )

    def _base_weights_for_profile_chain(
        self,
        profiles: list[CalibrationProfile],
    ) -> tuple[dict[str, float], float]:
        base_weights = self.current_weights.get_current_weights()
        total_blend_ratio = 0.0

        for profile in reversed(profiles[1:]):
            base_weights = self._blend_weight_maps(
                base_weights,
                profile.current_weights.get_current_weights(),
                profile.confidence_score,
            )
            total_blend_ratio = _merge_blend_ratios(
                total_blend_ratio,
                profile.confidence_score,
            )

        return base_weights, total_blend_ratio

    def _calculate_weight_delta(
        self,
        left_weights: dict[str, float],
        right_weights: dict[str, float],
    ) -> float:
        return max(
            (
                abs(left_weights.get(component, 0.0) - right_weights.get(component, 0.0))
                for component in set(left_weights) | set(right_weights)
            ),
            default=0.0,
        )

    def _effective_weights_for_profile_chain(
        self,
        profiles: list[CalibrationProfile],
    ) -> tuple[dict[str, float], float, float, list[str], dict[str, float], float, bool]:
        if not profiles:
            return self.current_weights.get_current_weights(), 0.0, 0.0, [], {}, 0.0, False

        selected_profile = profiles[0]
        selected_profile_weights = selected_profile.current_weights.get_current_weights()
        base_weights, base_blend_ratio = self._base_weights_for_profile_chain(profiles)
        effective_weights_without_transfer = self._blend_weight_maps(
            base_weights,
            selected_profile_weights,
            selected_profile.confidence_score,
        )
        total_blend_ratio_without_transfer = _merge_blend_ratios(
            base_blend_ratio,
            selected_profile.confidence_score,
        )

        (
            transfer_weights,
            meta_transfer_strength,
            meta_transfer_source_profiles,
            meta_transfer_source_shares,
        ) = (
            self._meta_transfer_prior(
                selected_profile,
                excluded_profile_ids={profile.profile_id for profile in profiles},
            )
        )

        if transfer_weights is None or meta_transfer_strength <= 0.0:
            return (
                effective_weights_without_transfer,
                total_blend_ratio_without_transfer,
                0.0,
                [],
                {},
                0.0,
                False,
            )

        base_weights_with_transfer = self._blend_weight_maps(
            base_weights,
            transfer_weights,
            meta_transfer_strength,
        )
        total_blend_ratio_with_transfer = _merge_blend_ratios(
            _merge_blend_ratios(
                base_blend_ratio,
                meta_transfer_strength,
            ),
            selected_profile.confidence_score,
        )
        effective_weights_with_transfer = self._blend_weight_maps(
            base_weights_with_transfer,
            selected_profile_weights,
            selected_profile.confidence_score,
        )
        meta_transfer_weight_delta = self._calculate_weight_delta(
            effective_weights_with_transfer,
            effective_weights_without_transfer,
        )
        meta_transfer_was_effective = (
            meta_transfer_weight_delta > META_TRANSFER_EFFECTIVE_EPSILON
        )

        return (
            (
                effective_weights_with_transfer
                if meta_transfer_was_effective
                else effective_weights_without_transfer
            ),
            (
                total_blend_ratio_with_transfer
                if meta_transfer_was_effective
                else total_blend_ratio_without_transfer
            ),
            meta_transfer_strength,
            meta_transfer_source_profiles,
            meta_transfer_source_shares,
            (
                meta_transfer_weight_delta
                if meta_transfer_was_effective
                else 0.0
            ),
            meta_transfer_was_effective,
        )

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
