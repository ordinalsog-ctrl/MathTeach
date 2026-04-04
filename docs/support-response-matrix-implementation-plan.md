# Support Response Matrix Implementation Plan

## Ziel

Dieser Plan uebersetzt die aktuelle Review-Lage in einen konkreten
Arbeitsablauf fuer die naechste Implementationsphase.

Der Fokus liegt auf:

- `ADHD-aware support`
- `dyscalculia-aware support`
- `dyslexia-aware support`
- `autism-spectrum-aware support`
- `language-sensitive support`
- `scarcity-aware support`
- spaeterer Code-Integration in Planner und Runtime

## Arbeitsprinzip

Die Reihenfolge lautet:

1. `structure before code`
2. `single profiles before mixed profiles`
3. `candidate defaults before hard rules`
4. `explainable rules before opaque adaptation`

## Phase A: Documentation Pass

Zeitrahmen:

- `weeks 1 to 3`

Deliverables:

- [support-response-matrix-structure.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-structure.md)
- [support-response-matrix-template.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-template.md)
- [support-response-matrix-adhd.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-adhd.md)
- [support-response-matrix-dyscalculia.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-dyscalculia.md)
- [support-response-matrix-dyslexia.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-dyslexia.md)
- [support-response-matrix-autism.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-autism.md)
- [support-response-matrix-language-sensitive.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-language-sensitive.md)
- [support-response-matrix-scarcity.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-scarcity.md)

Exit criteria:

- alle primaeren Response Dimensions sind fest
- sechs Einzelprofile sind operational beschrieben
- jede Matrix hat erkennbare Quellenanker

## Phase B: Code Skeleton

Zeitrahmen:

- `weeks 4 to 6`

Geplante Dateien:

- `src/mathteach/response_matrix.py`
- `src/mathteach/services/response_engine.py`
- spaeter `src/mathteach/services/profiler.py`
- `tests/test_response_matrix.py`

Mindestumfang:

- Datenmodelle fuer `support signal profile`
- Datenmodelle fuer `response settings`
- einfache regelbasierte Evaluation
- erste Tests fuer ADHD-, Dyscalculia-, Dyslexia-, Autism-, Language-Sensitive- und Scarcity-Pfade

## Phase C: Planner Integration

Zeitrahmen:

- `weeks 7 to 9`

Ziel:

- Response Settings in den bestehenden Planner ziehen

Geplante Wirkung:

- `planner.py` bekommt response-aware Entscheidungen
- Runtime-Modi werden nicht nur thematisch, sondern auch support-sensitiv gewaehlt
- `TeachingPlan` bekommt spaeter konkrete Response-Felder

Aktueller Stand:

- `TeachingPlan.response_settings` ist operational
- support-sensitive Moduswahl ist operational
- `planned_blocks` tragen jetzt konkrete `support_moves` und
  `support_scaffolds`
- erste Einzelprofile und Mischprofile wirken damit sichtbar bis in die
  Blockvorschau hinein
- `support_moves` und `support_scaffolds` reagieren jetzt auch auf
  `lesson_mode` und blockweise Beobachtungsevidenz
- Resume-Previews koennen jetzt auch getragene `last_observation_evidence`
  direkt wieder in Support-Ausgaben uebersetzen
- `TeachingPlan.resume_context` macht jetzt sichtbar, ob ein Plan frisch
  startet oder aus `inline_state`, `inline_checkpoint` oder
  `stored_checkpoint` fortgesetzt wird
- getragene Evidenz und konsumierte `pending_transition_message` sind
  jetzt auch als explizite Resume-Semantik im API-Output sichtbar
- Resume-Roundtrips ueber partielle Checkpoints sind jetzt als eigener
  Haertungspfad dokumentiert in
  [resume-semantics.md](/Users/jonasweiss/MathTeach/docs/resume-semantics.md)
