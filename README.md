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
- [docs/modern-math-review-triage-2026-04-01.md](/Users/jonasweiss/MathTeach/docs/modern-math-review-triage-2026-04-01.md): Priorisierung nach dem ersten externen Review der modernen Epoche
- [docs/modern-math-post-round-m1-audit-2026-04-01.md](/Users/jonasweiss/MathTeach/docs/modern-math-post-round-m1-audit-2026-04-01.md): Folgeaudit nach Runde M.1 der modernen Epoche
- [docs/modern-math-second-review-triage-2026-04-01.md](/Users/jonasweiss/MathTeach/docs/modern-math-second-review-triage-2026-04-01.md): Priorisierung nach dem zweiten externen Review der modernen Epoche
- [docs/modern-math-post-round-m2-audit-2026-04-01.md](/Users/jonasweiss/MathTeach/docs/modern-math-post-round-m2-audit-2026-04-01.md): Folgeaudit nach Runde M.2 der modernen Epoche
- [docs/modern-math-third-review-triage-2026-04-01.md](/Users/jonasweiss/MathTeach/docs/modern-math-third-review-triage-2026-04-01.md): Prioritaetskorrektur nach dem Review von Runde M.2
- [docs/modern-math-post-round-m3-audit-2026-04-01.md](/Users/jonasweiss/MathTeach/docs/modern-math-post-round-m3-audit-2026-04-01.md): Folgeaudit nach Runde M.3 der modernen Epoche
- [docs/modern-math-final-assessment-2026-04-01.md](/Users/jonasweiss/MathTeach/docs/modern-math-final-assessment-2026-04-01.md): Abschlussbewertung der modernen Epoche innerhalb des definierten Kanons
- [docs/full-corpus-final-assessment-2026-04-01.md](/Users/jonasweiss/MathTeach/docs/full-corpus-final-assessment-2026-04-01.md): Abschlussbewertung des historischen Gesamtkorpus vor der Vernetzungsphase
- [docs/cross-epoch-networking.md](/Users/jonasweiss/MathTeach/docs/cross-epoch-networking.md): Erste Architektur fuer Proof Lines, Equation Lines und Transmission Paths ueber alle Epochen
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
- [docs/teacher-mind-blueprint.md](/Users/jonasweiss/MathTeach/docs/teacher-mind-blueprint.md): Grundmodell der paedagogischen und psychologischen Lehrerschicht
- [docs/teacher-mind-charter.md](/Users/jonasweiss/MathTeach/docs/teacher-mind-charter.md): Verbindliche Regeln fuer selbstbeschriebene Lernbedarfe, lokale Speicherung und Nicht-Therapie-Rolle
- [docs/teacher-mind-foundation-stack.md](/Users/jonasweiss/MathTeach/docs/teacher-mind-foundation-stack.md): Reihenfolge des Tutor-Aufbaus: erst psychologische und paedagogische Grundlagen, dann Support- und Accessibility-Schichten
- [docs/teacher-mind-foundations-review-triage-2026-04-01.md](/Users/jonasweiss/MathTeach/docs/teacher-mind-foundations-review-triage-2026-04-01.md): Prioritaetskorrektur nach dem ersten umfassenden Review der psychologisch-paedagogischen Grundausbildung
- [docs/universal-tutor-system-review-triage-2026-04-01.md](/Users/jonasweiss/MathTeach/docs/universal-tutor-system-review-triage-2026-04-01.md): Prioritaetskorrektur fuer Universalitaet, Inklusion, Neurodiversitaet, Equity und lokale Systemarchitektur
- [docs/universal-round-u1-program.md](/Users/jonasweiss/MathTeach/docs/universal-round-u1-program.md): Erste universelle Designrunde fuer Motivation, Belonging, Errors, Equity/Scarcity und UDL
- [docs/psychological-foundations-program.md](/Users/jonasweiss/MathTeach/docs/psychological-foundations-program.md): Erster Teacher-Mind-Korpus fuer Lernen, Gedaechtnis, Abruf, Motivation und Anti-Myth-Guardrails
- [docs/pedagogical-foundations-program.md](/Users/jonasweiss/MathTeach/docs/pedagogical-foundations-program.md): Allgemeine Tutor-Grundausbildung fuer Erklaeraufbau, Scaffolding, Worked Examples, Feedback und Lernprogression
- [docs/learner-support-profiles.md](/Users/jonasweiss/MathTeach/docs/learner-support-profiles.md): Erste nicht-diagnostische Support-Profile fuer Lernbarrieren und Unterstuetzungsbedarfe
- [docs/pedagogical-strategy-matrix.md](/Users/jonasweiss/MathTeach/docs/pedagogical-strategy-matrix.md): Uebersetzung von Profilmix in Unterrichtsmodus, Tempo, Schrittgroesse und Interventionsstil
- [docs/teacher-mind-evidence-program.md](/Users/jonasweiss/MathTeach/docs/teacher-mind-evidence-program.md): Lokales Evidenzprogramm fuer serioese Leitquellen, Practice Guides und spaetere Einzelstudien des Teacher Mind
- [docs/closed-local-tutor-system-blueprint.md](/Users/jonasweiss/MathTeach/docs/closed-local-tutor-system-blueprint.md): Zielbild eines geschlossenen lokalen Tutorsystems als App oder eigenes Geraet
- [docs/roadmap.md](/Users/jonasweiss/MathTeach/docs/roadmap.md): MVP- und Ausbauphasen
- [data/math_core/foundation_manifest.json](/Users/jonasweiss/MathTeach/data/math_core/foundation_manifest.json): Erstes Sammelmanifest fuer mathematische Quellen
- [data/math_core/chronology_manifest.json](/Users/jonasweiss/MathTeach/data/math_core/chronology_manifest.json): Historischer Startkatalog fuer Antike bis Moderne Mathematik
- [data/math_core/source_access_manifest.json](/Users/jonasweiss/MathTeach/data/math_core/source_access_manifest.json): Register mit Werken, Zugriffspfaden und Ablagehinweisen
- [data/math_core/network_manifest.json](/Users/jonasweiss/MathTeach/data/math_core/network_manifest.json): Erstes Netzwerkmanifest fuer Proof Lines, Equation Lines, Transmission Paths und Domain Lines
- [data/teacher_mind/evidence_manifest.json](/Users/jonasweiss/MathTeach/data/teacher_mind/evidence_manifest.json): Startmanifest fuer die lokale Teacher-Mind-Evidenzbasis
- [data/teacher_mind/psychological_foundations_manifest.json](/Users/jonasweiss/MathTeach/data/teacher_mind/psychological_foundations_manifest.json): Startmanifest fuer die erste psychologische Grundausbildung des Tutors
- [data/teacher_mind/pedagogical_foundations_manifest.json](/Users/jonasweiss/MathTeach/data/teacher_mind/pedagogical_foundations_manifest.json): Startmanifest fuer die allgemeine paedagogische Grundausbildung des Tutors
- [data/teacher_mind/universal_round_u1_manifest.json](/Users/jonasweiss/MathTeach/data/teacher_mind/universal_round_u1_manifest.json): Startmanifest fuer die erste universelle Designrunde des Tutors
- [sql/001_foundation_schema.sql](/Users/jonasweiss/MathTeach/sql/001_foundation_schema.sql): Erstes Postgres-Schema fuer die Datenbasis
- [sql/002_math_corpus_collection.sql](/Users/jonasweiss/MathTeach/sql/002_math_corpus_collection.sql): Quellenkatalog, Collection-Queue und Ingestion-Tabellen
- [sql/003_math_history_program.sql](/Users/jonasweiss/MathTeach/sql/003_math_history_program.sql): Epochen, Werke und Story-Tabellen fuer Beweise und Gleichungen
- [sql/004_source_access_registry.sql](/Users/jonasweiss/MathTeach/sql/004_source_access_registry.sql): Zugriffsrouten und lokales Speicher-Audit fuer Quellen
- [sql/005_cross_epoch_network.sql](/Users/jonasweiss/MathTeach/sql/005_cross_epoch_network.sql): Generisches Schema fuer epochenuebergreifende Linien und Anker
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
- `GET /api/v1/corpus/network`
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
- Die epochenuebergreifende Vernetzung hat jetzt ein erstes Manifest mit Proof Lines, Equation Lines, Transmission Paths, Domain Lines und Application Bridges.
- Eine kleine API zeigt schon, wie Wissens- und Lehrlogik getrennt orchestriert werden.

Der naechste grosse Schritt ist der Aufbau des Mathematik-Korpus mit Zitationspflicht, Ontologie, Ingestion-Pipeline und Evaluationssuite.
