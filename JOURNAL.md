# MathTeach Journal

Stand: 2026-04-05

## Phase-H.8-Profile-Aware-Calibration 2026-04-05

Die H.7-Kalibrierung arbeitet jetzt nicht mehr nur global. Mit H.8
werden persistente Kalibrierungsdaten auch profilspezifisch entlang von
Support-Mix, Sequenz-Intent, dominanter Evidence und Blocktyp
ausgewertet.

Wichtigste Konsequenzen:

- `CalibrationProfile` fuehrt fuer kontextspezifische Slices jetzt
  eigene Gewichte, Sample-Groessen und Gewichts-Historien
- `CalibrationEngine` waehlt fuer `enriched_paths` jetzt das passendste
  Profil und mischt dessen Gewichte bei niedriger Konfidenz kontrolliert
  mit dem globalen H.7-Satz
- `DecisionRecord` und `calibration_context` tragen jetzt sichtbar
  `calibration_profile_id`, Profil-Konfidenz und
  Stratifikationsdimensionen
- `CalibrationStore` persistiert jetzt auch die profilspezifischen
  Kalibrierungsprofile statt nur globale Gewichte
- die API zeigt ueber neue Endpunkte die gespeicherten Profile und gibt
  bei Outcome-Updates zurueck, welcher Profil-Slice fortgeschrieben
  wurde

Neue oder aktualisierte Referenzartefakte:

- [src/mathteach/models.py](/Users/jonasweiss/MathTeach/src/mathteach/models.py)
- [src/mathteach/services/calibration_store.py](/Users/jonasweiss/MathTeach/src/mathteach/services/calibration_store.py)
- [src/mathteach/services/calibration_engine.py](/Users/jonasweiss/MathTeach/src/mathteach/services/calibration_engine.py)
- [src/mathteach/services/planner.py](/Users/jonasweiss/MathTeach/src/mathteach/services/planner.py)
- [src/mathteach/main.py](/Users/jonasweiss/MathTeach/src/mathteach/main.py)
- [tests/test_h8_profile_calibration.py](/Users/jonasweiss/MathTeach/tests/test_h8_profile_calibration.py)
- [tests/test_calibration_store.py](/Users/jonasweiss/MathTeach/tests/test_calibration_store.py)
- [tests/test_planner_runtime_flow.py](/Users/jonasweiss/MathTeach/tests/test_planner_runtime_flow.py)
- [tests/test_api.py](/Users/jonasweiss/MathTeach/tests/test_api.py)
- [docs/h8-profile-calibration.md](/Users/jonasweiss/MathTeach/docs/h8-profile-calibration.md)

Verifikation:

- `ruff`: ausstehend in dieser Runde
- gezielte Tests: `87 passed, 1 warning`
- Full-Suite: ausstehend in dieser Runde

## Phase-H.7-Persistent-Calibration 2026-04-05

Die H.6-Kalibrierung bleibt jetzt nicht mehr nur im Speicher. Mit H.7
koennen Entscheidungslogs, Outcome-Metriken und Gewichtshistorie
dateibasiert ueber Sessions und Prozessstarts hinweg erhalten bleiben.

Wichtigste Konsequenzen:

- neuer
  [calibration_store.py](/Users/jonasweiss/MathTeach/src/mathteach/services/calibration_store.py)
  als atomare JSON-Persistenz fuer Kalibrierungsdaten
- `CalibrationEngine` kann jetzt optional mit Store und Autosave laufen
  und laedt fruehere Entscheidungen sowie Gewichte beim Start wieder ein
- `CalibrationWeightsSnapshot` macht Gewichtsverschiebungen jetzt
  historisch nachvollziehbar statt nur den letzten Stand sichtbar
- `calibration_context` zeigt jetzt auch
  `persistent_store_path`, `persisted_decision_count`,
  `recent_success_rate` und `weight_stability_index`
- die API traegt jetzt neue H.7-Endpunkte fuer Outcome-Erfassung sowie
  Statistik- und History-Inspektion der Kalibrierung
- die bestehende H.6-Pfadentscheidung bleibt dabei erhalten; H.7 macht
  sie dauerhaft und ueber Neustarts hinweg nutzbar

Neue oder aktualisierte Referenzartefakte:

- [src/mathteach/config.py](/Users/jonasweiss/MathTeach/src/mathteach/config.py)
- [src/mathteach/main.py](/Users/jonasweiss/MathTeach/src/mathteach/main.py)
- [src/mathteach/models.py](/Users/jonasweiss/MathTeach/src/mathteach/models.py)
- [src/mathteach/services/calibration_store.py](/Users/jonasweiss/MathTeach/src/mathteach/services/calibration_store.py)
- [src/mathteach/services/calibration_engine.py](/Users/jonasweiss/MathTeach/src/mathteach/services/calibration_engine.py)
- [src/mathteach/services/planner.py](/Users/jonasweiss/MathTeach/src/mathteach/services/planner.py)
- [tests/test_calibration_store.py](/Users/jonasweiss/MathTeach/tests/test_calibration_store.py)
- [tests/test_h7_persistent_calibration.py](/Users/jonasweiss/MathTeach/tests/test_h7_persistent_calibration.py)
- [tests/test_api.py](/Users/jonasweiss/MathTeach/tests/test_api.py)
- [docs/h7-persistent-calibration.md](/Users/jonasweiss/MathTeach/docs/h7-persistent-calibration.md)

Verifikation:

- `ruff`: bestanden
- gezielte Tests: `57 passed, 1 warning`
- Full-Suite: `183 passed, 1 warning`

## Phase-H.6-Calibration 2026-04-05

Die H.5-Pfadbewertung ist jetzt nicht mehr statisch. Der Planner loggt
sichtbare Pfadentscheidungen, kann spaetere Outcomes an dieselbe
`decision_id` haengen und re-rankt die H.5-Pfade ueber eine erste
Kalibrierungsschicht.

Wichtigste Konsequenzen:

- neue Modelle fuer `DecisionRecord`, `OutcomeMetrics`,
  `CalibrationWeights` und `CalibrationContext`
- der neue
  [calibration_engine.py](/Users/jonasweiss/MathTeach/src/mathteach/services/calibration_engine.py)
  haelt Entscheidungslogs, Outcome-Updates und einfache
  Gewichtsanpassungen zusammen
- `build_teaching_plan(...)` akzeptiert jetzt optional einen
  `CalibrationEngine` und nutzt ihn, um `enriched_paths` vor der
  finalen Preview-Empfehlung neu zu sortieren
- der letzte Preview-Block uebernimmt jetzt sichtbar die kalibrierte
  Pfadreihenfolge statt nur die rohe H.4/H.5-Heuristik
- `TeachingPlan` traegt jetzt `calibration_context`, waehrend
  `sequence_planning_metadata` zusaetzlich
  `calibration_decision_id` und `calibration_rounds` sichtbar macht
- ueber `record_decision_outcome(...)` koennen spaetere Beobachtungen
  jetzt direkt auf die vorherige Pfadwahl zurueckgebucht werden

Neue oder aktualisierte Referenzartefakte:

- [src/mathteach/models.py](/Users/jonasweiss/MathTeach/src/mathteach/models.py)
- [src/mathteach/services/calibration_engine.py](/Users/jonasweiss/MathTeach/src/mathteach/services/calibration_engine.py)
- [src/mathteach/services/planner.py](/Users/jonasweiss/MathTeach/src/mathteach/services/planner.py)
- [tests/test_h6_calibration.py](/Users/jonasweiss/MathTeach/tests/test_h6_calibration.py)
- [tests/test_planner_runtime_flow.py](/Users/jonasweiss/MathTeach/tests/test_planner_runtime_flow.py)
- [tests/test_api.py](/Users/jonasweiss/MathTeach/tests/test_api.py)
- [docs/h6-calibration.md](/Users/jonasweiss/MathTeach/docs/h6-calibration.md)

Verifikation:

- `ruff`: bestanden
- gezielte Tests: `83 passed, 1 warning`
- Full-Suite: `176 passed, 1 warning`

## Phase-H.5-Long-Term-Integration 2026-04-05

Die H.4-Lookahead-Pfade werden jetzt nicht mehr nur lokal ueber
Evidenz und Profilpassung bewertet. Der Planner verknuepft sie erstmals
mit Langfristlernzielen, Session-Historie und einem kleinen
pilotdatengestuetzten Korrekturfaktor.

Wichtigste Konsequenzen:

- neue Modelle fuer `LongTermLearningGoal`, `SessionProgressTracker`,
  `EnrichedPathEvaluation` und `LongTermContext`
- der neue
  [learner_progress_model.py](/Users/jonasweiss/MathTeach/src/mathteach/services/learner_progress_model.py)
  leitet jetzt Lernziele, Konzept-Slugs und eine erste
  Mastery-Schaetzung aus dem bisherigen Sitzungsverlauf ab
- `enrich_candidate_paths(...)` in
  [block_sequence_planner.py](/Users/jonasweiss/MathTeach/src/mathteach/services/block_sequence_planner.py)
  bewertet H.4-Pfade jetzt zusaetzlich nach Goal Alignment,
  History Alignment, Evidence Continuity, Profile Match und
  Pilot-Adjustment
- `TeachingPlan` traegt jetzt sichtbar `long_term_context`,
  `enriched_paths`, `recommended_path_id` und
  `recommended_path_mastery_gain`
- die API kann damit jetzt zeigen, welcher Pfad nicht nur kurzfristig,
  sondern auch fuer Konzeptaufbau und stabilere Mastery sinnvoller ist

Neue oder aktualisierte Referenzartefakte:

- [src/mathteach/models.py](/Users/jonasweiss/MathTeach/src/mathteach/models.py)
- [src/mathteach/services/learner_progress_model.py](/Users/jonasweiss/MathTeach/src/mathteach/services/learner_progress_model.py)
- [src/mathteach/services/block_sequence_planner.py](/Users/jonasweiss/MathTeach/src/mathteach/services/block_sequence_planner.py)
- [src/mathteach/services/planner.py](/Users/jonasweiss/MathTeach/src/mathteach/services/planner.py)
- [tests/test_long_term_integration.py](/Users/jonasweiss/MathTeach/tests/test_long_term_integration.py)
- [tests/test_planner_runtime_flow.py](/Users/jonasweiss/MathTeach/tests/test_planner_runtime_flow.py)
- [tests/test_api.py](/Users/jonasweiss/MathTeach/tests/test_api.py)
- [docs/long-term-integration.md](/Users/jonasweiss/MathTeach/docs/long-term-integration.md)

Verifikation:

- `ruff`: bestanden
- gezielte Tests: `81 passed, 1 warning`
- Full-Suite: `172 passed, 1 warning`

## Phase-H.4-Lookahead-Path-Evaluation 2026-04-05

Die H.3-Blocksequenz ist jetzt nicht mehr auf genau eine direkte
Naechstblock-Empfehlung beschraenkt. Stattdessen bewertet der Planner
jetzt mehrere moegliche Lookahead-Pfade und macht sichtbar, warum der
ausgewaehlte Pfad gegenueber den Alternativen bevorzugt wurde.

Wichtigste Konsequenzen:

- `BlockSequenceDecision` traegt jetzt
  `selected_path_score` und `candidate_paths`
- jeder `PlannedTeachingBlock` zeigt jetzt nicht nur
  `next_block_type`, sondern auch mehrere bewertete Pfadoptionen
- `sequence_planning_metadata` macht jetzt sichtbar, wie viele
  Kandidaten bewertet wurden und welche Pfade als aktuelle Alternativen
  gelten
- die H.4-Pfadbewertung bleibt auf dem bestehenden H.3-Entscheidungsweg
  aufgesetzt, statt einen zweiten Planner-Pfad zu eroeffnen
- Pattern-, Support- und Sequenzheuristiken koennen jetzt nicht nur den
  naechsten Block, sondern auch kurze Pfadverlaeufe wie
  `guided_practice -> bridge_to_application -> concept_check` oder
  `error_recovery -> worked_example -> guided_practice` gegeneinander
  abwaegen

Neue oder aktualisierte Referenzartefakte:

- [src/mathteach/models.py](/Users/jonasweiss/MathTeach/src/mathteach/models.py)
- [src/mathteach/services/block_sequence_planner.py](/Users/jonasweiss/MathTeach/src/mathteach/services/block_sequence_planner.py)
- [src/mathteach/services/planner.py](/Users/jonasweiss/MathTeach/src/mathteach/services/planner.py)
- [tests/test_block_sequence_planner.py](/Users/jonasweiss/MathTeach/tests/test_block_sequence_planner.py)
- [tests/test_planner_runtime_flow.py](/Users/jonasweiss/MathTeach/tests/test_planner_runtime_flow.py)
- [tests/test_api.py](/Users/jonasweiss/MathTeach/tests/test_api.py)
- [docs/lookahead-path-planning.md](/Users/jonasweiss/MathTeach/docs/lookahead-path-planning.md)

