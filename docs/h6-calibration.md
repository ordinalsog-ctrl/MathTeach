# H.6 Calibration

Stand: 2026-04-05

## Ziel

H.6 erweitert die H.5-Pfadbewertung um eine erste empirische
Kalibrierungsschicht. Die Pfade werden damit nicht mehr nur nach
regelbasierten Gewichten sortiert, sondern gegen geloggte
Entscheidungen und spaeter beobachtete Outcomes nachjustiert.

## Neue Bausteine

- `DecisionRecord`
  - speichert, welcher Pfad gewaehlt wurde, welche Alternativen es gab
    und unter welchem Evidence- und Support-Kontext die Entscheidung
    fiel

- `OutcomeMetrics`
  - beschreibt spaeter beobachtete Ergebnisse wie
    `mastery_gain_estimate`, `error_rate_trend`,
    `observed_engagement` und `confidence_change`

- `CalibrationWeights`
  - verwaltet die aktiven Gewichte fuer
    `heuristic`, `goal_alignment`, `history_alignment`,
    `evidence_continuity`, `profile_match` und
    `pilot_data_adjustment`

- `CalibrationEngine`
  - loggt Entscheidungen
  - nimmt Outcome-Updates entgegen
  - berechnet aus genuegend abgeschlossenen Faellen neue Gewichte
  - re-rankt `enriched_paths` mit diesen Gewichten

## Laufzeitfluss

1. H.4/H.5 erzeugen wie bisher `candidate_paths` und `enriched_paths`.
2. `CalibrationEngine.apply_to_enriched_paths(...)` rechnet daraus die
   aktuell kalibrierte Sortierung.
3. Der letzte Preview-Block uebernimmt diese Sortierung als sichtbare
   Naechstblock-Empfehlung.
4. Der Planner loggt genau diese Entscheidung als `DecisionRecord`.
5. Spaeter kann ueber `record_decision_outcome(...)` ein beobachtetes
   Outcome fuer dieselbe `decision_id` nachgetragen werden.
6. Sobald genug abgeschlossene Entscheidungen vorliegen, passt die
   Engine ihre Gewichte an.

## Sichtbare API-Felder

`TeachingPlan` traegt jetzt zusaetzlich:

- `calibration_context`
  - `decision_id`
  - `calibration_rounds`
  - `logged_decision_count`
  - `last_calibration`
  - `active_weights`

`sequence_planning_metadata` traegt jetzt:

- `calibration_decision_id`
- `calibration_rounds`

`enriched_paths` traegt jetzt pro Pfad:

- `uncalibrated_total_score`
- `calibration_applied`
- in `score_breakdown` zusaetzlich
  - `uncalibrated_total`
  - `calibrated_total`

## Bewusste Grenzen der ersten H.6-Version

- die Kalibrierung ist noch in-memory und noch nicht ueber Sessions
  persistent
- sie nutzt noch keine externen Analytics-Systeme
- die Outcome-Schaetzung ist noch heuristisch und nicht aus echten
  Lernerdatensaetzen gelernt
- die Gewichtsanpassung ist bewusst einfach gehalten, damit sie
  nachvollziehbar bleibt

## Testanker

- [tests/test_h6_calibration.py](/Users/jonasweiss/MathTeach/tests/test_h6_calibration.py)
- [tests/test_planner_runtime_flow.py](/Users/jonasweiss/MathTeach/tests/test_planner_runtime_flow.py)
- [tests/test_api.py](/Users/jonasweiss/MathTeach/tests/test_api.py)

## Weiterfuehrung

H.7 ist jetzt als direkte Folgeschicht umgesetzt und macht die H.6-
Kalibrierung ueber einen dateibasierten Store persistent. Der Anschluss
ist dokumentiert in
[h7-persistent-calibration.md](/Users/jonasweiss/MathTeach/docs/h7-persistent-calibration.md).
