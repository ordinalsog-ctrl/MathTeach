from __future__ import annotations

from datetime import UTC, datetime, timedelta
from statistics import fmean

from mathteach.models import (
    CapTrendAggregation,
    DecisionRecord,
    EdgePolicyTrendAggregation,
    SteeringLogEntry,
)
from mathteach.services.calibration_engine import CalibrationEngine


def _adaptive_cap_distribution(
    per_source_caps: dict[str, dict[str, float | int | str]],
) -> dict[str, dict[str, int | float]]:
    grouped: dict[str, dict[str, float | int]] = {}

    for cap_info in per_source_caps.values():
        reason = str(cap_info.get("reason", "unknown"))
        stats = grouped.setdefault(
            reason,
            {
                "count": 0,
                "total_cap": 0.0,
            },
        )
        stats["count"] += 1
        stats["total_cap"] += float(cap_info.get("cap", 0.0))

    return {
        reason: {
            "count": int(stats["count"]),
            "avg_cap": round(
                float(stats["total_cap"]) / max(1, int(stats["count"])),
                4,
            ),
        }
        for reason, stats in grouped.items()
    }


def _edge_policy_distribution(
    steering_factors_by_source: dict[str, dict[str, float | bool | int | str]],
) -> dict[str, int]:
    grouped: dict[str, int] = {}
    for factors in steering_factors_by_source.values():
        policy = str(factors.get("edge_transfer_policy", "neutral_edge"))
        grouped[policy] = grouped.get(policy, 0) + 1
    return grouped


def _profile_family_label(support_profile: str | None) -> str:
    return support_profile or "generic"


def _target_profile_family(
    engine: CalibrationEngine,
    record: DecisionRecord,
) -> str:
    target_profile = (
        engine.get_profile(record.calibration_profile_id)
        if record.calibration_profile_id is not None
        else None
    )
    if target_profile is not None:
        return _profile_family_label(
            target_profile.stratification_dimensions.get("support_profile")
        )
    return _profile_family_label(
        record.calibration_stratification_dimensions.get("support_profile")
    )


def _source_profile_family(
    engine: CalibrationEngine,
    source_id: str,
    factors: dict[str, float | bool | int | str],
) -> str:
    if "source_support_profile" in factors:
        return _profile_family_label(str(factors.get("source_support_profile")) or None)
    source_profile = engine.get_profile(source_id)
    if source_profile is None:
        return "generic"
    return _profile_family_label(
        source_profile.stratification_dimensions.get("support_profile")
    )


