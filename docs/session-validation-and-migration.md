# Session Validation And Migration

## Zweck

Dieses Dokument beschreibt die erste echte Haertung zwischen
`SessionStore`, `SessionManager` und dem versionierten
`mode_adaptation_checkpoint`.

Ziel ist die klare Unterscheidung zwischen:

- unbekannter Session
- ungueltigem oder korruptem Checkpoint
- bekanntem, aber veraltetem Checkpoint mit Migrationsbedarf

## Aktuelle Regeln

### Unknown Session

- `session_id` ist gesetzt
- im `SessionStore` existiert kein Checkpoint
- Ergebnis: sauberer Neustart, kein Fehler

### Invalid Session

- gespeicherter Checkpoint ist korrupt oder semantisch ungueltig
- Beispiele:
  - unbekannte `schema_version`
  - nicht lesbarer Checkpoint
  - H.1-Zustand verletzt Budget- oder Cooldown-Grenzen
- Ergebnis: `400` ueber API

### Migration Required

- `schema_version` ist bekannt, aber nicht mehr aktuell
- wenn ein automatischer Migrationspfad existiert, wird der Checkpoint
  vor Resume auf die aktuelle Version gehoben
- wenn kein automatischer Migrationspfad existiert, bleibt das Ergebnis
  `410` ueber API

### Resume Conflict

- `session_id` und inline Resume-Daten werden gleichzeitig gesendet
- Ergebnis: `422` ueber API

## Aktuelle H.1-Versionierung

```python
CURRENT_MODE_ADAPTATION_CHECKPOINT_VERSION = "phase_h1_v1"
MIGRATABLE_MODE_ADAPTATION_CHECKPOINT_VERSIONS = {"phase_h0_v1"}
KNOWN_MODE_ADAPTATION_CHECKPOINT_VERSIONS = {
    "phase_h0_v1",
    "phase_h1_v1",
}
```

## H.1-State-Guardrails

Der aktuelle H.1-Validator sichert mindestens:

- `schema_version` ist bekannt
- nur die aktuelle Version darf ohne Migration fortgesetzt werden
- `mode_changes_in_session` ueberschreitet nicht das H.1-Wechselbudget
- `cooldown_blocks_remaining` ueberschreitet nicht die H.1-Cooldown-Grenze

## API-Semantik

Aktuelle Fehlerabbildung:

- `422`: Resume-Konflikt
- `400`: invalid session / invalid checkpoint
- `410`: bekannte, aber nicht automatisch migrierbare Session

## Aktueller Migrationsstand

Jetzt bereits live:

- `phase_h0_v1 -> phase_h1_v1`
- gespeicherte Alt-Checkpoints werden beim Resume automatisch migriert und
  direkt wieder als aktuelle Version gespeichert
- inline Alt-Checkpoints werden vor dem Planner-Aufruf normalisiert

## Naechster Ausbau

Die aktuelle Haertung ist jetzt die erste echte Migration-Engine.
Der naechste logische Schritt ist:

1. mehr als ein Migrationsschritt
2. spaetere Quarantaene fuer ungueltige Session-Dateien
3. Audit-Trail fuer Migrations- und Validierungsfehler
4. spaetere History-Schicht auf Basis nur validierter Checkpoints
