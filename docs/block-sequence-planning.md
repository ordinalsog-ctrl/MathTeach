# Block Sequence Planning

Stand: 2026-04-04

## Ziel

H.3 erweitert H.2g von blockweiser Move-Anpassung auf blocksequenzielle
Routing-Entscheidungen. Das System entscheidet jetzt nicht mehr nur,
wie ein Block unterstuetzt wird, sondern auch, welcher Blocktyp als
naechstes folgen sollte.

## Neue sichtbare Felder

`PlannedTeachingBlock` traegt jetzt:

- `sequence_intent`
- `transition_reason`
- `next_block_type`
- `alternative_next_block_types`
- `routing_confidence`
- `routing_rationale`

`TeachingPlan` traegt jetzt zusaetzlich:

- `block_sequence_state`
- `sequence_planning_metadata`

## Sequenz-Intents

Die aktuelle H.3-Schicht nutzt fuenf uebergeordnete Pfade:

- `concept_buildup`
- `confidence_building`
- `error_recovery_cycle`
- `mastery_path`
- `adaptive_remediation`

Diese Intents bestimmen die Lookahead-Reihenfolge, aus der Alternativen
und spaetere Preview-Bloecke aufgebaut werden.

## Routing-Regeln

Die erste H.3-Version nutzt bewusst eine kleine, explizite Regelmenge:

- `worked_example + rapid_consecutive_success`
  - naechster Block: `guided_practice`
  - Intent: `mastery_path`

- `guided_practice + stagnation_pattern`
  - naechster Block: `error_recovery`
  - Intent: `adaptive_remediation`

- `concept_introduction + vocabulary_gap`
  - naechster Block: `concept_introduction`
  - Intent: `concept_buildup`
  - Wirkung: Wiederholung mit kleinerer Sprachlast statt zu fruehem
    Vorwaertssprung

- `error_recovery + concept_confusion`
  - naechster Block: `worked_example`
  - Intent: `error_recovery_cycle`

- `guided_practice + confidence_buildup`
  - naechster Block: `bridge_to_application`
  - Intent: `mastery_path`

- `worked_example + ADHD + Dyscalculia`
  - naechster Block: `concept_check`, wenn kein staerkeres
    Erfolgsmuster vorliegt
  - Intent: `confidence_building`

## Planner-Integration

Der Planner arbeitet jetzt in drei Schichten:

1. H.2g baut den aktuellen Block mit `block_type`,
   `evidence_combination` und Konfliktaufloesung.
2. H.3 routet aus diesem Block den empfohlenen naechsten Blocktyp.
3. Der finale Preview-Block uebernimmt die letzte Routing-Entscheidung
   als seinen sichtbaren `block_type`.

Damit bleibt beobachteter Blockkontext stabil, waehrend die Vorschau
erstmals wirklich adaptiv wird.

## API-Sichtbarkeit

Die API kann jetzt gleichzeitig zeigen:

- welcher Blocktyp gerade aktiv war
- welcher Blocktyp als naechstes empfohlen wird
- warum diese Wahl getroffen wurde
- welche Alternativen aktuell sinnvoll waeren
- welcher grobere Sequenzpfad gerade aktiv ist

## Testanker

Die H.3-Schicht ist aktuell abgesichert ueber:

- [tests/test_block_sequence_planner.py](/Users/jonasweiss/MathTeach/tests/test_block_sequence_planner.py)
- [tests/test_planner_runtime_flow.py](/Users/jonasweiss/MathTeach/tests/test_planner_runtime_flow.py)
- [tests/test_api.py](/Users/jonasweiss/MathTeach/tests/test_api.py)

## Weiterfuehrung

H.4 ist jetzt als eigene Folgeschicht umgesetzt und bewertet mehrere
kurze Lookahead-Pfade statt nur einer direkten Naechstblock-Empfehlung.
Der Anschluss ist dokumentiert in
[lookahead-path-planning.md](/Users/jonasweiss/MathTeach/docs/lookahead-path-planning.md).
