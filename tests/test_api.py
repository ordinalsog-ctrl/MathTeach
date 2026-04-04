from pathlib import Path
import uuid

from fastapi.testclient import TestClient

from mathteach.main import app, session_store
from mathteach.models import ModeAdaptationCheckpoint, ModeAdaptationState


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_stack_endpoint() -> None:
    response = client.get("/api/v1/stack")

    assert response.status_code == 200
    payload = response.json()
    assert payload["primary_choice"] == "gpt-5.4"


def test_foundation_endpoint() -> None:
    response = client.get("/api/v1/foundation")

    assert response.status_code == 200
    payload = response.json()
    assert payload["knowledge_core"]["name"] == "Knowledge Core"
    assert payload["teacher_mind"]["name"] == "Teacher Mind"


def test_corpus_blueprint_endpoint() -> None:
    response = client.get("/api/v1/corpus/blueprint")

    assert response.status_code == 200
    payload = response.json()
    assert payload["domains"][0]["priority"] == "P0"
    assert "pedagogical literature" in payload["out_of_scope_for_now"]


def test_corpus_chronology_endpoint() -> None:
    response = client.get("/api/v1/corpus/chronology")

    assert response.status_code == 200
    payload = response.json()
    assert payload["eras"][0]["slug"] == "antiquity"
    assert payload["eras"][1]["canonical_figures"][0] == "Brahmagupta"
    assert payload["eras"][-1]["slug"] == "modern-mathematics"
    assert "Hilbert: Grundlagen der Geometrie" in payload["eras"][-1]["canonical_works"]
    assert "Russell and Whitehead: Principia Mathematica" in payload["eras"][-1]["canonical_works"]
    assert "Nicolas Bourbaki: Elements of Mathematics (Theory of Sets)" in payload["eras"][-1]["canonical_works"]


def test_corpus_source_access_endpoint() -> None:
    response = client.get("/api/v1/corpus/source-access")

    assert response.status_code == 200
    payload = response.json()
    assert payload["sources"][0]["slug"] == "rhind-mathematical-papyrus"
    assert payload["sources"][2]["access_routes"][0]["provider"] == "Clay Mathematics Institute"
    assert any(item["slug"] == "apollonius-conics" for item in payload["sources"])
    assert any(item["slug"] == "aryabhata-aryabhatiya" for item in payload["sources"])
    assert any(item["slug"] == "godel-undecidable-propositions" for item in payload["sources"])
    assert any(item["slug"] == "principia-mathematica" for item in payload["sources"])
    assert any(item["slug"] == "church-unsolvable-problem" for item in payload["sources"])
    assert any(item["slug"] == "grothendieck-tohoku-paper" for item in payload["sources"])
    assert any(item["slug"] == "napier-logarithmorum-canonis-descriptio" for item in payload["sources"])
    assert any(item["slug"] == "kepler-astronomia-nova" for item in payload["sources"])


def test_corpus_network_endpoint() -> None:
    response = client.get("/api/v1/corpus/network")

    assert response.status_code == 200
    payload = response.json()
    assert payload["proof_lines"][0]["slug"] == "exhaustion-to-integration-proof-line"
    assert any(item["slug"] == "hindu-arabic-number-transmission-path" for item in payload["transmission_paths"])
    assert any(item["slug"] == "logic-computation-domain-line" for item in payload["domain_lines"])
    assert any(item["slug"] == "chance-to-decision-bridge" for item in payload["application_bridges"])


