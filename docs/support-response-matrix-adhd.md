# Support Response Matrix: ADHD-Aware Support

## Rolle

Diese Matrix operationalisiert `ADHD-aware support` fuer MathTeach.

Sie ist:

- nicht-diagnostisch
- nicht-therapeutisch
- support-orientiert

Sie beschreibt, wie der Tutor reagieren soll, wenn Lernende deutliche Signale
von Aufmerksamkeits-, Uebergangs- oder exekutiver Reibung zeigen.

## Safety Frame

- keine ADHD-Diagnose durch den Tutor
- keine Identitaetsurteile
- selbstbeschriebene Hinweise des Lernenden haben Vorrang
- alle Einstellungen gelten als `candidate defaults`, nicht als starre Wahrheit

## Primaere Support Signals

- `attention_drift`
  - Fokus bricht waehrend erklaerender oder repetitiver Passagen schnell ab
- `working_memory_fragility`
  - mehrschrittige Aufgaben kippen ohne externe Struktur schnell weg
- `transition_friction`
  - Wechsel zwischen Aufgaben oder Darstellungen fuehlen sich chaotisch an
- `novelty_need`
  - leichte Variation stabilisiert Aufmerksamkeit besser als monotone Wiederholung
- `feedback_time_sensitivity`
  - spaetes Feedback verliert schnell seine lernsteuernde Wirkung
- `criticism_sensitivity`
  - harsche Korrektur fuehrt schnell zu Rueckzug oder Blockade

## Candidate Response Settings

| Dimension | Candidate Setting | Why | Source Anchors |
| --- | --- | --- | --- |
| `session_duration` | `12_to_15_minute_focus_blocks` | Kuerzere Einheiten reduzieren exekutive Ueberlastung und halten Erklaerungen handhabbar. | `cdc-adhd-classroom-support`, `barkley-executive-functions-adhd` |
| `break_pattern` | `short_structured_break_after_focus_block` | Regelmaessige kurze Pausen helfen bei Regulation und Rueckkehr in die Aufgabe. | `cdc-adhd-classroom-support`, `richardson-school-interventions-adhd` |
| `transition_buffer` | `explicit_transition_cue_before_new_step` | Klare Uebergaenge verhindern, dass Lernende zwischen Schritten den Faden verlieren. | `cdc-adhd-classroom-support`, `barkley-executive-functions-adhd` |
| `conceptual_increment` | `very_small_to_small` | Zu viel Neuheit pro Schritt erzeugt Suchlast statt Verstaendnis. | `barkley-executive-functions-adhd`, `kirschner-sweller-clark-minimal-guidance` |
| `worked_example_ratio` | `high_initial_examples` | Worked examples reduzieren Suchlast und entlasten das Arbeitsgedaechtnis. | `kirschner-sweller-clark-minimal-guidance`, `chi-self-explanations` |
| `fading_speed` | `gradual_when_stable` | Hilfe wird erst reduziert, wenn Aufmerksamkeit und Erfolg ueber mehrere Schritte stabil bleiben. | `rosenshine-principles-of-instruction`, `chi-self-explanations` |
| `symbolic_vs_verbal_balance` | `verbal_plus_visual_before_dense_symbolic` | Sprachliche und visuelle Einbettung macht Symbolik leichter anschlussfaehig. | `cdc-adhd-classroom-support`, `how-people-learn-ii` |
| `word_budget_per_chunk` | `short_chunks_under_100_words` | Kurze Chunks reduzieren Konkurrenz zwischen Leselast und mathematischem Denken. | `organizing-instruction-and-study`, `how-people-learn` |
| `chunk_limit` | `max_three_core_points` | Weniger parallele Punkte stabilisieren Fokus und Rueckerinnerung. | `organizing-instruction-and-study`, `dunlosky-effective-learning-techniques` |
| `primary_representation` | `concrete_or_light_visual_then_symbolic` | Fruehe Sichtbarkeit und Gegenstandsbezug helfen, bevor Symbolketten dominieren. | `how-people-learn-ii`, `cdc-adhd-classroom-support` |
| `error_detection_speed` | `immediate_or_near_immediate` | Schnelles Feedback verbindet Handlung und Rueckmeldung enger. | `richardson-school-interventions-adhd`, `the-power-of-feedback` |
| `error_response_style` | `normalize_then_strategy` | Fehler sollen entdramatisiert und direkt in eine Strategie uebersetzt werden. | `learning-from-errors`, `focus-on-formative-feedback` |
| `check_frequency` | `every_two_problems_or_major_step` | Haeufige kurze Checks verhindern langes Weiterlaufen mit Missverstaendnissen. | `using-student-achievement-data`, `the-power-of-feedback` |
| `check_method` | `brief_conversational_probe` | Kurze Rueckfragen sind weniger belastend als grosse Nachweise am Stueck. | `using-student-achievement-data`, `rosenshine-principles-of-instruction` |
| `checklists` | `on_by_default` | Externe Struktur ist hier funktionale Hilfe, nicht kosmetische Extraoption. | `cdc-adhd-classroom-support`, `barkley-executive-functions-adhd` |
| `timers` | `optional_visible_timer` | Sichtbare Zeitstruktur kann Orientierung und Abschlussverhalten verbessern. | `cdc-adhd-classroom-support`, `richardson-school-interventions-adhd` |

