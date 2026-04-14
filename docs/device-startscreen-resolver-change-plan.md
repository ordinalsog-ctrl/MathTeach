# Device Startscreen Resolver Change Plan

## Zweck

Dieses Dokument beschreibt den kleinsten spaeteren Umbau von
[device.js](/Users/jonasweiss/MathTeach/src/mathteach/ui/static/device.js),
damit der Startscreen nicht mehr aus direkter Hilfslogik, sondern aus
einer echten Resolver-Kette gerendert wird.

Es ist die letzte Planungsstufe vor echtem UI-Code fuer den
Startscreen-Resolver.

Es beantwortet nur:

`Welche konkrete bestehende Startscreen-Logik in device.js wird
ersetzt, und welche kleinen Funktionen treten an ihre Stelle?`

Es ist absichtlich:

- kein UI-Code
- kein Layoutentwurf
- kein Designentscheid

## Quellenbasis

Dieser Change Plan ist direkt aus folgenden Repo-Artefakten abgeleitet:

- [device-startscreen-state-mapping-spec.md](/Users/jonasweiss/MathTeach/docs/device-startscreen-state-mapping-spec.md)
- [device-startscreen-resolver-implementation-spec.md](/Users/jonasweiss/MathTeach/docs/device-startscreen-resolver-implementation-spec.md)
- [device-startscreen-runtime-field-spec.md](/Users/jonasweiss/MathTeach/docs/device-startscreen-runtime-field-spec.md)
- [device-startscreen-resolver-flow-spec.md](/Users/jonasweiss/MathTeach/docs/device-startscreen-resolver-flow-spec.md)
- [device.js](/Users/jonasweiss/MathTeach/src/mathteach/ui/static/device.js)

## Hauptziel

Der Startscreen soll spaeter nicht mehr direkt durch lose Hilfsfunktionen
wie `describeResumeTopic()` und `describeResumeSummary()` entstehen.

Stattdessen soll genau diese Kette gelten:

1. Input sammeln
2. Input normalisieren
3. Zustand aufloesen
4. Slots bauen
5. rendern

## Heutiger Zustand in device.js

Heute laeuft der Startscreen im Kern so:

1. `renderStartScreen()` liest direkt `state.profile.learnerName`
2. `renderStartScreen()` ruft `describeResumeTopic()` auf
3. `renderStartScreen()` ruft `describeResumeSummary()` auf
4. die Texte werden direkt in DOM-Slots geschrieben

### Heutige direkte Abhaengigkeiten

- `state.profile.learnerName`
- `state.lastPlan`
- `state.lastUpdatedAt`
- `pickActiveBlock(state.lastPlan)`

### Heutige Schwachstelle

Diese direkte Hilfslogik funktioniert fuer eine erste Shell, aber sie
kennt noch keinen expliziten Startscreen-Zustand.

Dadurch ist heute noch nicht sauber getrennt:

- `resume`
- `no_history`
- spaeter `unsafe_history`

## Zielstruktur nach dem Umbau

Nach dem Umbau soll der Startscreen in
[device.js](/Users/jonasweiss/MathTeach/src/mathteach/ui/static/device.js)
aus genau diesen kleinen Funktionen bestehen:

## 1. `collectStartscreenInput()`

Aufgabe:

- liest nur die erlaubten Runtime-Felder
- baut ein rohes Input-Objekt

## 2. `normalizeStartscreenInput(input)`

Aufgabe:

- erzeugt die kleinen Bool- und Kernwerte fuer den Resolver

## 3. `resolveStartscreenState(normalized)`

Aufgabe:

- entscheidet genau einen Zustand:
  - `resume`
  - `no_history`
  - spaeter `unsafe_history`

## 4. Zustandsspezifische Slot-Builder

Aufgabe:

- bauen genau die Slots fuer den jeweiligen Wire-Contract

Kleine Zielmenge:

- `buildResumeStartscreenSlots(normalized)`
- `buildNoHistoryStartscreenSlots(normalized)`
- spaeter `buildUnsafeHistoryStartscreenSlots(normalized)`

## 5. `renderStartscreenResolved(resolved)`

Aufgabe:

- liest nur `state_kind + slots`
- schreibt keine eigenen Resume-Heuristiken mehr

## Explizit zu ersetzende aktuelle Funktionen

## A. `renderStartScreen()`

Wird nicht entfernt, aber umgebaut.

### Heute

- direkte Textableitung
- direkter Zugriff auf `state`

### Ziel

- nur noch Orchestrator
- ruft Resolver-Kette auf
- reicht das aufgeloeste Ergebnis an den Renderer weiter

## B. `describeResumeTopic()`

### Ziel