Verifikation:

- `ruff`: bestanden
- gezielte Tests: `82 passed, 1 warning`
- Full-Suite: `168 passed, 1 warning`

## Phase-H.3-Block-Sequential-Planning 2026-04-04

Die Planung springt jetzt ueber H.2g hinaus: jeder Block traegt nicht
mehr nur seinen eigenen `block_type` und seine lokale
Conflict-Resolution, sondern auch eine sichtbare Routing-Entscheidung
fuer den naechsten Blocktyp. Die finale Vorschau kann damit erstmals
einen anderen Blocktyp zeigen als der aktuelle Modus heuristisch allein
erwarten liesse.

Wichtigste Konsequenzen:

- neue `BlockSequenceDecision`-, `BlockSequenceState`- und
  `SequencePlanningMetadata`-Modelle machen H.3 im API-Vertrag sichtbar
- `PlannedTeachingBlock` traegt jetzt
  `sequence_intent`, `transition_reason`, `next_block_type`,
  `alternative_next_block_types`, `routing_confidence` und
  `routing_rationale`
- der neue
  [block_sequence_planner.py](/Users/jonasweiss/MathTeach/src/mathteach/services/block_sequence_planner.py)
  routet den naechsten Blocktyp aus `block_type`,
  `EvidenceCombinationPattern` und aktiven Support-Profilen
- bekannte H.3-Pfade sind jetzt operational, z.B.
  `worked_example -> guided_practice` bei
  `rapid_consecutive_success`,
  `guided_practice -> error_recovery` bei
  `stagnation_pattern` oder
  `error_recovery -> worked_example` bei `concept_confusion`
- der Planner nutzt die letzte Routing-Entscheidung jetzt direkt fuer
  den finalen Preview-Block, sodass der naechste Blocktyp nicht mehr nur
  dokumentiert, sondern auch sichtbar vorausgeplant ist

Neue oder aktualisierte Referenzartefakte:

- [src/mathteach/models.py](/Users/jonasweiss/MathTeach/src/mathteach/models.py)
- [src/mathteach/services/block_sequence_planner.py](/Users/jonasweiss/MathTeach/src/mathteach/services/block_sequence_planner.py)
- [src/mathteach/services/planner.py](/Users/jonasweiss/MathTeach/src/mathteach/services/planner.py)
- [tests/test_block_sequence_planner.py](/Users/jonasweiss/MathTeach/tests/test_block_sequence_planner.py)
- [tests/test_planner_runtime_flow.py](/Users/jonasweiss/MathTeach/tests/test_planner_runtime_flow.py)
- [tests/test_api.py](/Users/jonasweiss/MathTeach/tests/test_api.py)
- [docs/block-sequence-planning.md](/Users/jonasweiss/MathTeach/docs/block-sequence-planning.md)

Verifikation:

- `ruff`: bestanden
- gezielte Tests: `81 passed, 1 warning`
- Full-Suite: `167 passed, 1 warning`

## Phase-H.2g-Blocktype-Evidence-Coupling 2026-04-04

Die H.2f-Mehrprofil-Regeln haengen jetzt nicht mehr primaer am
`lesson_mode`, sondern zusaetzlich an expliziten Blocktypen und
verdichteten Evidence-Kombinationsmustern. Damit kann derselbe
Support-Mix in einem `worked_example`-, `error_recovery`- oder
`concept_introduction`-Block sichtbar andere Moves erzeugen.

Wichtigste Konsequenzen:

- `PlannedTeachingBlock` traegt jetzt `block_type` und
  `evidence_combination`
- `EvidenceCombinationPattern` verdichtet Mehrblock- und Mischsignale zu
  wiederverwendbaren Mustern wie
  `rapid_consecutive_success`, `vocabulary_gap`,
  `stagnation_pattern`, `inconsistent_success`,
  `confidence_buildup` und `concept_confusion`
- der Planner leitet diese Muster jetzt blockweise ueber einen neuen
  `EvidencePatternDetector` ab, statt Blockkontext nur indirekt ueber
  `lesson_mode` zu approximieren
- `conflict_resolution_summary` macht H.2g jetzt sichtbar ueber
  `block_type_applied`, `evidence_patterns_applied`,
  `evidence_combination_rules_applied` und
  `blocktype_adjustments_applied`
- bekannte Kombinationen erzeugen jetzt gezielte neue Moves, z.B.
  `worked_example_accelerated_with_pacing_checks`,
  `reduce_text_density_while_maintaining_pacing`,
  `worked_example_concept_clarification_sequence`,
  `structured_error_analysis_with_prediction` oder
  `visual_concept_intro_minimal_text`

Neue oder aktualisierte Referenzartefakte:

- [src/mathteach/models.py](/Users/jonasweiss/MathTeach/src/mathteach/models.py)
- [src/mathteach/services/evidence_pattern_detector.py](/Users/jonasweiss/MathTeach/src/mathteach/services/evidence_pattern_detector.py)
- [src/mathteach/services/conflict_resolver.py](/Users/jonasweiss/MathTeach/src/mathteach/services/conflict_resolver.py)
- [src/mathteach/services/planner.py](/Users/jonasweiss/MathTeach/src/mathteach/services/planner.py)
- [tests/test_evidence_pattern_detector.py](/Users/jonasweiss/MathTeach/tests/test_evidence_pattern_detector.py)
- [tests/test_blocktype_evidence_coupling.py](/Users/jonasweiss/MathTeach/tests/test_blocktype_evidence_coupling.py)
- [tests/test_planner_runtime_flow.py](/Users/jonasweiss/MathTeach/tests/test_planner_runtime_flow.py)
- [tests/test_api.py](/Users/jonasweiss/MathTeach/tests/test_api.py)
- [docs/blocktype-evidence-coupling.md](/Users/jonasweiss/MathTeach/docs/blocktype-evidence-coupling.md)

Verifikation:

- `ruff`: bestanden
- gezielte Tests: `80 passed, 1 warning`
- Full-Suite: ausstehend in diesem Schritt

## Phase-H.2f-Mode-Evidence-Coupling 2026-04-04

Die H.2e-Mehrprofil-Regeln sind jetzt enger an `lesson_mode` und
feinere Evidence-Kombinationen gekoppelt. Dieselbe Profilkombination
liefert damit in `worked_example_tutoring`,
`guided_concept_explanation` und `origin_story_explanation` nicht mehr
dieselben Block-Moves.

Wichtigste Konsequenzen:

- `conflict_resolution_summary` traegt jetzt
  `lesson_mode_applied` und `mode_evidence_adjustments`
- der Block-Resolver bekommt den aktuellen `lesson_mode` direkt aus dem
  Planner uebergeben
- bekannte Mehrprofil-Regeln koennen jetzt je Modus unterschiedlich
  adaptieren, z.B.
  `worked_example_visual_concept_with_minimal_text`,
  `worked_example_release_after_concept_check`,
  `origin_story_bridge_with_concise_math_language` oder
  `guided_concept_rebuild_with_simple_language`
- dieselbe Triad kann damit jetzt je Modus unterschiedlich reagieren,
  statt nur ueber aktive Supports und allgemeine Evidence zu laufen
- API-Antworten machen diese Kontextkopplung jetzt sichtbar, ohne einen
  zweiten Parallelpfad neben `conflict_resolution_summary` aufzubauen

Neue oder aktualisierte Referenzartefakte:

- [src/mathteach/models.py](/Users/jonasweiss/MathTeach/src/mathteach/models.py)
- [src/mathteach/services/conflict_resolver.py](/Users/jonasweiss/MathTeach/src/mathteach/services/conflict_resolver.py)
- [src/mathteach/services/planner.py](/Users/jonasweiss/MathTeach/src/mathteach/services/planner.py)
- [tests/test_mode_evidence_coupling.py](/Users/jonasweiss/MathTeach/tests/test_mode_evidence_coupling.py)
- [tests/test_planner_runtime_flow.py](/Users/jonasweiss/MathTeach/tests/test_planner_runtime_flow.py)
- [tests/test_api.py](/Users/jonasweiss/MathTeach/tests/test_api.py)
- [docs/mode-evidence-coupling.md](/Users/jonasweiss/MathTeach/docs/mode-evidence-coupling.md)

Verifikation:

- `ruff`: bestanden
- gezielte Tests: `79 passed, 1 warning`
- Full-Suite: `148 passed, 1 warning`

## Phase-H.2e-Adaptive-Triad-Move-Transformation 2026-04-04

Die Block-Konfliktaufloesung ist jetzt einen Schritt weiter: Mischprofile
werden nicht mehr nur ueber `priority_ladder` geordnet, sondern bekannte
Pair- und Triad-Konstellationen koennen jetzt auch semantisch angepasste
Moves erzeugen.

Wichtigste Konsequenzen:

- `conflict_resolution_summary` traegt jetzt neben unterdrueckten und
  adaptierten Moves auch `generated_moves` und
  `move_dependencies_applied`
- bekannte neue Pair-Konstellationen wie `ADHD + Dyslexia`,
  `Dyscalculia + Language-Sensitive` und
  `Language-Sensitive + Autism-Spectrum` koennen jetzt blockweise
  gezielt umformen statt nur sortieren
- bekannte Triads wie
  `adhd_aware_support__dyscalculia_aware_support__language_sensitive_support`,
  `adhd_aware_support__dyslexia_aware_support__autism_spectrum_aware_support`
  und
  `dyscalculia_aware_support__language_sensitive_support__scarcity_aware_support`
  tragen jetzt eigene Move-Transformationen
- der Resolver kann jetzt komplementaere Moves erzeugen, z.B.
  `pair_visual_explanation_with_simple_language` oder
  `use_predictable_visual_reading_sequence`, wenn mehrere angepasste
  Moves sich gegenseitig sinnvoll ergaenzen
- API-Antworten machen damit nicht nur Priorisierung, sondern erstmals
  auch adaptive Move-Generierung transparent

Neue oder aktualisierte Referenzartefakte:

- [src/mathteach/models.py](/Users/jonasweiss/MathTeach/src/mathteach/models.py)
- [src/mathteach/services/conflict_resolver.py](/Users/jonasweiss/MathTeach/src/mathteach/services/conflict_resolver.py)
- [tests/test_block_conflict_resolution.py](/Users/jonasweiss/MathTeach/tests/test_block_conflict_resolution.py)
- [tests/test_planner_runtime_flow.py](/Users/jonasweiss/MathTeach/tests/test_planner_runtime_flow.py)
- [tests/test_api.py](/Users/jonasweiss/MathTeach/tests/test_api.py)
- [docs/triad-conflict-resolution-rules.md](/Users/jonasweiss/MathTeach/docs/triad-conflict-resolution-rules.md)
- [docs/support-response-matrix-implementation-plan.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-implementation-plan.md)

Verifikation:

- `ruff`: bestanden
- gezielte Tests: `73 passed, 1 warning`
- Full-Suite: `142 passed, 1 warning`

## Phase-H.2d-Block-Conflict-Resolution 2026-04-04

Die Support-Moves sind jetzt bei Mischprofilen nicht mehr nur eine
flache Sammlung paralleler Empfehlungen, sondern werden blockweise ueber
eine echte Konfliktaufloesung geordnet und begruendet.

Wichtigste Konsequenzen:

- `planned_blocks` tragen jetzt eine sichtbare
  `conflict_resolution_summary`
- der `conflict_resolver` wird jetzt nicht mehr nur fuer globale
  `response_settings`, sondern auch direkt im Blockpfad benutzt
- bekannte Paar-Konflikte wie `ADHD + Dyscalculia`,
  `ADHD + Language-Sensitive` und `Dyscalculia + Autism-Spectrum`
  koennen jetzt konkrete Moves unterdruecken oder abschwaechen
- die erste Triad-Gruppe
  `adhd_aware_support__dyscalculia_aware_support__language_sensitive_support`
  ist jetzt blockweise sichtbar inklusive `priority_ladder`
- konfliktive Moves werden jetzt fuer den Block nicht nur geordnet,
  sondern auf Wunsch auch adaptiv ersetzt, z.B.
  `increase_pacing_after_stable_success` →
  `increase_pacing_monitor_only_after_concept_recovery`
- API-Antworten machen diese Block-Entscheidung jetzt nachvollziehbar,
  statt dass konkurrierende Moves still nebeneinander stehen bleiben

Neue oder aktualisierte Referenzartefakte:

- [src/mathteach/models.py](/Users/jonasweiss/MathTeach/src/mathteach/models.py)
- [src/mathteach/services/conflict_resolver.py](/Users/jonasweiss/MathTeach/src/mathteach/services/conflict_resolver.py)
- [src/mathteach/services/planner.py](/Users/jonasweiss/MathTeach/src/mathteach/services/planner.py)
- [tests/test_block_conflict_resolution.py](/Users/jonasweiss/MathTeach/tests/test_block_conflict_resolution.py)
- [tests/test_planner_runtime_flow.py](/Users/jonasweiss/MathTeach/tests/test_planner_runtime_flow.py)
- [tests/test_api.py](/Users/jonasweiss/MathTeach/tests/test_api.py)
- [docs/support-response-matrix-implementation-plan.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-implementation-plan.md)

