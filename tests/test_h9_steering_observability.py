from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient

from mathteach.main import app
from mathteach.models import (
    BlockSequenceIntent,
    BlockType,
    DecisionRecord,
    EvidenceCombinationPattern,
    OutcomeMetrics,
)
from mathteach.services.calibration_engine import CalibrationEngine
from mathteach.services.calibration_observability import (
    AdaptiveCapsTrendQuery,
    EdgePolicyTrendQuery,
    SteeringLogQuery,
)
from mathteach.services.calibration_store import CalibrationStore


client = TestClient(app)


def _decision_with_steering(
    *,
    decision_id: str,
    timestamp: datetime,
    session_id: str,
    target_profile_id: str = "target_profile",
    target_support_profile: str = "adhd_aware_support",
    source_id: str = "donor_profile",
    source_support_profile: str = "adhd_aware_support",
    weak_penalty: bool = False,
    proven_boost: bool = False,
    adaptive_reason: str = "insufficient_history",
    adaptive_cap: float = 0.3,
    edge_policy: str | None = None,
    edge_policy_multiplier: float | None = None,
    family_policy: str | None = None,
    family_policy_multiplier: float | None = None,
    observed_outcome_score: float | None = None,
    include_family_snapshots: bool = True,
) -> DecisionRecord:
    observed_outcome = (
        OutcomeMetrics(
            mastery_gain_estimate=observed_outcome_score,
            error_rate_trend="improving",
            observed_engagement="high",
            accuracy_estimate=observed_outcome_score,
        )
        if observed_outcome_score is not None
        else None
    )
    return DecisionRecord(
        decision_id=decision_id,
        timestamp=timestamp,
        session_id=session_id,
        current_block_type=BlockType.WORKED_EXAMPLE,
        selected_block_type=BlockType.WORKED_EXAMPLE,
        evidence_patterns=[EvidenceCombinationPattern.RAPID_CONSECUTIVE_SUCCESS],
        active_supports=["adhd_aware_support"],
        sequence_intent=BlockSequenceIntent.MASTERY_PATH,
        available_candidate_paths=[f"path_{decision_id}"],
        chosen_path_id=f"path_{decision_id}",
        chosen_path_score=0.7,
        chosen_path_score_breakdown={"heuristic": 0.7},
        calibration_profile_id=target_profile_id,
        calibration_stratification_dimensions={
            "support_profile": target_support_profile,
        },
        transfer_target_profile_family_snapshot=(
            target_support_profile if include_family_snapshots else None
        ),
        transfer_source_profile_families_snapshot=(
            {source_id: source_support_profile} if include_family_snapshots else {}
        ),
        meta_transfer_strength=min(1.0, adaptive_cap),
        meta_transfer_source_profiles=[source_id],
        meta_transfer_source_shares={source_id: 1.0},
        meta_transfer_weight_delta=0.08,
        meta_transfer_was_effective=True,
        steering_weak_edge_penalty_applied=weak_penalty,
        steering_proven_donor_boost_applied=proven_boost,
        steering_edge_policy_applied=edge_policy not in (None, "neutral_edge"),
        steering_family_policy_applied=(
            family_policy not in (None, "neutral_family_policy")
        ),
        meta_transfer_source_steering_factors={
            source_id: {
                "weak_edge_penalty_applied": weak_penalty,
                "proven_donor_boost_applied": proven_boost,
                "penalty_multiplier": 0.6 if weak_penalty else 1.0,
                "boost_multiplier": 1.3 if proven_boost else 1.0,
                "edge_transfer_policy": edge_policy or "neutral_edge",
                "edge_transfer_policy_reason": (
                    "test_policy"
                    if edge_policy not in (None, "neutral_edge")
                    else "no_additional_edge_policy"
                ),
                "edge_transfer_policy_multiplier": (
                    edge_policy_multiplier
                    if edge_policy_multiplier is not None
                    else 1.0
                ),
                "family_transfer_policy": family_policy or "neutral_family_policy",
                "family_transfer_policy_reason": (
                    "test_family_policy"
                    if family_policy not in (None, "neutral_family_policy")
                    else "no_additional_family_policy"
                ),
                "family_transfer_policy_multiplier": (
                    family_policy_multiplier
                    if family_policy_multiplier is not None
                    else 1.0
                ),
                "source_family": source_support_profile,
                "target_family": target_support_profile,
                "family_pair_effectiveness": (
                    observed_outcome_score if observed_outcome_score is not None else 0.0
                ),
                "family_pair_samples": 4,
                "source_support_profile": source_support_profile,
                "target_support_profile": target_support_profile,
                "adaptive_transfer_cap": adaptive_cap,
                "adaptive_transfer_cap_reason": adaptive_reason,
            }
        },
        meta_transfer_source_adaptive_caps={
            source_id: {
                "cap": adaptive_cap,
                "reason": adaptive_reason,
                "effectiveness_observed": 0.15 if adaptive_reason == "weak_edge" else 0.8,
                "history_samples": 5,
            }
        },
        observed_outcome=observed_outcome,
        outcome_timestamp=(timestamp + timedelta(minutes=5)) if observed_outcome else None,
    )


