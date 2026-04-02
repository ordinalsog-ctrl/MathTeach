# Live Mode Adaptation Readiness Review

## Zweck

Dieses Dokument zieht die juengste Review-Lage zu Phase `H` zusammen.

Es beantwortet drei Fragen:

- Was an Phase `H` gilt jetzt als stark und bestaetigt
- Welche Restluecken bleiben vor der ersten Runtime-Implementierung
- Welche konkreten Entscheidungen werden deshalb vor dem Coding festgezogen

## Bestaetigter Stand

Die Reviews bestaetigen Phase `H` in ihrer aktuellen Form als:

- architektonisch sauber getrennt von Phase `G`
- auf Block-Ebene praktikabel geschnitten
- support-sensitiv statt nur modussensitiv
- paedagogisch vorsichtig durch `hysteresis` und `transition messaging`

Besonders bestaetigt wurden:

- `mode_selector` bleibt fuer die Startentscheidung zustaendig
- `runtime_mode_adapter` soll die Laufzeitanpassung tragen
- `ObservationSignal` ist als eigenes Datenobjekt sinnvoll
- ruhige Template-Uebergaenge sind fuer die erste Version besser als freie Generierung

## Restluecken Vor Der Ersten Runtime-Umsetzung

Trotz des starken Stands bleiben fuer den Schritt von Spezifikation zu Code
noch vier operative Fragen wichtig:

1. Wie sieht die API zwischen `planner`, `mode_selector` und
   `runtime_mode_adapter` genau aus
2. Wo findet die support-sensitive Interpretation roher Beobachtungen statt
3. Welche MVP-Schwellen gelten in `H.1` konkret
4. Wie wird ein Moduswechsel in den bestehenden Planner-Flow eingezogen

## Beschlossene Schaerfungen

Fuer die erste Implementierungsrunde gelten deshalb diese Entscheidungen:

### 1. Neue Runtime-Komponente

Die Phase-H-Logik lebt in:

- `src/mathteach/services/runtime_mode_adapter.py`

### 2. Signalinterpretation Als Eigener Schritt

Rohbeobachtungen werden vor der Adaptionsentscheidung support-sensitiv
interpretiert.

Die Zielidee ist:

- rohe Evidenz sammeln
- mit Profilkontext gewichten
- erst dann `ObservationSignal` fuer die Entscheidungslogik erzeugen

### 3. MVP-Kalibrierung Fuer H.1

Die erste Code-Runde arbeitet mit festen Startwerten:

- `observation_window_blocks = 2`
- `minimum_signal_strength_for_shift = meaningful`
- `min_blocks_in_mode = 2`
- `cooldown_blocks_after_change = 1`
- `max_mode_changes_per_session = 3`

Diese Werte gelten als Startkalibrierung, nicht als Endoptimierung.

### 4. Planner-Integration

Der Planner bleibt der Orchestrator.

Die Folge ist:

1. Phase `G` liefert den Startmodus
2. der Planner erzeugt einen Block im aktuellen Modus
3. Rohbeobachtungen werden gesammelt
4. `runtime_mode_adapter` entscheidet am Blockende ueber `stay` oder `shift`
5. bei Wechsel wird zuerst eine ruhige Uebergangsmeldung erzeugt
6. der naechste Block wird dann im neuen Modus geplant

## Unmittelbar Naechste Artefakte

Die naechste Coding-Session sollte direkt auf diese Artefakte zielen:

- `src/mathteach/services/runtime_mode_adapter.py`
- neue Adaptionsmodelle in `src/mathteach/models.py`
- erste Tests fuer Beobachtung, Hysterese und Moduswechsel

## Fazit

Phase `H` gilt damit auf Spezifikationsniveau als
`implementation-ready-for-H.1`.

Offen bleiben:

- spaetere Feinkalibrierung mit realen Nutzungsdaten
- tiefere support-spezifische Gewichtung
- history-aware Mehrsitzungsanpassung in spaeteren Phasen
