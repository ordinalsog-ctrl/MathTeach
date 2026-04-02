# Mode Selection Strategy

## Rolle

Dieses Dokument definiert die erste `support-sensitive Moduswahl` fuer den
Planner.

Es beantwortet:

- welcher Modus unter Konfliktlagen bevorzugt wird
- wann ein angefragter Modus bewusst ueberschrieben wird
- welche `constraints` den gewaehlten Modus einhegen

## Grundprinzip

MathTeach trennt jetzt drei Ebenen:

1. `response settings`
2. `conflict resolution`
3. `mode selection`

Der `conflict_resolver` klaert:

- welche Supportlagen kollidieren
- welche Prioritaetsleitern gelten

Der `mode_selector` klaert danach:

- in welchem Tutoring-Modus diese Aufloesung am lernwirksamsten getragen wird

## Aktive Modusfamilien

- `guided_concept_explanation`
- `worked_example_tutoring`
- `origin_story_explanation`
- `origin_then_example`
- `formal_compact_explanation`

## Designregel

Nicht jeder Konflikt braucht einen neuen Modus.

MathTeach arbeitet deshalb mit:

- wenigen stabilen Modi
- expliziten `constraints` innerhalb des Modus

## Decision Matrix

| Mixed Profile Situation | Primary Mode | Secondary Mode | Core Constraints |
| --- | --- | --- | --- |
| `ADHD + Dyscalculia + Scarcity` | `worked_example_tutoring` | `origin_then_example` | `immediate_relevance_signal`, `high_visual_and_concrete_support`, `low_notation_density`, `micro_success_cycles` |
| `ADHD + Autism + Scarcity` | `worked_example_tutoring` | `guided_concept_explanation` | `high_structure`, `minimal_mode_switching`, `predictable_checkpoint_structure`, `immediate_relevance_signal` |
| `Dyscalculia + Language-Sensitive + Scarcity` | `origin_then_example` | `worked_example_tutoring` | `short_origin_bridge`, `visual_heavy`, `term_support_first`, `quantity_before_symbols` |
| `ADHD + Scarcity` | `worked_example_tutoring` | `origin_then_example` | `micro_origin_bridge`, `immediate_relevance_signal`, `micro_success_cycles` |
| `ADHD + Dyscalculia` | `worked_example_tutoring` | `guided_concept_explanation` | `high_visual_and_concrete_support`, `low_notation_density` |
| `Dyscalculia + Language-Sensitive` | `origin_then_example` | `worked_example_tutoring` | `short_origin_bridge`, `term_support_first`, `quantity_before_symbols` |

## Override-Regeln

### 1. Pure Origin-Mode unter hoher Supportlast

Wenn der angefragte Modus `origin_story_explanation` ist, aber aktive
Supportlagen hohe Einstiegslast problematisch machen, wird auf
`origin_then_example` reduziert.

Regelidee:

- Ursprungssignal bleibt
- langer Vorlauf wird gekuerzt
- Handlungsfaehigkeit kommt frueher

### 2. Formal-Compact unter aktiver Supportlage

Wenn `formal_compact_explanation` angefragt wird, aber aktive Supportlagen
nicht-researchige Sitzungen deutlich strukturieren muessen, wird auf
`guided_concept_explanation` zurueckgesetzt.

## Session-Kontext in der ersten Version

Die erste Version nutzt als Session-Kontext:

- Zieltext aus dem Request
- Lernerprofil
- aktive Supports
- Konfliktpaare
- Triads
- Priority Ladders

Noch nicht enthalten:

- explizites Zeitbudget ausserhalb des Pace-Felds
- Lernhistorie ueber mehrere Sitzungen
- Live-Umschalten innerhalb derselben Session

## Noch offen

- dynamischer Moduswechsel waehrend einer Session
- feinere Moduswahl fuer vier oder mehr aktive Profile
- Nutzung echter Lernerhistorie fuer Moduswahl

## Naechste Ausbaustufe

Nach dieser Strategie folgt:

1. `mode selection tests erweitern`
2. `planner-level live mode adaptation`
3. `history-aware mode selection`