def test_steering_log_query_filters_penalized_edges() -> None:
    engine = CalibrationEngine(min_samples_for_calibration=999)
    now = datetime.now(UTC)
    engine.decision_log = [
        _decision_with_steering(
            decision_id="weak",
            timestamp=now,
            session_id="session_weak",
            weak_penalty=True,
            adaptive_reason="weak_edge",
            adaptive_cap=0.2,
        ),
        _decision_with_steering(
            decision_id="boost_only",
            timestamp=now,
            session_id="session_boost",
            proven_boost=True,
            adaptive_reason="strong_edge",
            adaptive_cap=0.45,
        ),
    ]

    query = SteeringLogQuery(engine)
    entries = query.get_steering_decisions(
        include_weak_edges=True,
        include_proven_boost=False,
        include_adaptive_caps=False,
    )

    assert len(entries) == 1
    assert entries[0].decision_id == "weak"
    assert entries[0].weak_edge_penalty_applied is True
    assert entries[0].weak_edge_penalty_factor == 0.6


def test_steering_log_query_filters_boosted_donors() -> None:
    engine = CalibrationEngine(min_samples_for_calibration=999)
    now = datetime.now(UTC)
    engine.decision_log = [
        _decision_with_steering(
            decision_id="plain",
            timestamp=now,
            session_id="session_plain",
            adaptive_reason="moderate",
            adaptive_cap=0.35,
        ),
        _decision_with_steering(
            decision_id="boosted",
            timestamp=now,
            session_id="session_boost",
            proven_boost=True,
            adaptive_reason="strong_edge",
            adaptive_cap=0.45,
            observed_outcome_score=0.8,
        ),
    ]

    query = SteeringLogQuery(engine)
    entries = query.get_steering_decisions(
        include_weak_edges=False,
        include_proven_boost=True,
        include_adaptive_caps=False,
    )

    assert len(entries) == 1
    assert entries[0].decision_id == "boosted"
    assert entries[0].proven_donor_boost_applied is True
    assert entries[0].proven_donor_boost_factor == 1.3
    assert entries[0].outcome_recorded is True
    assert entries[0].observed_outcome_score is not None


