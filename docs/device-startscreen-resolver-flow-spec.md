# Device Startscreen Resolver Flow Spec

## Zweck

Dieses Dokument beschreibt den reinen Ablauf des spaeteren
Startscreen-Resolvers.

Es verbindet:

- [device-startscreen-state-mapping-spec.md](/Users/jonasweiss/MathTeach/docs/device-startscreen-state-mapping-spec.md)
- [device-startscreen-resolver-implementation-spec.md](/Users/jonasweiss/MathTeach/docs/device-startscreen-resolver-implementation-spec.md)
- [device-startscreen-runtime-field-spec.md](/Users/jonasweiss/MathTeach/docs/device-startscreen-runtime-field-spec.md)

Es beantwortet nur:

`In welcher Reihenfolge liest, prueft und verarbeitet der Resolver seine
Eingaben, bevor genau ein Startscreen-Zustand entsteht?`

Es ist absichtlich:

- kein UI-Code
- kein API-Code
- kein Layoutplan

## Hauptregel

Der Flow dient nur dazu, aus echten Laufzeitdaten einen einzelnen
Startscreen-Zustand abzuleiten.

Er darf nicht:

- Zustandslogik und Slot-Bau vermischen
- mehrere moegliche Zustandszweige parallel offenlassen
- spaeteres Rendern vorwegnehmen

## Resolver-Flow in einem Satz

Der Startscreen-Resolver arbeitet immer in genau vier Stufen:

1. Input sammeln
2. Input normalisieren
3. Zustand entscheiden
4. Slots fuer genau diesen Zustand bauen

## Vollstaendiger Ablauf

## Phase 1: Input sammeln

Der Resolver liest nur das definierte Feldbudget aus:

- lokalem Device-State
- letztem Plan, falls vorhanden

Minimal heute:

- `profile.learnerName`
- `sessionId`
- `lastPlan`
- `lastUpdatedAt`
- `lastPlan.resume_context.resume_active`
- `lastPlan.resume_context.resume_source`
- `lastPlan.planned_blocks[0].goal`
- `lastPlan.planned_blocks[0].transition_message`

### Ausgabe dieser Phase

Ein rohes Input-Objekt ohne Interpretation.

## Phase 2: Input normalisieren

Die Eingabedaten werden in kleine resolver-interne Hilfswerte
ueberfuehrt.

Minimal:

- `has_name`
- `has_last_plan`
- `has_resume_context`
- `resume_active`
- `resume_source`
- `has_first_block`
- `has_resume_goal`
- `has_resume_transition_message`
- `has_explicit_unsafe_signal`

### Wichtige Normalisierungsregeln

- fehlendes `lastPlan` ergibt nie Fehler, sondern nur `has_last_plan =
  false`
- fehlendes `resume_context` wird defensiv als nicht resume-faehig
  behandelt
- fehlende Blockdaten werden defensiv als nicht resume-faehig behandelt
- `sessionId` und `lastUpdatedAt` bleiben Kontext, keine
  Zustandsbeweise

### Ausgabe dieser Phase

Ein kleines normalisiertes Resolver-Objekt mit Bool- und Kernwerten.

## Phase 3: Zustand entscheiden

Die Zustandsentscheidung laeuft strikt in genau dieser Reihenfolge:

1. `unsafe_history` pruefen
2. `resume` pruefen
3. sonst `no_history`

## Schritt 3A: Unsafe pruefen

Frage:

`Liegt ein explizites Unsafe-Signal vor?`

Heute ist diese Pruefung strukturell vorhanden, wird aber in der ersten
Version meist `false` liefern.

Wenn `true`:

- Resolver gibt sofort `state_kind = unsafe_history` aus
- kein weiterer Resume-Check

Wenn `false`:

- weiter zu Resume-Pruefung

## Schritt 3B: Resume pruefen

Frage:

`Ist ein stabiler Resume-Wiedereinstieg fachlich belegbar?`

Das ist heute der Fall, wenn mindestens die starke oder die schwache
Resume-Bedingung erfuellt ist.

### Starke Resume-Bedingung

- `has_last_plan == true`
- `resume_active == true`

### Schwache, aber zulaessige Fallback-Bedingung

- `has_last_plan == true`
- `has_first_block == true`
- `has_resume_goal == true`