Verifikation:

- `ruff`: bestanden
- gezielte Tests: `67 passed, 1 warning`
- Full-Suite: `136 passed, 1 warning`

## Phase-H.2c-Evidence-Expansion 2026-04-04

Die H.2c-Signalpalette ist jetzt verbreitert: der Planner leitet neben
den bisherigen H.1-/H.2b-Signalen jetzt auch erste neue
Triad-vorbereitende Evidence-Typen ab und uebersetzt sie direkt in
sichtbare Support-Moves.

Wichtigste Konsequenzen:

- neue Mehrblock- und Recovery-Signale sind jetzt operational:
  `rapid_success_two_blocks`, `rapid_success_three_blocks`,
  `vocabulary_request_again`, `error_recovery_with_hint`,
  `repeated_attempt_three_plus` und `mixed_success_inconsistent`
- diese Signale wirken jetzt nicht nur im Roh-State, sondern direkt in
  `support_moves` und teilweise auch in der Scaffold-Priorisierung
- Resume-Vorschauen koennen auch neue Signalsorten wie
  `rapid_success_three_blocks` jetzt wieder sichtbar aufnehmen
- `SignalInterpreter` kennt die neuen Evidence-Typen jetzt ebenfalls als
  staerkere Breakthrough-, Confusion-, Stagnation- oder
  Confidence-Recovery-Hinweise
- der naechste direkte Ausbau kann damit realistischer an echte
  Mischprofil-Konflikte gehen, statt Triad-Regeln nur auf einer zu
  duennen Signalbasis zu bauen

Neue oder aktualisierte Referenzartefakte:

- [src/mathteach/services/planner.py](/Users/jonasweiss/MathTeach/src/mathteach/services/planner.py)
- [src/mathteach/services/runtime_mode_adapter.py](/Users/jonasweiss/MathTeach/src/mathteach/services/runtime_mode_adapter.py)
- [tests/test_planner_runtime_flow.py](/Users/jonasweiss/MathTeach/tests/test_planner_runtime_flow.py)
- [tests/test_observation_signal_interpretation.py](/Users/jonasweiss/MathTeach/tests/test_observation_signal_interpretation.py)
- [tests/test_api.py](/Users/jonasweiss/MathTeach/tests/test_api.py)
- [docs/support-response-matrix-implementation-plan.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-implementation-plan.md)

Verifikation:

- `ruff`: bestanden
- gezielte Tests: `69 passed, 1 warning`
- Full-Suite: `131 passed, 1 warning`

## Phase-H.2b.3-Checkpoint-Roundtrip-Hardening 2026-04-04

Die sichtbare Resume-Semantik ist jetzt auch unter der Haube robuster
abgesichert: volle Checkpoint-Roundtrips und partielle H.1-Checkpoints
werden jetzt bewusst auf Resume-Sicherheit getestet.

Wichtigste Konsequenzen:

- `ModeAdaptationCheckpoint` ist jetzt nicht nur fuer den Idealpfad,
  sondern auch fuer partielle JSON-Roundtrips testseitig gehaertet
- fehlende optionale State-Felder fallen jetzt kontrolliert auf
  Modell-Defaults zurueck, statt spaet still als Resume-Risiko zu bleiben
- `SessionStore` ist jetzt auch fuer partielle H.1-Checkpoint-Dateien
  explizit abgesichert
- der API-Resume-Pfad ist jetzt auch gegen partielle gespeicherte
  Checkpoints getestet
- Admin-Inspection zeigt bei parsebaren Quarantaene-Checkpoints jetzt
  eine kompakte `resume_state_summary` statt nur Roh-JSON
- der neue Referenzanker
  [resume-semantics.md](/Users/jonasweiss/MathTeach/docs/resume-semantics.md)
  dokumentiert jetzt, welche Felder wirklich Lernadaptation tragen

Neue oder aktualisierte Referenzartefakte:

- [src/mathteach/services/session_manager.py](/Users/jonasweiss/MathTeach/src/mathteach/services/session_manager.py)
- [tests/test_mode_adaptation_persistence.py](/Users/jonasweiss/MathTeach/tests/test_mode_adaptation_persistence.py)
- [tests/test_session_store.py](/Users/jonasweiss/MathTeach/tests/test_session_store.py)
- [tests/test_api.py](/Users/jonasweiss/MathTeach/tests/test_api.py)
- [docs/resume-semantics.md](/Users/jonasweiss/MathTeach/docs/resume-semantics.md)
- [docs/support-response-matrix-implementation-plan.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-implementation-plan.md)

Verifikation:

- `ruff`: bestanden
- gezielte Tests: `47 passed, 1 warning`
- Full-Suite: `121 passed, 1 warning`

## Phase-H.2b-Resume-Context-Visibility 2026-04-04

Die Resume-Semantik ist jetzt nicht mehr nur implizit im Verhalten des
Planners versteckt, sondern wird als eigener `resume_context` im
`TeachingPlan` und damit auch im API-Output sichtbar.

Wichtigste Konsequenzen:

- `SessionManager` markiert Resume-Herkunft jetzt explizit als
  `fresh_start`, `inline_state`, `inline_checkpoint` oder
  `stored_checkpoint`
- `TeachingPlan.resume_context` zeigt jetzt sichtbar an, ob ein Plan
  wirklich auf einer Fortsetzung basiert oder frisch startet
- getragene `last_observation_evidence` sind jetzt nicht nur wirksam,
  sondern auch als `carried_observation_evidence` offen sichtbar
- Resume-Previews koennen damit explizit ausweisen, ob getragene Evidenz
  wirklich in `support_moves` und `support_scaffolds` eingeflossen ist
- offene `pending_transition_message` werden jetzt nicht nur konsumiert,
  sondern auch als `carried` und `consumed` nachvollziehbar gemacht
- die Resume-Semantik ist damit testbarer, debugbarer und spaeter auch
  besser anschlussfaehig fuer Admin-Diagnostik und Learning Analytics

Neue oder aktualisierte Referenzartefakte:

- [src/mathteach/models.py](/Users/jonasweiss/MathTeach/src/mathteach/models.py)
- [src/mathteach/services/session_manager.py](/Users/jonasweiss/MathTeach/src/mathteach/services/session_manager.py)
- [src/mathteach/services/planner.py](/Users/jonasweiss/MathTeach/src/mathteach/services/planner.py)
- [tests/test_session_manager.py](/Users/jonasweiss/MathTeach/tests/test_session_manager.py)
- [tests/test_planner_runtime_flow.py](/Users/jonasweiss/MathTeach/tests/test_planner_runtime_flow.py)
- [tests/test_api.py](/Users/jonasweiss/MathTeach/tests/test_api.py)
- [docs/support-response-matrix-implementation-plan.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-implementation-plan.md)

Verifikation:

- `ruff`: bestanden
- gezielte Tests: `65 passed, 1 warning`
- Full-Suite: `117 passed, 1 warning`

## Phase-Support-Block-Level-Response-Integration 2026-04-04

Die Support Response Matrix ist jetzt nicht mehr nur global im
`TeachingPlan` sichtbar, sondern greift direkt in die geplanten
Unterrichtsbloecke hinein.

Wichtigste Konsequenzen:

- `planned_blocks` tragen jetzt konkrete `support_moves` und
  `support_scaffolds`
- ADHD-, Dyscalculia-, Dyslexia-, Autism-, Language-Sensitive- und
  Scarcity-Support werden jetzt als blockweise Tutorhandlungen sichtbar
- Mischprofile bekommen auf Blockebene jetzt nicht nur globale
  `response_settings`, sondern eine faire Scaffold-Auswahl ueber mehrere
  aktive Supports
- `support_moves` und `support_scaffolds` reagieren jetzt zusaetzlich auf
  `lesson_mode` und beobachtete Runtime-Evidenz wie Verwirrung,
  Textueberlastung, Stagnation oder sichtbaren Erfolg
- die Symbol-Mengen-Bruecke fuer Dyscalculia-Support ist jetzt auch als
  operative Scaffold-Ausgabe im Runtime-Pfad angekommen
- Resume-Previews ohne neue `runtime_observations` nutzen jetzt ebenfalls
  `last_observation_evidence`, statt beim naechsten Block auf leere Evidenz
  zurueckzufallen
- der Planner uebersetzt Support-Profile damit klarer in operative
  Tutorentscheidungen statt nur in Hintergrundparameter
- der naechste direkte Ausbau ist jetzt nicht mehr Phase-A-Dokumentation,
  sondern tiefere support-aware Blockgenerierung und spaeter
  runtime-sensitive Response-Anpassung ueber Sitzungsverlaeufe

Neue oder aktualisierte Referenzartefakte:

- [src/mathteach/models.py](/Users/jonasweiss/MathTeach/src/mathteach/models.py)
- [src/mathteach/services/planner.py](/Users/jonasweiss/MathTeach/src/mathteach/services/planner.py)
- [src/mathteach/services/response_engine.py](/Users/jonasweiss/MathTeach/src/mathteach/services/response_engine.py)
- [tests/test_planner_runtime_flow.py](/Users/jonasweiss/MathTeach/tests/test_planner_runtime_flow.py)
- [tests/test_api.py](/Users/jonasweiss/MathTeach/tests/test_api.py)
- [tests/test_response_engine.py](/Users/jonasweiss/MathTeach/tests/test_response_engine.py)
- [docs/support-response-matrix-implementation-plan.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-implementation-plan.md)

Verifikation:

- `ruff`: bestanden
- `pytest`: `116 passed, 1 warning`
- Warning weiter nur wegen nicht schreibbarem `pytest`-Cache

## Phase-H-Multi-Step-Checkpoint-Migration 2026-04-04

Die Session-Haertung ist jetzt nicht mehr auf einen einzelnen
Versionssprung beschraenkt: der `CheckpointMigrator` kann jetzt
bekannte Legacy-Pfade iterativ bis zur aktuellen H.1-Version
durchlaufen.

Wichtigste Konsequenzen:

- `phase_h0_v0 -> phase_h0_v1 -> phase_h1_v1` ist jetzt als echte
  Migrationskette live
- `CheckpointMigrator` gibt jetzt nicht nur den neuen Checkpoint,
  sondern auch die vollstaendige Schrittfolge zurueck
- `SessionManager` protokolliert Einzelschritt- und Mehrschritt-
  Migrationen jetzt bewusst getrennt
- der Audit-Trail kennt jetzt neben `checkpoint_migrated` auch
  `checkpoint_migration_chain`
- gespeicherte und inline uebergebene Legacy-Checkpoints koennen jetzt
  ueber mehrere bekannte Altstufen hinweg weitergefuehrt werden
- der naechste direkte Ausbau ist jetzt nicht mehr die Migrationskette
  selbst, sondern spaetere Rollenhaertung fuer Admin-Pfade und danach
  echte H.2+-Schemaentwicklung

Neue oder aktualisierte Referenzartefakte:

- [src/mathteach/services/checkpoint_migrator.py](/Users/jonasweiss/MathTeach/src/mathteach/services/checkpoint_migrator.py)
- [src/mathteach/services/checkpoint_validation.py](/Users/jonasweiss/MathTeach/src/mathteach/services/checkpoint_validation.py)
- [src/mathteach/services/session_manager.py](/Users/jonasweiss/MathTeach/src/mathteach/services/session_manager.py)
- [src/mathteach/services/session_audit.py](/Users/jonasweiss/MathTeach/src/mathteach/services/session_audit.py)
- [tests/test_checkpoint_validation.py](/Users/jonasweiss/MathTeach/tests/test_checkpoint_validation.py)
- [tests/test_checkpoint_migrator.py](/Users/jonasweiss/MathTeach/tests/test_checkpoint_migrator.py)
- [tests/test_session_manager.py](/Users/jonasweiss/MathTeach/tests/test_session_manager.py)
- [tests/test_session_audit.py](/Users/jonasweiss/MathTeach/tests/test_session_audit.py)
- [tests/test_api.py](/Users/jonasweiss/MathTeach/tests/test_api.py)
- [docs/checkpoint-migrator.md](/Users/jonasweiss/MathTeach/docs/checkpoint-migrator.md)
- [docs/session-validation-and-migration.md](/Users/jonasweiss/MathTeach/docs/session-validation-and-migration.md)

Verifikation:

- `ruff`: bestanden
- `pytest`: `109 passed, 1 warning`
- Warning weiter nur wegen nicht schreibbarem `pytest`-Cache

## Phase-H-Admin-Repair-Paths 2026-04-04