- die H.2c-Signalbasis ist jetzt verbreitert um:
  `rapid_success_two_blocks`, `rapid_success_three_blocks`,
  `vocabulary_request_again`, `error_recovery_with_hint`,
  `repeated_attempt_three_plus` und `mixed_success_inconsistent`
- diese Signale greifen jetzt bereits in `support_moves`,
  Scaffold-Priorisierung und `SignalInterpreter` ein
- H.2d integriert jetzt eine blockweise Konfliktaufloesung:
  `planned_blocks` tragen bei Mischprofilen eine
  `conflict_resolution_summary` mit `pair_conflicts`, optionaler
  `triad_group`, `priority_ladder`, unterdrueckten und adaptierten Moves
- H.2e erweitert diese Blockauflosung jetzt um echte
  Move-Transformation:
  `generated_moves` und `move_dependencies_applied` machen sichtbar,
  wenn Pair-/Triad-Regeln Moves semantisch umbauen oder gezielt neue
  Kombinations-Moves erzeugen

## Phase D: Pilot and Validation

Zeitrahmen:

- `weeks 10 to 12`

Nur unter diesen Bedingungen:

- lokale Speicherung bleibt gewahrt
- Datensparsamkeit ist klar geregelt
- keine diagnostische oder therapeutische Selbstdarstellung des Systems

Beobachtungsfelder:

- Engagement
- Verstaendnisfortschritt
- Fehlererholung
- Abbruchpunkte
- wahrgenommene Sicherheit

## Phase E: Multi-Profile Conflict Resolution

Zeitrahmen:

- `next 2 to 3 weeks`

Ziel:

- von stabilen Einzelprofilen zu expliziter Konfliktaufloesung fuer Mischprofile

Deliverables:

- [profile-conflict-resolution.md](/Users/jonasweiss/MathTeach/docs/profile-conflict-resolution.md)
- [mixed-profile-scenarios.md](/Users/jonasweiss/MathTeach/docs/mixed-profile-scenarios.md)
- [profile-prioritization.md](/Users/jonasweiss/MathTeach/docs/profile-prioritization.md)
- `src/mathteach/services/conflict_resolver.py`
- `tests/test_profile_conflicts.py`

Erste Prioritaet:

- Konfliktpaare vor Triads
- explizite Resolver-Regeln vor Gewichtungsmodellen
- transparente API-Sichtbarkeit ueber `conflict_pairs` und `conflict_resolution_notes`

Aktueller Stand:

- Paar-Regeln sind operational
- erste Triads und `priority_ladders` sind operational
- `mode_selector` ist jetzt als eigene Schicht fuer support-sensitive Moduswahl eingefuehrt
- `runtime_mode_adapter` und erste H.1-Testfamilien sind operational
- ein erster echter `planner-level live mode adaptation`-Block-Loop ist jetzt
  operational
- Session-Resume ueber bestehenden `mode_adaptation_state` ist jetzt moeglich
- `pending_transition_message` wird jetzt ebenfalls ueber Resume getragen
- konsumierte `transition_message` wird jetzt nach Anzeige sauber geleert
- resume-faehige `last_observation_evidence` sind jetzt Teil des Runtime-State
- Mehrblock-Signale werden jetzt im Planner selbst verdichtet statt nur als
  Roh-Input erwartet
- sichtbare kleine Erfolge und ausbleibende Erfolgslinien werden jetzt
  ebenfalls direkt im Planner abgeleitet
- ein versionierter `mode_adaptation_checkpoint` ist jetzt als externer
  Resume- und Persistenzvertrag eingefuehrt
- naechster Ausbau ist jetzt primaer robuste Checkpoint-Persistenz,
  klare Resume-Semantik und spaetere Storage-Anbindung
- die Anschlussarchitektur fuer `SessionStore`, `session_id` und spaeteren
  `SessionManager` ist jetzt als naechste Bruecke dokumentiert
- `SessionStore` und erster `session_id`-Resume-Pfad sind jetzt operational
- `SessionManager` ist jetzt als Koordinationsschicht ueber `SessionStore`
  operational und entlastet den API-Pfad
