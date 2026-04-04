# Checkpoint Migrator

## Zweck

Dieses Dokument beschreibt die operative Migrationslogik fuer
`mode_adaptation_checkpoint`.

Der aktuelle Fokus liegt auf einem klaren, kleinen H.1-Pfad mit echter
Kettenfaehigkeit:

- bekannte Altversion erkennen
- bei Bedarf ueber mehrere bekannte Zwischenversionen heben
- den migrierten Checkpoint direkt wieder im `SessionStore` kanonisieren

## Aktueller Migrationspfad

Der aktuelle Migrator unterstuetzt:

- `phase_h0_v0 -> phase_h0_v1`
- `phase_h0_v1 -> phase_h1_v1`
- `phase_h0_v0 -> phase_h1_v1` als iterative Kette

Die Migration bleibt absichtlich konservativ:

- Kernzaehler und aktueller Modus bleiben erhalten
- sehr fruehe Legacy-Staende werden erst auf einen stabileren
  Zwischenstand gehoben und dann weiter nach H.1
- spaeter hinzugekommene H.1-Felder werden ueber die aktuellen
  Modell-Defaults oder bewusste Legacy-Defaults normalisiert
- der Checkpoint wird anschliessend als `phase_h1_v1` gespeichert

## Designprinzipien

- idempotent fuer bereits aktuelle Checkpoints
- isoliert von API und Store implementiert
- auditierbar ueber klaren Versionssprung oder Migrationskette
- jeder Migrationsschritt bleibt explizit sichtbar
- klein genug, um spaetere H.2+-Schritte sauber anzubauen

## Laufzeitverhalten

### Gespeicherter Checkpoint

1. `SessionManager` laedt den Checkpoint
2. `checkpoint_validation` erkennt Migrationsbedarf
3. `CheckpointMigrator` laeuft die bekannte Migrationskette bis zur
   aktuellen Version durch
4. der migrierte Checkpoint wird sofort wieder in den Store geschrieben
5. der Audit-Trail schreibt je nach Fall `checkpoint_migrated` oder
   `checkpoint_migration_chain`
6. der Planner arbeitet nur noch mit der aktuellen Version

### Inline-Checkpoint

1. `SessionManager` validiert den direkt uebergebenen Checkpoint
2. bei bekanntem Altformat wird er vor dem Planner-Aufruf ueber alle
   bekannten Zwischenschritte migriert
3. der Planner sieht nur noch den aktuellen Checkpoint

## Naechster Ausbau

Der aktuelle Stand ist jetzt die erste sichere Kettenmigration.
Der naechste logische Ausbau ist:

1. echte H.2+-Schemaaenderungen auf dieselbe Kettenlogik setzen
2. sichtbarer Reparaturpfad fuer quarantainierte Sessions weiter haerten
3. Audit-Trail fuer Migrationen und Fehler spaeter mit History koppeln
4. spaetere Kopplung an History- und Analytics-Schichten