class SteeringLogQuery:
    def __init__(self, engine: CalibrationEngine) -> None:
        self.engine = engine

    def _cutoff(self, time_window_minutes: int) -> datetime:
        return datetime.now(UTC) - timedelta(minutes=time_window_minutes)

    def _decision_matches_filters(
        self,
        record: DecisionRecord,
        *,
        session_id: str | None,
        cutoff: datetime,
        include_weak_edges: bool,
        include_proven_boost: bool,
        include_adaptive_caps: bool,
        include_edge_seeking: bool,
        include_edge_policy: bool,
    ) -> bool:
        if record.timestamp < cutoff:
            return False
        if session_id is not None and record.session_id != session_id:
            return False
        if (record.meta_transfer_strength or 0.0) <= 0.0:
            return False
        if not record.meta_transfer_source_profiles:
            return False

        has_weak = record.steering_weak_edge_penalty_applied
        has_boost = record.steering_proven_donor_boost_applied
        has_caps = bool(record.meta_transfer_source_adaptive_caps)
        has_edge_seeking = record.steering_edge_seeking_applied
        has_edge_policy = record.steering_edge_policy_applied

        return any(
            (
                include_weak_edges and has_weak,
                include_proven_boost and has_boost,
                include_adaptive_caps and has_caps,
                include_edge_seeking and has_edge_seeking,
                include_edge_policy and has_edge_policy,
            )
        )

    def get_steering_decisions(
        self,
        *,
        session_id: str | None = None,
        time_window_minutes: int = 1440,
        include_weak_edges: bool = True,
        include_proven_boost: bool = True,
        include_adaptive_caps: bool = True,
        include_edge_seeking: bool = True,
        include_edge_policy: bool = True,
    ) -> list[SteeringLogEntry]:
        cutoff = self._cutoff(time_window_minutes)
        entries: list[SteeringLogEntry] = []

        for record in self.engine.decision_log:
            if not self._decision_matches_filters(
                record,
                session_id=session_id,
                cutoff=cutoff,
                include_weak_edges=include_weak_edges,
                include_proven_boost=include_proven_boost,
                include_adaptive_caps=include_adaptive_caps,
                include_edge_seeking=include_edge_seeking,
                include_edge_policy=include_edge_policy,
            ):
                continue

            steering_factors = record.meta_transfer_source_steering_factors
            target_family = _target_profile_family(self.engine, record)
            source_families = {
                source_id: _source_profile_family(self.engine, source_id, factors)
                for source_id, factors in steering_factors.items()
            }
            weak_sources = [
                source_id
                for source_id, factors in steering_factors.items()
                if bool(factors.get("weak_edge_penalty_applied", False))
            ]
            proven_sources = [
                source_id
                for source_id, factors in steering_factors.items()
                if bool(factors.get("proven_donor_boost_applied", False))
            ]
            weak_factor = (
                float(steering_factors[weak_sources[0]].get("penalty_multiplier", 0.0))
                if weak_sources
                else None
            )
            boost_factor = (
                float(steering_factors[proven_sources[0]].get("boost_multiplier", 0.0))
                if proven_sources
                else None
            )
            edge_seeking_sources = [
                source_id
                for source_id, factors in steering_factors.items()
                if bool(factors.get("edge_seeking_applied", False))
            ]
            edge_seeking_factor = (
                float(
                    steering_factors[edge_seeking_sources[0]].get(
                        "edge_seeking_multiplier",
                        0.0,
                    )
                )
                if edge_seeking_sources
                else None
            )
            edge_policy_sources = [
                source_id
                for source_id, factors in steering_factors.items()
                if str(factors.get("edge_transfer_policy", "neutral_edge"))
                != "neutral_edge"
            ]
            observed_outcome_score = (
                record.observed_outcome.composite_score()
                if record.observed_outcome is not None
                else None
            )

            entries.append(
                SteeringLogEntry(
                    decision_id=record.decision_id,
                    session_id=record.session_id,
                    timestamp=record.timestamp,
                    transfer_target_profile_id=record.calibration_profile_id,
                    transfer_target_profile_family=target_family,
                    transfer_source_profiles=record.meta_transfer_source_profiles,
                    transfer_source_profile_families=source_families,
                    weak_edge_penalty_applied=record.steering_weak_edge_penalty_applied,
                    weak_edge_penalty_sources=weak_sources,
                    weak_edge_penalty_factor=weak_factor,
                    proven_donor_boost_applied=record.steering_proven_donor_boost_applied,
                    proven_donor_boost_sources=proven_sources,
                    proven_donor_boost_factor=boost_factor,
                    edge_seeking_applied=record.steering_edge_seeking_applied,
                    edge_seeking_sources=edge_seeking_sources,
                    edge_seeking_factor=edge_seeking_factor,
                    edge_policy_applied=record.steering_edge_policy_applied,
                    edge_policy_sources=edge_policy_sources,
                    edge_policy_distribution=_edge_policy_distribution(
                        steering_factors
                    ),
                    adaptive_cap_distribution=_adaptive_cap_distribution(
                        record.meta_transfer_source_adaptive_caps
                    ),
                    meta_transfer_source_adaptive_caps=record.meta_transfer_source_adaptive_caps,
                    meta_transfer_source_shares=record.meta_transfer_source_shares,
                    meta_transfer_source_steering_factors=steering_factors,
                    meta_transfer_strength=record.meta_transfer_strength,
                    meta_transfer_weight_delta=record.meta_transfer_weight_delta,
                    meta_transfer_was_effective=record.meta_transfer_was_effective,
                    outcome_recorded=record.observed_outcome is not None,
                    observed_outcome_score=observed_outcome_score,
                )
            )

        entries.sort(key=lambda item: item.timestamp, reverse=True)
        return entries