def test_steering_log_query_filters_edge_seeking_decisions() -> None:
    engine = CalibrationEngine(min_samples_for_calibration=999)
    now = datetime.now(UTC)
    edge_seeking_record = _decision_with_steering(
        decision_id="edge_seeking",
        timestamp=now,
        session_id="session_edge",
        source_id="edge_donor",
        adaptive_reason="insufficient_history",
        adaptive_cap=0.3,
    ).model_copy(
        update={
            "steering_edge_seeking_applied": True,
            "meta_transfer_source_steering_factors": {
                "edge_donor": {
                    "weak_edge_penalty_applied": False,
                    "proven_donor_boost_applied": False,
                    "edge_seeking_applied": True,
                    "edge_seeking_multiplier": 1.15,
                    "edge_seeking_reason": "probe_insufficient_history_for_sparse_target",
                    "adaptive_transfer_cap": 0.3,
                    "adaptive_transfer_cap_reason": "insufficient_history",
                }
            },
        }
    )
    engine.decision_log = [
        _decision_with_steering(
            decision_id="plain_caps_only",
            timestamp=now - timedelta(minutes=5),
            session_id="session_plain",
            adaptive_reason="moderate",
            adaptive_cap=0.35,
        ),
        edge_seeking_record,
    ]

    query = SteeringLogQuery(engine)
    entries = query.get_steering_decisions(
        include_weak_edges=False,
        include_proven_boost=False,
        include_adaptive_caps=False,
        include_edge_seeking=True,
    )

    assert len(entries) == 1
    assert entries[0].decision_id == "edge_seeking"
    assert entries[0].edge_seeking_applied is True
    assert entries[0].edge_seeking_factor == 1.15
    assert entries[0].edge_seeking_sources == ["edge_donor"]


def test_steering_log_query_filters_edge_policy_decisions() -> None:
    engine = CalibrationEngine(min_samples_for_calibration=999)
    now = datetime.now(UTC)
    engine.decision_log = [
        _decision_with_steering(
            decision_id="neutral_caps_only",
            timestamp=now - timedelta(minutes=5),
            session_id="session_plain",
            adaptive_reason="moderate",
            adaptive_cap=0.35,
        ),
        _decision_with_steering(
            decision_id="trusted_policy",
            timestamp=now,
            session_id="session_policy",
            source_id="policy_donor",
            proven_boost=True,
            adaptive_reason="strong_edge",
            adaptive_cap=0.45,
            edge_policy="trusted_edge",
            edge_policy_multiplier=1.05,
        ),
    ]

    query = SteeringLogQuery(engine)
    entries = query.get_steering_decisions(
        include_weak_edges=False,
        include_proven_boost=False,
        include_adaptive_caps=False,
        include_edge_seeking=False,
        include_edge_policy=True,
    )

    assert len(entries) == 1
    assert entries[0].decision_id == "trusted_policy"
    assert entries[0].edge_policy_applied is True
    assert entries[0].edge_policy_sources == ["policy_donor"]
    assert entries[0].edge_policy_distribution["trusted_edge"] == 1


def test_steering_log_query_filters_family_policy_decisions() -> None:
    engine = CalibrationEngine(min_samples_for_calibration=999)
    now = datetime.now(UTC)
    engine.decision_log = [
        _decision_with_steering(
            decision_id="neutral_family",
            timestamp=now - timedelta(minutes=5),
            session_id="session_plain",
            adaptive_reason="moderate",
            adaptive_cap=0.35,
        ),
        _decision_with_steering(
            decision_id="family_policy",
            timestamp=now,
            session_id="session_family",
            source_id="family_donor",
            source_support_profile="adhd_aware_support",
            target_support_profile="adhd_aware_support",
            family_policy="same_family_preference",
            family_policy_multiplier=1.02,
            observed_outcome_score=0.6,
        ),
    ]

    query = SteeringLogQuery(engine)
    entries = query.get_steering_decisions(
        include_weak_edges=False,
        include_proven_boost=False,
        include_adaptive_caps=False,
        include_edge_seeking=False,
        include_edge_policy=False,
        include_family_policy=True,
    )

    assert len(entries) == 1
    assert entries[0].decision_id == "family_policy"
    assert entries[0].family_policy_applied is True
    assert entries[0].family_policy_factor == 1.02
    assert entries[0].family_policy_sources == ["family_donor"]
    assert entries[0].family_policy_distribution == {"same_family_preference": 1}