def test_tutoring_plan_endpoint() -> None:
    response = client.post(
        "/api/v1/tutoring/plan",
        json={
            "objective": "Erklaere mir die quadratische Gleichung anschaulich.",
            "learner_profile": {
                "age_group": "teen",
                "math_level": "high_school",
                "confidence": "low",
                "preferred_pace": "balanced",
                "language": "de",
                "wants_visuals": True,
                "wants_history": True,
            },
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["lesson_mode"] == "guided_concept_explanation"
    assert payload["audience_mode"] == "teen"
    assert payload["mode_adaptation_state"]["current_mode"] == "guided_concept_explanation"
    assert payload["mode_adaptation_checkpoint"]["schema_version"] == "phase_h1_v1"
    assert (
        payload["mode_adaptation_checkpoint"]["mode_adaptation_state"]["current_mode"]
        == "guided_concept_explanation"
    )
    assert payload["mode_adaptation_state"]["blocks_in_current_mode"] == 0
    assert payload["planned_blocks"][0]["mode"] == "guided_concept_explanation"
    assert payload["mode_adaptation_trace"] == []
    assert payload["support_signal_profile"]["active_supports"] == []
    assert payload["response_settings"]["session_duration"] == "25_to_35_minute_guided_block"
    assert payload["retrieval_plan"]["include_history"] is True
    assert payload["retrieval_plan"]["history_mode"] == "supporting_only"
    assert payload["session_id"] is None
    assert payload["resume_context"]["resume_source"] == "fresh_start"
    assert payload["resume_context"]["resume_active"] is False


def test_tutoring_plan_origin_story_mode() -> None:
    response = client.post(
        "/api/v1/tutoring/plan",
        json={
            "objective": "Erklaere mir als Mathe-Laie die Differentialgleichung und warum sie notwendig wurde.",
            "learner_profile": {
                "age_group": "adult",
                "math_level": "high_school",
                "confidence": "low",
                "preferred_pace": "gentle",
                "language": "de",
                "wants_visuals": True,
                "wants_history": False,
            },
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["lesson_mode"] == "origin_story_explanation"
    assert payload["mode_selection"]["requested_mode"] == "origin_story_explanation"
    assert payload["mode_selection"]["selected_mode"] == "origin_story_explanation"
    assert payload["mode_adaptation_state"]["current_mode"] == "origin_story_explanation"
    assert payload["planned_blocks"][0]["mode"] == "origin_story_explanation"
    assert payload["response_settings"]["error_response_style"] == "gentle_normalize_then_strategy"
    assert payload["retrieval_plan"]["include_history"] is True
    assert payload["retrieval_plan"]["history_mode"] == "origin_first"
    assert "application_bridge" in payload["retrieval_plan"]["network_focus"]


def test_tutoring_plan_simulates_blockwise_mode_shift() -> None:
    response = client.post(
        "/api/v1/tutoring/plan",
        json={
            "objective": "Erklaere mir mit Beispiel, warum die quadratische Gleichung so funktioniert.",
            "learner_profile": {
                "age_group": "teen",
                "math_level": "high_school",
                "confidence": "low",
                "preferred_pace": "balanced",
                "language": "de",
                "wants_visuals": True,
                "wants_history": True,
            },
            "runtime_observations": [
                {"evidence": ["repeated_concept_error"]},
                {"evidence": ["repeated_concept_error"]},
                {"evidence": ["repeated_concept_error"]},
            ],
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["lesson_mode"] == "origin_then_example"
    assert len(payload["mode_adaptation_trace"]) == 3
    assert payload["mode_adaptation_trace"][-1]["changed"] is True
    assert payload["mode_adaptation_trace"][-1]["mode_after"] == "worked_example_tutoring"
    assert payload["mode_adaptation_trace"][-1]["transition_message"] is not None
    assert payload["planned_blocks"][-1]["mode"] == "worked_example_tutoring"
    assert payload["planned_blocks"][-1]["transition_message"] is not None
    assert payload["mode_adaptation_state"]["current_mode"] == "worked_example_tutoring"
    assert payload["mode_adaptation_state"]["mode_changes_in_session"] == 1


def test_tutoring_plan_can_resume_mode_adaptation_state() -> None:
    response = client.post(
        "/api/v1/tutoring/plan",
        json={
            "objective": "Erklaere mir mit Beispiel, warum die quadratische Gleichung so funktioniert.",
            "learner_profile": {
                "age_group": "teen",
                "math_level": "high_school",
                "confidence": "low",
                "preferred_pace": "balanced",
                "language": "de",
                "wants_visuals": True,
                "wants_history": True,
            },
            "mode_adaptation_state": {
                "current_mode": "worked_example_tutoring",
                "blocks_in_current_mode": 2,
                "mode_changes_in_session": 1,
                "cooldown_blocks_remaining": 0,
            },
            "runtime_observations": [
                {"evidence": ["pattern_recognized", "transfer_success"]},
            ],
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["lesson_mode"] == "worked_example_tutoring"
    assert payload["planned_blocks"][0]["mode"] == "worked_example_tutoring"
    assert payload["mode_adaptation_trace"][0]["changed"] is True
    assert payload["mode_adaptation_trace"][0]["mode_after"] == "guided_concept_explanation"
    assert payload["mode_adaptation_state"]["current_mode"] == "guided_concept_explanation"
    assert payload["resume_context"]["resume_source"] == "inline_state"
    assert payload["resume_context"]["resume_active"] is True


def test_tutoring_plan_can_resume_from_mode_adaptation_checkpoint() -> None:
    response = client.post(
        "/api/v1/tutoring/plan",
        json={
            "objective": "Erklaere mir mit Beispiel, warum die quadratische Gleichung so funktioniert.",
            "learner_profile": {
                "age_group": "teen",
                "math_level": "high_school",
                "confidence": "low",
                "preferred_pace": "balanced",
                "language": "de",
                "wants_visuals": True,
                "wants_history": True,
            },
            "mode_adaptation_checkpoint": {
                "schema_version": "phase_h1_v1",
                "mode_adaptation_state": {
                    "current_mode": "worked_example_tutoring",
                    "blocks_in_current_mode": 2,
                    "mode_changes_in_session": 1,
                    "cooldown_blocks_remaining": 0,
                },
            },
            "runtime_observations": [
                {"evidence": ["pattern_recognized", "transfer_success"]},
            ],
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["lesson_mode"] == "worked_example_tutoring"
    assert payload["planned_blocks"][0]["mode"] == "worked_example_tutoring"
    assert payload["mode_adaptation_trace"][0]["changed"] is True
    assert payload["mode_adaptation_trace"][0]["mode_after"] == "guided_concept_explanation"
    assert payload["mode_adaptation_checkpoint"]["schema_version"] == "phase_h1_v1"
    assert (
        payload["mode_adaptation_checkpoint"]["mode_adaptation_state"]["current_mode"]
        == "guided_concept_explanation"
    )
    assert payload["resume_context"]["resume_source"] == "inline_checkpoint"
    assert payload["resume_context"]["resume_active"] is True


def test_tutoring_plan_auto_migrates_inline_mode_adaptation_checkpoint() -> None:
    response = client.post(
        "/api/v1/tutoring/plan",
        json={
            "objective": "Erklaere mir mit Beispiel, warum die quadratische Gleichung so funktioniert.",
            "learner_profile": {
                "age_group": "teen",
                "math_level": "high_school",
                "confidence": "low",
                "preferred_pace": "balanced",
                "language": "de",
                "wants_visuals": True,
                "wants_history": True,
            },
            "mode_adaptation_checkpoint": {
                "schema_version": "phase_h0_v1",
                "mode_adaptation_state": {
                    "current_mode": "worked_example_tutoring",
                    "blocks_in_current_mode": 2,
                    "mode_changes_in_session": 1,
                    "cooldown_blocks_remaining": 0,
                },
            },
            "runtime_observations": [
                {"evidence": ["pattern_recognized", "transfer_success"]},
            ],
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["mode_adaptation_checkpoint"]["schema_version"] == "phase_h1_v1"
    assert payload["mode_adaptation_state"]["current_mode"] == "guided_concept_explanation"


def test_tutoring_plan_auto_migrates_inline_mode_adaptation_checkpoint_across_multiple_steps() -> None:
    response = client.post(
        "/api/v1/tutoring/plan",
        json={
            "objective": "Erklaere mir mit Beispiel, warum die quadratische Gleichung so funktioniert.",
            "learner_profile": {
                "age_group": "teen",
                "math_level": "high_school",
                "confidence": "low",
                "preferred_pace": "balanced",
                "language": "de",
                "wants_visuals": True,
                "wants_history": True,
            },
            "mode_adaptation_checkpoint": {
                "schema_version": "phase_h0_v0",
                "mode_adaptation_state": {
                    "current_mode": "worked_example_tutoring",
                    "blocks_in_current_mode": 2,
                    "mode_changes_in_session": 1,
                    "cooldown_blocks_remaining": 0,
                    "last_observation_evidence": ["legacy_signal_should_be_reset"],
                },
            },
            "runtime_observations": [
                {"evidence": ["pattern_recognized", "transfer_success"]},
            ],
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["mode_adaptation_checkpoint"]["schema_version"] == "phase_h1_v1"
    assert payload["mode_adaptation_state"]["current_mode"] == "guided_concept_explanation"


def test_tutoring_plan_rejects_state_and_checkpoint_together() -> None:
    response = client.post(
        "/api/v1/tutoring/plan",
        json={
            "objective": "Erklaere mir die quadratische Gleichung anschaulich.",
            "learner_profile": {
                "age_group": "teen",
                "math_level": "high_school",
                "confidence": "low",
                "preferred_pace": "balanced",
                "language": "de",
                "wants_visuals": True,
                "wants_history": True,
            },
            "mode_adaptation_state": {
                "current_mode": "guided_concept_explanation",
                "blocks_in_current_mode": 1,
                "mode_changes_in_session": 0,
            },
            "mode_adaptation_checkpoint": {
                "schema_version": "phase_h1_v1",
                "mode_adaptation_state": {
                    "current_mode": "guided_concept_explanation",
                    "blocks_in_current_mode": 1,
                    "mode_changes_in_session": 0,
                },
            },
        },
    )

    assert response.status_code == 422


def test_tutoring_plan_stores_checkpoint_under_session_id() -> None:
    session_id = f"api-session-{uuid.uuid4()}"
    session_store.delete_checkpoint(session_id)

    response = client.post(
        "/api/v1/tutoring/plan",
        json={
            "session_id": session_id,
            "objective": "Erklaere mir die quadratische Gleichung anschaulich.",
            "learner_profile": {
                "age_group": "teen",
                "math_level": "high_school",
                "confidence": "low",
                "preferred_pace": "balanced",
                "language": "de",
                "wants_visuals": True,
                "wants_history": True,
            },
        },
    )

    assert response.status_code == 200
    payload = response.json()
    stored = session_store.load_checkpoint(session_id)

    assert payload["session_id"] == session_id
    assert stored is not None
    assert stored.mode_adaptation_state.current_mode == "guided_concept_explanation"


def test_tutoring_plan_resumes_from_session_id_store() -> None:
    session_id = f"api-session-{uuid.uuid4()}"
    session_store.delete_checkpoint(session_id)

    first_response = client.post(
        "/api/v1/tutoring/plan",
        json={
            "session_id": session_id,
            "objective": "Erklaere mir mit Beispiel, warum die quadratische Gleichung so funktioniert.",
            "learner_profile": {
                "age_group": "teen",
                "math_level": "high_school",
                "confidence": "low",
                "preferred_pace": "balanced",
                "language": "de",
                "wants_visuals": True,
                "wants_history": True,
            },
            "runtime_observations": [
                {"evidence": ["repeated_concept_error"]},
                {"evidence": ["repeated_concept_error"]},
                {"evidence": ["repeated_concept_error"]},
            ],
        },
    )

    assert first_response.status_code == 200
    first_payload = first_response.json()
    assert first_payload["mode_adaptation_state"]["current_mode"] == "worked_example_tutoring"

    resume_response = client.post(
        "/api/v1/tutoring/plan",
        json={
            "session_id": session_id,
            "objective": "Erklaere mir mit Beispiel, warum die quadratische Gleichung so funktioniert.",
            "learner_profile": {
                "age_group": "teen",
                "math_level": "high_school",
                "confidence": "low",
                "preferred_pace": "balanced",
                "language": "de",
                "wants_visuals": True,
                "wants_history": True,
            },
        },
    )

    assert resume_response.status_code == 200
    resume_payload = resume_response.json()
    assert resume_payload["session_id"] == session_id
    assert resume_payload["lesson_mode"] == "worked_example_tutoring"
    assert resume_payload["planned_blocks"][0]["mode"] == "worked_example_tutoring"


def test_tutoring_plan_rejects_session_id_and_inline_checkpoint_together() -> None:
    response = client.post(
        "/api/v1/tutoring/plan",
        json={
            "session_id": "sess-conflict",
            "objective": "Erklaere mir die quadratische Gleichung anschaulich.",
            "learner_profile": {
                "age_group": "teen",
                "math_level": "high_school",
                "confidence": "low",
                "preferred_pace": "balanced",
                "language": "de",
                "wants_visuals": True,
                "wants_history": True,
            },
            "mode_adaptation_checkpoint": {
                "schema_version": "phase_h1_v1",
                "mode_adaptation_state": {
                    "current_mode": "guided_concept_explanation",
                    "blocks_in_current_mode": 1,
                    "mode_changes_in_session": 0,
                },
            },
        },
    )

    assert response.status_code == 422


def test_tutoring_plan_auto_migrates_stored_session_checkpoint() -> None:
    session_id = f"api-session-migration-{uuid.uuid4()}"
    session_store.delete_checkpoint(session_id)
    session_store.save_checkpoint(
        session_id,
        ModeAdaptationCheckpoint(
            schema_version="phase_h0_v1",
            mode_adaptation_state=ModeAdaptationState(
                current_mode="guided_concept_explanation",
                blocks_in_current_mode=1,
                mode_changes_in_session=0,
                cooldown_blocks_remaining=0,
            ),
        ),
    )
    response = client.post(
        "/api/v1/tutoring/plan",
        json={
            "session_id": session_id,
            "objective": "Erklaere mir die quadratische Gleichung anschaulich.",
            "learner_profile": {
                "age_group": "teen",
                "math_level": "high_school",
                "confidence": "low",
                "preferred_pace": "balanced",
                "language": "de",
                "wants_visuals": True,
                "wants_history": True,
            },
        },
    )

    assert response.status_code == 200
    payload = response.json()
    stored = session_store.load_checkpoint(session_id)

    assert payload["session_id"] == session_id
    assert payload["mode_adaptation_checkpoint"]["schema_version"] == "phase_h1_v1"
    assert stored is not None
    assert stored.schema_version == "phase_h1_v1"
    session_store.delete_checkpoint(session_id)


def test_tutoring_plan_auto_migrates_stored_session_checkpoint_across_multiple_steps() -> None:
    session_id = f"api-session-chain-migration-{uuid.uuid4()}"
    session_store.delete_checkpoint(session_id)
    session_store.save_checkpoint(
        session_id,
        ModeAdaptationCheckpoint(
            schema_version="phase_h0_v0",
            mode_adaptation_state=ModeAdaptationState(
                current_mode="guided_concept_explanation",
                blocks_in_current_mode=1,
                mode_changes_in_session=0,
                cooldown_blocks_remaining=0,
                last_observation_evidence=["legacy_signal_should_be_reset"],
            ),
        ),
    )
    response = client.post(
        "/api/v1/tutoring/plan",
        json={
            "session_id": session_id,
            "objective": "Erklaere mir die quadratische Gleichung anschaulich.",
            "learner_profile": {
                "age_group": "teen",
                "math_level": "high_school",
                "confidence": "low",
                "preferred_pace": "balanced",
                "language": "de",
                "wants_visuals": True,
                "wants_history": True,
            },
        },
    )

    assert response.status_code == 200
    payload = response.json()
    stored = session_store.load_checkpoint(session_id)

    assert payload["session_id"] == session_id
    assert payload["mode_adaptation_checkpoint"]["schema_version"] == "phase_h1_v1"
    assert stored is not None
    assert stored.schema_version == "phase_h1_v1"
    assert stored.mode_adaptation_state.last_observation_evidence == []
    session_store.delete_checkpoint(session_id)


def test_tutoring_plan_returns_400_for_invalid_stored_checkpoint() -> None:
    session_id = f"api-session-invalid-{uuid.uuid4()}"
    session_store.delete_checkpoint(session_id)
    invalid_path = session_store.session_path(session_id)
    invalid_path.write_text(
        '{\n'
        '  "schema_version": "phase_h1_v1",\n'
        '  "mode_adaptation_state": {\n'
        '    "current_mode": "guided_concept_explanation",\n'
        '    "blocks_in_current_mode": -2,\n'
        '    "mode_changes_in_session": 0,\n'
        '    "cooldown_blocks_remaining": 0,\n'
        '    "last_observation_evidence": []\n'
        "  }\n"
        "}\n",
        encoding="utf-8",
    )
    response = client.post(
        "/api/v1/tutoring/plan",
        json={
            "session_id": session_id,
            "objective": "Erklaere mir die quadratische Gleichung anschaulich.",
            "learner_profile": {
                "age_group": "teen",
                "math_level": "high_school",
                "confidence": "low",
                "preferred_pace": "balanced",
                "language": "de",
                "wants_visuals": True,
                "wants_history": True,
            },
        },
    )

    assert response.status_code == 400
    assert "could not be resumed" in response.json()["detail"]
    assert session_store.load_checkpoint(session_id) is None
    session_store.delete_checkpoint(session_id)


def test_tutoring_plan_starts_clean_after_quarantine_for_same_session_id() -> None:
    session_id = f"api-session-clean-restart-{uuid.uuid4()}"
    session_store.delete_checkpoint(session_id)
    invalid_path = session_store.session_path(session_id)
    invalid_path.write_text(
        '{\n'
        '  "schema_version": "phase_h1_v1",\n'
        '  "mode_adaptation_state": {\n'
        '    "current_mode": "guided_concept_explanation",\n'
        '    "blocks_in_current_mode": -2,\n'
        '    "mode_changes_in_session": 0,\n'
        '    "cooldown_blocks_remaining": 0,\n'
        '    "last_observation_evidence": []\n'
        "  }\n"
        "}\n",
        encoding="utf-8",
    )

    first_response = client.post(
        "/api/v1/tutoring/plan",
        json={
            "session_id": session_id,
            "objective": "Erklaere mir die quadratische Gleichung anschaulich.",
            "learner_profile": {
                "age_group": "teen",
                "math_level": "high_school",
                "confidence": "low",
                "preferred_pace": "balanced",
                "language": "de",
                "wants_visuals": True,
                "wants_history": True,
            },
        },
    )
    second_response = client.post(
        "/api/v1/tutoring/plan",
        json={
            "session_id": session_id,
            "objective": "Erklaere mir die quadratische Gleichung anschaulich.",
            "learner_profile": {
                "age_group": "teen",
                "math_level": "high_school",
                "confidence": "low",
                "preferred_pace": "balanced",
                "language": "de",
                "wants_visuals": True,
                "wants_history": True,
            },
        },
    )

    assert first_response.status_code == 400
    assert second_response.status_code == 200
    assert second_response.json()["session_id"] == session_id
    assert session_store.load_checkpoint(session_id) is not None
    session_store.delete_checkpoint(session_id)


def test_admin_quarantine_list_and_inspect_session() -> None:
    session_id = f"api-session-inspect-{uuid.uuid4()}"
    session_store.delete_checkpoint(session_id)
    invalid_path = session_store.session_path(session_id)
    invalid_path.write_text(
        '{\n'
        '  "schema_version": "phase_h1_v1",\n'
        '  "mode_adaptation_state": {\n'
        '    "current_mode": "guided_concept_explanation",\n'
        '    "blocks_in_current_mode": -2,\n'
        '    "mode_changes_in_session": 0,\n'
        '    "cooldown_blocks_remaining": 0,\n'
        '    "last_observation_evidence": []\n'
        "  }\n"
        "}\n",
        encoding="utf-8",
    )

    client.post(
        "/api/v1/tutoring/plan",
        json={
            "session_id": session_id,
            "objective": "Erklaere mir die quadratische Gleichung anschaulich.",
            "learner_profile": {
                "age_group": "teen",
                "math_level": "high_school",
                "confidence": "low",
                "preferred_pace": "balanced",
                "language": "de",
                "wants_visuals": True,
                "wants_history": True,
            },
        },
    )

    list_response = client.get("/api/v1/admin/quarantine/sessions")
    inspect_response = client.get(f"/api/v1/admin/quarantine/{session_id}")

    assert list_response.status_code == 200
    assert any(
        item["session_id"] == session_id for item in list_response.json()["sessions"]
    )
    assert inspect_response.status_code == 200
    assert inspect_response.json()["session"]["session_id"] == session_id
    assert inspect_response.json()["preview_status"] == "unparseable"


def test_admin_can_restore_quarantined_session_after_manual_repair() -> None:
    session_id = f"api-session-restore-{uuid.uuid4()}"
    session_store.delete_checkpoint(session_id)
    invalid_path = session_store.session_path(session_id)
    invalid_path.write_text(
        '{\n'
        '  "schema_version": "phase_h1_v1",\n'
        '  "mode_adaptation_state": {\n'
        '    "current_mode": "guided_concept_explanation",\n'
        '    "blocks_in_current_mode": -2,\n'
        '    "mode_changes_in_session": 0,\n'
        '    "cooldown_blocks_remaining": 0,\n'
        '    "last_observation_evidence": []\n'
        "  }\n"
        "}\n",
        encoding="utf-8",
    )

    client.post(
        "/api/v1/tutoring/plan",
        json={
            "session_id": session_id,
            "objective": "Erklaere mir die quadratische Gleichung anschaulich.",
            "learner_profile": {
                "age_group": "teen",
                "math_level": "high_school",
                "confidence": "low",
                "preferred_pace": "balanced",
                "language": "de",
                "wants_visuals": True,
                "wants_history": True,
            },
        },
    )
    inspect_response = client.get(f"/api/v1/admin/quarantine/{session_id}")
    quarantine_path = Path(inspect_response.json()["session"]["quarantine_path"])
    quarantine_path.write_text(
        '{\n'
        '  "schema_version": "phase_h1_v1",\n'
        '  "mode_adaptation_state": {\n'
        '    "current_mode": "guided_concept_explanation",\n'
        '    "blocks_in_current_mode": 1,\n'
        '    "mode_changes_in_session": 0,\n'
        '    "cooldown_blocks_remaining": 0,\n'
        '    "last_observation_evidence": []\n'
        "  }\n"
        "}\n",
        encoding="utf-8",
    )

    restore_response = client.post(f"/api/v1/admin/quarantine/{session_id}/restore")
    resume_response = client.post(
        "/api/v1/tutoring/plan",
        json={
            "session_id": session_id,
            "objective": "Erklaere mir die quadratische Gleichung anschaulich.",
            "learner_profile": {
                "age_group": "teen",
                "math_level": "high_school",
                "confidence": "low",
                "preferred_pace": "balanced",
                "language": "de",
                "wants_visuals": True,
                "wants_history": True,
            },
        },
    )

    assert restore_response.status_code == 200
    assert restore_response.json()["session_id"] == session_id
    assert resume_response.status_code == 200
    assert resume_response.json()["session_id"] == session_id
    assert session_store.load_checkpoint(session_id) is not None
    session_store.delete_checkpoint(session_id)


def test_tutoring_plan_resume_derives_cross_block_breakthrough() -> None:
    response = client.post(
        "/api/v1/tutoring/plan",
        json={
            "objective": "Erklaere mir diese Aufgabe mit Beispiel.",
            "learner_profile": {
                "age_group": "teen",
                "math_level": "high_school",
                "confidence": "medium",
                "preferred_pace": "balanced",
                "language": "de",
                "wants_visuals": True,
                "wants_history": False,
            },
            "mode_adaptation_state": {
                "current_mode": "worked_example_tutoring",
                "blocks_in_current_mode": 2,
                "mode_changes_in_session": 0,
                "cooldown_blocks_remaining": 0,
                "last_observation_evidence": ["transfer_success"],
            },
            "runtime_observations": [
                {"evidence": ["transfer_success"]},
            ],
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert "transfer_success_two_blocks" in payload["planned_blocks"][0]["observed_evidence"]
    assert payload["mode_adaptation_trace"][0]["changed"] is True
    assert payload["mode_adaptation_trace"][0]["mode_after"] == "guided_concept_explanation"
    assert payload["mode_adaptation_state"]["current_mode"] == "guided_concept_explanation"


def test_tutoring_plan_resume_keeps_pending_transition_message() -> None:
    response = client.post(
        "/api/v1/tutoring/plan",
        json={
            "objective": "Erklaere mir mit Beispiel, warum die quadratische Gleichung so funktioniert.",
            "learner_profile": {
                "age_group": "teen",
                "math_level": "high_school",
                "confidence": "low",
                "preferred_pace": "balanced",
                "language": "de",
                "wants_visuals": True,
                "wants_history": True,
            },
            "mode_adaptation_state": {
                "current_mode": "worked_example_tutoring",
                "blocks_in_current_mode": 0,
                "mode_changes_in_session": 1,
                "cooldown_blocks_remaining": 1,
                "pending_transition_message": (
                    "Das ist eine Stelle, an der viele kurz haengen bleiben. "
                    "Ich nehme etwas Last raus. "
                    "Wir gehen jetzt in kleineren Schritten weiter."
                ),
            },
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["planned_blocks"][0]["transition_message"] is not None
    assert "kleineren Schritten" in payload["planned_blocks"][0]["transition_message"]
    assert payload["mode_adaptation_state"]["pending_transition_message"] is None
    assert payload["resume_context"]["pending_transition_message_carried"] is True
    assert payload["resume_context"]["pending_transition_message_consumed"] is True


def test_tutoring_plan_session_resume_reuses_last_observation_evidence_for_preview_support() -> None:
    session_id = f"api-session-evidence-preview-{uuid.uuid4()}"
    session_store.delete_checkpoint(session_id)
    session_store.save_checkpoint(
        session_id,
        ModeAdaptationCheckpoint(
            mode_adaptation_state=ModeAdaptationState(
                current_mode="guided_concept_explanation",
                blocks_in_current_mode=1,
                mode_changes_in_session=0,
                cooldown_blocks_remaining=0,
                last_observation_evidence=["text_overload", "vocabulary_request"],
            ),
        ),
    )

    response = client.post(
        "/api/v1/tutoring/plan",
        json={
            "session_id": session_id,
            "objective": "Explain this word problem in small clear steps.",
            "learner_profile": {
                "age_group": "teen",
                "math_level": "middle_school",
                "confidence": "low",
                "preferred_pace": "balanced",
                "language": "en",
                "wants_visuals": True,
                "wants_history": False,
                "declared_support_needs": ["dyslexia_aware_support"],
            },
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["planned_blocks"][0]["observed_evidence"] == [
        "text_overload",
        "vocabulary_request",
    ]
    assert "split_problem_text_into_shorter_chunks" in payload["planned_blocks"][0]["support_moves"]
    assert "key_term_glossary" in payload["planned_blocks"][0]["support_scaffolds"]
    assert payload["resume_context"]["resume_source"] == "stored_checkpoint"
    assert payload["resume_context"]["resume_active"] is True
    assert payload["resume_context"]["carried_observation_evidence"] == [
        "text_overload",
        "vocabulary_request",
    ]
    assert payload["resume_context"]["used_carried_observation_evidence"] is True
    session_store.delete_checkpoint(session_id)


def test_tutoring_plan_derives_missing_success_line_for_scarcity_support() -> None:
    response = client.post(
        "/api/v1/tutoring/plan",
        json={
            "objective": "Erklaere mir die quadratische Gleichung anschaulich.",
            "learner_profile": {
                "age_group": "teen",
                "math_level": "high_school",
                "confidence": "low",
                "preferred_pace": "balanced",
                "language": "de",
                "wants_visuals": True,
                "wants_history": False,
                "declared_support_needs": ["scarcity_aware_support"],
            },
            "runtime_observations": [
                {"evidence": ["single_concept_error"]},
                {"evidence": ["single_concept_error"]},
                {"evidence": ["single_concept_error"]},
            ],
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert "no_success_visible_two_blocks" in payload["planned_blocks"][1]["observed_evidence"]
    assert payload["mode_adaptation_trace"][1]["changed"] is False
    assert payload["mode_adaptation_trace"][2]["changed"] is True
    assert payload["mode_adaptation_trace"][2]["mode_after"] == "worked_example_tutoring"


def test_tutoring_plan_declared_adhd_support() -> None:
    response = client.post(
        "/api/v1/tutoring/plan",
        json={
            "objective": "Erklaere mir diese Aufgabe Schritt fuer Schritt mit Beispiel.",
            "learner_profile": {
                "age_group": "teen",
                "math_level": "high_school",
                "confidence": "low",
                "preferred_pace": "gentle",
                "language": "de",
                "wants_visuals": True,
                "wants_history": False,
                "declared_support_needs": ["adhd_aware_support"],
            },
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["support_signal_profile"]["adhd_aware_support"] == "declared"
    assert payload["response_settings"]["session_duration"] == "12_to_15_minute_focus_blocks"
    assert "step_labels" in payload["response_settings"]["external_scaffolds"]
    assert "announce_short_goal_before_block" in payload["planned_blocks"][0]["support_moves"]
    assert "step_labels" in payload["planned_blocks"][0]["support_scaffolds"]


def test_tutoring_plan_declared_dyslexia_support() -> None:
    response = client.post(
        "/api/v1/tutoring/plan",
        json={
            "objective": "Erklaere mir diese Textaufgabe in kleinen Schritten.",
            "learner_profile": {
                "age_group": "teen",
                "math_level": "middle_school",
                "confidence": "low",
                "preferred_pace": "balanced",
                "language": "de",
                "wants_visuals": True,
                "wants_history": False,
                "declared_support_needs": ["dyslexia_aware_support"],
            },
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["support_signal_profile"]["dyslexia_aware_support"] == "declared"
    assert payload["response_settings"]["language_support"] == (
        "glossary_plus_key_terms_plus_simplified_syntax"
    )
    assert "key_term_highlighting" in payload["response_settings"]["external_scaffolds"]
    assert "reduce_text_load_before_problem_solving" in payload["planned_blocks"][0]["support_moves"]


def test_tutoring_plan_declared_autism_support() -> None:
    response = client.post(
        "/api/v1/tutoring/plan",
        json={
            "objective": "Erklaere mir das bitte sehr klar und Schritt fuer Schritt.",
            "learner_profile": {
                "age_group": "teen",
                "math_level": "middle_school",
                "confidence": "medium",
                "preferred_pace": "balanced",
                "language": "de",
                "wants_visuals": True,
                "wants_history": False,
                "declared_support_needs": ["autism_spectrum_aware_support"],
            },
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["support_signal_profile"]["autism_spectrum_aware_support"] == "declared"
    assert payload["response_settings"]["sensory_load_level"] == "minimal_and_high_contrast"
    assert payload["response_settings"]["language_support"] == "explicit_literal_instructions"
    assert "consistent_session_structure" in payload["response_settings"]["external_scaffolds"]
    assert "keep_structure_predictable_and_literal" in payload["planned_blocks"][0]["support_moves"]


def test_tutoring_plan_language_sensitive_support() -> None:
    response = client.post(
        "/api/v1/tutoring/plan",
        json={
            "objective": "Explain this word problem in small clear steps.",
            "learner_profile": {
                "age_group": "teen",
                "math_level": "middle_school",
                "confidence": "medium",
                "preferred_pace": "balanced",
                "language": "en",
                "wants_visuals": True,
                "wants_history": False,
            },
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["support_signal_profile"]["language_sensitive_support"] == "possible"
    assert payload["response_settings"]["language_support"] == (
        "translated_key_terms_glossary_and_simplified_syntax"
    )
    assert "key_term_glossary" in payload["response_settings"]["external_scaffolds"]
    assert "bridge_everyday_language_and_math_terms" in payload["planned_blocks"][0]["support_moves"]
    assert any("math vocabulary" in item for item in payload["teaching_pattern"])


def test_tutoring_plan_declared_scarcity_support() -> None:
    response = client.post(
        "/api/v1/tutoring/plan",
        json={
            "objective": "Erklaere mir diese Aufgabe klar und nutzbar fuer den Alltag.",
            "learner_profile": {
                "age_group": "teen",
                "math_level": "middle_school",
                "confidence": "low",
                "preferred_pace": "balanced",
                "language": "de",
                "wants_visuals": True,
                "wants_history": False,
                "declared_support_needs": ["scarcity_aware_support"],
            },
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["support_signal_profile"]["scarcity_aware_support"] == "declared"
    assert payload["response_settings"]["language_support"] == "plain_goal_and_relevance_framing"
    assert "clear_success_criteria" in payload["response_settings"]["external_scaffolds"]
    assert "mark_small_visible_wins" in payload["planned_blocks"][0]["support_moves"]
    assert any("visible progress" in item for item in payload["teaching_pattern"])


def test_tutoring_plan_makes_block_support_runtime_sensitive_under_confusion() -> None:
    response = client.post(
        "/api/v1/tutoring/plan",
        json={
            "objective": "Erklaere mir diese Aufgabe Schritt fuer Schritt mit Beispiel.",
            "learner_profile": {
                "age_group": "teen",
                "math_level": "middle_school",
                "confidence": "low",
                "preferred_pace": "gentle",
                "language": "de",
                "wants_visuals": True,
                "wants_history": False,
                "declared_support_needs": [
                    "adhd_aware_support",
                    "dyscalculia_aware_support",
                ],
            },
            "runtime_observations": [
                {"evidence": ["repeated_concept_error"]},
            ],
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert "rebuild_last_step_after_confusion" in payload["planned_blocks"][0]["support_moves"]
    assert "return_to_quantity_model_before_symbols" in payload["planned_blocks"][0]["support_moves"]
    assert "number_lines" in payload["planned_blocks"][0]["support_scaffolds"]


def test_tutoring_plan_makes_block_support_runtime_sensitive_under_text_overload() -> None:
    response = client.post(
        "/api/v1/tutoring/plan",
        json={
            "objective": "Explain this word problem in small clear steps.",
            "learner_profile": {
                "age_group": "teen",
                "math_level": "middle_school",
                "confidence": "low",
                "preferred_pace": "balanced",
                "language": "en",
                "wants_visuals": True,
                "wants_history": False,
                "declared_support_needs": ["dyslexia_aware_support"],
            },
            "runtime_observations": [
                {"evidence": ["text_overload", "vocabulary_request"]},
            ],
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert "split_problem_text_into_shorter_chunks" in payload["planned_blocks"][0]["support_moves"]
    assert "clarify_terms_before_retrying_math_step" in payload["planned_blocks"][0]["support_moves"]
    assert "key_term_glossary" in payload["planned_blocks"][0]["support_scaffolds"]


def test_tutoring_plan_mixed_profile_conflict_resolution() -> None:
    response = client.post(
        "/api/v1/tutoring/plan",
        json={
            "objective": "Erklaere mir diese Aufgabe Schritt fuer Schritt mit Beispiel.",
            "learner_profile": {
                "age_group": "teen",
                "math_level": "middle_school",
                "confidence": "low",
                "preferred_pace": "gentle",
                "language": "de",
                "wants_visuals": True,
                "wants_history": False,
                "declared_support_needs": [
                    "adhd_aware_support",
                    "dyscalculia_aware_support",
                ],
            },
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["response_settings"]["session_duration"] == (
        "15_to_18_minute_concrete_focus_blocks"
    )
    assert payload["response_settings"]["break_pattern"] == (
        "ultradian_micro_breaks_within_concrete_work"
    )
    assert "adhd_aware_support__dyscalculia_aware_support" in payload["response_settings"][
        "conflict_pairs"
    ]
    assert "announce_short_goal_before_block" in payload["planned_blocks"][0]["support_moves"]
    assert "keep_quantity_representation_visible" in payload["planned_blocks"][0]["support_moves"]
    assert payload["mode_selection"]["selected_mode"] == "worked_example_tutoring"
    assert "low_notation_density" in payload["mode_selection"]["constraints"]
    assert any("conflict-resolution rules" in item for item in payload["teaching_pattern"])


def test_tutoring_plan_triad_priority_ladders() -> None:
    response = client.post(
        "/api/v1/tutoring/plan",
        json={
            "objective": "Erklaere mir diese Aufgabe klar, Schritt fuer Schritt und mit Sinn.",
            "learner_profile": {
                "age_group": "teen",
                "math_level": "middle_school",
                "confidence": "low",
                "preferred_pace": "gentle",
                "language": "de",
                "wants_visuals": True,
                "wants_history": False,
                "declared_support_needs": [
                    "adhd_aware_support",
                    "dyscalculia_aware_support",
                    "scarcity_aware_support",
                ],
            },
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["response_settings"]["session_duration"] == (
        "15_to_18_minute_concrete_success_blocks"
    )
    assert (
        "adhd_aware_support__dyscalculia_aware_support__scarcity_aware_support"
        in payload["response_settings"]["triad_groups"]
    )
    assert "conceptual_grounding_before_speed" in payload["response_settings"][
        "priority_ladders"
    ]
    assert payload["mode_selection"]["selected_mode"] == "worked_example_tutoring"
    assert "micro_success_cycles" in payload["mode_selection"]["constraints"]
    assert any("priority ladders" in item for item in payload["teaching_pattern"])


def test_tutoring_plan_origin_mode_reduced_under_adhd_scarcity() -> None:
    response = client.post(
        "/api/v1/tutoring/plan",
        json={
            "objective": "Erklaere mir als Laie warum das notwendig wurde.",
            "learner_profile": {
                "age_group": "teen",
                "math_level": "middle_school",
                "confidence": "low",
                "preferred_pace": "gentle",
                "language": "de",
                "wants_visuals": True,
                "wants_history": False,
                "declared_support_needs": [
                    "adhd_aware_support",
                    "scarcity_aware_support",
                ],
            },
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["mode_selection"]["requested_mode"] == "origin_story_explanation"
    assert payload["mode_selection"]["selected_mode"] == "origin_then_example"
    assert "micro_origin_bridge" in payload["mode_selection"]["constraints"]
    assert payload["retrieval_plan"]["history_mode"] == "supporting_only"
