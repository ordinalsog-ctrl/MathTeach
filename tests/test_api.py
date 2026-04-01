from fastapi.testclient import TestClient

from mathteach.main import app


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


def test_corpus_source_access_endpoint() -> None:
    response = client.get("/api/v1/corpus/source-access")

    assert response.status_code == 200
    payload = response.json()
    assert payload["sources"][0]["slug"] == "rhind-mathematical-papyrus"
    assert payload["sources"][2]["access_routes"][0]["provider"] == "Clay Mathematics Institute"
    assert any(item["slug"] == "apollonius-conics" for item in payload["sources"])
    assert any(item["slug"] == "aryabhata-aryabhatiya" for item in payload["sources"])
    assert any(item["slug"] == "napier-logarithmorum-canonis-descriptio" for item in payload["sources"])
    assert any(item["slug"] == "kepler-astronomia-nova" for item in payload["sources"])


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
    assert payload["audience_mode"] == "teen"
    assert payload["retrieval_plan"]["include_history"] is True