def test_steering_log_exposes_cross_family_probe_budget_metadata() -> None:
    engine = CalibrationEngine(min_samples_for_calibration=999)
    now = datetime.now(UTC)
    engine.decision_log = [
        _decision_with_steering(
            decision_id="family_budget_guard",
            timestamp=now,
            session_id="session_budget",
            source_id="budget_donor",
            source_support_profile="adhd_aware_support+language_sensitive_support",
            target_support_profile="adhd_aware_support",
            family_policy="cross_family_probe_budget_guard",
            family_policy_multiplier=0.88,
        ).model_copy(
            update={
                "meta_transfer_source_steering_factors": {
                    "budget_donor": {
                        "family_transfer_policy": "cross_family_probe_budget_guard",
                        "family_transfer_policy_reason": "limit_repeated_cross_family_probes_without_signal",
                        "family_transfer_policy_multiplier": 0.88,
                        "source_support_profile": "adhd_aware_support+language_sensitive_support",
                        "target_support_profile": "adhd_aware_support",
                        "source_family": "adhd_aware_support+language_sensitive_support",
                        "target_family": "adhd_aware_support",
                        "family_pair_effectiveness": 0.0,
                        "family_pair_samples": 1,
                        "cross_family_recent_probe_count": 2,
                        "cross_family_recent_success_count": 0,
                        "cross_family_probe_budget_remaining": 0,
                        "cross_family_probe_budget_exhausted": True,
                    }
                }
            }
        )
    ]

    entries = SteeringLogQuery(engine).get_steering_decisions(
        include_weak_edges=False,
        include_proven_boost=False,
        include_adaptive_caps=False,
        include_edge_seeking=False,
        include_edge_policy=False,
        include_family_policy=True,
    )

    assert len(entries) == 1
    factors = entries[0].meta_transfer_source_steering_factors["budget_donor"]
    assert factors["cross_family_recent_probe_count"] == 2
    assert factors["cross_family_recent_success_count"] == 0
    assert factors["cross_family_probe_budget_remaining"] == 0
    assert factors["cross_family_probe_budget_exhausted"] is True


def test_steering_log_includes_profile_families() -> None:
    engine = CalibrationEngine(min_samples_for_calibration=999)
    now = datetime.now(UTC)
    engine.decision_log = [
        _decision_with_steering(
            decision_id="family_view",
            timestamp=now,
            session_id="family_session",
            source_id="language_donor",
            source_support_profile="language_sensitive_support",
            target_support_profile="adhd_aware_support",
            edge_policy="explore_edge",
            edge_policy_multiplier=1.02,
        )
    ]

    entries = SteeringLogQuery(engine).get_steering_decisions(
        include_weak_edges=False,
        include_proven_boost=False,
        include_adaptive_caps=False,
        include_edge_seeking=False,
        include_edge_policy=True,
    )

    assert len(entries) == 1
    assert entries[0].transfer_target_profile_family == "adhd_aware_support"
    assert (
        entries[0].transfer_source_profile_families["language_donor"]
        == "language_sensitive_support"
    )