Wenn eine dieser Bedingungen greift:

- Resolver gibt `state_kind = resume` aus

Wenn keine greift:

- weiter zu `no_history`

## Schritt 3C: No-History

Wenn weder `unsafe_history` noch `resume` sauber belegt sind, gibt der
Resolver immer aus:

- `state_kind = no_history`

Das ist kein Fehlerzustand, sondern der definierte sichere Default.

### Ausgabe dieser Phase

Genau ein Zustand:

- `unsafe_history`
  oder
- `resume`
  oder
- `no_history`

## Phase 4: Slots bauen

Erst nachdem `state_kind` feststeht, wird genau ein Builder aufgerufen.

Beispielhafte Form:

```text
if state_kind == "unsafe_history":
    slots = buildUnsafeHistorySlots(normalized_input)
elif state_kind == "resume":
    slots = buildResumeSlots(normalized_input)
else:
    slots = buildNoHistorySlots(normalized_input)
```

## Builder-Disziplin

Jeder Builder darf nur seinen eigenen Wire-Contract bedienen.

Nicht erlaubt:

- `resume`-Titel im `no_history`-Builder
- Sicherheits-/Recovery-Sprache im `resume`-Builder
- Fallback auf generische Mischtexte

## Phase 5: Render-Input zurueckgeben

Der Resolver gibt erst ganz am Ende ein kleines Render-Input-Objekt
zurueck:

```text
{
  state_kind,
  slots,
}
```

Dieses Objekt darf danach von der UI verwendet werden, aber nicht mehr
nachtraeglich in einen anderen Zustand umgebogen werden.

## Harte Abbruch- und Fallback-Regeln

## 1. Keine Ausnahme wegen leerer History

Fehlende oder leere History ist normal.

Der Flow faellt in diesem Fall sauber auf `no_history`.

## 2. Keine Unsafe-Interpretation aus Frontend-Fehlern

Ein fehlgeschlagener Request oder ein spaeter Netzwerkfehler darf den
Startscreen-Resolver nicht rueckwirkend in `unsafe_history` kippen.

## 3. Kein implizites Upgrade zu Resume

Unklare oder partielle Daten duerfen nicht als Resume aufgewertet
werden.

## 4. Kein nachtraegliches State-Mischen

Wenn `state_kind` entschieden ist, bleiben alle anderen Startscreen-
Zweige fuer diesen Renderlauf geschlossen.

## Minimaler Pseudoflow

```text
input = collectStartscreenInput()
normalized = normalizeStartscreenInput(input)

if normalized.has_explicit_unsafe_signal:
    state_kind = "unsafe_history"
elif normalized.resume_active or (
    normalized.has_last_plan and
    normalized.has_first_block and
    normalized.has_resume_goal
):
    state_kind = "resume"
else:
    state_kind = "no_history"

slots = buildSlotsForState(state_kind, normalized)

return {
  state_kind,
  slots,
}
```

## Beziehung zur spaeteren UI

Dieser Flow ist bewusst kleiner als eine eigentliche UI-Implementierung.

Er sorgt nur dafuer, dass spaeter:

- der richtige Startscreen-Zustand gewaehlt wird
- die UI nicht aus losem Textzusammenbau entsteht
- jeder spaetere Screen auf einem klaren Runtime-Zustand steht

## Aktueller UI-Zwischenstand

Mit dieser Flow-Spec ist die Startscreen-Kette jetzt fast vollstaendig:

- Evidenzmatrix
- Contract
- Blueprint
- Wire-Contracts
- State-Mapping
- Resolver-Implementierungs-Spec
- Runtime-Field-Spec
- Resolver-Flow-Spec

Noch nicht getan:

- kein UI-Code fuer den Resolver
- keine neue sichtbare Startscreen-Oberflaeche
- keine neuen Runtime-Felder fuer `unsafe_history`

## Folgeschritt

Der naechste saubere Schritt ist jetzt ein kleiner
Startscreen-Resolver-Change-Plan fuer
[device.js](/Users/jonasweiss/MathTeach/src/mathteach/ui/static/device.js):

- welche bestehende Hilfslogik ersetzt wird
- welche neuen kleinen Funktionen entstehen
- welche Renderfunktion kuenftig nur noch `state_kind + slots` liest
