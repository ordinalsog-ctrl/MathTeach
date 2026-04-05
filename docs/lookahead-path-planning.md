# Lookahead Path Planning

Stand: 2026-04-05

## Ziel

H.4 erweitert H.3 von einer direkten Naechstblock-Entscheidung auf
mehrere bewertete Lookahead-Pfade. Das System waehlte schon zuvor den
naechsten Blocktyp adaptiv; jetzt bewertet es zusaetzlich mehrere kurze
Pfadoptionen und macht den gewaehlten Pfad transparent.

## Neue sichtbare Felder

`BlockSequenceDecision` traegt jetzt:

- `selected_path_score`
- `candidate_paths`

`PlannedTeachingBlock` traegt jetzt zusaetzlich:

- `selected_path_score`
- `candidate_paths`

`SequencePlanningMetadata` traegt jetzt:

- `candidate_path_count`
- `candidate_paths`

## Was ist ein Pfad?

Ein Pfad ist eine kurze, bewertete Folge kommender Blocktypen, zum
Beispiel:

- `guided_practice -> bridge_to_application -> concept_check`
- `error_recovery -> worked_example -> guided_practice`
- `concept_introduction -> worked_example -> guided_practice`

Die erste Blockart des besten Pfads bleibt weiterhin der sichtbare
`next_block_type`. H.4 erklaert jetzt aber, warum gerade dieser kurze
Verlauf den Alternativen vorgezogen wurde.

## Bewertungslogik

Die aktuelle H.4-Version bewertet Pfade ueber eine kleine, explizite
Heuristikschicht:

- Bonus fuer Pfade, die mit der staerksten H.3-Naechstblock-Empfehlung
  beginnen
- Bonus fuer Intent-Passung, z.B. Transfer in `mastery_path` oder fruehe
  Reparatur in `adaptive_remediation`
- Bonus fuer Evidence-Passung, z.B. fruehe `error_recovery` bei
  `stagnation_pattern` oder fruehe Sprach-/Konzeptnahe bei
  `vocabulary_gap`
- Bonus fuer Support-Mix, z.B. fruehe `concept_check`-Bausteine bei
  `ADHD + Dyscalculia`
- kleine Abzuege fuer unnoetige Wiederholung oder zu fruehen Sprung in
  unpassende Pfade

## API-Sichtbarkeit

Die API kann jetzt z.B. sichtbar machen:

- welcher Block als naechstes empfohlen wird
- welche zwei oder drei Alternativpfade mitgedacht wurden
- welcher Score den aktuell gewaehlten Pfad getragen hat
- welche Begruendungen pro Pfad gesammelt wurden

## Testanker

Die H.4-Schicht ist aktuell abgesichert ueber:

- [tests/test_block_sequence_planner.py](/Users/jonasweiss/MathTeach/tests/test_block_sequence_planner.py)
- [tests/test_planner_runtime_flow.py](/Users/jonasweiss/MathTeach/tests/test_planner_runtime_flow.py)
- [tests/test_api.py](/Users/jonasweiss/MathTeach/tests/test_api.py)

## Naechster Schritt

H.5 kann jetzt auf echter Pfadbewertung aufsetzen: nicht nur heuristisch
kurze Pfade sortieren, sondern spaeter Pfade staerker an langfristige
Lernziele, Session-Historie und Pilotdaten kalibrieren.