## Runtime Preferences

Bevorzugt:

- `worked_example_tutoring`
- `origin_then_example`

Nur bei ausdruecklicher Nachfrage oder hoher Stabilitaet:

- `origin_story_explanation`

Zu vermeiden:

- lange ununterbrochene Formalpassagen
- grosse Problemserien ohne Zwischenfeedback
- implizite Aufgabenuebergaenge ohne Markierung

## External Scaffolds

Standardmaessig aktiv:

- `step_labels`
- `micro-checkpoints`
- `visible_progress_markers`
- `short_goal_for_this_block`

Nur vorsichtig reduzieren:

- wenn mehrere kurze Bloecke hintereinander stabil funktionieren
- wenn der Lernende explizit weniger Struktur wuenscht

## Error Handling

Bevorzugte Sequenz:

1. Fehler kurz markieren
2. Fehler normalisieren
3. passende Strategie nennen
4. sofortiges Mini-Recovery-Beispiel geben

Nicht bevorzugt:

- pauschales `falsch`
- lange nachtraegliche Fehlerlisten
- zu spaete Sammelkorrekturen

## Progress Signals

Hinweise, dass die Einstellungen wirken:

- Fokus bleibt ueber einen ganzen Kurzblock stabil
- weniger Abbruch zwischen Rechenschritten
- Worked examples werden zunehmend selbst erklaert
- Fehler werden schneller korrigierbar

Hinweise, dass nachjustiert werden muss:

- schneller Rueckzug trotz kurzer Bloecke
- wiederholte Desorientierung an Uebergaengen
- Text wird ueberflogen, aber nicht verarbeitet
- Checks zeigen keinen Uebergang von Nachsprechen zu Verstehen

## Source Anchors

- `cdc-adhd-classroom-support`
- `richardson-school-interventions-adhd`
- `barkley-executive-functions-adhd`
- `organizing-instruction-and-study`
- `chi-self-explanations`
- `rosenshine-principles-of-instruction`
- `the-power-of-feedback`
- `focus-on-formative-feedback`
- `learning-from-errors`

## Offene Punkte

- Exakte Zeitfenster bleiben `candidate defaults` und muessen spaeter validiert werden.
- Der Umgang mit starker Kritikempfindlichkeit braucht spaeter noch feinere Guardrails.
- Kombinationen mit `dyslexia-aware support` und `scarcity-aware support` werden erst nach stabiler Einzelmatrix operationalisiert.
