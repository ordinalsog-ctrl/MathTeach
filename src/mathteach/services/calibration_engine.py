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
META_TRANSFER_WEAK_EDGE_PENALTY_MULTIPLIER = 0.6
META_TRANSFER_PROVEN_DONOR_EFFECTIVENESS_THRESHOLD = 0.7
META_TRANSFER_PROVEN_DONOR_BOOST_MULTIPLIER = 1.3
META_TRANSFER_ADAPTIVE_HISTORY_MIN_SAMPLES = 3
META_TRANSFER_INSUFFICIENT_HISTORY_BLEND = 0.3
META_TRANSFER_WEAK_EDGE_MAX_BLEND = 0.2
META_TRANSFER_LOW_EFFECTIVENESS_MAX_BLEND = 0.3
META_TRANSFER_STRONG_EDGE_MAX_BLEND = 0.45
META_TRANSFER_WEAK_EDGE_EFFECTIVENESS_THRESHOLD = 0.25
META_TRANSFER_LOW_EFFECTIVENESS_THRESHOLD = 0.5
META_TRANSFER_STRONG_EDGE_EFFECTIVENESS_THRESHOLD = 0.7
META_TRANSFER_EDGE_SEEKING_MIN_SIMILARITY = 0.25
META_TRANSFER_EDGE_SEEKING_INSUFFICIENT_HISTORY_MULTIPLIER = 1.15
META_TRANSFER_EDGE_SEEKING_WEAK_EDGE_RECOVERY_MULTIPLIER = 1.2
META_TRANSFER_EDGE_POLICY_TRUSTED_MULTIPLIER = 1.05
META_TRANSFER_EDGE_POLICY_EXPLORE_MULTIPLIER = 1.02
META_TRANSFER_EDGE_POLICY_RECOVERY_MULTIPLIER = 0.98
META_TRANSFER_EDGE_POLICY_CAUTIOUS_MULTIPLIER = 0.96
META_TRANSFER_EDGE_POLICY_GUARDED_MULTIPLIER = 0.9
META_TRANSFER_FAMILY_POLICY_MIN_SAMPLES = 3
META_TRANSFER_FAMILY_POLICY_STRONG_EFFECTIVENESS_THRESHOLD = 0.6
META_TRANSFER_FAMILY_POLICY_WEAK_EFFECTIVENESS_THRESHOLD = 0.2
META_TRANSFER_FAMILY_POLICY_SAME_FAMILY_MIN_EFFECTIVENESS = 0.5
META_TRANSFER_FAMILY_POLICY_TRUSTED_MULTIPLIER = 1.04
META_TRANSFER_FAMILY_POLICY_SAME_FAMILY_MULTIPLIER = 1.02
META_TRANSFER_FAMILY_POLICY_GUARDED_MULTIPLIER = 0.93
META_TRANSFER_FAMILY_POLICY_CROSS_FAMILY_PROBE_MULTIPLIER = 0.95


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


def _edge_policy_distribution(
    steering_factors_by_source: dict[str, dict[str, float | bool | int | str]],
) -> dict[str, int]:
    distribution: dict[str, int] = {}
    for factors in steering_factors_by_source.values():
        policy = str(factors.get("edge_transfer_policy", "neutral_edge"))
        distribution[policy] = distribution.get(policy, 0) + 1
    return distribution


