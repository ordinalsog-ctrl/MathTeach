# Device Startscreen State Mapping Spec

## Zweck

Dieses Dokument verbindet die drei vorhandenen Startscreen-Wire-
Contracts mit der realen Runtime-Semantik.

Es beantwortet nur diese Frage:

`Welcher vorhandene Runtime-Zustand fuehrt auf welchen
Startscreen-Zustand?`

Es ist absichtlich:

- kein Mockup
- kein Layoutplan
- kein Stilentscheid

## Quellenbasis

Diese Spec ist direkt aus folgenden Repo-Artefakten abgeleitet:

- [device-ui-evidence-matrix.md](/Users/jonasweiss/MathTeach/docs/device-ui-evidence-matrix.md)
- [device-startscreen-contract.md](/Users/jonasweiss/MathTeach/docs/device-startscreen-contract.md)
- [device-startscreen-blueprint.md](/Users/jonasweiss/MathTeach/docs/device-startscreen-blueprint.md)
- [device-startscreen-wire-contract-resume.md](/Users/jonasweiss/MathTeach/docs/device-startscreen-wire-contract-resume.md)
- [device-startscreen-wire-contract-no-history.md](/Users/jonasweiss/MathTeach/docs/device-startscreen-wire-contract-no-history.md)
- [device-startscreen-wire-contract-unsafe-history.md](/Users/jonasweiss/MathTeach/docs/device-startscreen-wire-contract-unsafe-history.md)
- [models.py](/Users/jonasweiss/MathTeach/src/mathteach/models.py)
- [planner.py](/Users/jonasweiss/MathTeach/src/mathteach/services/planner.py)
- [session_manager.py](/Users/jonasweiss/MathTeach/src/mathteach/services/session_manager.py)
- [device.js](/Users/jonasweiss/MathTeach/src/mathteach/ui/static/device.js)

## Hauptregel

Der Startscreen muss immer den kleinsten sicheren Zustand waehlen.

Das bedeutet:

- `Resume` nur dann, wenn ein stabiler Wiedereinstieg wirklich belegbar
  ist
- sonst `kein Verlauf`
- `unsicherer Verlauf` nur dann, wenn die Runtime dafuer ein explizites
  Signal traegt

Nicht erlaubt:

- schwache Heuristiken als sicheres Resume auszugeben
- technische Unsicherheit in Resume-Rhetorik zu verstecken
- aus unvollstaendigen Daten einen zu "smarten" Startscreen zu bauen

## Zielzustandsfamilie

Die Device-UI kennt auf Startscreen-Ebene genau diese drei Wire-
Contracts:

1. [device-startscreen-wire-contract-resume.md](/Users/jonasweiss/MathTeach/docs/device-startscreen-wire-contract-resume.md)
2. [device-startscreen-wire-contract-no-history.md](/Users/jonasweiss/MathTeach/docs/device-startscreen-wire-contract-no-history.md)
3. [device-startscreen-wire-contract-unsafe-history.md](/Users/jonasweiss/MathTeach/docs/device-startscreen-wire-contract-unsafe-history.md)

## Reale Eingangssignale

## 1. Device-Shell-Zustand heute

Die lokale Device-Shell in
[device.js](/Users/jonasweiss/MathTeach/src/mathteach/ui/static/device.js)
traegt heute sichtbar:

- `state.profile`
- `state.sessionId`
- `state.lastPlan`
- `state.lastUpdatedAt`

Davon ist fuer den Startscreen aktuell direkt verwertbar:

- `state.profile.learnerName`
- `state.lastPlan`
- `state.lastUpdatedAt`
- `state.sessionId`

## 2. Resume-Semantik im Backend

Das Backend kennt ueber
[models.py](/Users/jonasweiss/MathTeach/src/mathteach/models.py) und
[planner.py](/Users/jonasweiss/MathTeach/src/mathteach/services/planner.py)
bereits:

- `resume_source`
- `resume_active`

Zulaessige Resume-Quellen sind:

- `fresh_start`
- `inline_state`
- `inline_checkpoint`
- `stored_checkpoint`

## 3. Session-Validierung und Quarantaene

[session_manager.py](/Users/jonasweiss/MathTeach/src/mathteach/services/session_manager.py)
behandelt defekte oder nicht resume-faehige Checkpoints bereits
schutzorientiert:

- ungueltige gespeicherte Checkpoints werden quarantainiert
- nicht resume-faehige Checkpoints fallen fuer neue Requests auf
  `fresh_start` zurueck
- der technische Grund bleibt aus der Lernoberflaeche herausgehalten

Das ist fachlich richtig fuer die Safety-Schicht, hat aber eine
wichtige UI-Folge:

- die Device-Shell bekommt heute nicht automatisch ein explizites
  `unsafe_history`-Signal

## Zustandsresolver

Der Startscreen-Zustand wird durch eine einzige Resolver-Funktion
bestimmt.

Sie darf nur einen der drei Zielzustaende ausgeben:

- `resume`
- `no_history`
- `unsafe_history`

## Harte Prioritaetsregel

Die Reihenfolge der Entscheidung ist:

1. `unsafe_history`
2. `resume`
3. `no_history`

Aber:

- Zustand `1` darf nur verwendet werden, wenn die Runtime ihn wirklich
  kennt
- wenn dieses Signal fehlt, faellt die Entscheidung auf `resume` oder
  `no_history` zurueck