def test_steering_log_prefers_persisted_family_snapshots() -> None:
    engine = CalibrationEngine(min_samples_for_calibration=999)
    now = datetime.now(UTC)
    engine.decision_log = [
        _decision_with_steering(
            decision_id="snapshot_family_view",
            timestamp=now,
            session_id="family_snapshot_session",
            source_id="snapshot_donor",
            source_support_profile="language_sensitive_support",
            target_support_profile="adhd_aware_support",
        ).model_copy(
            update={
                "transfer_target_profile_family_snapshot": "legacy_target_family",
                "transfer_source_profile_families_snapshot": {
                    "snapshot_donor": "legacy_source_family"
                },
                "calibration_stratification_dimensions": {
                    "support_profile": "reclassified_target_family"
                },
                "meta_transfer_source_steering_factors": {
                    "snapshot_donor": {
                        "source_support_profile": "reclassified_source_family",
                        "target_support_profile": "reclassified_target_family",
                    }
                },
            }
        )
    ]

    entries = SteeringLogQuery(engine).get_steering_decisions(
        include_weak_edges=False,
        include_proven_boost=False,
        include_adaptive_caps=True,
        include_edge_seeking=False,
        include_edge_policy=False,
        include_family_policy=False,
    )

    assert len(entries) == 1
    assert entries[0].transfer_target_profile_family == "legacy_target_family"
    assert (
        entries[0].transfer_source_profile_families["snapshot_donor"]
        == "legacy_source_family"
    )


def test_steering_log_falls_back_when_family_snapshots_are_missing() -> None:
    engine = CalibrationEngine(min_samples_for_calibration=999)
    now = datetime.now(UTC)
    engine.decision_log = [
        _decision_with_steering(
            decision_id="fallback_family_view",
            timestamp=now,
            session_id="family_fallback_session",
            source_id="fallback_donor",
            source_support_profile="language_sensitive_support",
            target_support_profile="adhd_aware_support",
            include_family_snapshots=False,
        )
    ]

    entries = SteeringLogQuery(engine).get_steering_decisions(
        include_weak_edges=False,
        include_proven_boost=False,
        include_adaptive_caps=True,
        include_edge_seeking=False,
        include_edge_policy=False,
        include_family_policy=False,
    )

    assert len(entries) == 1
    assert entries[0].transfer_target_profile_family == "adhd_aware_support"
    assert (
        entries[0].transfer_source_profile_families["fallback_donor"]
        == "language_sensitive_support"
    )


def test_adaptive_caps_trends_aggregates_by_reason() -> None:
    engine = CalibrationEngine(min_samples_for_calibration=999)
    now = datetime.now(UTC)
    engine.decision_log = [
        _decision_with_steering(
            decision_id="weak_a",
            timestamp=now,
            session_id="s1",
            source_id="donor_a",
            adaptive_reason="weak_edge",
            adaptive_cap=0.2,
        ),
        _decision_with_steering(
            decision_id="weak_b",
            timestamp=now - timedelta(minutes=10),
            session_id="s2",
            source_id="donor_b",
            adaptive_reason="weak_edge",
            adaptive_cap=0.2,
        ),
        _decision_with_steering(
            decision_id="strong",
            timestamp=now - timedelta(minutes=20),
            session_id="s3",
            source_id="donor_c",
            adaptive_reason="strong_edge",
            adaptive_cap=0.45,
        ),
    ]

    query = AdaptiveCapsTrendQuery(engine)
    trends = query.get_cap_distribution_trends(aggregate_by="reason")

    assert trends["weak_edge"].count == 2
    assert trends["weak_edge"].avg_cap == 0.2
    assert trends["strong_edge"].count == 1
    assert trends["strong_edge"].max_cap == 0.45


def test_adaptive_caps_trends_respects_time_window() -> None:
    engine = CalibrationEngine(min_samples_for_calibration=999)
    now = datetime.now(UTC)
    engine.decision_log = [
        _decision_with_steering(
            decision_id="recent",
            timestamp=now - timedelta(hours=2),
            session_id="recent_session",
            source_id="recent_donor",
            adaptive_reason="weak_edge",
            adaptive_cap=0.2,
        ),
        _decision_with_steering(
            decision_id="older",
            timestamp=now - timedelta(hours=48),
            session_id="older_session",
            source_id="older_donor",
            adaptive_reason="strong_edge",
            adaptive_cap=0.45,
        ),
    ]

    query = AdaptiveCapsTrendQuery(engine)
    trends_24h = query.get_cap_distribution_trends(time_window_hours=24)
    trends_72h = query.get_cap_distribution_trends(time_window_hours=72)

    assert "weak_edge" in trends_24h
    assert "strong_edge" not in trends_24h
    assert "strong_edge" in trends_72h