def _family_policy_distribution(
    steering_factors_by_source: dict[str, dict[str, float | bool | int | str]],
) -> dict[str, int]:
    distribution: dict[str, int] = {}
    for factors in steering_factors_by_source.values():
        policy = str(factors.get("family_transfer_policy", "neutral_family_policy"))
        distribution[policy] = distribution.get(policy, 0) + 1
    return distribution


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
            final_candidate_strength
            for _, _, _, _, final_candidate_strength in candidates
        ]
        total_strength = sum(candidate_strengths)
        source_shares = _normalize_source_shares(
            [candidate.profile_id for candidate, _, _, _, _ in candidates],
            (
                {
                    candidate.profile_id: strength / total_strength
                    for (candidate, _, _, _, _), strength in zip(
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
                "adjusted_similarity_score": steering_factors["adjusted_similarity_score"],
                "final_candidate_strength": steering_factors["final_candidate_strength"],
                "steering_weak_edge_penalty_applied": steering_factors[
                    "weak_edge_penalty_applied"
                ],
                "steering_proven_donor_boost_applied": steering_factors[
                    "proven_donor_boost_applied"
                ],
                "steering_edge_seeking_applied": steering_factors[
                    "edge_seeking_applied"
                ],
                "edge_seeking_reason": steering_factors["edge_seeking_reason"],
                "edge_transfer_policy": steering_factors["edge_transfer_policy"],
                "edge_transfer_policy_reason": steering_factors[
                    "edge_transfer_policy_reason"
                ],
                "edge_transfer_policy_multiplier": steering_factors[
                    "edge_transfer_policy_multiplier"
                ],
                "policy_adjusted_candidate_strength": steering_factors[
                    "policy_adjusted_candidate_strength"
                ],
                "family_transfer_policy": steering_factors["family_transfer_policy"],
                "family_transfer_policy_reason": steering_factors[
                    "family_transfer_policy_reason"
                ],
                "family_transfer_policy_multiplier": steering_factors[
                    "family_transfer_policy_multiplier"
                ],
                "source_family": steering_factors["source_family"],
                "target_family": steering_factors["target_family"],
                "family_pair_effectiveness": steering_factors[
                    "family_pair_effectiveness"
                ],
                "family_pair_samples": steering_factors["family_pair_samples"],
                "family_policy_adjusted_candidate_strength": steering_factors[
                    "family_policy_adjusted_candidate_strength"
                ],
                "adaptive_transfer_cap": self._adaptive_transfer_cap_info(
                    candidate.profile_id,
                    profile.profile_id,
                )["cap"],
                "adaptive_transfer_cap_reason": self._adaptive_transfer_cap_info(
                    candidate.profile_id,
                    profile.profile_id,
                )["reason"],
            }
            for candidate, similarity_score, historical_effectiveness, steering_factors, _ in candidates
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
                steering_weak_edge_penalty_applied,
                steering_proven_donor_boost_applied,
                steering_edge_seeking_applied,
                steering_edge_policy_applied,
                steering_family_policy_applied,
                meta_transfer_source_steering_factors,
                meta_transfer_source_adaptive_caps,
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
                        "steering_weak_edge_penalty_applied": (
                            steering_weak_edge_penalty_applied
                        ),
                        "steering_proven_donor_boost_applied": (
                            steering_proven_donor_boost_applied
                        ),
                        "steering_edge_seeking_applied": (
                            steering_edge_seeking_applied
                        ),
                        "steering_edge_policy_applied": (
                            steering_edge_policy_applied
                        ),
                        "steering_family_policy_applied": (
                            steering_family_policy_applied
                        ),
                        "meta_transfer_source_steering_factors": (
                            meta_transfer_source_steering_factors
                        ),
                        "meta_transfer_source_adaptive_caps": (
                            meta_transfer_source_adaptive_caps
                        ),
                        "edge_policy_distribution": _edge_policy_distribution(
                            meta_transfer_source_steering_factors
                        ),
                        "family_policy_distribution": _family_policy_distribution(
                            meta_transfer_source_steering_factors
                        ),
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
                    "adjusted_similarity_score": steering_factors["adjusted_similarity_score"],
                    "final_candidate_strength": steering_factors["final_candidate_strength"],
                    "steering_weak_edge_penalty_applied": steering_factors[
                        "weak_edge_penalty_applied"
                    ],
                    "steering_proven_donor_boost_applied": steering_factors[
                        "proven_donor_boost_applied"
                    ],
                    "steering_edge_seeking_applied": steering_factors[
                        "edge_seeking_applied"
                    ],
                    "edge_seeking_reason": steering_factors["edge_seeking_reason"],
                    "edge_transfer_policy": steering_factors["edge_transfer_policy"],
                    "edge_transfer_policy_reason": steering_factors[
                        "edge_transfer_policy_reason"
                    ],
                    "edge_transfer_policy_multiplier": steering_factors[
                        "edge_transfer_policy_multiplier"
                    ],
                    "policy_adjusted_candidate_strength": steering_factors[
                        "policy_adjusted_candidate_strength"
                    ],
                    "family_transfer_policy": steering_factors[
                        "family_transfer_policy"
                    ],
                    "family_transfer_policy_reason": steering_factors[
                        "family_transfer_policy_reason"
                    ],
                    "family_transfer_policy_multiplier": steering_factors[
                        "family_transfer_policy_multiplier"
                    ],
                    "source_family": steering_factors["source_family"],
                    "target_family": steering_factors["target_family"],
                    "family_pair_effectiveness": steering_factors[
                        "family_pair_effectiveness"
                    ],
                    "family_pair_samples": steering_factors["family_pair_samples"],
                    "family_policy_adjusted_candidate_strength": steering_factors[
                        "family_policy_adjusted_candidate_strength"
                    ],
                    "adaptive_transfer_cap": self._adaptive_transfer_cap_info(
                        candidate.profile_id,
                        profile.profile_id,
                    )["cap"],
                    "adaptive_transfer_cap_reason": self._adaptive_transfer_cap_info(
                        candidate.profile_id,
                        profile.profile_id,
                    )["reason"],
                }
                for candidate, similarity_score, historical_effectiveness, steering_factors, _ in meta_candidates
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

    def _weak_transfer_edge_keys(self) -> set[tuple[str, str]]:
        return {
            (edge["source_profile_id"], edge["target_profile_id"])
            for edge in self.compute_weak_transfers()
        }

    def _edge_effectiveness_history(
        self,
        source_profile_id: str,
        target_profile_id: str,
    ) -> list[float]:
        target_profile = self.get_profile(target_profile_id)
        if target_profile is None:
            return []

        donor_outcomes: list[float] = []
        for entry in self._effective_transfer_history_entries(target_profile):
            if source_profile_id not in entry.source_profile_ids:
                continue
            normalized_source_shares = _normalize_source_shares(
                entry.source_profile_ids,
                entry.source_shares,
            )
            share = normalized_source_shares.get(source_profile_id, 0.0)
            if share <= 0.0:
                continue
            donor_outcomes.append(entry.outcome_score * share)
        return donor_outcomes

    def _transfer_effectiveness_for_pair(
        self,
        source_profile_id: str,
        target_profile_id: str,
    ) -> float:
        donor_outcomes = self._edge_effectiveness_history(
            source_profile_id,
            target_profile_id,
        )
        if not donor_outcomes:
            return 0.0
        return fmean(donor_outcomes)

    def _adaptive_transfer_cap_info(
        self,
        source_profile_id: str,
        target_profile_id: str,
    ) -> dict[str, float | int | str]:
        donor_outcomes = self._edge_effectiveness_history(
            source_profile_id,
            target_profile_id,
        )
        history_samples = len(donor_outcomes)
        effectiveness = fmean(donor_outcomes) if donor_outcomes else 0.0

        if history_samples < META_TRANSFER_ADAPTIVE_HISTORY_MIN_SAMPLES:
            cap = META_TRANSFER_INSUFFICIENT_HISTORY_BLEND
            reason = "insufficient_history"
        elif effectiveness < META_TRANSFER_WEAK_EDGE_EFFECTIVENESS_THRESHOLD:
            cap = META_TRANSFER_WEAK_EDGE_MAX_BLEND
            reason = "weak_edge"
        elif effectiveness < META_TRANSFER_LOW_EFFECTIVENESS_THRESHOLD:
            cap = META_TRANSFER_LOW_EFFECTIVENESS_MAX_BLEND
            reason = "low_effectiveness"
        elif effectiveness < META_TRANSFER_STRONG_EDGE_EFFECTIVENESS_THRESHOLD:
            cap = META_TRANSFER_MAX_BLEND
            reason = "moderate"
        else:
            cap = META_TRANSFER_STRONG_EDGE_MAX_BLEND
            reason = "strong_edge"

        return {
            "cap": round(cap, 4),
            "reason": reason,
            "effectiveness_observed": round(effectiveness, 4),
            "history_samples": history_samples,
        }

    def _adaptive_transfer_max_blend(
        self,
        source_profile_id: str,
        target_profile_id: str,
    ) -> tuple[float, str]:
        cap_info = self._adaptive_transfer_cap_info(
            source_profile_id,
            target_profile_id,
        )
        return float(cap_info["cap"]), str(cap_info["reason"])

    def _profile_family_label(self, support_profile: str | None) -> str:
        return support_profile or "generic"

    def _target_profile_family_for_record(self, record: DecisionRecord) -> str:
        if record.transfer_target_profile_family_snapshot is not None:
            return self._profile_family_label(record.transfer_target_profile_family_snapshot)
        if record.calibration_profile_id is not None:
            target_profile = self.get_profile(record.calibration_profile_id)
            if target_profile is not None:
                return self._profile_family_label(
                    target_profile.stratification_dimensions.get("support_profile")
                )
        return self._profile_family_label(
            record.calibration_stratification_dimensions.get("support_profile")
        )

    def _source_profile_family_for_record(
        self,
        record: DecisionRecord,
        source_profile_id: str,
    ) -> str:
        if source_profile_id in record.transfer_source_profile_families_snapshot:
            return self._profile_family_label(
                record.transfer_source_profile_families_snapshot.get(source_profile_id)
            )
        source_factors = record.meta_transfer_source_steering_factors.get(
            source_profile_id,
            {},
        )
        if "source_support_profile" in source_factors:
            return self._profile_family_label(
                str(source_factors.get("source_support_profile")) or None
            )
        source_profile = self.get_profile(source_profile_id)
        if source_profile is None:
            return "generic"
        return self._profile_family_label(
            source_profile.stratification_dimensions.get("support_profile")
        )

    def _family_pair_effectiveness_history(
        self,
        source_family: str,
        target_family: str,
    ) -> list[float]:
        outcomes: list[float] = []
        for record in self.decision_log:
            if (
                record.observed_outcome is None
                or not record.meta_transfer_was_effective
                or not record.meta_transfer_source_profiles
            ):
                continue
            if self._target_profile_family_for_record(record) != target_family:
                continue

            outcome_score = self._compute_outcome_score(record.observed_outcome)
            normalized_shares = _normalize_source_shares(
                record.meta_transfer_source_profiles,
                record.meta_transfer_source_shares,
            )
            for source_profile_id in record.meta_transfer_source_profiles:
                if (
                    self._source_profile_family_for_record(record, source_profile_id)
                    != source_family
                ):
                    continue
                share = normalized_shares.get(source_profile_id, 0.0)
                if share <= 0.0:
                    continue
                outcomes.append(outcome_score * share)
        return outcomes

    def _family_pair_effectiveness_summary(
        self,
        source_family: str,
        target_family: str,
    ) -> dict[str, float | int]:
        outcomes = self._family_pair_effectiveness_history(source_family, target_family)
        return {
            "sample_size": len(outcomes),
            "effectiveness": round(fmean(outcomes), 4) if outcomes else 0.0,
        }

    def _family_transfer_policy_info(
        self,
        *,
        source_profile: CalibrationProfile,
        target_profile: CalibrationProfile,
        pair_effectiveness: float,
        edge_seeking_applied: bool,
    ) -> dict[str, float | str | int]:
        source_family = self._profile_family_label(
            source_profile.stratification_dimensions.get("support_profile")
        )
        target_family = self._profile_family_label(
            target_profile.stratification_dimensions.get("support_profile")
        )
        family_pair_summary = self._family_pair_effectiveness_summary(
            source_family,
            target_family,
        )
        family_pair_effectiveness = float(family_pair_summary["effectiveness"])
        family_pair_samples = int(family_pair_summary["sample_size"])

        if (
            family_pair_samples >= META_TRANSFER_FAMILY_POLICY_MIN_SAMPLES
            and family_pair_effectiveness
            >= META_TRANSFER_FAMILY_POLICY_STRONG_EFFECTIVENESS_THRESHOLD
        ):
            return {
                "policy": "trusted_family_pair",
                "reason": "prefer_historically_strong_family_pair",
                "multiplier": META_TRANSFER_FAMILY_POLICY_TRUSTED_MULTIPLIER,
                "source_family": source_family,
                "target_family": target_family,
                "family_pair_effectiveness": round(family_pair_effectiveness, 4),
                "family_pair_samples": family_pair_samples,
            }

        if (
            source_family == target_family
            and pair_effectiveness >= META_TRANSFER_FAMILY_POLICY_SAME_FAMILY_MIN_EFFECTIVENESS
        ):
            return {
                "policy": "same_family_preference",
                "reason": "prefer_same_support_family_with_nonweak_pair",
                "multiplier": META_TRANSFER_FAMILY_POLICY_SAME_FAMILY_MULTIPLIER,
                "source_family": source_family,
                "target_family": target_family,
                "family_pair_effectiveness": round(family_pair_effectiveness, 4),
                "family_pair_samples": family_pair_samples,
            }

        if (
            family_pair_samples >= META_TRANSFER_FAMILY_POLICY_MIN_SAMPLES
            and family_pair_effectiveness
            < META_TRANSFER_FAMILY_POLICY_WEAK_EFFECTIVENESS_THRESHOLD
        ):
            return {
                "policy": "guarded_family_pair",
                "reason": "downweight_historically_weak_family_pair",
                "multiplier": META_TRANSFER_FAMILY_POLICY_GUARDED_MULTIPLIER,
                "source_family": source_family,
                "target_family": target_family,
                "family_pair_effectiveness": round(family_pair_effectiveness, 4),
                "family_pair_samples": family_pair_samples,
            }

        if (
            edge_seeking_applied
            and source_family != target_family
            and family_pair_samples < META_TRANSFER_FAMILY_POLICY_MIN_SAMPLES
        ):
            return {
                "policy": "cross_family_probe_guard",
                "reason": "keep_cross_family_sparse_probe_conservative",
                "multiplier": META_TRANSFER_FAMILY_POLICY_CROSS_FAMILY_PROBE_MULTIPLIER,
                "source_family": source_family,
                "target_family": target_family,
                "family_pair_effectiveness": round(family_pair_effectiveness, 4),
                "family_pair_samples": family_pair_samples,
            }

        return {
            "policy": "neutral_family_policy",
            "reason": "no_additional_family_policy",
            "multiplier": 1.0,
            "source_family": source_family,
            "target_family": target_family,
            "family_pair_effectiveness": round(family_pair_effectiveness, 4),
            "family_pair_samples": family_pair_samples,
        }

    def _edge_transfer_policy_info(
        self,
        *,
        weak_edge_penalty_applied: bool,
        proven_donor_boost_applied: bool,
        edge_seeking_applied: bool,
        edge_seeking_reason: str,
        cap_reason: str,
    ) -> dict[str, float | str]:
        if proven_donor_boost_applied and cap_reason in {"moderate", "strong_edge"}:
            return {
                "policy": "trusted_edge",
                "reason": "prefer_proven_effective_edge",
                "multiplier": META_TRANSFER_EDGE_POLICY_TRUSTED_MULTIPLIER,
            }
        if (
            edge_seeking_applied
            and edge_seeking_reason == "probe_insufficient_history_for_sparse_target"
        ):
            return {
                "policy": "explore_edge",
                "reason": "probe_sparse_target_with_insufficient_history",
                "multiplier": META_TRANSFER_EDGE_POLICY_EXPLORE_MULTIPLIER,
            }
        if (
            edge_seeking_applied
            and edge_seeking_reason == "recover_weak_edge_for_sparse_target"
        ):
            return {
                "policy": "recovery_edge",
                "reason": "retest_guarded_edge_for_sparse_target",
                "multiplier": META_TRANSFER_EDGE_POLICY_RECOVERY_MULTIPLIER,
            }
        if weak_edge_penalty_applied or cap_reason == "weak_edge":
            return {
                "policy": "guarded_edge",
                "reason": "protect_target_from_weak_edge",
                "multiplier": META_TRANSFER_EDGE_POLICY_GUARDED_MULTIPLIER,
            }
        if cap_reason == "low_effectiveness":
            return {
                "policy": "cautious_edge",
                "reason": "downweight_low_effectiveness_edge",
                "multiplier": META_TRANSFER_EDGE_POLICY_CAUTIOUS_MULTIPLIER,
            }
        return {
            "policy": "neutral_edge",
            "reason": "no_additional_edge_policy",
            "multiplier": 1.0,
        }

    def _should_seek_edges_for_profile(
        self,
        target_profile: CalibrationProfile,
        candidate_diagnostics: list[dict[str, object]],
    ) -> bool:
        if target_profile.outcome_count >= PROFILE_PARTIAL_INHERITANCE_THRESHOLD:
            return False
        if not candidate_diagnostics:
            return False
        if any(
            bool(item["proven_donor_boost_applied"])
            or str(item["cap_reason"]) in {"moderate", "strong_edge"}
            for item in candidate_diagnostics
        ):
            return False

        exploratory_candidates = [
            item
            for item in candidate_diagnostics
            if float(item["similarity_score"]) >= META_TRANSFER_EDGE_SEEKING_MIN_SIMILARITY
        ]
        if not exploratory_candidates:
            return False
        if len(exploratory_candidates) < 2:
            return True
        return all(
            str(item["cap_reason"]) in {"insufficient_history", "weak_edge"}
            for item in exploratory_candidates
        )

    def _meta_transfer_candidates(
        self,
        target_profile: CalibrationProfile,
        *,
        excluded_profile_ids: set[str],
    ) -> list[
        tuple[
            CalibrationProfile,
            float,
            float,
            dict[str, float | bool | str],
            float,
        ]
    ]:
        ranked_candidates: list[
            tuple[
                CalibrationProfile,
                float,
                float,
                dict[str, float | bool | str],
                float,
            ]
        ] = []
        weak_edges = self._weak_transfer_edge_keys()
        candidate_diagnostics: list[dict[str, object]] = []

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
            pair_effectiveness = self._transfer_effectiveness_for_pair(
                candidate.profile_id,
                target_profile.profile_id,
            )
            penalty_multiplier = 1.0
            boost_multiplier = 1.0
            weak_edge_penalty_applied = (
                candidate.profile_id,
                target_profile.profile_id,
            ) in weak_edges
            if weak_edge_penalty_applied:
                penalty_multiplier = META_TRANSFER_WEAK_EDGE_PENALTY_MULTIPLIER
            proven_donor_boost_applied = (
                pair_effectiveness > META_TRANSFER_PROVEN_DONOR_EFFECTIVENESS_THRESHOLD
            )
            if proven_donor_boost_applied:
                boost_multiplier = META_TRANSFER_PROVEN_DONOR_BOOST_MULTIPLIER
            cap_info = self._adaptive_transfer_cap_info(
                candidate.profile_id,
                target_profile.profile_id,
            )
            candidate_diagnostics.append(
                {
                    "candidate": candidate,
                    "similarity_score": similarity_score,
                    "historical_effectiveness": historical_effectiveness,
                    "pair_effectiveness": pair_effectiveness,
                    "penalty_multiplier": penalty_multiplier,
                    "boost_multiplier": boost_multiplier,
                    "weak_edge_penalty_applied": weak_edge_penalty_applied,
                    "proven_donor_boost_applied": proven_donor_boost_applied,
                    "cap_reason": cap_info["reason"],
                }
            )

        edge_seeking_active = self._should_seek_edges_for_profile(
            target_profile,
            candidate_diagnostics,
        )

        for item in candidate_diagnostics:
            candidate = item["candidate"]
            similarity_score = float(item["similarity_score"])
            historical_effectiveness = float(item["historical_effectiveness"])
            pair_effectiveness = float(item["pair_effectiveness"])
            penalty_multiplier = float(item["penalty_multiplier"])
            boost_multiplier = float(item["boost_multiplier"])
            weak_edge_penalty_applied = bool(item["weak_edge_penalty_applied"])
            proven_donor_boost_applied = bool(item["proven_donor_boost_applied"])
            cap_reason = str(item["cap_reason"])

            edge_seeking_applied = False
            edge_seeking_multiplier = 1.0
            edge_seeking_reason = ""
            if (
                edge_seeking_active
                and not proven_donor_boost_applied
                and similarity_score >= META_TRANSFER_EDGE_SEEKING_MIN_SIMILARITY
            ):
                if weak_edge_penalty_applied:
                    edge_seeking_applied = True
                    edge_seeking_multiplier = (
                        META_TRANSFER_EDGE_SEEKING_WEAK_EDGE_RECOVERY_MULTIPLIER
                    )
                    edge_seeking_reason = "recover_weak_edge_for_sparse_target"
                elif cap_reason == "insufficient_history":
                    edge_seeking_applied = True
                    edge_seeking_multiplier = (
                        META_TRANSFER_EDGE_SEEKING_INSUFFICIENT_HISTORY_MULTIPLIER
                    )
                    edge_seeking_reason = "probe_insufficient_history_for_sparse_target"

            adjusted_similarity_score = max(
                0.0,
                min(
                    1.0,
                    similarity_score
                    * penalty_multiplier
                    * boost_multiplier
                    * edge_seeking_multiplier,
                ),
            )
            final_candidate_strength = (
                adjusted_similarity_score * candidate.confidence_score
            ) + (0.25 * historical_effectiveness)
            edge_policy_info = self._edge_transfer_policy_info(
                weak_edge_penalty_applied=weak_edge_penalty_applied,
                proven_donor_boost_applied=proven_donor_boost_applied,
                edge_seeking_applied=edge_seeking_applied,
                edge_seeking_reason=edge_seeking_reason,
                cap_reason=cap_reason,
            )
            edge_policy_multiplier = float(edge_policy_info["multiplier"])
            policy_adjusted_candidate_strength = final_candidate_strength * (
                edge_policy_multiplier
            )
            family_policy_info = self._family_transfer_policy_info(
                source_profile=candidate,
                target_profile=target_profile,
                pair_effectiveness=pair_effectiveness,
                edge_seeking_applied=edge_seeking_applied,
            )
            family_policy_multiplier = float(family_policy_info["multiplier"])
            family_policy_adjusted_candidate_strength = (
                policy_adjusted_candidate_strength * family_policy_multiplier
            )
            steering_factors: dict[str, float | bool | str] = {
                "base_similarity_score": round(similarity_score, 4),
                "adjusted_similarity_score": round(adjusted_similarity_score, 4),
                "historical_effectiveness": round(historical_effectiveness, 4),
                "pair_effectiveness": round(pair_effectiveness, 4),
                "source_support_profile": (
                    candidate.stratification_dimensions.get("support_profile")
                    or "generic"
                ),
                "target_support_profile": (
                    target_profile.stratification_dimensions.get("support_profile")
                    or "generic"
                ),
                "penalty_multiplier": round(penalty_multiplier, 4),
                "boost_multiplier": round(boost_multiplier, 4),
                "weak_edge_penalty_applied": weak_edge_penalty_applied,
                "proven_donor_boost_applied": proven_donor_boost_applied,
                "edge_seeking_applied": edge_seeking_applied,
                "edge_seeking_multiplier": round(edge_seeking_multiplier, 4),
                "edge_seeking_reason": edge_seeking_reason,
                "edge_seeking_target_sparse": edge_seeking_active,
                "final_candidate_strength": round(final_candidate_strength, 4),
                "edge_transfer_policy": str(edge_policy_info["policy"]),
                "edge_transfer_policy_reason": str(edge_policy_info["reason"]),
                "edge_transfer_policy_multiplier": round(edge_policy_multiplier, 4),
                "policy_adjusted_candidate_strength": round(
                    policy_adjusted_candidate_strength,
                    4,
                ),
                "family_transfer_policy": str(family_policy_info["policy"]),
                "family_transfer_policy_reason": str(family_policy_info["reason"]),
                "family_transfer_policy_multiplier": round(
                    family_policy_multiplier,
                    4,
                ),
                "source_family": str(family_policy_info["source_family"]),
                "target_family": str(family_policy_info["target_family"]),
                "family_pair_effectiveness": round(
                    float(family_policy_info["family_pair_effectiveness"]),
                    4,
                ),
                "family_pair_samples": int(family_policy_info["family_pair_samples"]),
                "family_policy_adjusted_candidate_strength": round(
                    family_policy_adjusted_candidate_strength,
                    4,
                ),
            }
            ranked_candidates.append(
                (
                    candidate,
                    similarity_score,
                    historical_effectiveness,
                    steering_factors,
                    family_policy_adjusted_candidate_strength,
                )
            )

        ranked_candidates.sort(
            key=lambda item: (
                item[4],
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
    ) -> tuple[
        dict[str, float] | None,
        float,
        list[str],
        dict[str, float],
        dict[str, dict[str, float | bool | int | str]],
        dict[str, dict[str, float | int | str]],
    ]:
        candidates = self._meta_transfer_candidates(
            selected_profile,
            excluded_profile_ids=excluded_profile_ids,
        )
        if not candidates:
            return None, 0.0, [], {}, {}, {}

        active_candidates: list[
            tuple[
                CalibrationProfile,
                float,
                float,
                dict[str, float | bool | str],
                float,
                float,
            ]
        ] = []
        adaptive_caps_by_source: dict[str, dict[str, float | int | str]] = {}

        for (
            candidate,
            similarity_score,
            historical_effectiveness,
            steering_factors,
            family_policy_adjusted_candidate_strength,
        ) in candidates:
            cap_info = self._adaptive_transfer_cap_info(
                candidate.profile_id,
                selected_profile.profile_id,
            )
            adaptive_candidate_strength = family_policy_adjusted_candidate_strength * (
                float(cap_info["cap"]) / META_TRANSFER_MAX_BLEND
            )
            if adaptive_candidate_strength <= 0.0:
                continue

            adaptive_caps_by_source[candidate.profile_id] = {
                **cap_info,
                "raw_candidate_strength": float(
                    steering_factors["final_candidate_strength"]
                ),
                "policy_adjusted_candidate_strength": float(
                    steering_factors["policy_adjusted_candidate_strength"]
                ),
                "family_policy_adjusted_candidate_strength": float(
                    steering_factors["family_policy_adjusted_candidate_strength"]
                ),
                "adaptive_candidate_strength": round(adaptive_candidate_strength, 4),
            }
            active_candidates.append(
                (
                    candidate,
                    similarity_score,
                    historical_effectiveness,
                    steering_factors,
                    family_policy_adjusted_candidate_strength,
                    adaptive_candidate_strength,
                )
            )

        if not active_candidates:
            return None, 0.0, [], {}, {}, {}

        candidate_strengths = [
            adaptive_candidate_strength
            for *_, adaptive_candidate_strength in active_candidates
        ]
        total_strength = sum(candidate_strengths)
        if total_strength <= 0.0:
            return None, 0.0, [], {}, {}, {}

        transfer_weights: dict[str, float] = {}
        all_components = {
            component
            for candidate, _, _, _, _, _ in active_candidates
            for component in candidate.current_weights.get_current_weights()
        }
        for component in all_components:
            transfer_weights[component] = sum(
                candidate.current_weights.get_current_weights().get(component, 0.0)
                * strength
                for (candidate, _, _, _, _, _), strength in zip(
                    active_candidates,
                    candidate_strengths,
                    strict=True,
                )
            ) / total_strength

        source_profiles = [candidate.profile_id for candidate, _, _, _, _, _ in active_candidates]
        source_shares = _normalize_source_shares(
            source_profiles,
            {
                candidate.profile_id: strength / total_strength
                for (candidate, _, _, _, _, _), strength in zip(
                    active_candidates,
                    candidate_strengths,
                    strict=True,
                )
            },
        )
        per_source_cap_limits = [
            float(adaptive_caps_by_source[source_id]["cap"]) / share
            for source_id, share in source_shares.items()
            if share > 0.0
        ]
        adaptive_global_cap = min(
            max(
                float(adaptive_caps_by_source[source_id]["cap"])
                for source_id in source_profiles
            ),
            min(per_source_cap_limits, default=META_TRANSFER_MAX_BLEND),
        )
        transfer_strength = min(
            adaptive_global_cap,
            total_strength / len(candidate_strengths),
        )
        steering_factors_by_source = {
            candidate.profile_id: {
                **steering_factors,
                "adaptive_transfer_cap": adaptive_caps_by_source[candidate.profile_id]["cap"],
                "adaptive_transfer_cap_reason": adaptive_caps_by_source[candidate.profile_id]["reason"],
                "adaptive_transfer_effectiveness_observed": adaptive_caps_by_source[
                    candidate.profile_id
                ]["effectiveness_observed"],
                "adaptive_transfer_history_samples": adaptive_caps_by_source[
                    candidate.profile_id
                ]["history_samples"],
                "raw_candidate_strength": adaptive_caps_by_source[candidate.profile_id][
                    "raw_candidate_strength"
                ],
                "policy_adjusted_candidate_strength": adaptive_caps_by_source[
                    candidate.profile_id
                ]["policy_adjusted_candidate_strength"],
                "family_policy_adjusted_candidate_strength": adaptive_caps_by_source[
                    candidate.profile_id
                ]["family_policy_adjusted_candidate_strength"],
                "adaptive_candidate_strength": adaptive_caps_by_source[candidate.profile_id][
                    "adaptive_candidate_strength"
                ],
                "applied_source_contribution": round(
                    transfer_strength * source_shares.get(candidate.profile_id, 0.0),
                    4,
                ),
            }
            for candidate, _, _, steering_factors, _, _ in active_candidates
        }
        adaptive_caps_by_source = {
            source_id: {
                **cap_info,
                "applied_source_contribution": round(
                    transfer_strength * source_shares.get(source_id, 0.0),
                    4,
                ),
            }
            for source_id, cap_info in adaptive_caps_by_source.items()
        }
        return (
            _normalize_weight_map(transfer_weights),
            transfer_strength,
            source_profiles,
            source_shares,
            steering_factors_by_source,
            adaptive_caps_by_source,
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
    ) -> tuple[
        dict[str, float],
        float,
        float,
        list[str],
        dict[str, float],
        float,
        bool,
        bool,
        bool,
        bool,
        bool,
        bool,
        dict[str, dict[str, float | bool | int | str]],
        dict[str, dict[str, float | int | str]],
    ]:
        if not profiles:
            return (
                self.current_weights.get_current_weights(),
                0.0,
                0.0,
                [],
                {},
                0.0,
                False,
                False,
                False,
                False,
                False,
                False,
                {},
                {},
            )

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
            meta_transfer_source_steering_factors,
            meta_transfer_source_adaptive_caps,
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
                False,
                False,
                False,
                False,
                False,
                {},
                {},
            )

        steering_weak_edge_penalty_applied = any(
            factor.get("weak_edge_penalty_applied", False)
            for factor in meta_transfer_source_steering_factors.values()
        )
        steering_proven_donor_boost_applied = any(
            factor.get("proven_donor_boost_applied", False)
            for factor in meta_transfer_source_steering_factors.values()
        )
        steering_edge_seeking_applied = any(
            factor.get("edge_seeking_applied", False)
            for factor in meta_transfer_source_steering_factors.values()
        )
        steering_edge_policy_applied = any(
            str(factor.get("edge_transfer_policy", "neutral_edge")) != "neutral_edge"
            for factor in meta_transfer_source_steering_factors.values()
        )
        steering_family_policy_applied = any(
            str(factor.get("family_transfer_policy", "neutral_family_policy"))
            != "neutral_family_policy"
            for factor in meta_transfer_source_steering_factors.values()
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
            steering_weak_edge_penalty_applied,
            steering_proven_donor_boost_applied,
            steering_edge_seeking_applied,
            steering_edge_policy_applied,
            steering_family_policy_applied,
            meta_transfer_source_steering_factors,
            meta_transfer_source_adaptive_caps,
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