## Mindestmapping fuer die aktuelle Runtime

Mit den heute im Device-Shell-Zustand sichtbaren Feldern gilt dieses
Mindestmapping:

## Fall A: Resume vorhanden

Verwende
[device-startscreen-wire-contract-resume.md](/Users/jonasweiss/MathTeach/docs/device-startscreen-wire-contract-resume.md),
wenn alle folgenden Bedingungen erfuellt sind:

- `state.lastPlan` ist vorhanden
- der Plan enthaelt genug Inhalt, um einen stabilen Resume-Titel und
  einen Resume-Satz zu bilden
- es gibt keinen expliziten Unsafe-Marker

Praktische Mindestbelege sind:

- ein vorhandener letzter Plan
- eine daraus ableitbare Resume-Beschreibung
- eine sinnvolle primaere Fortsetzungsaktion

## Fall B: Kein Verlauf

Verwende
[device-startscreen-wire-contract-no-history.md](/Users/jonasweiss/MathTeach/docs/device-startscreen-wire-contract-no-history.md),
wenn mindestens eine der folgenden Bedingungen gilt:

- `state.lastPlan` fehlt
- die lokale Shell hat noch keinen nutzbaren Lernstand
- das Backend liefert effektiv `fresh_start`
- es gibt zwar `sessionId`, aber keinen stabilen sichtbaren Resume-
  Inhalt

Wichtig:

- `sessionId` allein ist niemals ein Resume-Beleg
- `learnerName` allein ist niemals ein Resume-Beleg
- `lastUpdatedAt` allein ist niemals ein Resume-Beleg

## Fall C: Unsicherer Verlauf

Verwende
[device-startscreen-wire-contract-unsafe-history.md](/Users/jonasweiss/MathTeach/docs/device-startscreen-wire-contract-unsafe-history.md),
nur wenn die Runtime spaeter mindestens eines dieser expliziten Signale
traegt:

- ein sichtbares `resume_status = unsafe`
- ein expliziter `resume_recovery_required`-Marker
- ein Device-seitig weitergereichtes Signal, dass ein gespeicherter
  Verlauf absichtlich nicht als direkter Resume-Kern benutzt werden darf

## Ehrliche aktuelle Einschraenkung

Mit der heute vorhandenen Device-Shell ist `unsafe_history` als
Wire-Contract schon fachlich definiert, aber noch nicht voll von der UI-
Runtime aufloesbar.

Heute gilt deshalb:

- defekte oder ungueltige gespeicherte Sessions werden backend-seitig
  bereits sicher abgefangen
- die Lernoberflaeche sieht in vielen dieser Faelle nur `fresh_start`
  statt eines expliziten `unsafe_history`

Darum darf die aktuelle UI nicht so tun, als koenne sie bereits
zuverlaessig zwischen `no_history` und `unsafe_history` unterscheiden,
wenn dieses Zusatzsignal noch nicht vorliegt.

## Mapping-Tabelle

| Runtime-Signalbild | Zielzustand | Wire-Contract |
| --- | --- | --- |
| `lastPlan` vorhanden, kein Unsafe-Signal | `resume` | [device-startscreen-wire-contract-resume.md](/Users/jonasweiss/MathTeach/docs/device-startscreen-wire-contract-resume.md) |
| kein `lastPlan` oder effektiver `fresh_start` | `no_history` | [device-startscreen-wire-contract-no-history.md](/Users/jonasweiss/MathTeach/docs/device-startscreen-wire-contract-no-history.md) |
| explizites Unsafe-/Recovery-Signal vorhanden | `unsafe_history` | [device-startscreen-wire-contract-unsafe-history.md](/Users/jonasweiss/MathTeach/docs/device-startscreen-wire-contract-unsafe-history.md) |

## Fallback-Regeln

Wenn die Datenlage unklar ist, gilt immer die sicherere kleinere
Abbildung.

Das bedeutet:

- unklarer Resume-Beleg -> `no_history`
- partieller oder leerer Resume-Inhalt -> `no_history`
- implizite technische Vermutung ohne Marker -> nicht `unsafe_history`

## Nicht erlaubte Resolver-Heuristiken

Der Resolver darf nicht:

- allein aus `sessionId` einen Resume-Zustand bauen
- allein aus Zeitstempel-Aktualitaet ein Resume ableiten
- ein leeres oder generisches Resume-Modul rendern, nur weil frueher
  schon einmal etwas gelernt wurde
- technische Unsicherheit ohne explizite Runtime-Signale als
  `unsafe_history` markieren

## Umsetzungspflicht fuer die Device-UI

Die spaetere Device-Implementierung braucht vor dem Rendern genau einen
kleinen Startscreen-Resolver.

Seine Aufgabe ist nicht Gestaltung, sondern nur:

1. vorhandene Runtime-Felder lesen
2. Zustand nach dieser Spec aufloesen
3. genau einen Wire-Contract aktivieren

Er darf nicht:

- Wire-Contracts mischen
- Resume-Inhalte improvisieren
- mehrere Startscreen-Zustaende gleichzeitig zeigen

## Folgeschritt

Der naechste saubere technische Schritt ist eine kleine
Implementierungs-Spec fuer diesen Resolver:

- benoetigte Felder
- Resolver-Reihenfolge
- Default-Fallbacks
- spaetere Erweiterung fuer explizite `unsafe_history`-Signale
