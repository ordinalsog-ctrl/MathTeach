# Session Quarantine And Audit

## Zweck

Dieses Dokument beschreibt die erste Betriebs-Haertung nach
`checkpoint_validation` und `checkpoint_migrator`.

Ziel ist:

- defekte Sessions aus dem aktiven Store zu entfernen
- Migrationen und Resume-Fehler nachvollziehbar zu protokollieren
- Wiederholungsfehler beim Resume zu vermeiden

## Aktueller Stand

Jetzt bereits live:

- `SessionQuarantine` verschiebt defekte Checkpoint-Dateien aus dem aktiven
  Store in einen separaten Quarantaene-Bereich
- fuer jede Quarantaene wird eine Metadatei mit Grund und Ursprungspfad
  geschrieben
- `SessionAuditLogger` schreibt JSONL-Ereignisse fuer:
  - erfolgreiche Checkpoint-Migration
  - invalide Sessions
  - fehlgeschlagene Migrationen
  - manuelle Restore- und Discard-Aktionen
- der API-Pfad bietet jetzt erste Admin-Endpunkte fuer:
  - `list`
  - `inspect`
  - `restore`
  - `discard`

## Laufzeitverhalten

### Invalider gespeicherter Checkpoint

1. `SessionManager` versucht Resume
2. Laden oder Validieren scheitert
3. die Checkpoint-Datei wird in Quarantaene verschoben
4. ein Audit-Eintrag wird geschrieben
5. der aktuelle Request erhaelt weiter einen Fehler
6. ein spaeterer Resume-Versuch mit derselben `session_id` startet sauber neu

### Fehlgeschlagene Migration

1. `SessionManager` erkennt Migrationsbedarf
2. `CheckpointMigrator` kann den Pfad nicht sicher ausfuehren
3. die betroffene Datei wird in Quarantaene verschoben
4. ein Audit-Eintrag mit Versionshinweis wird geschrieben
5. der aktuelle Request bleibt ein expliziter Fehlerfall

### Manuelle Wiederherstellung

1. Admin listet oder inspiziert quarantainierte Sessions
2. die quarantainierte Datei kann read-only geprueft und extern repariert werden
3. `restore` validiert oder migriert die Datei erneut
4. nur gueltige aktuelle Checkpoints werden in den aktiven Store
   zurueckgeschrieben
5. ein spaeterer Resume-Request arbeitet wieder mit dem aktiven Store

### Spaeterer Clean Start

1. eine defekte Session wird beim ersten Resume quarantainiert
2. dieselbe `session_id` hat danach keinen aktiven Checkpoint mehr
3. ein spaeterer Request mit derselben `session_id` startet sauber neu

## Nicht Ziel Dieser Stufe

- noch keine automatische Reparatur defekter Sessions
- noch kein ausgebautes Rollen- oder Rechtekonzept fuer Admin-Pfade
- noch kein vollstaendiger Audit-Export
- noch keine mehrstufige Quarantaene-Policy

## Naechster Ausbau

1. sichtbare Admin-Pfade spaeter mit Repair-Workflow oder Rollenmodell haerten
2. Audit-Trail spaeter mit Session-History koppeln
3. Mehrschritt-Migrationen spaeter ebenfalls auditierbar machen
4. Reparatur- oder Reimport-Hooks fuer manuell gepruefte Sessions erweitern