Die Session-Betriebshaertung hat jetzt eine sichtbare Admin-Oberflaeche:
quarantainierte Sessions koennen nicht mehr nur intern isoliert, sondern
jetzt auch gelistet, inspiziert, wiederhergestellt oder verworfen werden.

Wichtigste Konsequenzen:

- der API-Pfad hat jetzt erste Admin-Endpunkte fuer Quarantaene-Sessions
- `SessionManager` kapselt jetzt auch `list`, `inspect`, `restore` und
  `discard` fuer quarantainierte Sessions
- `SessionQuarantine` traegt jetzt echte Admin-Operationen statt nur
  `quarantine_file`
- nach Quarantaene ist jetzt explizit getestet, dass dieselbe `session_id`
  spaeter wieder sauber als neue Session starten kann
- manuell reparierte Quarantaene-Dateien koennen jetzt in den aktiven Store
  zurueckgeschrieben werden
- der naechste direkte Ausbau ist jetzt nicht mehr nur Sichtbarkeit,
  sondern spaeter Monitoring-/Repair-Workflows und Mehrschritt-Migrationen

Neue oder aktualisierte Referenzartefakte:

- [src/mathteach/main.py](/Users/jonasweiss/MathTeach/src/mathteach/main.py)
- [src/mathteach/services/session_manager.py](/Users/jonasweiss/MathTeach/src/mathteach/services/session_manager.py)
- [src/mathteach/services/session_quarantine.py](/Users/jonasweiss/MathTeach/src/mathteach/services/session_quarantine.py)
- [src/mathteach/services/session_audit.py](/Users/jonasweiss/MathTeach/src/mathteach/services/session_audit.py)
- [tests/test_api.py](/Users/jonasweiss/MathTeach/tests/test_api.py)
- [tests/test_session_quarantine.py](/Users/jonasweiss/MathTeach/tests/test_session_quarantine.py)
- [tests/test_session_audit.py](/Users/jonasweiss/MathTeach/tests/test_session_audit.py)
- [docs/session-quarantine-and-audit.md](/Users/jonasweiss/MathTeach/docs/session-quarantine-and-audit.md)

Verifikation:

- `ruff`: bestanden
- `pytest`: `102 passed, 1 warning`
- Warning weiter nur wegen nicht schreibbarem `pytest`-Cache

## Phase-H-Session-Quarantine-And-Audit 2026-04-04

Die Session-Migration hat jetzt ihre erste Betriebs-Haertung:
defekte oder nicht migrierbare Sessions bleiben nicht mehr im aktiven
Resume-Pfad liegen, sondern werden jetzt quarantainiert und auditiert.

Wichtigste Konsequenzen:

- `SessionQuarantine` verschiebt defekte Checkpoints aus dem aktiven Store in
  einen separaten Quarantaene-Bereich
- `SessionAuditLogger` protokolliert jetzt erfolgreiche Migrationen,
  invalide Sessions und fehlgeschlagene Migrationen
- gespeicherte Sessions, die beim Laden oder Validieren scheitern, fuehren
  nicht mehr zu endlosen Wiederholungsfehlern auf derselben Datei
- nach Quarantaene wird ein spaeterer Request mit derselben `session_id`
  sauber als neuer Start behandelt
- der naechste direkte Ausbau ist jetzt nicht mehr die Betriebsgrundlage,
  sondern sichtbarere Admin-/Repair-Pfade und spaetere Mehrschritt-
  Migrationen

Neue oder aktualisierte Referenzartefakte:

- [src/mathteach/services/session_quarantine.py](/Users/jonasweiss/MathTeach/src/mathteach/services/session_quarantine.py)
- [src/mathteach/services/session_audit.py](/Users/jonasweiss/MathTeach/src/mathteach/services/session_audit.py)
- [src/mathteach/services/session_manager.py](/Users/jonasweiss/MathTeach/src/mathteach/services/session_manager.py)
- [src/mathteach/services/session_store.py](/Users/jonasweiss/MathTeach/src/mathteach/services/session_store.py)
- [tests/test_session_quarantine.py](/Users/jonasweiss/MathTeach/tests/test_session_quarantine.py)
- [tests/test_session_audit.py](/Users/jonasweiss/MathTeach/tests/test_session_audit.py)
- [tests/test_session_manager.py](/Users/jonasweiss/MathTeach/tests/test_session_manager.py)
- [tests/test_api.py](/Users/jonasweiss/MathTeach/tests/test_api.py)
- [docs/session-quarantine-and-audit.md](/Users/jonasweiss/MathTeach/docs/session-quarantine-and-audit.md)

Verifikation:

- `ruff`: bestanden
- `pytest`: `94 passed, 1 warning`
- Warning weiter nur wegen nicht schreibbarem `pytest`-Cache

## Phase-H-Checkpoint-Migrator 2026-04-04

Die Session-Haertung hat jetzt nicht mehr nur Migrationserkennung,
sondern einen ersten echten Migrationspfad: bekannte `phase_h0_v1`
Checkpoints werden jetzt automatisch nach `phase_h1_v1` gehoben.

Wichtigste Konsequenzen:

- `CheckpointMigrator` ist jetzt als eigene Schicht live im Repo
- gespeicherte `phase_h0_v1`-Checkpoints werden beim Resume automatisch
  migriert und direkt wieder im Store als `phase_h1_v1` gespeichert
- inline uebergebene Alt-Checkpoints werden vor dem Planner-Aufruf auf die
  aktuelle Version normalisiert
- der Planner sieht damit nur noch aktuelle Checkpoints
- die `410 migration-required`-Semantik bleibt fuer spaetere bekannte, aber
  nicht automatisch migrierbare Versionen erhalten
- der naechste echte Ausbau ist jetzt nicht mehr die Migration selbst,
  sondern Quarantaene/Audit-Trail fuer defekte Sessions und spaetere
  Mehrschritt-Migrationen

Neue oder aktualisierte Referenzartefakte:

- [src/mathteach/services/checkpoint_migrator.py](/Users/jonasweiss/MathTeach/src/mathteach/services/checkpoint_migrator.py)
- [src/mathteach/services/session_manager.py](/Users/jonasweiss/MathTeach/src/mathteach/services/session_manager.py)
- [tests/test_checkpoint_migrator.py](/Users/jonasweiss/MathTeach/tests/test_checkpoint_migrator.py)
- [tests/test_session_manager.py](/Users/jonasweiss/MathTeach/tests/test_session_manager.py)
- [tests/test_api.py](/Users/jonasweiss/MathTeach/tests/test_api.py)
- [docs/checkpoint-migrator.md](/Users/jonasweiss/MathTeach/docs/checkpoint-migrator.md)

Verifikation:

- `ruff`: bestanden
- `pytest`: `94 passed, 1 warning`
- Warning weiter nur wegen nicht schreibbarem `pytest`-Cache

## Phase-H-Session-Validation-And-Migration-Gate 2026-04-04

Die Session-Persistenz hat jetzt ihre erste echte Validierungskante:
`SessionManager` unterscheidet nicht mehr nur zwischen Resume und Neustart,
sondern jetzt explizit zwischen `unknown`, `invalid` und
`migration-required`.

Wichtigste Konsequenzen:

- eine neue Validierungsschicht prueft `schema_version`,
  Checkpoint-Zustandsgrenzen und H.1-Budgetregeln
- unbekannte Sessions bleiben bewusst ein sauberer Neustart
- bekannte, aber veraltete Checkpoints fuehren jetzt explizit zu
  `migration-required`
- korrupt gespeicherte oder semantisch ungueltige Checkpoints fuehren jetzt
  explizit zu `invalid session`
- der API-Pfad bildet diese Faelle jetzt sauber auf `400`, `410` und `422`
  ab
- der naechste direkte Schritt ist jetzt keine grobe Session-Koordination
  mehr, sondern ein echter `checkpoint_migrator` und spaetere
  Quarantaene-/Audit-Logik fuer defekte Sessions

Neue oder aktualisierte Referenzartefakte:

- [src/mathteach/services/checkpoint_validation.py](/Users/jonasweiss/MathTeach/src/mathteach/services/checkpoint_validation.py)
- [src/mathteach/services/session_manager.py](/Users/jonasweiss/MathTeach/src/mathteach/services/session_manager.py)
- [src/mathteach/main.py](/Users/jonasweiss/MathTeach/src/mathteach/main.py)
- [src/mathteach/models.py](/Users/jonasweiss/MathTeach/src/mathteach/models.py)
- [tests/test_checkpoint_validation.py](/Users/jonasweiss/MathTeach/tests/test_checkpoint_validation.py)
- [tests/test_session_manager.py](/Users/jonasweiss/MathTeach/tests/test_session_manager.py)
- [tests/test_api.py](/Users/jonasweiss/MathTeach/tests/test_api.py)
- [docs/session-validation-and-migration.md](/Users/jonasweiss/MathTeach/docs/session-validation-and-migration.md)

Verifikation:

- `ruff`: bestanden
- `pytest`: `90 passed, 1 warning`
- Warning weiter nur wegen nicht schreibbarem `pytest`-Cache

## Phase-H-Session-Manager 2026-04-04

Die Session-Persistenz hat jetzt ihre erste echte Koordinationsschicht:
`SessionManager` sitzt zwischen API, `SessionStore` und Planner und zieht
die Resume-Regeln aus `main.py` heraus.

Wichtigste Konsequenzen:

- `SessionManager` koordiniert jetzt `session_id`, gespeicherte Checkpoints
  und inline Resume-Daten zentral
- Konflikte zwischen `session_id` und direkter Runtime-Eingabe werden jetzt
  nicht mehr implizit im API-Pfad, sondern explizit in der neuen
  Koordinationsschicht behandelt
- `main.py` ist wieder deutlich schlanker und delegiert Laden, Resume und
  Persistieren an den Manager
- `SessionRequest` bleibt fuer Legacy- und Testpfade flexibel, waehrend die
  Konfliktregel jetzt an der Session-Grenze erzwungen wird
- der file-backed `SessionStore` bleibt MVP, aber der naechste Ausbaupfad
  heisst jetzt klar: Version-Haertung, unbekannte Session-Semantik und
  spaetere `SessionManager`-Erweiterung statt weiterer API-Glue-Code

Neue oder aktualisierte Referenzartefakte:

- [src/mathteach/services/session_manager.py](/Users/jonasweiss/MathTeach/src/mathteach/services/session_manager.py)
- [src/mathteach/main.py](/Users/jonasweiss/MathTeach/src/mathteach/main.py)
- [src/mathteach/models.py](/Users/jonasweiss/MathTeach/src/mathteach/models.py)
- [src/mathteach/config.py](/Users/jonasweiss/MathTeach/src/mathteach/config.py)
- [tests/test_session_manager.py](/Users/jonasweiss/MathTeach/tests/test_session_manager.py)
- [docs/session-storage-architecture.md](/Users/jonasweiss/MathTeach/docs/session-storage-architecture.md)

Verifikation:

- `ruff`: bestanden
- `pytest`: `80 passed, 1 warning`
- Warning weiter nur wegen nicht schreibbarem `pytest`-Cache

## Phase-H-Session-Store-MVP 2026-04-04

Die erste echte Storage-Stufe fuer `Phase H` ist jetzt im Repo
angekommen: `SessionStore` plus `session_id`-Resume ueber den API-Pfad.

Wichtigste Konsequenzen:

- `SessionStore` existiert jetzt als file-backed MVP-Huelle
- `SessionRequest` kann jetzt optional mit `session_id` arbeiten
- der API-Pfad laedt bei bekannter `session_id` den gespeicherten
  `mode_adaptation_checkpoint`
- der API-Pfad speichert nach jeder Planerzeugung den neuen Checkpoint
  wieder zur Session ab
- Konflikte zwischen `session_id` und inline Resume-Daten werden jetzt
  explizit mit `422` abgewiesen
- der naechste direkte Schritt ist jetzt nicht mehr `SessionStore`,
  sondern spaeter `SessionManager` und robustere Storage-Semantik

Neue oder aktualisierte Referenzartefakte:

- [src/mathteach/services/session_store.py](/Users/jonasweiss/MathTeach/src/mathteach/services/session_store.py)
- [src/mathteach/main.py](/Users/jonasweiss/MathTeach/src/mathteach/main.py)
- [src/mathteach/models.py](/Users/jonasweiss/MathTeach/src/mathteach/models.py)
- [tests/test_session_store.py](/Users/jonasweiss/MathTeach/tests/test_session_store.py)
- [tests/test_api.py](/Users/jonasweiss/MathTeach/tests/test_api.py)
- [docs/session-storage-architecture.md](/Users/jonasweiss/MathTeach/docs/session-storage-architecture.md)

Verifikation:

- `ruff`: bestanden
- `pytest`: `76 passed, 1 warning`
- Warning weiter nur wegen nicht schreibbarem `pytest`-Cache

