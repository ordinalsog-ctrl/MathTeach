# Checkpoint Migrator

## Zweck

Dieses Dokument beschreibt die erste echte Migrationslogik fuer
`mode_adaptation_checkpoint`.

Der aktuelle Fokus liegt auf einem klaren, kleinen H.1-Pfad:

- bekannte Altversion erkennen
- auf die aktuelle Checkpoint-Version heben
- den migrierten Checkpoint direkt wieder im `SessionStore` kanonisieren

## Aktueller Migrationspfad

Der aktuelle Migrator unterstuetzt:

- `phase_h0_v1 -> phase_h1_v1`

Die Migration ist absichtlich konservativ:

- Kernzaehler und aktueller Modus bleiben erhalten
- spaeter hinzugekommene H.1-Felder werden ueber die aktuellen
  Modell-Defaults normalisiert
- der Checkpoint wird anschliessend als `phase_h1_v1` gespeichert

## Designprinzipien

- idempotent fuer bereits aktuelle Checkpoints
- isoliert von API und Store implementiert
- auditierbar ueber klaren Versionssprung
- klein genug, um spaetere Mehrschritt-Migrationen sauber anzubauen

## Laufzeitverhalten

### Gespeicherter Checkpoint

1. `SessionManager` laedt den Checkpoint
2. `checkpoint_validation` erkennt Migrationsbedarf
3. `CheckpointMigrator` hebt den Checkpoint auf die aktuelle Version
4. der migrierte Checkpoint wird sofort wieder in den Store geschrieben
5. der Planner arbeitet nur noch mit der aktuellen Version

### Inline-Checkpoint

1. `SessionManager` validiert den direkt uebergebenen Checkpoint
2. bei bekanntem Altformat wird er vor dem Planner-Aufruf migriert
3. der Planner sieht nur noch den aktuellen Checkpoint

## Naechster Ausbau

Der aktuelle Stand ist bewusst nur die erste sichere Stufe.
Der naechste logische Ausbau ist:

1. mehr als ein Migrationsschritt
2. Quarantaene fuer nicht reparierbare Session-Dateien
3. Audit-Trail fuer Migrationen und Fehler
4. spaetere Kopplung an History- und Analytics-Schichten
