# Live Mode Adaptation Persistence Review 2026-04-02

## Einordnung

Die neue Review-Lage bestaetigt einen qualitativen Zustandswechsel:

- `Phase H.1` ist nicht mehr nur `implementation-ready`
- `Phase H.1` ist jetzt als erste echte Runtime-Stufe live im Code
- der Hauptengpass verschiebt sich damit von Architektur und Grundintegration
  zu `Persistence`, `Resume-Semantik` und spaeterer externer
  Session-Fortsetzung

## Bestaetigter Stand

Die Reviews bestaetigen die aktuelle Runtime-Schichtung ausdruecklich:

1. `RawBlockObservation`
2. `SignalInterpreter`
3. `ObservationSignal`
4. `RuntimeModeAdapter`
5. `ModeAdaptationState`
6. `Planner-Block-Loop`
7. API-Ausgabe von `planned_blocks`, `mode_adaptation_trace` und
   `mode_adaptation_state`

Zusammen mit der juengsten Signalverdichtung ist damit jetzt real vorhanden:

- support-sensitive Signalinterpretation
- blockweise `stay/shift`-Entscheidung
- Hysterese, Cooldown und Change-Budget
- Transition-Messaging
- Resume-Pfade
- Mehrblock-Signale
- sichtbare kleine Erfolgs- und Stagnationslinien

## Hauptluecke

Der naechste systemische Engpass ist jetzt nicht mehr:

- `Mode Selection`
- `Conflict Resolution`
- `Triads`
- `erste Runtime-Integration`

Sondern:

- robuste externe `Persistence-Schnittstelle`
- saubere `Resume-Semantik` ueber API-Grenzen hinweg
- verlustfreie Serialisierung von `ModeAdaptationState`
- spaetere Storage- und History-Anbindung

## Konkrete Naechste Arbeitspakete

### 1. Serialization And Validation

`ModeAdaptationState` und angrenzende Runtime-Objekte sollen explizit gegen
Roundtrip-Verlust abgesichert werden:

- serialisieren
- deserialisieren
- gleiche Semantik behalten
- ungueltige oder veraltete Payloads sauber erkennen

### 2. Resume API Contract

Die API soll klarer festziehen:

- welcher Runtime-State von aussen uebergeben werden darf
- welche Felder Pflicht-, welche Kompatibilitaetsfelder sind
- wie Resume mit `pending_transition_message`, Cooldown und
  Change-Budget funktioniert

### 3. Planner Resume Semantics

Der Planner soll nicht nur simulieren, sondern eindeutig dokumentieren:

- wann ein bestehender Zustand uebernommen wird
- wie `blocks_in_current_mode` fortgeschrieben wird
- wie `last_observation_evidence` ueber API-Resume weiterlebt
- wie ein Resume ohne neue Beobachtung gegenueber einem Resume mit neuer
  Block-Evidenz behandelt wird

### 4. Storage Handoff

Noch nicht als Vollimplementierung, aber als naechste Anschlussstelle:

- welches Objekt spaeter gespeichert wird
- welche Versionierung noetig ist
- wie Session-IDs und Runtime-State zueinander stehen

## Risiko-Liste Fuer Den Naechsten Ausbau

- verlorene `pending_transition_message` beim Resume
- Reset von Change-Budget oder Cooldown trotz laufender Session
- Resume-Payloads mit unvollstaendigem oder altem Runtime-State
- inkonsistente Behandlung von `last_observation_evidence`
- implizite statt explizite API-Semantik fuer Sitzungsfortsetzung

## Empfehlung

Der naechste direkte Schritt sollte kein weiterer Review-Thread und auch
keine neue Adaptionsheuristik sein, sondern:

1. Serialisierungs- und Resume-Tests
2. API-Vertrag fuer `mode_adaptation_state` schaerfen
3. Planner-Semantik fuer echte Sitzungsfortsetzung dokumentieren und haerten
4. danach erste Storage-/History-Schnittstelle vorbereiten

## Fazit

`Phase H.1` ist jetzt als MVP-Runtime real genug, dass die richtige
Weiterentwicklung nicht mehr im `Was adaptieren wir?`, sondern im
`Wie ueberlebt dieser Zustand echte Sitzungen?` liegt.
