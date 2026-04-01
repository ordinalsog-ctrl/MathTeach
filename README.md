# MathTeach

MathTeach ist die Grundlage fuer einen globalen Mathe-Lehrer-Agenten: fachlich tief in Mathematik, historisch praezise, didaktisch anpassungsfaehig und in der Lage, vom Grundschulkind bis zum Professor sinnvoll zu erklaeren.

## Kernprinzip

MathTeach trennt zwei Systeme bewusst voneinander:

- `Knowledge Core`: sachlich, nuechtern, zitierbar, historisch verankert
- `Teacher Mind`: paedagogisch, psychologisch, adaptiv, motivierend

Der Lehrer darf nie die Mathematik "umbiegen". Er darf nur entscheiden, wie dieselbe Mathematik fuer eine bestimmte Person am besten vermittelt wird.

## Produktthese

Ein wirklich starker Mathe-Agent braucht nicht nur ein grosses Modell. Er braucht:

- ein starkes Reasoning-LLM fuer Unterricht, Planung und Erklaerung,
- ein kuratiertes Mathematik-Wissenssystem mit Quellen, Herleitungen und Anwendungen,
- einen paedagogischen Anpassungslayer fuer Alter, Vorwissen, Sprache und Motivation,
- eine nachvollziehbare Retrieval-Pipeline, damit Antworten nicht nur eloquent, sondern belegbar sind.

## Empfohlener Modell-Stack

Stand der Empfehlung: 2026-04-01, auf Basis offizieller Modelldokumentation.

- `gpt-5.4` als Hauptmodell fuer Tutor-Orchestrierung, Tool-Nutzung und komplexes fachliches Reasoning
- `gpt-5.4-mini` fuer schnelle, guenstigere Nebenaufgaben wie Klassifikation, Session-Routing und Hint-Generierung
- `gemini-2.5-pro` fuer Batch-Ingestion sehr grosser PDFs, Buecher und Dokumentkorpora mit Langkontext
- `claude-opus-4-6` als optionales Zweitmodell fuer harte Gegenpruefung bei schwierigen Forschungs- und Erklaerungsfaellen
- `text-embedding-3-large` fuer semantische Suche ueber mathematische Quellen

Warum diese Aufteilung:

- Ein einzelnes Modell ist fuer dieses Vorhaben zu schwach als alleinige Architektur.
- Lehrgespraeche brauchen andere Latenz-, Kosten- und Tool-Anforderungen als Offline-Korpusaufbau.
- Historische und fachliche Zuverlaessigkeit steigen, wenn Retrieval, Zitationspflicht und Cross-Checks systematisch eingebaut sind.

## Architektur in einem Satz

MathTeach ist ein `teacher-agent + math knowledge graph + hybrid retrieval + learner-model` System.

## Repository-Inhalt

- [docs/architecture.md](/Users/jonasweiss/MathTeach/docs/architecture.md): Zielarchitektur und Komponenten
- [docs/data-foundation.md](/Users/jonasweiss/MathTeach/docs/data-foundation.md): Trennung von Knowledge Core und Teacher Mind
- [docs/knowledge-system.md](/Users/jonasweiss/MathTeach/docs/knowledge-system.md): Mathematik-Korpus, Graphmodell und Retrieval
- [docs/roadmap.md](/Users/jonasweiss/MathTeach/docs/roadmap.md): MVP- und Ausbauphasen
- [sql/001_foundation_schema.sql](/Users/jonasweiss/MathTeach/sql/001_foundation_schema.sql): Erstes Postgres-Schema fuer die Datenbasis
- [src/mathteach/main.py](/Users/jonasweiss/MathTeach/src/mathteach/main.py): FastAPI-Startpunkt
- [src/mathteach/services/foundation.py](/Users/jonasweiss/MathTeach/src/mathteach/services/foundation.py): Datenfundament fuer Wissenskern und Lehrerfigur
- [src/mathteach/services/planner.py](/Users/jonasweiss/MathTeach/src/mathteach/services/planner.py): Erste Planungslogik fuer Tutor-Sessions

## Schnellstart

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn mathteach.main:app --reload
```

Danach:

- `GET /health`
- `GET /api/v1/stack`
- `GET /api/v1/foundation`
- `POST /api/v1/tutoring/plan`

## Naechste Produktstufe

Die aktuelle Repo-Version ist bewusst die erste belastbare Basis:

- Produkt- und Systemrichtung sind festgelegt.
- Das Modell- und Datenkonzept ist dokumentiert.
- Das Datenfundament ist jetzt explizit zweigeteilt in fachlichen Wissenskern und paedagogische Lehrerfigur.
- Eine kleine API zeigt schon, wie Wissens- und Lehrlogik getrennt orchestriert werden.

Der naechste grosse Schritt ist der Aufbau des Mathematik-Korpus mit Zitationspflicht, Ontologie, Ingestion-Pipeline und Evaluationssuite.
