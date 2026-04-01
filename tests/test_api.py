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
    assert payload["retrieval_plan"]["include_history"] is True
    assert payload["retrieval_plan"]["history_mode"] == "supporting_only"


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
    assert payload["retrieval_plan"]["include_history"] is True
    assert payload["retrieval_plan"]["history_mode"] == "origin_first"
    assert "application_bridge" in payload["retrieval_plan"]["network_focus"]
