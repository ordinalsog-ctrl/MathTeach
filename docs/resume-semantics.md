# Resume Semantics

Stand: 2026-04-04

## Ziel

Diese Notiz zieht die operative Grenze zwischen reinem UI-Fortsetzen und
echter Lernfortsetzung.

Ein Resume in MathTeach bedeutet nicht nur:

- ein Checkpoint wurde gefunden

Sondern:

- der relevante Runtime-State wird wiederhergestellt
- offene Uebergangslogik bleibt nachvollziehbar
- getragene Beobachtungsevidenz kann den naechsten Block weiter
  beeinflussen

## Uebertragene Felder

| Feld | Kategorie | Regel beim Resume |
| --- | --- | --- |
| `current_mode` | Lernadaptation | wird direkt uebernommen |
| `blocks_in_current_mode` | Lernadaptation | wird fortgesetzt |
| `mode_changes_in_session` | Lernadaptation | wird fortgesetzt |
| `last_change_reason` | Lernadaptation | bleibt erhalten, wenn vorhanden |
| `cooldown_blocks_remaining` | Lernadaptation | wird fortgesetzt; fehlend = `0` |
| `pending_transition_message` | UI plus Lernfuehrung | wird in der ersten Resume-Vorschau angezeigt und danach konsumiert |
| `last_observation_evidence` | Lernadaptation | kann in die erste Blockvorschau uebernommen werden; fehlend = `[]` |

## Resume-Quellen

`TeachingPlan.resume_context.resume_source` unterscheidet jetzt:

- `fresh_start`
- `inline_state`
- `inline_checkpoint`
- `stored_checkpoint`

Das macht im API-Output sichtbar, ob ein Plan wirklich fortgesetzt wurde
oder nur frisch startet.

## Resume-Context im API-Output

`TeachingPlan.resume_context` dokumentiert:

- ob Resume aktiv war
- welche Evidenz getragen wurde
- ob diese Evidenz fuer die erste Blockplanung genutzt wurde
- ob eine `pending_transition_message` getragen und konsumiert wurde

## Default- und Backfill-Regeln

Aktuelle H.1-/H.2b-Regel:

- fehlende optionale State-Felder werden ueber Modell-Defaults
  backfilled
- fehlendes `cooldown_blocks_remaining` wird zu `0`
- fehlende `pending_transition_message` wird zu `None`
- fehlende `last_observation_evidence` wird zu `[]`

Dadurch bleiben auch partielle Checkpoints resume-faehig, solange
`current_mode`, `blocks_in_current_mode` und
`mode_changes_in_session` vorhanden und valide sind.

## Operative Bedeutung

Diese Semantik ist die Grundlage fuer:

- robustere Session-Roundtrips ueber Store und API
- aussagekraeftigere Admin-Inspection in der Quarantaene
- spaetere Analytics ueber getragene Evidenz und konsumierte
  Uebergangslogik
- spaetere Conflict-Resolver, die Resume-Kontext bewusst mitnutzen