## Phase-H-Storage-Bridge 2026-04-04

Die neue Review-Lage bestaetigt, dass der Checkpoint-Vertrag jetzt stark
genug ist, um die naechste Schicht nicht mehr als abstrakte Persistenzidee,
sondern als konkrete `Session Storage`-Bruecke zu formulieren.

Wichtigste Konsequenzen:

- der naechste Engpass heisst jetzt nicht mehr allgemein `Persistence`,
  sondern konkret `SessionStore` plus spaeter `SessionManager`
- `mode_adaptation_checkpoint` ist damit offiziell die Ziel-Form fuer
  spaetere Session-Persistenz
- die naechste API-Erweiterung soll mit `session_id` arbeiten statt nur mit
  direkt uebergebenem Runtime-State
- der Schritt von Blocksimulation zu echter Langzeit-Session ist jetzt als
  konkrete Anschlussarchitektur beschrieben

Neue oder aktualisierte Referenzartefakte:

- [docs/session-storage-architecture.md](/Users/jonasweiss/MathTeach/docs/session-storage-architecture.md)
- [docs/mode-adaptation-checkpoint-contract.md](/Users/jonasweiss/MathTeach/docs/mode-adaptation-checkpoint-contract.md)
- [README.md](/Users/jonasweiss/MathTeach/README.md)
- [docs/support-response-matrix-implementation-plan.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-implementation-plan.md)

Verifikation:

- Review-Triage auf Basis des grünen Checkpoint-Vertrags
- keine neue Runtime-Logik in diesem Schritt

## Phase-H-Checkpoint-Contract 2026-04-04

Die H.1-Runtime hat jetzt nicht nur internen Resume-Zustand, sondern auch
einen versionierten externen Checkpoint-Vertrag fuer API und spaetere
Persistenz.

Wichtigste Konsequenzen:

- `ModeAdaptationCheckpoint` ist jetzt als versionierter Wrapper live im
  Modell-Layer
- `SessionRequest` akzeptiert jetzt bevorzugt
  `mode_adaptation_checkpoint` fuer Resume
- `TeachingPlan` liefert jetzt neben `mode_adaptation_state` auch einen
  serialisierbaren `mode_adaptation_checkpoint`
- Legacy-Resume ueber `mode_adaptation_state` bleibt vorerst kompatibel,
  aber doppelte Runtime-Eingaben werden jetzt explizit abgewiesen
- Roundtrip-, API- und Planner-Tests sichern den neuen Resume-Vertrag ab

Neue oder aktualisierte Referenzartefakte:

- [src/mathteach/models.py](/Users/jonasweiss/MathTeach/src/mathteach/models.py)
- [src/mathteach/services/planner.py](/Users/jonasweiss/MathTeach/src/mathteach/services/planner.py)
- [tests/test_mode_adaptation_persistence.py](/Users/jonasweiss/MathTeach/tests/test_mode_adaptation_persistence.py)
- [tests/test_planner_runtime_flow.py](/Users/jonasweiss/MathTeach/tests/test_planner_runtime_flow.py)
- [tests/test_api.py](/Users/jonasweiss/MathTeach/tests/test_api.py)
- [docs/mode-adaptation-checkpoint-contract.md](/Users/jonasweiss/MathTeach/docs/mode-adaptation-checkpoint-contract.md)

Verifikation:

- `ruff`: bestanden
- `pytest`: `70 passed, 1 warning`
- Warning weiter nur wegen nicht schreibbarem `pytest`-Cache

## Phase-H-H1-Runtime-Review 2026-04-02

Die neue Review-Lage bestaetigt den qualitativen Sprung von
`implementation-ready` zu echter `runtime live`-Stufe fuer `Phase H.1`.

Wichtigste Konsequenzen:

- `Phase H.1` gilt jetzt nicht mehr primär als Planungs- oder
  Integrationsbaustelle, sondern als reale MVP-Runtime-Schicht
- die Hauptluecke verschiebt sich jetzt von Signal- und Blocklogik zu
  `Persistence`, `Resume-Semantik` und spaeterer externer Storage-Anbindung
- der bestaetigte naechste Engpass ist jetzt die robuste
  `mode_adaptation_state`-Schnittstelle nach aussen
- die naechste Session soll deshalb auf Serialisierung, Resume-API und
  Planner-Fortsetzungslogik zielen statt auf weitere Review-Runden

Neue oder aktualisierte Referenzartefakte:

- [docs/live-mode-adaptation-persistence-review-2026-04-02.md](/Users/jonasweiss/MathTeach/docs/live-mode-adaptation-persistence-review-2026-04-02.md)
- [README.md](/Users/jonasweiss/MathTeach/README.md)
- [docs/support-response-matrix-implementation-plan.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-implementation-plan.md)

Verifikation:

- Review-Triage auf Basis des bereits grünen H.1-Runtime-Stands
- keine neue Runtime-Logik in diesem Schritt

## Phase-H-Success-Visibility-Signals 2026-04-02

Die H.1-Runtime-Schicht deckt jetzt zusaetzliche reale Blockmuster ab,
vor allem sichtbare kleine Erfolge und ausbleibende Erfolgslinien ueber
mehrere Bloecke.

Wichtigste Konsequenzen:

- der Planner leitet jetzt `visible_small_success` automatisch aus lokalen
  Fortschrittsindikatoren ab
- bei wiederholter Schwierigkeit ohne sichtbaren Erfolg entsteht jetzt
  automatisch `no_success_visible_two_blocks`
- diese Linie greift jetzt auch direkt im `scarcity_aware_support`-Pfad
- API- und Planner-Tests sichern diese neuen Signalfenster explizit ab

Neue oder aktualisierte Referenzartefakte:

- [src/mathteach/services/planner.py](/Users/jonasweiss/MathTeach/src/mathteach/services/planner.py)
- [tests/test_planner_runtime_flow.py](/Users/jonasweiss/MathTeach/tests/test_planner_runtime_flow.py)
- [tests/test_api.py](/Users/jonasweiss/MathTeach/tests/test_api.py)

Verifikation:

- `ruff`: bestanden
- `pytest`: `65 passed, 1 warning`
- Warning weiter nur wegen nicht schreibbarem `pytest`-Cache

## Phase-H-Multi-Block-Observation-Windows 2026-04-02

Die H.1-Runtime-Schicht verdichtet jetzt wiederkehrende Beobachtungsmuster
ueber Blockgrenzen hinweg, statt nur rohe Einzelblock-Evidenz zu
verarbeiten.

Wichtigste Konsequenzen:

- `ModeAdaptationState` traegt jetzt auch `last_observation_evidence`
- der Planner leitet jetzt automatisch Mehrblock-Signale wie
  `transfer_success_two_blocks`, `no_progress_two_blocks`,
  `no_progress_three_blocks` und
  `repeated_concept_error_across_blocks` ab
- diese Verdichtung funktioniert jetzt auch ueber Resume-Grenzen hinweg
- API- und Planner-Tests sichern jetzt nicht nur einzelne Blocks, sondern
  auch resume-uebergreifende Beobachtungsfenster ab

Neue oder aktualisierte Referenzartefakte:

- [src/mathteach/models.py](/Users/jonasweiss/MathTeach/src/mathteach/models.py)
- [src/mathteach/services/planner.py](/Users/jonasweiss/MathTeach/src/mathteach/services/planner.py)
- [src/mathteach/services/runtime_mode_adapter.py](/Users/jonasweiss/MathTeach/src/mathteach/services/runtime_mode_adapter.py)
- [tests/test_planner_runtime_flow.py](/Users/jonasweiss/MathTeach/tests/test_planner_runtime_flow.py)
- [tests/test_api.py](/Users/jonasweiss/MathTeach/tests/test_api.py)

Verifikation:

- `ruff`: bestanden
- `pytest`: `62 passed, 1 warning`
- Warning weiter nur wegen nicht schreibbarem `pytest`-Cache

## Phase-H-Budget-And-Transition-Consumption 2026-04-02

Die H.1-Runtime-Schicht behandelt jetzt zwei wichtige Robustheitsfaelle
sauberer:

- angezeigte `transition_message` wird nach Anzeige konsumiert und nicht
  unnoetig mehrfach weitergetragen
- das Wechselbudget ueber laengere Sequenzen ist jetzt durch direkte Tests
  abgesichert

Wichtigste Konsequenzen:

- `pending_transition_message` verschwindet nach dem angezeigten Block wieder
  aus dem Zustand
- `no_success_visible_two_blocks` und `visible_small_success` sind jetzt
  staerker im Signalraum verankert
- laengere Sequenzen mit drei erlaubten Wechseln und blockiertem vierten
  Wechsel sind jetzt direkt getestet

Neue oder aktualisierte Referenzartefakte:

- [src/mathteach/services/runtime_mode_adapter.py](/Users/jonasweiss/MathTeach/src/mathteach/services/runtime_mode_adapter.py)
- [src/mathteach/services/planner.py](/Users/jonasweiss/MathTeach/src/mathteach/services/planner.py)
- [tests/test_observation_signal_interpretation.py](/Users/jonasweiss/MathTeach/tests/test_observation_signal_interpretation.py)
- [tests/test_runtime_mode_adapter.py](/Users/jonasweiss/MathTeach/tests/test_runtime_mode_adapter.py)
- [tests/test_planner_runtime_flow.py](/Users/jonasweiss/MathTeach/tests/test_planner_runtime_flow.py)
- [tests/test_api.py](/Users/jonasweiss/MathTeach/tests/test_api.py)

Verifikation:

- `ruff`: bestanden
- `pytest`: `59 passed, 1 warning`
- Warning weiter nur wegen nicht schreibbarem `pytest`-Cache

## Phase-H-Pending-Transition-Persistence 2026-04-02

Die H.1-Runtime-Fortsetzung traegt jetzt nicht nur den Moduszustand,
sondern auch offene Uebergangssprache sauber ueber Session-Grenzen.

Wichtigste Konsequenzen:

- `ModeAdaptationState` traegt jetzt `pending_transition_message`
- ein offener Moduswechsel kann damit beim naechsten Resume weiter
  angezeigt werden
- das Wechselbudget ist jetzt durch explizite Tests gegen Erschoepfung
  abgesichert
- Resume-, Cooldown- und Uebergangspersistenz sind jetzt gemeinsam
  ueber API- und Planner-Tests abgedeckt

Neue oder aktualisierte Referenzartefakte:

- [src/mathteach/models.py](/Users/jonasweiss/MathTeach/src/mathteach/models.py)
- [src/mathteach/services/runtime_mode_adapter.py](/Users/jonasweiss/MathTeach/src/mathteach/services/runtime_mode_adapter.py)
- [src/mathteach/services/planner.py](/Users/jonasweiss/MathTeach/src/mathteach/services/planner.py)
- [tests/test_runtime_mode_adapter.py](/Users/jonasweiss/MathTeach/tests/test_runtime_mode_adapter.py)
- [tests/test_planner_runtime_flow.py](/Users/jonasweiss/MathTeach/tests/test_planner_runtime_flow.py)
- [tests/test_api.py](/Users/jonasweiss/MathTeach/tests/test_api.py)

Verifikation:

- `ruff`: bestanden
- `pytest`: `56 passed, 1 warning`
- Warning weiter nur wegen nicht schreibbarem `pytest`-Cache

## Phase-H-Session-Resume 2026-04-02

Der erste H.1-Block-Loop kann jetzt nicht nur mehrere Bloecke in einer
Vorschau simulieren, sondern auch mit einem bestehenden
`mode_adaptation_state` fortgesetzt werden.

Wichtigste Konsequenzen:

- `SessionRequest` kann jetzt einen bestehenden `mode_adaptation_state`
  wieder aufnehmen
- der Planner setzt dann im aktuellen Runtime-Modus fort statt wieder bei der
  reinen Startwahl von Phase `G` zu beginnen
- laengere Blockfolgen mit Mehrfachwechseln sind jetzt testbar abgesichert
- Cooldown- und Resume-Verhalten sind jetzt ueber API und Planner-Tests
  abgedeckt

Neue oder aktualisierte Referenzartefakte:

- [src/mathteach/models.py](/Users/jonasweiss/MathTeach/src/mathteach/models.py)
- [src/mathteach/services/planner.py](/Users/jonasweiss/MathTeach/src/mathteach/services/planner.py)
- [tests/test_planner_runtime_flow.py](/Users/jonasweiss/MathTeach/tests/test_planner_runtime_flow.py)
- [tests/test_api.py](/Users/jonasweiss/MathTeach/tests/test_api.py)

Verifikation:

- `ruff`: bestanden
- `pytest`: `53 passed, 1 warning`
- Warning weiter nur wegen nicht schreibbarem `pytest`-Cache

## Phase-H-Block-Loop 2026-04-02

