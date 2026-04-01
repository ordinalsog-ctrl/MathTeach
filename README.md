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
- [docs/math-corpus-blueprint.md](/Users/jonasweiss/MathTeach/docs/math-corpus-blueprint.md): Startplan fuer die mathematische Quellensammlung
- [docs/math-history-program.md](/Users/jonasweiss/MathTeach/docs/math-history-program.md): Chronologisches Sammelprogramm fuer die erste Mathegeschichte
- [docs/modern-math-baseline-audit-2026-04-01.md](/Users/jonasweiss/MathTeach/docs/modern-math-baseline-audit-2026-04-01.md): Startaudit fuer die neue Epoche Moderne Mathematik
- [docs/literature-gap-audit-2026-04-01.md](/Users/jonasweiss/MathTeach/docs/literature-gap-audit-2026-04-01.md): Vergleich unseres Stands mit kanonischer Literatur fuer Antike bis Fruehe Neuzeit
- [docs/literature-gap-audit-2026-04-01-post-round-a.md](/Users/jonasweiss/MathTeach/docs/literature-gap-audit-2026-04-01-post-round-a.md): Folgeaudit nach der ersten Brueckenwerk-Runde
- [docs/literature-gap-audit-2026-04-01-post-round-b.md](/Users/jonasweiss/MathTeach/docs/literature-gap-audit-2026-04-01-post-round-b.md): Folgeaudit nach Runde B
- [docs/literature-gap-audit-2026-04-01-post-round-c.md](/Users/jonasweiss/MathTeach/docs/literature-gap-audit-2026-04-01-post-round-c.md): Folgeaudit nach Runde C
- [docs/literature-gap-audit-2026-04-01-post-round-c1.md](/Users/jonasweiss/MathTeach/docs/literature-gap-audit-2026-04-01-post-round-c1.md): Folgeaudit nach Runde C.1
- [docs/external-feedback-triage-2026-04-01.md](/Users/jonasweiss/MathTeach/docs/external-feedback-triage-2026-04-01.md): Einordnung externer LLM-Rueckmeldungen in kommende Runden
- [docs/external-feedback-triage-2026-04-01-second-assessment.md](/Users/jonasweiss/MathTeach/docs/external-feedback-triage-2026-04-01-second-assessment.md): Prioritaetskorrektur nach der zweiten externen Bewertung
- [docs/curation-loop.md](/Users/jonasweiss/MathTeach/docs/curation-loop.md): Fester Arbeitszyklus aus Audit, Werk-Ergaenzung und Folgeaudit
- [docs/source-access-program.md](/Users/jonasweiss/MathTeach/docs/source-access-program.md): Wie historische Quellen gelesen, beschafft und lokal abgelegt werden
- [docs/data-foundation.md](/Users/jonasweiss/MathTeach/docs/data-foundation.md): Trennung von Knowledge Core und Teacher Mind
- [docs/knowledge-system.md](/Users/jonasweiss/MathTeach/docs/knowledge-system.md): Mathematik-Korpus, Graphmodell und Retrieval
- [docs/roadmap.md](/Users/jonasweiss/MathTeach/docs/roadmap.md): MVP- und Ausbauphasen
- [data/math_core/foundation_manifest.json](/Users/jonasweiss/MathTeach/data/math_core/foundation_manifest.json): Erstes Sammelmanifest fuer mathematische Quellen
- [data/math_core/chronology_manifest.json](/Users/jonasweiss/MathTeach/data/math_core/chronology_manifest.json): Historischer Startkatalog fuer Antike bis Moderne Mathematik
- [data/math_core/source_access_manifest.json](/Users/jonasweiss/MathTeach/data/math_core/source_access_manifest.json): Register mit Werken, Zugriffspfaden und Ablagehinweisen
- [sql/001_foundation_schema.sql](/Users/jonasweiss/MathTeach/sql/001_foundation_schema.sql): Erstes Postgres-Schema fuer die Datenbasis
- [sql/002_math_corpus_collection.sql](/Users/jonasweiss/MathTeach/sql/002_math_corpus_collection.sql): Quellenkatalog, Collection-Queue und Ingestion-Tabellen
- [sql/003_math_history_program.sql](/Users/jonasweiss/MathTeach/sql/003_math_history_program.sql): Epochen, Werke und Story-Tabellen fuer Beweise und Gleichungen
- [sql/004_source_access_registry.sql](/Users/jonasweiss/MathTeach/sql/004_source_access_registry.sql): Zugriffsrouten und lokales Speicher-Audit fuer Quellen
- [src/mathteach/main.py](/Users/jonasweiss/MathTeach/src/mathteach/main.py): FastAPI-Startpunkt
- [src/mathteach/services/corpus.py](/Users/jonasweiss/MathTeach/src/mathteach/services/corpus.py): Blueprint-Service fuer die Mathe-Datenbank
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
- `GET /api/v1/corpus/blueprint`
- `GET /api/v1/corpus/chronology`
- `GET /api/v1/corpus/source-access`
- `POST /api/v1/tutoring/plan`

## Naechste Produktstufe

Die aktuelle Repo-Version ist bewusst die erste belastbare Basis:

- Produkt- und Systemrichtung sind festgelegt.
- Das Modell- und Datenkonzept ist dokumentiert.
- Das Datenfundament ist jetzt explizit zweigeteilt in fachlichen Wissenskern und paedagogische Lehrerfigur.
- Die mathematische Datensammlung hat jetzt ein erstes Manifest mit Prioritaeten, Quellenfamilien und Collection-Queue.
- Die erste historische Sammelschicht ordnet Mathematik nach Epochen, Werken, Beweisen und Gleichungsgeschichten.
- Die Chronologie reicht jetzt als erste belastbare Linie von der Antike bis in die Moderne.
- Das erste Quellenregister sagt jetzt auch, wo historische Werke heute gelesen werden koennen und wie Rohdateien lokal abgelegt werden sollen.
- Eine kleine API zeigt schon, wie Wissens- und Lehrlogik getrennt orchestriert werden.

Der naechste grosse Schritt ist der Aufbau des Mathematik-Korpus mit Zitationspflicht, Ontologie, Ingestion-Pipeline und Evaluationssuite.
