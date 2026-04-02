# MathTeach Journal

Stand: 2026-04-02

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