Die vertiefte Planner-Integration fuer Phase `H.1` ist jetzt als erster
echter Block-Loop im Repo angekommen.

Wichtigste Konsequenzen:

- `SessionRequest` kann jetzt optionale `runtime_observations` tragen
- der Planner simuliert damit jetzt mehrere Bloecke statt nur einen
  Startzustand
- `planned_blocks` und `mode_adaptation_trace` sind jetzt Teil des
  `TeachingPlan`
- `ModeAdaptationState` wird jetzt zwischen beobachteten Bloecken
  fortgeschrieben
- ein Moduswechsel landet jetzt sichtbar im naechsten Preview-Block

Neue oder aktualisierte Referenzartefakte:

- [src/mathteach/services/planner.py](/Users/jonasweiss/MathTeach/src/mathteach/services/planner.py)
- [src/mathteach/models.py](/Users/jonasweiss/MathTeach/src/mathteach/models.py)
- [tests/test_planner_runtime_flow.py](/Users/jonasweiss/MathTeach/tests/test_planner_runtime_flow.py)
- [tests/test_api.py](/Users/jonasweiss/MathTeach/tests/test_api.py)

Verifikation:

- `ruff`: bestanden
- `pytest`: `50 passed, 1 warning`
- Warning weiter nur wegen nicht schreibbarem `pytest`-Cache

## Phase-H-H1-Code-Review 2026-04-02

Die neue Review-Lage bestaetigt, dass Phase `H.1` nicht mehr nur
`implementation-ready`, sondern bereits real im MVP-Rahmen implementiert ist.

Wichtigste Konsequenzen:

- der Status verschiebt sich von `ready for code` zu `first runtime logic live`
- die Hauptluecke ist nicht mehr Architektur, sondern `blockweise Planner-Integration`
- `SignalInterpreter`, `RuntimeModeAdapter`, Hysterese und Transition-Sprache
  gelten jetzt als bestaetigte Kernbausteine
- der naechste direkte Schritt ist ein echter Block-Loop statt nur eines
  initialen `mode_adaptation_state`

Neue oder aktualisierte Referenzartefakte:

- [docs/live-mode-adaptation-h1-code-review-2026-04-02.md](/Users/jonasweiss/MathTeach/docs/live-mode-adaptation-h1-code-review-2026-04-02.md)
- [src/mathteach/services/runtime_mode_adapter.py](/Users/jonasweiss/MathTeach/src/mathteach/services/runtime_mode_adapter.py)
- [src/mathteach/services/planner.py](/Users/jonasweiss/MathTeach/src/mathteach/services/planner.py)
- [tests/test_runtime_mode_adapter.py](/Users/jonasweiss/MathTeach/tests/test_runtime_mode_adapter.py)
- [tests/test_observation_signal_interpretation.py](/Users/jonasweiss/MathTeach/tests/test_observation_signal_interpretation.py)
- [tests/test_transition_language.py](/Users/jonasweiss/MathTeach/tests/test_transition_language.py)

Verifikation:

- Review-Triage auf Basis des bereits gruenen H.1-Code-Checkpoints
- keine neue Runtime-Logik in diesem Schritt

## Phase-H-H1-Code-Start 2026-04-02

Die erste echte Runtime-Umsetzung fuer Phase `H.1` ist jetzt im Repo
angekommen.

Wichtigste Konsequenzen:

- `runtime_mode_adapter.py` existiert jetzt als erste operative H-Komponente
- `SignalInterpreter` sitzt jetzt zwischen roher Blockbeobachtung und
  Adaptionsentscheidung
- neue Modelle fuer `RawBlockObservation`, `ObservationSignal`,
  `SignalInterpretationResult`, `ModeAdaptationState` und
  `ModeAdaptationDecision` sind jetzt im gemeinsamen Modell-Layer verankert
- der Planner liefert jetzt bereits einen initialen
  `mode_adaptation_state` fuer spaetere Blockanpassung mit aus
- die ersten drei H-Testfamilien sind jetzt real im Code:
  Beobachtung, Adapterlogik und Transition-Sprache

Neue oder aktualisierte Referenzartefakte:

- [src/mathteach/services/runtime_mode_adapter.py](/Users/jonasweiss/MathTeach/src/mathteach/services/runtime_mode_adapter.py)
- [src/mathteach/models.py](/Users/jonasweiss/MathTeach/src/mathteach/models.py)
- [src/mathteach/services/planner.py](/Users/jonasweiss/MathTeach/src/mathteach/services/planner.py)
- [tests/test_observation_signal_interpretation.py](/Users/jonasweiss/MathTeach/tests/test_observation_signal_interpretation.py)
- [tests/test_runtime_mode_adapter.py](/Users/jonasweiss/MathTeach/tests/test_runtime_mode_adapter.py)
- [tests/test_transition_language.py](/Users/jonasweiss/MathTeach/tests/test_transition_language.py)
- [tests/test_api.py](/Users/jonasweiss/MathTeach/tests/test_api.py)

Verifikation:

- `ruff`: bestanden
- `pytest`: `47 passed, 1 warning`
- Warning weiter nur wegen nicht schreibbarem `pytest`-Cache

## Phase-H-Finalbewertung 2026-04-02

Die neue Review-Lage bestaetigt Phase `H` jetzt nicht mehr nur als
gut vorbereitet, sondern als tatsaechlich `implementation-ready-for-H.1`.

Wichtigste Konsequenzen:

- es gibt fuer `H.1` keine blockierenden Architekturfragen mehr
- die Restpunkte sind jetzt klar als Feintuning und nicht als Vorbedingungen
  eingeordnet
- die naechste Session soll direkt mit `runtime_mode_adapter`,
  Adaptionsmodellen und Testfamilien starten
- Phase `H` gilt damit als abgeschlossen in der Planungs- und
  Spezifikationsdimension und offen nur noch in der Code-Dimension

Neue oder aktualisierte Referenzartefakte:

- [docs/live-mode-adaptation-final-assessment-2026-04-02.md](/Users/jonasweiss/MathTeach/docs/live-mode-adaptation-final-assessment-2026-04-02.md)
- [docs/live-mode-adaptation-readiness-review-2026-04-02.md](/Users/jonasweiss/MathTeach/docs/live-mode-adaptation-readiness-review-2026-04-02.md)
- [docs/live-mode-adaptation-specification.md](/Users/jonasweiss/MathTeach/docs/live-mode-adaptation-specification.md)
- [docs/live-mode-adaptation-program.md](/Users/jonasweiss/MathTeach/docs/live-mode-adaptation-program.md)
- [README.md](/Users/jonasweiss/MathTeach/README.md)

Verifikation:

- reine Abschlussbewertung auf Doku-Basis
- keine neue Runtime-Logik in diesem Schritt

## Phase-H-Implementierungsreife 2026-04-02

Der neue Review bestaetigt, dass Phase `H` nicht mehr nur konzeptionell,
sondern fast direkt codefaehig beschrieben ist.

Wichtigste Konsequenzen:

- die verbleibenden Restluecken sind jetzt auf API, Kalibrierung und
  Planner-Integration eingegrenzt
- `runtime_mode_adapter` ist jetzt als naechste konkrete Runtime-Komponente
  noch klarer positioniert
- `SignalInterpreter` ist jetzt als eigener Schritt zwischen roher Evidenz
  und eigentlicher Adaptionsentscheidung festgezogen
- erste MVP-Defaults fuer `H.1` sind jetzt als Startkalibrierung beschrieben
- die Planner-Folge `start mode -> block -> observe -> interpret -> adapt`
  ist jetzt explizit dokumentiert

Neue oder aktualisierte Referenzartefakte:

- [docs/live-mode-adaptation-readiness-review-2026-04-02.md](/Users/jonasweiss/MathTeach/docs/live-mode-adaptation-readiness-review-2026-04-02.md)
- [docs/live-mode-adaptation-specification.md](/Users/jonasweiss/MathTeach/docs/live-mode-adaptation-specification.md)
- [docs/live-mode-adaptation-program.md](/Users/jonasweiss/MathTeach/docs/live-mode-adaptation-program.md)
- [docs/support-response-matrix-implementation-plan.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-implementation-plan.md)
- [README.md](/Users/jonasweiss/MathTeach/README.md)

Verifikation:

- reine Doku- und Spezifikationsschaerfung
- keine neue Runtime-Logik in diesem Schritt

## Phase-H-Planungsschaerfung 2026-04-02

Der neue Review hat die entscheidende Frage gestellt, ob Phase `H` schon
wirklich implementierungsreif beschrieben ist oder noch zu vage bleibt.

Wichtigste Konsequenzen:

- `observation signals` sind jetzt nicht nur benannt, sondern mit ersten
  Schwellenklassen beschrieben
- `Block` und Beobachtungstakt sind jetzt explizit definiert
- eine erste `adaptation decision matrix` ist jetzt festgehalten
- `hysteresis` hat jetzt ersten Pseudocode und konkrete Guardrails
- `transition messaging` ist jetzt als Template-Struktur statt nur als Idee
  beschrieben
- die Rueckwaertskompatibilitaet zwischen Phase `G` und `H` ist jetzt klarer
  formuliert

Neue oder aktualisierte Referenzartefakte:

- [docs/live-mode-adaptation-specification.md](/Users/jonasweiss/MathTeach/docs/live-mode-adaptation-specification.md)
- [docs/live-mode-adaptation-program.md](/Users/jonasweiss/MathTeach/docs/live-mode-adaptation-program.md)
- [README.md](/Users/jonasweiss/MathTeach/README.md)

Verifikation:

- reine Doku- und Planungsschaerfung
- keine neue Runtime-Logik in diesem Schritt

## Phase-H-Spezifikation 2026-04-02

Der neue Review hat gezeigt, dass Phase `H` als Programm bereits klar war,
aber operativ noch zu grob blieb.

Wichtigste Konsequenzen:

- die offenen Luecken von Phase `H` sind jetzt explizit spezifiziert
- `observation signals`, `runtime_mode_adapter`, `hysteresis` und
  `transition messaging` sind jetzt auf Implementierungsniveau beschrieben
- `mode_selector` bleibt fuer den Startmodus zustaendig
- eine neue Komponente `runtime_mode_adapter` ist jetzt als sauberer Ort fuer
  blockweise Live-Anpassung festgelegt

Neue oder aktualisierte Referenzartefakte:

- [docs/live-mode-adaptation-specification.md](/Users/jonasweiss/MathTeach/docs/live-mode-adaptation-specification.md)
- [docs/live-mode-adaptation-program.md](/Users/jonasweiss/MathTeach/docs/live-mode-adaptation-program.md)
- [docs/support-response-matrix-implementation-plan.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-implementation-plan.md)
- [README.md](/Users/jonasweiss/MathTeach/README.md)

Verifikation:

- reine Doku- und Planungsschaerfung
- keine neue Runtime-Logik in diesem Schritt

## Phase-H-Programm 2026-04-02

Der neue Review ist jetzt nicht nur als Triage, sondern als erstes
konkretes Arbeitsprogramm fuer die naechste Architekturphase verankert.

Wichtigste Konsequenzen:

- `planner-level live mode adaptation` ist jetzt als eigene Phase `H`
  beschrieben
- die naechste Implementierung soll auf `Block-Ebene` arbeiten
- Beobachtungssignale, Wechselregeln, Hysterese und ruhige
  Uebergangssprache sind jetzt explizit als erste Arbeitspakete definiert
- noch keine neue Runtime-Logik, aber ein klarer Bauplan fuer die naechste
  Session

Neue oder aktualisierte Referenzartefakte:

- [docs/live-mode-adaptation-program.md](/Users/jonasweiss/MathTeach/docs/live-mode-adaptation-program.md)
- [docs/support-response-matrix-implementation-plan.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-implementation-plan.md)
- [docs/roadmap.md](/Users/jonasweiss/MathTeach/docs/roadmap.md)
- [README.md](/Users/jonasweiss/MathTeach/README.md)

Verifikation:

- reine Doku- und Programmphase
- keine neue Runtime-Logik in diesem Schritt

## Review-Triage Nach G 2026-04-02

Die neuen Reviews bestaetigen Phase `G` nicht nur als erfolgreichen
Feature-Schritt, sondern als echte Architekturverschiebung.

Wichtigste Konsequenzen:

- `mode_selector` gilt jetzt als stabile neue Schicht zwischen
  `conflict_resolver` und `planner`
- die Trennung zwischen `requested_mode` und `selected_mode` ist jetzt
  ausdruecklich projekttragend
- die naechste Phase ist jetzt klar als `planner-level live mode adaptation`
  benannt
- die Live-Phase soll zunaechst auf `Block-Ebene` arbeiten, nicht auf jedem
  Einzelschritt
- `Hysterese` und ruhige Uebergangssprache sind jetzt fruehe Guardrails

Neue oder aktualisierte Referenzartefakte:

