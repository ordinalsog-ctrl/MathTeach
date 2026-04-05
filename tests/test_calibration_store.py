from pathlib import Path

from mathteach.models import (
    CalibrationWeights,
    CalibrationWeightsSnapshot,
    DecisionAlternative,
    DecisionRecord,
    OutcomeMetrics,
)
from mathteach.services.calibration_store import CalibrationData, CalibrationStore


def test_store_loads_empty_data_when_file_missing(tmp_path: Path) -> None:
    store = CalibrationStore(tmp_path / "calibration.json")

    data = store.load()

    assert data.decision_records == []
    assert data.outcome_metrics == []
    assert isinstance(data.calibration_weights, CalibrationWeights)
    assert data.weights_history == []


def test_store_saves_and_loads_data_correctly(tmp_path: Path) -> None:
    store = CalibrationStore(tmp_path / "calibration.json")
    snapshot = CalibrationWeightsSnapshot(
        active_weights={"heuristic": 0.35, "goal_alignment": 0.2},
        trigger_decision_id="decision-1",
        outcome_score=0.82,
    )
    payload = CalibrationData(
        decision_records=[
            DecisionRecord(
                decision_id="decision-1",
                session_id="session-1",
                current_block_type="worked_example",
                chosen_path_id="path_1",
                chosen_path_score=0.78,
                chosen_path_score_breakdown={"heuristic": 0.7},
                alternative_paths=[
                    DecisionAlternative(
                        path_id="path_2",
                        score=0.7,
                        score_breakdown={"heuristic": 0.65},
                    )
                ],
            )
        ],
        outcome_metrics=[
            OutcomeMetrics(
                observed_evidence=["visible_small_success"],
                mastery_gain_estimate=0.3,
                observed_engagement="high",
            )
        ],
        calibration_weights=CalibrationWeights(),
        weights_history=[snapshot],
    )

    store.save(payload)
    loaded = store.load()

    assert len(loaded.decision_records) == 1
    assert loaded.decision_records[0].decision_id == "decision-1"
    assert len(loaded.outcome_metrics) == 1
    assert len(loaded.weights_history) == 1
    assert loaded.weights_history[0].trigger_decision_id == "decision-1"


def test_store_statistics_report_recent_success_and_stability(tmp_path: Path) -> None:
    store = CalibrationStore(tmp_path / "calibration.json")
    store.save(
        CalibrationData(
            outcome_metrics=[
                OutcomeMetrics(
                    mastery_gain_estimate=0.5,
                    observed_engagement="high",
                    error_rate_trend="improving",
                )
            ],
            weights_history=[
                CalibrationWeightsSnapshot(
                    active_weights={"heuristic": 0.4, "goal_alignment": 0.6},
                ),
                CalibrationWeightsSnapshot(
                    active_weights={"heuristic": 0.45, "goal_alignment": 0.55},
                ),
            ],
        )
    )

    stats = store.get_statistics()

    assert stats["total_outcomes"] == 1
    assert stats["recent_success_rate"] > 0.0
    assert 0.0 <= stats["weight_stability_index"] <= 1.0