- eine erste H.1-Validierungs- und Migrationskante fuer Checkpoints ist jetzt
  operational
- der automatische `checkpoint_migrator` traegt jetzt auch erste
  Mehrschritt-Ketten bis `phase_h1_v1`
- eine erste Quarantaene- und Audit-Schicht fuer defekte Sessions ist jetzt
  ebenfalls operational

Arbeitsregel fuer den naechsten Ausbau:

- `Phase H.1` ist jetzt code-started und testgruen
- zuerst support-aware Blockgenerierung vertiefen statt neue reine
  Infrastrukturlagen vorzuziehen
- dann `ModeAdaptationState` robuster ueber Sequenzen, Resume und Randfaelle pruefen
- danach punktuelle Repair-/Admin-Pfade und Audit-Kopplung weiter haerten
- dann Persistenzfelder fuer offene Uebergaenge und Budgetgrenzen stabil halten
- dann End-to-End-Blocksimulationen verbreitern
- danach Signalabdeckung und Randfaelle verbreitern
- erst spaeter `history-aware mode adaptation`

Programmgrundlage:

- [live-mode-adaptation-program.md](/Users/jonasweiss/MathTeach/docs/live-mode-adaptation-program.md)
- [live-mode-adaptation-specification.md](/Users/jonasweiss/MathTeach/docs/live-mode-adaptation-specification.md)

## Technische Zwischenziele

### 1. Support Signal Profile

Braucht spaeter mindestens:

- cognitive signals
- support-family signals
- motivation signals
- emotional safety signals
- context signals
- domain-specific signals

### 2. Response Settings

Braucht spaeter mindestens:

- pacing
- step_size
- notation_density
- text_load
- visualization
- error_handling
- language_support
- self_check_rhythm
- external_scaffolds

### 3. Evidence Traceability

Jede spaetere Regel soll rueckfuehrbar bleiben auf:

- Matrix-Dokument
- Quellenanker
- spaetere Testfaelle

## Unmittelbar Naechste Aufgaben

1. `support_moves` je Modus und Support-Profil noch topic-sensitiver machen
2. `support_scaffolds` jetzt weiter an Blocktyp und Runtime-Signal verfeinern
3. Roundtrip-Serialisierung fuer `ModeAdaptationCheckpoint` weiter haerten
4. Planner-Semantik fuer echte Sitzungsfortsetzung dokumentieren und haerten
5. Persistenz von `pending_transition_message` und Budgetzustand extern absichern
6. Signalabdeckung spaeter weiter verbreitern und kalibrieren
7. `conflict_resolver` fuer gemischte Profile weiter ausbauen
8. Triad-Szenarien und Prioritaetsleitern weiter verbreitern
9. Moduswahl spaeter mit Lernerhistorie koppeln
10. Wechselregeln spaeter gegen weiteres `mode thrashing` absichern

Naechster direkter Coding-Start:

- H.2f die neuen H.2e-Adaptationen noch feiner an Evidenz und Lesson
  Mode koppeln, statt sie nur auf Support-Gruppen zu gruenden
- weitere Triad-Gruppen und besondere Vierer-Konstellationen nur dann
  ergaenzen, wenn echte Konfliktmuster im Pilot oder in Tests sichtbar
  werden
- Scaffold-Auswahl weiter dynamisch nach konkurrierenden Signalen
  staffeln, passend zu den jetzt reicheren `support_moves`
- spaeter History- und Storage-Schicht fuer echte Sitzungsfortsetzung
  vorbereiten

## Nicht-Ziele Des Naechsten Sprints

- noch keine Vollabdeckung aller Support-Familien
- noch keine gemischten Profile als Hauptpfad
- noch keine vollstaendige UI-Neugestaltung
- noch keine klinisch anmutenden Frageboegen
- noch keine Live-Wechsel nach jedem Einzelschritt