class AdaptiveCapsTrendQuery:
    def __init__(self, engine: CalibrationEngine) -> None:
        self.engine = engine

    def _cutoff(self, time_window_hours: int) -> datetime:
        return datetime.now(UTC) - timedelta(hours=time_window_hours)

    def _aggregate_key(
        self,
        *,
        aggregate_by: str,
        source_id: str,
        cap_info: dict[str, float | int | str],
    ) -> str:
        if aggregate_by == "reason":
            return str(cap_info.get("reason", "unknown"))
        if aggregate_by == "profile":
            return source_id
        if aggregate_by == "effectiveness_bucket":
            effectiveness = float(cap_info.get("effectiveness_observed", 0.0))
            if effectiveness < 0.25:
                return "lt_0.25"
            if effectiveness < 0.5:
                return "0.25_to_0.49"
            if effectiveness < 0.7:
                return "0.50_to_0.69"
            return "gte_0.70"
        raise ValueError("Unsupported aggregate_by value.")

    def _trend_direction(
        self,
        points: list[tuple[datetime, float]],
    ) -> str:
        if len(points) < 2:
            return "stable"
        ordered = sorted(points, key=lambda item: item[0])
        midpoint = max(1, len(ordered) // 2)
        older = [cap for _, cap in ordered[:midpoint]]
        newer = [cap for _, cap in ordered[midpoint:]]
        if not newer:
            return "stable"
        older_avg = fmean(older)
        newer_avg = fmean(newer)
        if newer_avg - older_avg > 0.01:
            return "increasing"
        if older_avg - newer_avg > 0.01:
            return "decreasing"
        return "stable"

    def get_cap_distribution_trends(
        self,
        *,
        time_window_hours: int = 24,
        aggregate_by: str = "reason",
    ) -> dict[str, CapTrendAggregation]:
        cutoff = self._cutoff(time_window_hours)
        grouped_caps: dict[str, list[tuple[datetime, float, str]]] = {}

        for record in self.engine.decision_log:
            if record.timestamp < cutoff:
                continue
            if not record.meta_transfer_source_adaptive_caps:
                continue
            for source_id, cap_info in record.meta_transfer_source_adaptive_caps.items():
                key = self._aggregate_key(
                    aggregate_by=aggregate_by,
                    source_id=source_id,
                    cap_info=cap_info,
                )
                grouped_caps.setdefault(key, []).append(
                    (
                        record.timestamp,
                        float(cap_info.get("cap", 0.0)),
                        record.decision_id,
                    )
                )

        result: dict[str, CapTrendAggregation] = {}
        for key, points in grouped_caps.items():
            caps = [cap for _, cap, _ in points]
            result[key] = CapTrendAggregation(
                aggregate_key=key,
                count=len(caps),
                sample_size=len({decision_id for _, _, decision_id in points}),
                total_cap=round(sum(caps), 4),
                avg_cap=round(fmean(caps), 4),
                min_cap=round(min(caps), 4),
                max_cap=round(max(caps), 4),
                trend_direction=self._trend_direction(
                    [(timestamp, cap) for timestamp, cap, _ in points]
                ),
            )

        return result


class EdgePolicyTrendQuery:
    def __init__(self, engine: CalibrationEngine) -> None:
        self.engine = engine

    def _cutoff(self, time_window_hours: int) -> datetime:
        return datetime.now(UTC) - timedelta(hours=time_window_hours)

    def _aggregate_key(
        self,
        *,
        aggregate_by: str,
        policy: str,
        source_family: str,
        target_family: str,
    ) -> str:
        if aggregate_by == "policy":
            return policy
        if aggregate_by == "source_family":
            return source_family
        if aggregate_by == "target_family":
            return target_family
        if aggregate_by == "family_pair":
            return f"{source_family}->{target_family}"
        raise ValueError("Unsupported aggregate_by value.")

    def _trend_direction(
        self,
        points: list[tuple[datetime, float]],
    ) -> str:
        if len(points) < 2:
            return "stable"
        ordered = sorted(points, key=lambda item: item[0])
        midpoint = max(1, len(ordered) // 2)
        older = [value for _, value in ordered[:midpoint]]
        newer = [value for _, value in ordered[midpoint:]]
        if not newer:
            return "stable"
        older_avg = fmean(older)
        newer_avg = fmean(newer)
        if newer_avg - older_avg > 0.01:
            return "increasing"
        if older_avg - newer_avg > 0.01:
            return "decreasing"
        return "stable"

    def get_policy_trends(
        self,
        *,
        time_window_hours: int = 24,
        aggregate_by: str = "policy",
    ) -> dict[str, EdgePolicyTrendAggregation]:
        cutoff = self._cutoff(time_window_hours)
        grouped: dict[str, list[tuple[datetime, float, float, str, str]]] = {}

        for record in self.engine.decision_log:
            if record.timestamp < cutoff:
                continue
            if not record.meta_transfer_source_steering_factors:
                continue
            target_family = _target_profile_family(self.engine, record)
            for source_id, factors in record.meta_transfer_source_steering_factors.items():
                policy = str(factors.get("edge_transfer_policy", "neutral_edge"))
                source_family = _source_profile_family(self.engine, source_id, factors)
                key = self._aggregate_key(
                    aggregate_by=aggregate_by,
                    policy=policy,
                    source_family=source_family,
                    target_family=target_family,
                )
                grouped.setdefault(key, []).append(
                    (
                        record.timestamp,
                        float(factors.get("edge_transfer_policy_multiplier", 1.0)),
                        float(factors.get("pair_effectiveness", 0.0)),
                        policy,
                        record.decision_id,
                    )
                )

        result: dict[str, EdgePolicyTrendAggregation] = {}
        for key, points in grouped.items():
            multipliers = [multiplier for _, multiplier, _, _, _ in points]
            effectiveness_values = [
                pair_effectiveness
                for _, _, pair_effectiveness, _, _ in points
            ]
            policy_distribution: dict[str, int] = {}
            for _, _, _, policy, _ in points:
                policy_distribution[policy] = policy_distribution.get(policy, 0) + 1
            result[key] = EdgePolicyTrendAggregation(
                aggregate_key=key,
                count=len(points),
                sample_size=len({decision_id for *_, decision_id in points}),
                avg_policy_multiplier=round(fmean(multipliers), 4),
                min_policy_multiplier=round(min(multipliers), 4),
                max_policy_multiplier=round(max(multipliers), 4),
                avg_pair_effectiveness=round(fmean(effectiveness_values), 4),
                policy_distribution=policy_distribution,
                trend_direction=self._trend_direction(
                    [(timestamp, multiplier) for timestamp, multiplier, _, _, _ in points]
                ),
            )

        return result
