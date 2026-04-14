# Device Startscreen Resolver Implementation Spec

## Zweck

Dieses Dokument beschreibt die kleinste spaetere Implementierung des
Startscreen-Resolvers fuer das Device.

Es ist die technische Ableitung aus:

- [device-startscreen-state-mapping-spec.md](/Users/jonasweiss/MathTeach/docs/device-startscreen-state-mapping-spec.md)
- [device-startscreen-wire-contract-resume.md](/Users/jonasweiss/MathTeach/docs/device-startscreen-wire-contract-resume.md)
- [device-startscreen-wire-contract-no-history.md](/Users/jonasweiss/MathTeach/docs/device-startscreen-wire-contract-no-history.md)
- [device-startscreen-wire-contract-unsafe-history.md](/Users/jonasweiss/MathTeach/docs/device-startscreen-wire-contract-unsafe-history.md)

Es beantwortet nur diese Frage:

`Welche kleine technische Resolver-Schicht braucht die Device-UI vor dem
Rendern des Startscreens?`

Es ist absichtlich:

- kein UI-Code
- kein Mockup
- kein CSS-Plan

## Hauptregel

Der Resolver entscheidet nur den Startscreen-Zustand.

Er gestaltet nichts.

Er darf:

- Runtime-Felder lesen
- Zustand klassifizieren
- die benoetigten sichtbaren Slots fuer genau einen Wire-Contract
  vorbereiten

Er darf nicht:

- mehrere Startscreen-Zustaende mischen
- Resume-Inhalte frei erfinden
- fehlende Runtime-Signale psychologisch "wegdesignen"

## Implementierungsort

Die spaetere minimale Implementierung gehoert in die lokale Device-Shell
in
[device.js](/Users/jonasweiss/MathTeach/src/mathteach/ui/static/device.js).

Heute rendert
[renderStartScreen() in device.js](/Users/jonasweiss/MathTeach/src/mathteach/ui/static/device.js)
direkt aus:

- `state.profile.learnerName`
- `state.lastPlan`
- `state.lastUpdatedAt`

Das reicht fuer eine erste Shell, ist aber noch kein sauberer
zustandsgebundener Resolver.

## Zielbild

Vor dem Rendern des Startscreens gibt es genau eine kleine
Resolver-Funktion.

Beispielhafte Form:

```text
resolveStartscreenState(input) -> {
  state_kind,
  slots,
}
```

Dabei ist:

- `state_kind` genau eins aus `resume`, `no_history`,
  `unsafe_history`
- `slots` die bereits vorbereiteten sichtbaren Texte fuer genau diesen
  einen Wire-Contract

## Minimaler Input

Die erste Resolver-Version darf nur Felder verwenden, die heute bereits
in der Device-Shell oder im aktuellen Plan plausibel vorhanden sind.

## Aus lokalem Device-State

- `profile.learnerName`
- `sessionId`
- `lastPlan`
- `lastUpdatedAt`

## Aus dem letzten Plan, falls vorhanden

Minimal nur das, was heute bereits fuer den Resume-Kern lesbar ist:

- erster aktiver Block
- dessen `goal`
- dessen `transition_message`, falls vorhanden

## Fuer spaeter erweiterbar

Noch nicht fuer die erste Resolver-Version verpflichtend, aber
vorgesehen:

- `resume_source`
- `resume_active`
- expliziter `resume_status`
- expliziter `resume_recovery_required`

## Output-Vertrag

Der Resolver gibt genau zwei Dinge zurueck:

## 1. `state_kind`

Zulaessige Werte:

- `resume`
- `no_history`
- `unsafe_history`

## 2. `slots`

`slots` ist kein freies Datenobjekt, sondern an die vorhandenen Wire-
Contracts gebunden.

Minimal benoetigte Slot-Familien:

### fuer `resume`

- `welcome_line`
- `resume_title`
- `resume_summary`
- `primary_cta_label`
- optional `secondary_line`

### fuer `no_history`

- `welcome_line`
- `start_core`
- `primary_cta_label`
- optional `secondary_line`
- optional `start_hint`

### fuer `unsafe_history`

- `welcome_line`
- `safe_restart_core`
- `primary_cta_label`
- optional `secondary_line`
- optional `de_escalation_hint`

## Resolver-Reihenfolge

Die Implementierung muss strikt in dieser Reihenfolge arbeiten:

1. Eingabedaten normalisieren
2. explizite Unsafe-Signale pruefen
3. stabilen Resume-Beleg pruefen
4. sonst auf `no_history` zurueckfallen
5. erst danach Slots fuer genau diesen Zustand bauen

Nicht erlaubt:

- erst Texte bauen und dann den Zustand hineininterpretieren
- einen Resume-Text bauen und spaeter doch auf `no_history` wechseln

## Schritt 1: Eingabedaten normalisieren

