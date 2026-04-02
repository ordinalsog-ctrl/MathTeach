# Support Response Matrix: Language-Sensitive Support

## Rolle

Diese Matrix operationalisiert `language-sensitive support` fuer MathTeach.

Sie ist:

- nicht-diagnostisch
- nicht-therapeutisch
- support-orientiert

Sie beschreibt, wie der Tutor reagieren soll, wenn Sprachlast, Fachwortdichte
oder der Abstand zwischen Alltagssprache und mathemischer Fachsprache den
Zugang zur Mathematik erschweren.

## Safety Frame

- keine Gleichsetzung von Sprachbarriere mit mathemischer Schwaeche
- keine Defiziterzaehlung ueber Mehrsprachigkeit
- sprachliche Bruecken gelten als Zugangsbedingung, nicht als Absenkung des Niveaus
- alle Einstellungen gelten als `candidate defaults`

## Primaere Support Signals

- `term_density_friction`
  - mehrere neue Fachwoerter gleichzeitig machen den Einstieg instabil
- `everyday_to_math_gap`
  - Alltagssprache und mathemische Bedeutung werden nicht automatisch verbunden
- `syntax_load_friction`
  - lange oder verschachtelte Saetze blockieren das mathemische Verstehen
- `word_problem_language_barrier`
  - Textaufgaben scheitern teilweise an Sprache, bevor die Mathematik sichtbar wird
- `key_term_confirmation_need`
  - wichtige Begriffe muessen haeufig kurz gesichert werden, bevor der naechste Schritt traegt

## Candidate Response Settings

| Dimension | Candidate Setting | Why | Source Anchors |
| --- | --- | --- | --- |
| `symbolic_vs_verbal_balance` | `everyday_language_bridge_before_compact_symbolic` | Fachwoerter und Symbole werden erst an klare Alltagssprache und sichtbare Bedeutung angebunden. | `ies-english-learners-practice-guide`, `sharma-sharma-multilingual-math-meta-analysis` |
| `word_budget_per_chunk` | `short_chunks_with_controlled_vocabulary` | Kurze Chunks mit kontrolliertem Wortschatz reduzieren Sprachlast ohne den mathemischen Kern zu verlieren. | `ies-english-learners-practice-guide`, `organizing-instruction-and-study` |
| `primary_representation` | `visual_plus_term_support_before_dense_language` | Visuals und explizite Begriffshilfen tragen die Bedeutung, bevor dichte Sprache verlangt wird. | `cast-udl-guidelines-3`, `sharma-sharma-multilingual-math-meta-analysis` |
| `error_response_style` | `clarify_term_meaning_then_math_correction` | Vor einer mathemischen Korrektur wird geprueft, ob ein Begriff oder eine sprachliche Formulierung den Fehler ausgeloest hat. | `focus-on-formative-feedback`, `ies-english-learners-practice-guide` |
| `check_frequency` | `every_major_step_with_term_confirmation` | Kurze Term-Checks verhindern, dass Sprachmissverstaendnisse mehrere Schritte lang mitgeschleppt werden. | `using-student-achievement-data`, `the-power-of-feedback` |
| `language_support` | `translated_key_terms_glossary_and_simplified_syntax` | Schluesselbegriffe, Glossar-Hilfen und klare Syntax oeffnen den Zugang zur fachlichen Idee. | `ies-english-learners-practice-guide`, `cast-udl-guidelines-3` |
| `external_scaffolds` | `key_term_glossary_and_everyday_math_bridge` | Sichtbare Begriffsbruecken und kurze Sprachhilfen machen die Mathematik anschlussfaehiger. | `ies-english-learners-practice-guide`, `rosenshine-principles-of-instruction` |

## Runtime Preferences

Bevorzugt:

- `guided_concept_explanation`
- `worked_example_tutoring`
- `origin_then_example`

Besonders hilfreich:

- kurze Begriffsbruecken vor jeder formalen Verdichtung
- Visualisierung plus explizite Benennung der mathemischen Rolle eines Terms
- kontrollierte Satzlaenge in Textaufgaben

Zu vermeiden:

- mehrere neue Fachwoerter in einem einzigen Schritt
- lange Schachtelsaetze vor der eigentlichen Mathematik
- Annahme, dass Sprachreibung automatisch eine Fachluecke beweist

## External Scaffolds

Standardmaessig aktiv:

- `key_term_glossary`
- `everyday_to_math_language_bridge`
- `translated_key_terms_when_needed`
- `term_confirmation_checks`

Optional spaeter:

- zweisprachige Begriffskarten
- umschaltbare Alltagssprache-zu-Fachsprache-Ansicht

## Error Handling

Bevorzugte Sequenz:

1. pruefen, ob ein Begriff oder eine Formulierung unklar war
2. mathemische Rolle des Terms sichtbar machen
3. dann erst die Operation oder Regel lokal korrigieren

Nicht bevorzugt:

- sofortige Fachkorrektur ohne Sprachklaerung
- dichte Umformulierungen mit neuen Fachwoertern waehrend der Fehlerkorrektur

## Progress Signals

Hinweise, dass die Einstellungen wirken:

- Fachwoerter werden ruhiger und konsistenter verwendet
- Textaufgaben kippen seltener schon an der Sprachschicht
- mathemische Symbole werden sicherer mit ihren Bedeutungen verbunden
- Rueckfragen betreffen eher den Inhalt als einzelne Woerter

Hinweise, dass nachjustiert werden muss:

- richtige Ideen sind sichtbar, brechen aber an Textaufgaben weg
- Begriffe muessen ueber mehrere Schritte hinweg neu erklaert werden
- Satzlaenge oder Wortdichte blockiert weiter deutlich

## Source Anchors

- `ies-english-learners-practice-guide`
- `sharma-sharma-multilingual-math-meta-analysis`
- `cast-udl-guidelines-3`
- `organizing-instruction-and-study`
- `using-student-achievement-data`
- `the-power-of-feedback`
- `focus-on-formative-feedback`
- `rosenshine-principles-of-instruction`

## Offene Punkte

- Zweisprachige Ausgabeformate werden spaeter gesondert operationalisiert.
- Die Kombination mit `scarcity-aware support` braucht spaeter eine eigene Priorisierungslogik.
- Audio- und Vorlesekanal folgen spaeter als eigene Runtime-Schicht.