- [docs/mode-selection-review-triage-2026-04-02.md](/Users/jonasweiss/MathTeach/docs/mode-selection-review-triage-2026-04-02.md)
- [docs/architecture-v2.md](/Users/jonasweiss/MathTeach/docs/architecture-v2.md)
- [docs/mode-selection-strategy.md](/Users/jonasweiss/MathTeach/docs/mode-selection-strategy.md)
- [docs/support-response-matrix-implementation-plan.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-implementation-plan.md)
- [docs/roadmap.md](/Users/jonasweiss/MathTeach/docs/roadmap.md)

Verifikation:

- reine Doku- und Architektur-Triage
- keine neue Runtime-Logik in diesem Schritt

## Support-Sensitive-Mode-Selection 2026-04-02 G

Die erste eigene `mode_selector`-Schicht ist jetzt zwischen
`conflict_resolver` und `planner` eingezogen.

Wichtigste Konsequenzen:

- `requested_mode` und `selected_mode` sind jetzt explizit getrennt
- Moduswahl ist jetzt support-sensitiv statt nur request-sensitiv
- Triads und Konfliktpaare koennen jetzt echte `mode overrides` ausloesen
- Modus-Constraints sind jetzt sichtbar und testbar
- die naechste Engstelle verschiebt sich jetzt in `planner-level live mode adaptation`

Neue oder aktualisierte Referenzartefakte:

- [docs/mode-selection-strategy.md](/Users/jonasweiss/MathTeach/docs/mode-selection-strategy.md)
- [src/mathteach/services/mode_selector.py](/Users/jonasweiss/MathTeach/src/mathteach/services/mode_selector.py)
- [src/mathteach/services/planner.py](/Users/jonasweiss/MathTeach/src/mathteach/services/planner.py)
- [src/mathteach/models.py](/Users/jonasweiss/MathTeach/src/mathteach/models.py)
- [tests/test_mode_selection.py](/Users/jonasweiss/MathTeach/tests/test_mode_selection.py)
- [tests/test_api.py](/Users/jonasweiss/MathTeach/tests/test_api.py)

Erste explizite Modusentscheidungen:

- `ADHD + Dyscalculia + Scarcity -> worked_example_tutoring`
- `ADHD + Autism + Scarcity -> worked_example_tutoring`
- `Dyscalculia + Language-Sensitive + Scarcity -> origin_then_example`
- `ADHD + Scarcity + origin_story request -> origin_then_example`

Verifikation:

- `ruff`: bestanden
- `pytest`: `38 passed, 1 warning`
- Warning weiter nur wegen nicht schreibbarem `pytest`-Cache

## Triads-And-Priority-Ladders 2026-04-02 F

Die erste Triad-Schicht ist jetzt auf dem bestehenden `conflict_resolver`
aufgebaut.

Wichtigste Konsequenzen:

- `triad_groups` und `priority_ladders` sind jetzt Teil der `response settings`
- erste explizite Triads sind jetzt operationalisiert
- Priorisierung wird damit nicht nur implizit, sondern sichtbar und testbar
- die naechste Engstelle verschiebt sich jetzt in die `support-sensitive Moduswahl im Planner`

Neue oder aktualisierte Referenzartefakte:

- [docs/profile-prioritization.md](/Users/jonasweiss/MathTeach/docs/profile-prioritization.md)
- [docs/profile-conflict-resolution.md](/Users/jonasweiss/MathTeach/docs/profile-conflict-resolution.md)
- [docs/mixed-profile-scenarios.md](/Users/jonasweiss/MathTeach/docs/mixed-profile-scenarios.md)
- [src/mathteach/services/conflict_resolver.py](/Users/jonasweiss/MathTeach/src/mathteach/services/conflict_resolver.py)
- [tests/test_profile_conflicts.py](/Users/jonasweiss/MathTeach/tests/test_profile_conflicts.py)

Zuerst operationalisierte Triads:

- `ADHD + Dyscalculia + Scarcity`
- `ADHD + Autism + Scarcity`
- `Dyscalculia + Language-Sensitive + Scarcity`

Verifikation:

- `ruff`: bestanden
- `pytest`: `32 passed, 1 warning`
- Warning weiter nur wegen nicht schreibbarem `pytest`-Cache

## Mixed-Profile-Architektur 2026-04-02 E

Die Reviews zur naechsten Engstelle sind jetzt in eine erste echte
`mixed profile`-Schicht uebersetzt.

Wichtigste Konsequenzen:

- Einzelprofile bleiben die Basis, aber nicht mehr der Endzustand
- `conflict_resolver` ist jetzt als eigene Schicht eingefuehrt
- Konfliktpaare werden explizit erkannt statt nur implizit von Lade-Reihenfolge getragen
- `response settings` tragen jetzt transparente `conflict_pairs` und `conflict_resolution_notes`

Neue oder aktualisierte Referenzartefakte:

- [docs/profile-conflict-resolution.md](/Users/jonasweiss/MathTeach/docs/profile-conflict-resolution.md)
- [docs/mixed-profile-scenarios.md](/Users/jonasweiss/MathTeach/docs/mixed-profile-scenarios.md)
- [src/mathteach/services/conflict_resolver.py](/Users/jonasweiss/MathTeach/src/mathteach/services/conflict_resolver.py)
- [tests/test_profile_conflicts.py](/Users/jonasweiss/MathTeach/tests/test_profile_conflicts.py)

Zuerst operationalisierte Konfliktpaare:

- `ADHD + Dyscalculia`
- `ADHD + Autism`
- `ADHD + Scarcity`
- `Dyscalculia + Language-Sensitive`
- `Dyscalculia + Scarcity`

Verifikation:

- `ruff`: bestanden
- `pytest`: `28 passed, 1 warning`
- Warning weiter nur wegen nicht schreibbarem `pytest`-Cache

## Runtime-Ausbau 2026-04-02 D

Die Scarcity-Linie ist jetzt als sechste operative Profilfamilie eingebunden.

Wichtigste Konsequenzen:

- `scarcity-aware support` ist jetzt in Doku, Engine, Planner und API operationalisiert
- Tutorverhalten priorisiert nun auch Relevanz, Wiedereinstieg und kleine sichtbare Erfolge
- die naechste echte Engstelle sind jetzt gemischte Supportprofile und Priorisierungsregeln

Neue oder aktualisierte Referenzartefakte:

- [docs/support-response-matrix-scarcity.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-scarcity.md)
- [docs/support-response-matrix-implementation-plan.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-implementation-plan.md)
- [src/mathteach/services/response_engine.py](/Users/jonasweiss/MathTeach/src/mathteach/services/response_engine.py)
- [src/mathteach/services/planner.py](/Users/jonasweiss/MathTeach/src/mathteach/services/planner.py)
- [tests/test_response_engine.py](/Users/jonasweiss/MathTeach/tests/test_response_engine.py)
- [tests/test_api.py](/Users/jonasweiss/MathTeach/tests/test_api.py)

Verifikation:

- `ruff`: bestanden
- `pytest`: `22 passed, 1 warning`
- Warning weiter nur wegen nicht schreibbarem `pytest`-Cache

## Runtime-Ausbau 2026-04-02 C

Die erste sprachsensible Profilfamilie ist jetzt operativ in Doku, Engine,
Planner und API eingebunden.

Wichtigste Konsequenzen:

- `language-sensitive support` ist jetzt die fuenfte operative Einzelprofilfamilie
- nicht nur das Signal, sondern auch konkrete `response settings` werden jetzt abgeleitet
- der Planner reagiert jetzt auch auf sprachsensible Unterstuetzung
- die naechste Profilfamilie ist jetzt klar `scarcity-aware support`

Neue oder aktualisierte Referenzartefakte:

- [docs/support-response-matrix-language-sensitive.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-language-sensitive.md)
- [docs/support-response-matrix-implementation-plan.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-implementation-plan.md)
- [src/mathteach/services/response_engine.py](/Users/jonasweiss/MathTeach/src/mathteach/services/response_engine.py)
- [src/mathteach/services/planner.py](/Users/jonasweiss/MathTeach/src/mathteach/services/planner.py)
- [tests/test_response_engine.py](/Users/jonasweiss/MathTeach/tests/test_response_engine.py)
- [tests/test_api.py](/Users/jonasweiss/MathTeach/tests/test_api.py)

Verifikation:

- `ruff`: bestanden
- `pytest`: `20 passed, 1 warning`
- Warning weiter nur wegen nicht schreibbarem `pytest`-Cache

## Review-Einarbeitung 2026-04-02 B

Ein weiterer operativer Review-Schritt hat die Richtung der `Support Response Matrix`
konkretisiert.

Wichtigste Konsequenzen:

- der Uebergang von Theorie zu `Decision Rules` ist jetzt explizit dokumentiert
- `ADHD-aware support` und `dyscalculia-aware support` sind die ersten
  operativen Einzelprofile
- es gibt jetzt einen ersten `Implementation Plan` fuer die Matrix-Phase
- exakte klinisch klingende Prozent- oder Diagnosemodelle bleiben bewusst
  ausserhalb der aktiven Architektur

Neue Referenzdokumente aus dieser Review-Einarbeitung:

- [docs/support-response-matrix-review-triage-2026-04-02.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-review-triage-2026-04-02.md)
- [docs/support-response-matrix-template.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-template.md)
- [docs/support-response-matrix-adhd.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-adhd.md)
- [docs/support-response-matrix-dyscalculia.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-dyscalculia.md)
- [docs/support-response-matrix-dyslexia.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-dyslexia.md)
- [docs/support-response-matrix-autism.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-autism.md)
- [docs/support-response-matrix-language-sensitive.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-language-sensitive.md)
- [docs/support-response-matrix-scarcity.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-scarcity.md)
- [docs/support-response-matrix-implementation-plan.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-implementation-plan.md)

## Review-Einarbeitung 2026-04-02

Der externe Journal-Review wurde als naechste Prioritaetskorrektur uebernommen.

Wichtigste Konsequenzen:

- der bisherige Stand wird als `solide und strategisch sauber` bestaetigt
- die Hauptluecke liegt jetzt in der `Operationalisierung`
- der naechste Hauptschritt ist nicht neue Allgemeintheorie, sondern die `Support Response Matrix`
- die aktive Zielarchitektur wird jetzt klarer als `lokal-first`, `geschlossen` und `rule-based` gefasst
- die Support-Matrix arbeitet mit `support signals` statt mit diagnostischen Prozentmodellen

Neue Referenzdokumente aus dieser Review-Einarbeitung:

- [docs/journal-review-triage-2026-04-02.md](/Users/jonasweiss/MathTeach/docs/journal-review-triage-2026-04-02.md)
- [docs/support-response-matrix-structure.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-structure.md)
- [docs/architecture-v2.md](/Users/jonasweiss/MathTeach/docs/architecture-v2.md)

## Projektkern

MathTeach ist aktuell als `geschlossenes lokales Mathematik-Lernsystem` angelegt.

Zielbild:

- kompletter lokaler Mathematik-Korpus
- lokaler `Teacher Mind`
- keine Cloud-Pflicht
- nutzbar als App oder eigenes Geraet
- stark fuer armutsbetroffene Lernende, aber ebenso fuer Schule, Studium und erwachsene Selbstlerner

Die Architektur trennt weiterhin:

- `Knowledge Core`
- `Teacher Mind`
- `Teaching Intelligence Engine`

## Aktueller Mathematik-Korpus

Die mathematische Grundsammlung ist fuer die erste grosse Projektphase ueber vier Epochen aufgebaut und als stabiler Kern zu betrachten.

### Antiquity

- `Euclid: Elements`
- `Archimedes: On the Sphere and Cylinder`
- `Archimedes: The Method`
- `Apollonius: Conics`
- `Diophantus: Arithmetica`
- `Heron: Metrica`
- `Pappus: Collection`
- `Hipparchus: commentary and chord-table tradition`
- `Theon of Alexandria: Euclid and Ptolemy commentary tradition`
- `Hypatia: commentary tradition on Arithmetica and Conics`
- `Eutocius of Ascalon: commentaries on Archimedes and Apollonius`
- `Aryabhata: Aryabhatiya`

### Medieval Transmission and Synthesis

- `Brahmasphutasiddhanta`
- `Al-Khwarizmi: Book on Addition and Subtraction after the Method of the Indians`
- `Al-Khwarizmi: Al-jabr`
- `Fibonacci: Liber Abaci`
- `Bhaskara II: Lilavati`
- `Bhaskara II: Bijaganita`
- `Omar Khayyam: Demonstration concerning problems of algebra`
- `Adelard of Bath: Euclid translation tradition`
- `Al-Karaji: Al-Fakhri`
- `Nicole Oresme: Tractatus de configurationibus qualitatum et motuum`
- `Regiomontanus: De triangulis omnimodis`
- `Nasir al-Din al-Tusi: Treatise on the Quadrilateral`