Diese Funktion soll als freie Startscreen-Hilfsfunktion verschwinden.

Ihre Aufgabe geht spaeter in den zustandsgebundenen Resume-Slot-Builder
ueber.

## C. `describeResumeSummary()`

### Ziel

Auch diese Funktion soll als freie globale Startscreen-Hilfsfunktion
verschwinden.

Ihre Aufgabe geht in den zustandsgebundenen Resume-Slot-Builder ueber.

## D. `pickActiveBlock()`

### Ziel

`pickActiveBlock()` bleibt voraussichtlich als allgemeine Hilfsfunktion
erhalten, darf aber nicht mehr direkt die gesamte Startscreen-Semantik
tragen.

Sie wird kuenftig nur noch als Datenhelfer unterhalb des Resolvers
benutzt.

## Phasierter Umbau

Der Umbau soll klein und rueckbausicher bleiben.

## Phase 1: Resolver-Skelett einfuehren

Neue kleine Funktionen anlegen:

- `collectStartscreenInput()`
- `normalizeStartscreenInput()`
- `resolveStartscreenState()`

Wichtig:

- noch ohne sichtbare Veraenderung des Startscreens
- nur interne Strukturverbesserung

## Phase 2: Slot-Builder einfuehren

Neue kleine Builder:

- `buildResumeStartscreenSlots()`
- `buildNoHistoryStartscreenSlots()`

`unsafe_history` kann in dieser Phase strukturell angelegt sein, aber
noch auf fehlendes explizites Runtime-Signal ruecksicht nehmen.

## Phase 3: Renderer umstellen

`renderStartScreen()` wird dann auf dieses Muster umgestellt:

```text
input = collectStartscreenInput()
normalized = normalizeStartscreenInput(input)
resolved = resolveStartscreenState(normalized)
renderStartscreenResolved(resolved)
```

Erst ab diesem Punkt verschwinden:

- `describeResumeTopic()`
- `describeResumeSummary()`

## Phase 4: Aufraeumen

Nach erfolgreicher Umstellung:

- alte freie Resume-Hilfslogik entfernen
- keine doppelte Startscreen-Semantik im File belassen

## Harte Umbau-Regeln

## 1. Kein sichtbarer Zusatz-UI-Scope

Der Change Plan erlaubt nur den Startscreen-Resolver-Umbau.

Nicht enthalten:

- neue Screens
- neues Layout
- neue Illustrationen
- Onboarding- oder Lernscreen-Umbau

## 2. Keine semantische Erweiterung im selben Schritt

Wenn wir den Resolver einfuehren, darf dabei nicht gleichzeitig eine
neue psychologische oder fachliche Startscreen-Semantik dazukommen.

## 3. Keine implizite Unsafe-Logik

Es darf kein `unsafe_history`-Screen gerendert werden, solange kein
explizites Runtime-Signal vorhanden ist.

## 4. Keine parallelen Startscreen-Systeme

Nach der Umstellung darf nicht sowohl die alte als auch die neue
Startscreen-Semantik dauerhaft nebeneinander im Code leben.

## Akzeptanzkriterien fuer den spaeteren Code-Schritt

Der spaetere eigentliche Code-Umbau ist nur dann sauber, wenn:

- `renderStartScreen()` keine eigenen Resume-Heuristiken mehr enthaelt
- `describeResumeTopic()` und `describeResumeSummary()` nicht mehr die
  Startscreen-Zustandslogik tragen
- der Resolver genau einen Zustand ausgibt
- der Renderer nur noch aufgeloeste Slots liest
- `resume` und `no_history` technisch sauber getrennt sind
- die aktuelle sichtbare UI nicht "smarter" wirkt als die Runtime
  belegen kann

## Aktueller UI-Zwischenstand

Mit diesem Change Plan ist die Startscreen-Kette jetzt bis direkt vor
den ersten echten Code-Umbau geschlossen:

- Evidenzmatrix
- Contract
- Blueprint
- Wire-Contracts
- State-Mapping
- Resolver-Implementierungs-Spec
- Runtime-Field-Spec
- Resolver-Flow-Spec
- Resolver-Change-Plan fuer `device.js`

Noch bewusst offen:

- kein neuer UI-Code
- keine neuen sichtbaren Startscreens
- keine neue Unsafe-Runtime

## Folgeschritt

Der naechste saubere Schritt ist jetzt der erste kleine echte
Code-Umbau im Startscreen:

- Resolver-Skelett in
  [device.js](/Users/jonasweiss/MathTeach/src/mathteach/ui/static/device.js)
- noch ohne neues Design
- noch ohne neue Illustration
- nur als interne Strukturbereinigung entlang dieses Plans
