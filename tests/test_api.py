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