### Early Modern Analysis and Chance

- `Newton: Method of Fluxions`
- `Leibniz: Nova Methodus pro Maximis et Minimis`
- `Pascal and Fermat correspondence on games of chance`
- `Descartes: La Geometrie`
- `Cavalieri: Geometria indivisibilibus continuorum nova quadam ratione promota`
- `Wallis: Arithmetica infinitorum`
- `Huygens: De Ratiociniis in Ludo Aleae`
- `Viete: In artem analyticam isagoge`
- `Stevin: De Thiende`
- `Napier: Mirifici logarithmorum canonis descriptio`
- `Jacob Bernoulli: Ars Conjectandi`
- `Kepler: Astronomia nova`
- `Fermat: Methodus ad disquirendam maximam et minimam`
- `Barrow: Lectiones geometricae`
- `Henry Briggs: Arithmetica logarithmica`
- `Gregory of Saint-Vincent: Opus geometricum`

### Modern Mathematics

- `Gauss: Disquisitiones Arithmeticae`
- `Fourier: Theorie analytique de la chaleur`
- `Abel: Memoire sur les equations algebriques, ou l'on demontre l'impossibilite de la resolution de l'equation generale du cinquieme degre`
- `Cauchy: Cours d'analyse de l'Ecole Royale Polytechnique`
- `Weierstrass: Mathematische Werke`
- `Galois: Memoire sur les conditions de resolubilite des equations par radicaux`
- `Hamilton: Elements of Quaternions`
- `Cayley: The collected mathematical papers of Arthur Cayley`
- `Kronecker: Werke`
- `Riemann: Ueber die Hypothesen welche der Geometrie zu Grunde liegen`
- `Dedekind: Was sind und was sollen die Zahlen?`
- `Peano: Arithmetices principia, nova methodo exposita`
- `Cantor: Beitrage zur Begrundung der transfiniten Mengenlehre`
- `Zermelo: Untersuchungen ueber die Grundlagen der Mengenlehre I`
- `Hausdorff: Grundzuege der Mengenlehre`
- `Klein: Vergleichende Betrachtungen ueber neuere geometrische Forschungen`
- `Poincare: Analysis Situs`
- `Russell and Whitehead: Principia Mathematica`
- `Hilbert: Grundlagen der Geometrie`
- `Hilbert and Ackermann: Grundzuege der theoretischen Logik`
- `John von Neumann and Oskar Morgenstern: Theory of Games and Economic Behavior`
- `Nicolas Bourbaki: Elements of Mathematics (Theory of Sets)`
- `Emmy Noether: Idealtheorie in Ringbereichen`
- `Lebesgue: Integrale, longueur, aire`
- `Alonzo Church: An Unsolvable Problem of Elementary Number Theory`
- `Gerhard Gentzen: Untersuchungen ueber das logische Schliessen I and II`
- `Kolmogorov: Grundbegriffe der Wahrscheinlichkeitsrechnung`
- `Godel: Ueber formal unentscheidbare Saetze der Principia Mathematica und verwandter Systeme I`
- `Turing: On Computable Numbers, with an Application to the Entscheidungsproblem`
- `Alexander Grothendieck: Sur quelques points d'algebre homologique`
- `Jean-Pierre Serre: Geometrie algebrique et geometrie analytique`

## Aktueller Teacher-Mind-Stand

Der Teacher Mind ist jetzt als gestufter lokaler Wissensaufbau dokumentiert.

Reihenfolge:

1. `Safety and Restraint`
2. `Psychological Foundations`
3. `Pedagogical Foundations`
4. `Universal Round U.1`
5. `Universal Round U.2`
6. `Universal Round U.3`
7. `Universal Round U.4`
8. spaeter `Mathematics Teaching Foundations`
9. spaeter konkrete Runtime- und Response-Matrizen

### Psychological Foundations

- `How People Learn II: Learners, Contexts, and Cultures`
- `How People Learn: Brain, Mind, Experience, and School`
- `Improving Students' Learning With Effective Learning Techniques: Promising Directions From Cognitive and Educational Psychology`
- `Test-Enhanced Learning: Taking Memory Tests Improves Long-Term Retention`
- `The Critical Importance of Retrieval for Learning`
- `Organizing Instruction and Study to Improve Student Learning`
- `Using Student Achievement Data to Support Instructional Decision Making`
- `Learning Styles: Concepts and Evidence`

### Pedagogical Foundations

- `Organizing Instruction and Study to Improve Student Learning`
- `Using Student Achievement Data to Support Instructional Decision Making`
- `Principles of Instruction: Research-Based Strategies That All Teachers Should Know`
- `The Power of Feedback`
- `Focus on Formative Feedback`
- `Self-Explanations: How Students Study and Use Examples in Learning to Solve Problems`
- `Why Minimal Guidance During Instruction Does Not Work`

### Universal Round U.1

- `Self-Determination Theory and the Facilitation of Intrinsic Motivation, Social Development, and Well-Being`
- `A Question of Belonging: Race, Social Fit, and Achievement`
- `Psychological Safety and Learning Behavior in Work Teams`
- `Learning from Errors`
- `Poverty Impedes Cognitive Function`
- `Stereotype Threat and the Intellectual Test Performance of African Americans`
- `Inclusion and Education: All Means All`
- `CAST Universal Design for Learning Guidelines 3.0`

### Universal Round U.2

- `When and Where Do We Apply What We Learn? A Taxonomy for Far Transfer`
- `Toward a Model of Transfer as Sense-Making`
- `Reasoning and Learning by Analogy`
- `Situated Learning: Legitimate Peripheral Participation`
- `Mind in Society: The Development of Higher Psychological Processes`
- `Cognitive Apprenticeship: Teaching the Craft of Reading, Writing, and Mathematics`
- `An Educational Psychology Success Story: Social Interdependence Theory and Cooperative Learning`
- `The Adult Learner`
- `Learning in Adulthood: A Comprehensive Guide`

### Universal Round U.3

- `ADHD in the Classroom: Helping Children Succeed in School`
- `Learning Disabilities`
- `Reading and Reading Disorders`
- `Infographic: Does your child struggle with Math? Dyscalculia could be the reason.`
- `CAST Universal Design for Learning Guidelines 3.0`
- `SAMHSA's Concept of Trauma and Guidance for a Trauma-Informed Approach`
- `How People Learn II: Learners, Contexts, and Cultures`
- `The Adult Learner`
- `Learning Styles: Concepts and Evidence`
- `Why Minimal Guidance During Instruction Does Not Work`
- `Neuroscience and Education: Myths and Messages`

### Universal Round U.4

- `ADHD in the Classroom: Helping Children Succeed in School`
- `Non-pharmacological interventions for attention-deficit/hyperactivity disorder (ADHD) delivered in school settings: systematic reviews of quantitative and qualitative research`
- `Genetics of childhood disorders: XVII. ADHD, Part 1: The executive functions and ADHD`
- `Dyscalculia: from brain to education`
- `Developmental dyscalculia and basic numerical capacities: a study of 8-9-year-old students`
- `Infographic: Does your child struggle with Math? Dyscalculia could be the reason.`
- `Reading and Reading Disorders`
- `Dyslexia (specific reading disability)`
- `Treatment and Intervention for Autism Spectrum Disorder`
- `Visual supports at home and in the community for individuals with autism spectrum disorders: A scoping review`
- `Issues in the use of visual supports to promote communication in individuals with autism spectrum disorder`
- `Teaching Academic Content and Literacy to English Learners in Elementary and Middle School`
- `Successful teaching practices for English language learners in multilingual mathematics classrooms: a meta-analysis`

## Runtime-Stand

Neben dem Dokumentationsstand gibt es jetzt auch einen ersten offenen Runtime-Zweig, der in diesem Commit mitgesichert wird:

- `Tutor Runtime Modes` als eigene Doku
- erster Planner-Routing-Ansatz fuer:
  - `worked_example_tutoring`
  - `origin_story_explanation`
  - `origin_then_example`
- erweiterte `TeachingPlan`- und `RetrievalPlan`-Modelle
- erste API-Tests fuer den Unterschied zwischen Beispielmodus und Ursprungserklaerung

Seit dem letzten operativen Schritt existiert nun auch ein erster
`response_engine` im Code:

- `support signal profile` als eigenes Datenmodell
- `response settings` als eigenes Datenmodell
- `response_matrix.py` als eigenes Modellmodul
- erste regelbasierte Ableitung fuer:
- `ADHD-aware support`
- `dyscalculia-aware support`
- `dyslexia-aware support`
- `autism-spectrum-aware support`
- `language-sensitive support`
- `scarcity-aware support`
- `TeachingPlan` liefert diese Settings jetzt direkt mit aus
- neue Service- und API-Tests sichern den Pfad ab

Betroffene Dateien:

- [docs/tutor-runtime-modes.md](/Users/jonasweiss/MathTeach/docs/tutor-runtime-modes.md)
- [docs/architecture.md](/Users/jonasweiss/MathTeach/docs/architecture.md)
- [docs/roadmap.md](/Users/jonasweiss/MathTeach/docs/roadmap.md)
- [src/mathteach/models.py](/Users/jonasweiss/MathTeach/src/mathteach/models.py)
- [src/mathteach/response_matrix.py](/Users/jonasweiss/MathTeach/src/mathteach/response_matrix.py)
- [src/mathteach/services/planner.py](/Users/jonasweiss/MathTeach/src/mathteach/services/planner.py)
- [src/mathteach/services/response_engine.py](/Users/jonasweiss/MathTeach/src/mathteach/services/response_engine.py)
- [tests/test_api.py](/Users/jonasweiss/MathTeach/tests/test_api.py)
- [tests/test_response_matrix.py](/Users/jonasweiss/MathTeach/tests/test_response_matrix.py)
- [tests/test_response_engine.py](/Users/jonasweiss/MathTeach/tests/test_response_engine.py)

## Wichtige Spannung im Repo

Es gibt aktuell noch eine bewusst nicht aufgeloeste Spannung:

- die Produktvision ist inzwischen stark `lokal`, `geschlossen` und notfalls `ohne AI`
- die [README.md](/Users/jonasweiss/MathTeach/README.md) enthaelt noch einen aelteren Modell-Stack mit Cloud-LLMs

Das ist kein Fehler dieses Journal-Schritts, sondern eine offene Architektur-Aufraeumarbeit fuer die naechste oder eine spaetere Session.

Mit dem Review vom `2026-04-02` ist diese Spannung jetzt enger gefasst:

- `architecture-v2` ist die aktive Richtung
- die aelteren Cloud- und Modellpassagen in der README gelten als `Legacy-/Explorationsstand`
- die naechste groessere Repo-Bereinigung sollte README und Runtime explizit an die lokale Zielarchitektur angleichen

## Letzte groessere Commit-Linie

- `7d5ee28` Add universal round U4 program
- `ff995e9` Add universal round U3 program
- `a3e3923` Add universal round U2 program
- `0ad7674` Add universal round U1 program
- `542d690` Triage universal tutor system review
- `7846931` Triage teacher mind foundations review
- `f8b7491` Add pedagogical foundations program
- `7fe991a` Add psychological foundations program
- `792f538` Reorder teacher mind around core foundations
- `a618ff5` Add teacher mind evidence program
- `57036bd` Define pedagogical strategy matrix
- `1cafc85` Define learner support profiles

## Empfohlener naechster Schritt

Der logisch naechste starke Schritt ist:

- kein neuer Theorieblock
- sondern die naechste Code-Stufe der `Support Response Matrix`

also die Uebersetzung von:

- `ADHD-aware support`
- `dyscalculia-aware support`
- `dyslexia-aware support`
- `autism-spectrum-aware support`
- `ELL / language-sensitive support`

in konkrete Tutorentscheidungen ueber:

- `pacing`
- `step_size`
- `notation_density`
- `text_load`
- `visualization`
- `error_handling`
- `language_support`
- `self_check_rhythm`
- `external_scaffolds`

Empfohlene erste Ausbaureihenfolge:

1. `response_engine` weiter entlang aller Response Dimensions ausbauen
2. Planner staerker response-aware machen
3. dann gemischte Supportprofile sauber priorisieren
4. danach support-sensitive Moduswahl im Planner vertiefen

Direkt vorbereitete naechste Arbeitsartefakte:

1. [support-response-matrix-adhd.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-adhd.md)
2. [support-response-matrix-dyscalculia.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-dyscalculia.md)
3. [support-response-matrix-language-sensitive.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-language-sensitive.md)
4. [support-response-matrix-scarcity.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-scarcity.md)
5. [profile-conflict-resolution.md](/Users/jonasweiss/MathTeach/docs/profile-conflict-resolution.md)
6. [mixed-profile-scenarios.md](/Users/jonasweiss/MathTeach/docs/mixed-profile-scenarios.md)
7. [support-response-matrix-implementation-plan.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-implementation-plan.md)
