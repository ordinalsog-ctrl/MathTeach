# Mode Adaptation Checkpoint Contract

## Zweck

Dieses Dokument definiert die erste externe Persistenzform fuer den
blockweisen Runtime-Zustand von `Phase H.1`.

Der Checkpoint ist die bevorzugte Form, um einen laufenden
`mode_adaptation_state` ueber API-Grenzen, Session-Resumes und spaetere
Storage-Schichten hinweg zu tragen.

## Modell

Der Checkpoint liegt als versioniertes Objekt vor:

```json
{
  "schema_version": "phase_h1_v1",
  "mode_adaptation_state": {
    "current_mode": "worked_example_tutoring",
    "blocks_in_current_mode": 2,
    "mode_changes_in_session": 1,
    "last_change_reason": "breakthrough_signal",
    "cooldown_blocks_remaining": 1,
    "pending_transition_message": "Wir gehen jetzt in kleineren Schritten weiter.",
    "last_observation_evidence": ["transfer_success_two_blocks"]
  }
}
```

## Request-Vertrag

`POST /api/v1/tutoring/plan` akzeptiert jetzt fuer Resume zwei Formen:

1. Legacy-kompatibel: `mode_adaptation_state`
2. Bevorzugt: `mode_adaptation_checkpoint`

Regel:

- genau eine der beiden Formen darf uebergeben werden
- werden beide uebergeben, antwortet die API mit `422`

## Response-Vertrag

Jeder `TeachingPlan` liefert jetzt:

- `mode_adaptation_state`
- `mode_adaptation_checkpoint`

Damit kann ein Client:

- direkt mit dem nackten Runtime-State weiterarbeiten
- oder den versionierten Checkpoint 1:1 persistieren und spaeter wieder
  als Resume-Payload zurueckgeben

## Semantik

Der Checkpoint beschreibt den aktuellen Runtime-Zustand nach dem letzten
simulierten oder verarbeiteten Block:

- aktueller Modus
- Blockzaehler im Modus
- Change-Budget-Stand
- Cooldown-Stand
- offene Transition-Meldung
- letzte relevante Beobachtungslinie

## H.1-Grenze

Der Checkpoint ist noch kein vollwertiger Storage-Layer.
Er ist die stabile externe Form, auf der spaeter aufgesetzt wird:

- Session-Persistenz
- Datenbank-Ablage
- History-aware Mode Adaptation
- Resume ueber Prozess- und App-Neustarts hinweg

## Naechster Ausbau

Die naechsten passenden Schritte auf Basis dieses Vertrags sind:

1. Roundtrip- und Kompatibilitaetstests erweitern
2. Resume-Semantik an API- und Planner-Grenzen weiter haerten
3. spaetere Storage-Huelle mit Session-ID und Versionierung vorbereiten