Vor jeder Entscheidung werden diese Hilfswerte abgeleitet:

- `has_name`
- `has_last_plan`
- `has_resume_goal`
- `has_resume_summary_source`
- `has_explicit_unsafe_signal`

Wichtig:

- `sessionId` wird gelesen, aber nicht als Resume-Beleg gewertet
- `lastUpdatedAt` wird gelesen, aber nicht als Resume-Beleg gewertet

## Schritt 2: Unsafe pruefen

Nur wenn ein explizites Unsafe-Signal vorhanden ist, darf der Resolver
`unsafe_history` ausgeben.

Heute ist das in der Device-Shell voraussichtlich noch nicht der Fall.

Darum muss die erste Resolver-Version diese Pruefung zwar strukturell
enthalten, aber realistisch oft `false` ergeben lassen.

## Schritt 3: Resume pruefen

`resume` ist nur zulaessig, wenn:

- `lastPlan` vorhanden ist
- daraus ein stabiler Resume-Titel gewonnen werden kann
- daraus ein stabiler Resume-Satz oder ein sauberer Fallback-Satz
  gewonnen werden kann

Beispiele fuer Resume-Belege:

- erster aktiver Block mit `goal`
- sinnvolle `transition_message`
- sonst konservativer Resume-Satz auf Basis des aktiven Blocks

Keine Resume-Belege sind:

- nur `sessionId`
- nur `lastUpdatedAt`
- nur ein Lernendenname

## Schritt 4: No-History als sicherer Default

Wenn weder `unsafe_history` noch `resume` sauber belegbar sind, gibt der
Resolver immer `no_history` aus.

Das ist kein Verlust, sondern die psychologisch sichere Default-
Abbildung.

## Slot-Bau pro Zustand

Die Slot-Erzeugung ist zustandsgebunden.

Es gibt also nicht eine globale Textgenerator-Funktion, sondern drei
kleine Builder.

Beispielhafte Form:

```text
buildResumeSlots(input)
buildNoHistorySlots(input)
buildUnsafeHistorySlots(input)
```

## Builder-Regeln

### Resume-Builder

Muss:

- den letzten sinnvollen Wiedereinstieg klein und konkret halten
- den Resume-Titel aus dem staerksten vorhandenen Plan-Signal gewinnen
- einen ruhigen Fortsetzungssatz bauen

Darf nicht:

- historische Meta-Infos stapeln
- mehrere Resume-Wege anbieten

### No-History-Builder

Muss:

- den ersten Schritt klein und sicher machen
- ohne Defizitton formulieren

Darf nicht:

- den fehlenden Verlauf problematisieren
- Setup- oder Profilrhetorik aufmachen

### Unsafe-History-Builder

Muss:

- den sicheren Wiedereinstieg fokussieren
- technische Ursachen unsichtbar halten

Darf nicht:

- Fehler-, Reparatur- oder Datenverlustsprache tragen

## Beziehung zur heutigen Device-Shell

Die aktuelle Shell in
[device.js](/Users/jonasweiss/MathTeach/src/mathteach/ui/static/device.js)
enthaelt heute bereits diese Hilfsfunktionen:

- `describeResumeTopic()`
- `describeResumeSummary()`
- `renderStartScreen()`

Die Resolver-Implementierung soll diese direkte Kopplung spaeter
ersetzen durch:

1. `resolveStartscreenState(...)`
2. zustandsgebundenen Slot-Bau
3. ein kleines `renderStartscreenFromResolvedState(...)`

## Nicht erlaubte Abkuerzungen

Die spaetere Implementierung darf nicht:

- `resume` rendern, nur weil `lastPlan` irgendein Objekt ist
- `unsafe_history` simulieren, nur weil eine Anfrage fehlschlug
- Fehlertexte direkt in Startscreen-Slots schreiben
- denselben Text fuer `resume` und `no_history` recyceln

## Erste Implementierungsgrenze

Die erste Resolver-Version ist dann fertig, wenn sie:

1. `resume` und `no_history` sauber unterscheiden kann
2. `unsafe_history` als strukturellen Platzhalter mit explizitem
   Zukunftshaken enthaelt
3. alle drei Zustaende ueber exakt einen technischen Eintrittspunkt
   aufloest

Sie ist noch nicht verpflichtet:

- `unsafe_history` schon voll aus Runtime-Daten zu speisen
- neue Backend-Felder einzufuehren
- sichtbare UI-Aenderungen ausserhalb des Startscreen-Zustandsaufloesers
  zu machen

## Folgeschritt

Der naechste saubere Schritt nach dieser Spec ist kein komplettes
Startscreen-Redesign, sondern eine kleine Runtime-Field-Spec:

- welche Felder heute schon in der API oder Device-Shell vorhanden sind
- welche Felder fuer explizites `unsafe_history` spaeter noetig werden
- welche Feldnamen dafuer fachlich sauber waeren
