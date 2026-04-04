# Session Storage Architecture

## Zweck

Dieses Dokument beschreibt den naechsten Ausbau nach dem
`mode_adaptation_checkpoint`-Vertrag:

- Persistenz des Runtime-Zustands ueber echte Session-Grenzen
- spaetere Wiederaufnahme nach App- oder Prozess-Neustart
- vorbereitete Basis fuer `history-aware mode adaptation`

## Zielbild

Der Flow soll mittelfristig so aussehen:

1. Client startet oder setzt Session fort
2. API laedt vorhandenen Checkpoint ueber `session_id`
3. Planner verarbeitet neue Runtime-Beobachtungen
4. API liefert neuen `TeachingPlan` plus aktualisierten Checkpoint
5. `SessionStore` speichert den neuen Checkpoint wieder ab

## Kernkomponenten

### SessionStore

Verantwortung:

- Checkpoint anhand einer `session_id` speichern
- Checkpoint anhand einer `session_id` laden
- spaeter Versionierung und Migration vorbereiten

MVP-Schnittstelle:

```python
class SessionStore:
    def save_checkpoint(
        self,
        session_id: str,
        checkpoint: ModeAdaptationCheckpoint,
    ) -> None:
        ...

    def load_checkpoint(
        self,
        session_id: str,
    ) -> ModeAdaptationCheckpoint | None:
        ...
```

### SessionManager

Verantwortung:

- Resume-Pfad koordinieren
- API-Eingabe, Checkpoint und Planner verbinden
- Konflikte zwischen direktem Checkpoint und serverseitiger Session aufloesen

MVP-Regeln:

- explizit uebergebener Checkpoint hat Vorrang vor leerer Session
- doppelte, widerspruechliche Resume-Quellen werden explizit abgewiesen
- `schema_version` bleibt beim Speichern und Laden erhalten

## API-Ausbau

### Kurzfristig

Bestehender Pfad:

- `POST /api/v1/tutoring/plan`

Weiterhin akzeptiert:

- `mode_adaptation_state`
- `mode_adaptation_checkpoint`

### Naechste Stufe

Zusatzfelder:

- optionale `session_id`

Beispiel:

```json
{
  "session_id": "sess_mathteach_0001",
  "objective": "Erklaere mir die quadratische Gleichung anschaulich.",
  "learner_profile": { "...": "..." },
  "runtime_observations": [
    {"evidence": ["repeated_concept_error"]}
  ]
}
```

Antwort:

```json
{
  "session_id": "sess_mathteach_0001",
  "mode_adaptation_checkpoint": {
    "schema_version": "phase_h1_v1",
    "mode_adaptation_state": { "...": "..." }
  }
}
```

## MVP-Speicherstrategie

Fuer den ersten Persistenzschritt reicht:

- lokale JSON- oder SQLite-basierte Ablage
- ein Datensatz pro `session_id`
- noch keine komplexe Historienanalyse

Nicht Ziel der ersten Storage-Stufe:

- Multi-User-Rechteverwaltung
- verteilte Synchronisierung
- Konfliktauflosung zwischen mehreren gleichzeitigen Clients

## Validierung

Die erste Storage-Stufe sollte mindestens testen:

1. Checkpoint speichern und identisch wieder laden
2. Resume ueber `session_id` ohne Datenverlust
3. `pending_transition_message` bleibt ueber Neustart erhalten
4. Cooldown und Change-Budget bleiben ueber Neustart erhalten
5. unbekannte `session_id` fuehrt zu sauberem Neustart statt inkonsistentem Zustand

## Aktueller Stand

Jetzt bereits umgesetzt:

1. [src/mathteach/services/session_store.py](/Users/jonasweiss/MathTeach/src/mathteach/services/session_store.py)
2. file-backed MVP-Implementierung
3. API-Test fuer `session_id`-Resume

## Naechster Coding-Schritt

Der naechste direkte Ausbau auf Basis dieses Dokuments ist:

1. `src/mathteach/services/session_manager.py`
2. saubere Trennung zwischen API-Huelle und Resume-Koordination
3. Konfliktregeln zwischen unbekannter Session, vorhandenem Checkpoint und
   spaeteren Versionen
4. spaeter Storage-Haertung und History-Anbindung