def test_edge_policy_trends_aggregate_by_family_pair() -> None:
    engine = CalibrationEngine(min_samples_for_calibration=999)
    now = datetime.now(UTC)
    engine.decision_log = [
        _decision_with_steering(
            decision_id="trusted_same_family",
            timestamp=now,
            session_id="s1",
            source_id="donor_a",
            source_support_profile="adhd_aware_support",
            target_support_profile="adhd_aware_support",
            edge_policy="trusted_edge",
            edge_policy_multiplier=1.05,
            proven_boost=True,
            adaptive_reason="strong_edge",
            adaptive_cap=0.45,
        ),
        _decision_with_steering(
            decision_id="guarded_cross_family",
            timestamp=now - timedelta(minutes=30),
            session_id="s2",
            source_id="donor_b",
            source_support_profile="language_sensitive_support",
            target_support_profile="adhd_aware_support",
            edge_policy="guarded_edge",
            edge_policy_multiplier=0.9,
            weak_penalty=True,
            adaptive_reason="weak_edge",
            adaptive_cap=0.2,
        ),
    ]

    trends = EdgePolicyTrendQuery(engine).get_policy_trends(
        aggregate_by="family_pair"
    )

    assert "adhd_aware_support->adhd_aware_support" in trends
    assert "language_sensitive_support->adhd_aware_support" in trends
    assert (
        trends["adhd_aware_support->adhd_aware_support"].policy_distribution[
            "trusted_edge"
        ]
        == 1
    )
    assert (
        trends["language_sensitive_support->adhd_aware_support"].policy_distribution[
            "guarded_edge"
        ]
        == 1
    )


def test_edge_policy_trends_prefer_persisted_family_snapshots() -> None:
    engine = CalibrationEngine(min_samples_for_calibration=999)
    now = datetime.now(UTC)
    engine.decision_log = [
        _decision_with_steering(
            decision_id="snapshot_policy_pair",
            timestamp=now,
            session_id="snapshot_pair_session",
            source_id="policy_snapshot_donor",
            source_support_profile="language_sensitive_support",
            target_support_profile="adhd_aware_support",
            edge_policy="guarded_edge",
            edge_policy_multiplier=0.9,
            include_family_snapshots=True,
        ).model_copy(
            update={
                "transfer_target_profile_family_snapshot": "legacy_target_family",
                "transfer_source_profile_families_snapshot": {
                    "policy_snapshot_donor": "legacy_source_family"
                },
                "calibration_stratification_dimensions": {
                    "support_profile": "reclassified_target_family"
                },
                "meta_transfer_source_steering_factors": {
                    "policy_snapshot_donor": {
                        "edge_transfer_policy": "guarded_edge",
                        "edge_transfer_policy_multiplier": 0.9,
                        "pair_effectiveness": 0.1,
                        "source_support_profile": "reclassified_source_family",
                        "target_support_profile": "reclassified_target_family",
                    }
                },
            }
        )
    ]

    trends = EdgePolicyTrendQuery(engine).get_policy_trends(
        aggregate_by="family_pair"
    )

    assert "legacy_source_family->legacy_target_family" in trends


