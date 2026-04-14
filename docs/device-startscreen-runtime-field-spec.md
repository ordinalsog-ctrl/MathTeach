# Device Startscreen Runtime Field Spec

## Zweck

Dieses Dokument legt fest, welche Runtime-Felder der spaetere
Startscreen-Resolver lesen darf, welche Felder heute schon vorhanden
sind und welche fuer spaeteres explizites `unsafe_history` noch fehlen.

Es ist die Feld-Ebene unterhalb von:

- [device-startscreen-state-mapping-spec.md](/Users/jonasweiss/MathTeach/docs/device-startscreen-state-mapping-spec.md)
- [device-startscreen-resolver-implementation-spec.md](/Users/jonasweiss/MathTeach/docs/device-startscreen-resolver-implementation-spec.md)

Es beantwortet nur:

`Welche Daten hat der Resolver heute wirklich, und welche muessten fuer
spaetere Zustandslogik noch sauber nachgereicht werden?`

Es ist absichtlich:

- kein UI-Code
- keine API-Implementierung
- kein Renderplan

## Hauptregel

Der Resolver darf nur Felder lesen, deren fachliche Bedeutung klar und
stabil ist.

Nicht erlaubt:

- Felder fuer Resume-Zwecke umdeuten, die nur technische Identitaet
  tragen
- aus beliebigen Planfragmenten einen Resume-Zustand konstruieren
- einen `unsafe_history`-Pfad zu bauen, solange dafuer kein explizites
  Runtime-Signal existiert

## Feldquellen

Der spaetere Resolver darf Daten aus genau zwei Quellen lesen:

## 1. Lokaler Device-Shell-State

Aus
[device.js](/Users/jonasweiss/MathTeach/src/mathteach/ui/static/device.js):

- `state.profile`
- `state.sessionId`
- `state.lastPlan`
- `state.lastUpdatedAt`

## 2. Letzter Plan

Aus
[TeachingPlan in models.py](/Users/jonasweiss/MathTeach/src/mathteach/models.py):

- `session_id`
- `planned_blocks`
- `resume_context`

## Felder, die heute schon real vorhanden sind

## A. Device-Shell-Felder

| Feld | Quelle | Heute vorhanden | Resolver-Rolle |
| --- | --- | --- | --- |
| `profile.learnerName` | local state | ja | Personalisierung, nie Zustandsbeweis |
| `sessionId` | local state | ja | technische Session-Identitaet, nie Resume-Beweis |
| `lastPlan` | local state | ja | primaere Quelle fuer Resume oder No-History |
| `lastUpdatedAt` | local state | ja | Kontext fuer Resume-Satz, nie Resume-Beweis |

## B. Plan-Felder

| Feld | Quelle | Heute vorhanden | Resolver-Rolle |
| --- | --- | --- | --- |
| `session_id` | `TeachingPlan` | ja | Rueckbindung an Session, nie alleiniger Resume-Beweis |
| `planned_blocks` | `TeachingPlan` | ja | Resume-Titel und Resume-Satz ableitbar |
| `planned_blocks[0].goal` | `PlannedTeachingBlock` | ja | primaerer Resume-Titel-Kandidat |
| `planned_blocks[0].transition_message` | `PlannedTeachingBlock` | ja | primaerer Resume-Satz-Kandidat |
| `resume_context.resume_source` | `ResumeContext` | ja | Herkunft des Resume-Pfads |
| `resume_context.resume_active` | `ResumeContext` | ja | explizites Resume-Signal |

## C. ResumeContext-Felder

Diese Felder sind heute schon im Planmodell vorhanden, aber fuer den
Startscreen nur sekundar relevant:

- `resume_context.carried_observation_evidence`
- `resume_context.used_carried_observation_evidence`
- `resume_context.pending_transition_message_carried`
- `resume_context.pending_transition_message_consumed`

Sie koennen spaeter intern hilfreich sein, sind aber fuer die erste
Startscreen-Resolver-Version nicht noetig.

## Feldklassifikation fuer den Resolver

## 1. Primaere Zustandsfelder

Diese Felder darf der Resolver fuer die eigentliche Zustandswahl lesen:

- `lastPlan`
- `lastPlan.resume_context.resume_active`
- `lastPlan.resume_context.resume_source`
- `lastPlan.planned_blocks`
- `lastPlan.planned_blocks[0].goal`
- `lastPlan.planned_blocks[0].transition_message`

## 2. Sichtbarkeits- und Personalisierungsfelder

Diese Felder duerfen in Slots einfliessen, aber nie die Zustandswahl
tragen:

- `profile.learnerName`
- `lastUpdatedAt`

## 3. Technische Identitaetsfelder

Diese Felder duerfen gelesen, aber nicht als psychologischer oder
didaktischer Resume-Beweis verwendet werden:

- `sessionId`
- `lastPlan.session_id`

## Erlaubte Minimalnutzung heute

Mit den heute vorhandenen Feldern darf die erste Resolver-Version
bereits sauber unterscheiden zwischen:

- `resume`
- `no_history`

## Saubere Resume-Bedingung heute

`resume` ist heute fachlich sauber belegbar, wenn:

- `lastPlan` vorhanden ist
- `resume_context.resume_active == true`
  oder
- ein stabiler erster `planned_block` mit `goal` vorliegt

Wobei gilt:

- `resume_context.resume_active` ist das staerkere explizite Signal
- `planned_blocks[0].goal` ist ein zulaessiger fachlicher Fallback
- `transition_message` verbessert den Resume-Satz, ist aber nicht allein
  ausreichend

## Saubere No-History-Bedingung heute

`no_history` ist heute fachlich sauber, wenn:

- `lastPlan` fehlt
  oder
- `resume_context.resume_active == false` und kein belastbarer Resume-
  Block vorliegt
  oder
- `resume_source == "fresh_start"`

## Ehrliche Grenze heute

Mit den heute vorhandenen Feldern ist `unsafe_history` noch nicht
explizit entscheidbar.

Der Grund ist nicht fehlende Safety im Backend, sondern fehlende
sichtbare Runtime-Semantik in der Device-Shell.

Backend-seitig ist bereits vorhanden:

- Quarantaene fuer ungueltige Checkpoints
- Rueckfall auf `fresh_start`

Device-seitig fehlt aber noch ein explizites Signal wie:

- `resume_status = unsafe`
  oder
- `resume_recovery_required = true`

## Bevorzugte zusaetzliche Zukunftsfelder

Wenn spaeter `unsafe_history` sauber sichtbar werden soll, braucht der
Resolver ein explizites Feldset.

Die bevorzugte kleine Zukunftsvariante ist:

## Option A: Ein Statusfeld

- `resume_status`

Zulaessige Werte:

- `fresh_start`
- `resume_ready`
- `unsafe_history`

Vorteile:

- genau ein Resolver-Feld
- gut lesbar in Device-UI und API
- vermeidet Bool-Kombinationen

## Option B: Ein Bool plus Herkunft

- `resume_recovery_required: bool`
- kombiniert mit vorhandenem `resume_source`

Vorteile:

- kleine Erweiterung

Nachteile:

- semantisch weniger klar als ein echtes Statusfeld
- Bool plus Kontext ist fehleranfaelliger als ein expliziter Enum-
  Zustand

## Bevorzugte Empfehlung

Wenn wir spaeter die Runtime erweitern, ist fuer den Startscreen-
Resolver fachlich sauberer:

- `resume_status`

als ein einzelnes Bool.

## Feldbudget fuer Phase 1 des Resolvers

Die erste echte Resolver-Implementierung braucht noch keine neuen
Backend-Felder.

Phase 1 darf sich auf dieses Feldbudget beschraenken:

- `profile.learnerName`
- `lastPlan`
- `lastUpdatedAt`
- `lastPlan.resume_context.resume_active`
- `lastPlan.resume_context.resume_source`
- `lastPlan.planned_blocks[0].goal`
- `lastPlan.planned_blocks[0].transition_message`

## Feldbudget fuer spaetere Unsafe-Phase

Wenn `unsafe_history` spaeter wirklich sichtbar aufgeloest werden soll,
kommt minimal dazu:

- `lastPlan.resume_context.resume_status`
  oder
- ein gleichwertiges explizites Unsafe-Signal

## Nicht erlaubte Feldverwendung

Folgende Nutzungen sind fuer den Resolver unzulaessig:

- `sessionId` -> `resume`
- `lastUpdatedAt` -> `resume`
- leeres `lastPlan`-Objekt -> `resume`
- reine Request-Fehler im Frontend -> `unsafe_history`
- Quarantaene nur implizit backend-seitig -> sichtbarer
  `unsafe_history`-Screen ohne Runtime-Signal

## Beziehung zur spaeteren UI

Diese Spec legt keine sichtbaren Texte fest.

Sie sorgt nur dafuer, dass spaetere UI-Screens auf der richtigen
Laufzeitsemantik stehen.

Das bedeutet:

- erst Felder
- dann Resolver
- dann sichtbarer Wire-Contract
- erst danach spaetere UI-Implementierung

## Folgeschritt

Der naechste saubere Schritt ist jetzt kein neues Feld und kein neues
Design, sondern ein kleiner Resolver-Flow:

- Eingabe
- Feldnormalisierung
- Zustandsentscheidung
- Slot-Bau

also eine reine Ablauf-Spec fuer den Startscreen-Resolver.
