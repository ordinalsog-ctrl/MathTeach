# Long-Term Integration

Stand: 2026-04-05

## Ziel

H.5 erweitert die H.4-Pfadbewertung um drei laengerfristige
Orientierungen:

- Lernziele
- Session-Historie
- pilotdatengestuetzte Pfadkorrektur

Damit kann das System jetzt besser unterscheiden, ob ein Pfad zwar
kurzfristig gut aussieht, aber fuer stabile Mastery oder spaetere
Transferziele weniger passend ist.

## Neue sichtbare Felder

`TeachingPlan` traegt jetzt:

- `long_term_context`
- `enriched_paths`
- `recommended_path_id`
- `recommended_path_mastery_gain`

`long_term_context` zeigt aktuell:

- `session_id`
- `current_concept`
- `learning_goals`
- `concept_mastery_tracking`
- `history_entry_count`

## Neue Kernmodelle

- `LongTermLearningGoal`
- `SessionHistoryEntry`
- `SessionProgressTracker`
- `EnrichedPathEvaluation`
- `PathScoringCriteria`
- `LongTermContext`

## Bewertungslogik

Die H.5-Schicht startet mit einer bewusst kleinen, expliziten
Scoring-Struktur:

- `heuristic`
  - bestehender H.4-Score

- `goal_alignment`
  - bewertet, ob der Pfad die aktiven Lernziele sinnvoll stuetzt

- `history_alignment`
  - bewertet, ob der Pfad auf dem bisherigen Sitzungsverlauf aufbaut

- `evidence_continuity`
  - bewertet, ob der Pfad zu den aktiven Evidence-Mustern passt

- `profile_match`
  - bewertet, ob die fruehen Schritte des Pfads zum aktiven Support-Mix
    passen

- `pilot_data_adjustment`
  - kleiner Korrekturfaktor aus einer ersten, bewusst schlanken
    Erfolgsraten-Tabelle

## Session-Tracking

Die erste H.5-Version nutzt noch kein grosses Persistenzsystem. Statt
dessen baut sie zur Laufzeit einen `SessionProgressTracker` aus den
bereits geplanten und beobachteten Bloecken.

Dadurch sind jetzt schon moeglich:

- einfache Konzept-Slug-Erkennung aus dem Objective
- erste Learning Goals passend zum aktuellen Modus
- eine rollierende Mastery-Schaetzung pro Konzept
- sichtbare History-Eintraege ueber die bereits beobachteten Bloecke

## Pilotdaten

Die Pilotdaten-Schicht ist in H.5 bewusst klein gehalten:

- sie ist noch kein externes Analytics-System
- sie ist noch kein lernendes Modell
- sie ist eine erste regelbasierte Erfolgsraten-Tabelle fuer bekannte
  Blocktyp-/Pattern-Kombinationen

Damit steht schon die Architektur fuer spaetere echte Kalibrierung,
ohne dass der aktuelle Planner auf noch nicht existierende Datensaetze
warten muss.

## Testanker

Die H.5-Schicht ist aktuell abgesichert ueber:

- [tests/test_long_term_integration.py](/Users/jonasweiss/MathTeach/tests/test_long_term_integration.py)
- [tests/test_planner_runtime_flow.py](/Users/jonasweiss/MathTeach/tests/test_planner_runtime_flow.py)
- [tests/test_api.py](/Users/jonasweiss/MathTeach/tests/test_api.py)

## Naechster Schritt

H.6 kann jetzt die Gewichtungen und Pilotdaten empirischer kalibrieren:
nicht nur regelbasiert plausible Pfade scoren, sondern die Scores
spaeter an echten Lernergebnissen nachjustieren.