def test_steering_observability_api_endpoints_return_valid_schema(tmp_path) -> None:
    store_path = tmp_path / "steering_observability.json"
    engine = CalibrationEngine(
        min_samples_for_calibration=999,
        store=CalibrationStore(store_path),
    )
    now = datetime.now(UTC)
    engine.decision_log = [
        _decision_with_steering(
            decision_id="api_weak",
            timestamp=now,
            session_id="api_session",
            weak_penalty=True,
            source_id="api_donor_weak",
            adaptive_reason="weak_edge",
            adaptive_cap=0.2,
            edge_policy="guarded_edge",
            edge_policy_multiplier=0.9,
            family_policy="guarded_family_pair",
            family_policy_multiplier=0.93,
            source_support_profile="language_sensitive_support",
            target_support_profile="adhd_aware_support",
        ),
        _decision_with_steering(
            decision_id="api_strong",
            timestamp=now - timedelta(minutes=30),
            session_id="api_session",
            proven_boost=True,
            source_id="api_donor_strong",
            adaptive_reason="strong_edge",
            adaptive_cap=0.45,
            edge_policy="trusted_edge",
            edge_policy_multiplier=1.05,
            family_policy="same_family_preference",
            family_policy_multiplier=1.02,
            observed_outcome_score=0.85,
        ).model_copy(
            update={
                "steering_edge_seeking_applied": True,
                "steering_edge_policy_applied": True,
                "steering_family_policy_applied": True,
                "meta_transfer_source_steering_factors": {
                    "api_donor_strong": {
                        "weak_edge_penalty_applied": False,
                        "proven_donor_boost_applied": True,
                        "boost_multiplier": 1.3,
                        "edge_seeking_applied": True,
                        "edge_seeking_multiplier": 1.15,
                        "edge_seeking_reason": "probe_insufficient_history_for_sparse_target",
                        "edge_transfer_policy": "trusted_edge",
                        "edge_transfer_policy_reason": "prefer_proven_effective_edge",
                        "edge_transfer_policy_multiplier": 1.05,
                        "family_transfer_policy": "same_family_preference",
                        "family_transfer_policy_reason": "prefer_same_support_family_with_nonweak_pair",
                        "family_transfer_policy_multiplier": 1.02,
                        "source_support_profile": "adhd_aware_support",
                        "target_support_profile": "adhd_aware_support",
                        "source_family": "adhd_aware_support",
                        "target_family": "adhd_aware_support",
                        "family_pair_effectiveness": 0.85,
                        "family_pair_samples": 4,
                        "adaptive_transfer_cap": 0.45,
                        "adaptive_transfer_cap_reason": "strong_edge",
                    }
                },
            }
        ),
    ]
    engine.force_save()

    log_response = client.get(
        "/api/v1/admin/calibration/steering-log",
        params={"store_path": str(store_path), "session_id": "api_session"},
    )
    trends_response = client.get(
        "/api/v1/admin/calibration/adaptive-caps-trends",
        params={"store_path": str(store_path), "aggregate_by": "reason"},
    )
    policy_trends_response = client.get(
        "/api/v1/admin/calibration/edge-policy-trends",
        params={"store_path": str(store_path), "aggregate_by": "family_pair"},
    )

    assert log_response.status_code == 200
    assert trends_response.status_code == 200
    assert policy_trends_response.status_code == 200

    log_payload = log_response.json()
    trends_payload = trends_response.json()
    policy_trends_payload = policy_trends_response.json()

    assert log_payload["total_count"] == 2
    assert log_payload["entries"][0]["adaptive_cap_distribution"]
    assert "meta_transfer_source_adaptive_caps" in log_payload["entries"][0]
    assert "edge_seeking_applied" in log_payload["entries"][0]
    assert "edge_policy_applied" in log_payload["entries"][0]
    assert "edge_policy_distribution" in log_payload["entries"][0]
    assert "family_policy_applied" in log_payload["entries"][0]
    assert "family_policy_distribution" in log_payload["entries"][0]
    assert "transfer_target_profile_family" in log_payload["entries"][0]
    assert "transfer_source_profile_families" in log_payload["entries"][0]
    assert "weak_edge" in trends_payload["trends"]
    assert "strong_edge" in trends_payload["trends"]
    assert trends_payload["trends"]["weak_edge"]["avg_cap"] == 0.2
    assert "aggregate_by" in policy_trends_payload
    assert policy_trends_payload["aggregate_by"] == "family_pair"
    assert policy_trends_payload["trends"]
