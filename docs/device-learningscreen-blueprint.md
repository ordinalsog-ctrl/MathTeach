# Device Learningscreen Blueprint

## Zweck

Dieses Dokument ist die erste konkrete Ableitung des
`device-learningscreen-contract`.

Es beschreibt die Lernansicht als strukturellen Bauplan.

Es legt fest:

- welche Zonen ein Lernscreen haben darf
- in welcher Reihenfolge diese Zonen wahrgenommen werden sollen
- welche Rolle jede Zone hat
- welche Zonen und Inhaltskombinationen verboten sind

Es ist bewusst:

- kein Mockup
- kein Layoutdesign
- kein CSS-Plan

## Quellenbasis

Dieser Blueprint ist direkt aus folgenden Repo-Dokumenten abgeleitet:

- [device-ui-evidence-matrix.md](/Users/jonasweiss/MathTeach/docs/device-ui-evidence-matrix.md)
- [device-learningscreen-contract.md](/Users/jonasweiss/MathTeach/docs/device-learningscreen-contract.md)
- [rpi-touch-ui-lastenheft.md](/Users/jonasweiss/MathTeach/docs/rpi-touch-ui-lastenheft.md)

## Hauptlogik

Der Lernscreen ist kein Mehrzweck-Screen.

Er ist ein `Traeger fuer genau eine mathematische Idee`.

Darum gilt:

- ein primaerer Blickanker
- ein primaerer Gedanke
- ein sichtbarer naechster Schritt

Nicht erlaubt:

- konkurrierende Hauptzonen
- gleich starke Wissens- und Metazonen
- gleichzeitige Theorie-, Historie-, Uebungs- und Systemflaechen

## Wahrnehmungsreihenfolge

Die beabsichtigte Reihenfolge des ersten Blicks ist:

1. `mathematische Hauptidee`
2. `primaerer Traeger`
3. `naechster kleiner Schritt`
4. `unterstuetzende Notizen`
5. `Handlungsoptionen`

Nicht erlaubt:

- zuerst Systemstatus
- zuerst Metadaten
- zuerst dekorative Illustration
- zuerst Aktionsflaechen

## Zonen des Lernscreens

Ein Lernscreen darf aus genau diesen Zonen bestehen.

## Zone A: Hauptaussage

### Aufgabe

- die aktuelle mathematische Idee benennen

### Inhalt

- ein kurzer Hauptsatz

### Muss

- eindeutig sein
- genau eine Idee tragen
- ohne Nebenzweige formuliert sein

### Darf nicht

- mehrere neue Begriffe auf einmal einfuehren
- mehrere mathematische Ziele koppeln

## Zone B: Primaerer Traeger

### Aufgabe

- die Idee sichtbar machen

### Inhalt

Genau eins von:

- Visualisierung
- Worked Example
- strukturierte Symbolzeile
- Mengen- oder Beziehungstraeger

### Muss

- erster inhaltlicher Blickanker des Screens sein
- direkt an der Hauptidee haengen

### Darf nicht

- dekorativ sein
- mehrere Hauptobjekte aufmachen
- durch Nebeninfos ueberlagert werden

## Zone C: Schritt- und Uebergangszone

### Aufgabe

- zeigen, was jetzt passiert und was als naechstes moeglich ist

### Inhalt

- kurzer Relevanz- oder Uebergangssatz
- kleine sichtbare Schrittorientierung

### Muss

- explizit sein
- den Uebergang klar benennen

### Darf nicht

- implizit bleiben
- den Screen in eine mehrstufige Roadmap aufblasen

## Zone D: Fokus-Notiz

### Aufgabe

- sagen, worauf jetzt besonders geachtet werden soll

### Inhalt

- eine kurze Fokusnotiz

### Muss

- auf den primaeren Traeger verweisen
- lokal bleiben

### Darf nicht

- zweite Hauptidee werden
- neue Erklaerungsebene aufmachen

## Zone E: Scaffold-Notiz

### Aufgabe

- die aktive Hilfsstruktur sichtbar machen

### Inhalt

- eine kurze Scaffold-Notiz

### Muss

- klein sein
- funktional sein

### Darf nicht

- Motivationsfloskel sein
- Metakommentar ueber das ganze System werden

## Zone F: Handlungszone

### Aufgabe

- dem Lernenden wenige, sinnvolle naechste Handlungen anbieten

### Inhalt

- `2` bis `3` Handlungen

### Muss

- direkt aus der aktuellen Idee hervorgehen
- sprachlich ruhig sein

### Darf nicht

- technisch wirken
- mehr als drei Optionen enthalten
- gleichwertig mit Navigation oder Settings konkurrieren

## Nicht zulaessige Zonen

Ein Lernscreen darf diese Zonen nicht enthalten:

- Dashboard-Zone
- Statistikzone
- Session-Historie
- Themennavigation
- Systemdiagnostik
- grosse Meta-Erklaerung der Engine
- zweite Illustration ohne mathematische Notwendigkeit

## Inhaltsbudget

Ein Lernscreen darf insgesamt nicht mehr tragen als:

- `1` Hauptsatz
- `1` primaerer Traeger
- `1` Uebergangssatz
- `1` Fokus-Notiz
- `1` Scaffold-Notiz
- `2` bis `3` Handlungen

Wenn mehr gebraucht wird, ist die Idee fuer einen einzelnen Lernscreen
zu gross und muss geteilt werden.

## Strukturregeln

### 1. Nur eine Hauptzone

Es darf nur eine Zone geben, die wie "das Zentrum des Lernens auf
diesem Screen" wirkt.

### 2. Notizen sind untergeordnet

Fokus- und Scaffold-Notizen duerfen nie gleich stark wirken wie die
Hauptidee.

### 3. Handlungen kommen nach der Idee

Buttons oder Handlungen duerfen nicht vor der mathematischen Idee
dominieren.

### 4. Recovery verkleinert, nicht vergroessert

Wenn der Lernende stockt, darf der spaetere Recovery-Screen nicht mehr
Zonen bekommen als der Ausgangsscreen.

## Blueprint nach Lernzustand

## Zustand A: Erst-Erklaerung

### Reihenfolge

1. Hauptaussage
2. primaerer Traeger
3. Fokus
4. naechster kleiner Schritt
5. Handlungen

### Charakter

- stabilisierend
- bedeutungsnah
- kleine Schrittweite

## Zustand B: Wiederholung / Recovery

### Reihenfolge

1. dieselbe Hauptidee kleiner
2. expliziterer Traeger oder expliziterer Teil davon
3. engerer Fokus
4. Handlungen

### Charakter

- keine neue Idee
- weniger Last
- mehr Explizitheit

## Zustand C: Uebergang zum naechsten Schritt

### Reihenfolge

1. was jetzt stabil ist
2. welcher naechste kleine Schritt folgt
3. Handlungsentscheidung

### Charakter

- knapp
- ruhig
- vorhersagbar

## Illustrationsposition

Wenn eine Illustration oder Visualisierung eingesetzt wird, dann als
Teil von Zone B.

Sie ist:

- primaerer Traeger
  oder
- nicht vorhanden

Nicht erlaubt:

- zusaetzliche stimmungsbildende Illustration neben dem primaeren
  Traeger
- Bild plus separates Hauptdiagramm

## Symbolikposition

Symbolik darf nur in zwei Rollen auftreten:

- als Teil des primaeren Traegers
- als kleine Verknuepfung in Fokus- oder Scaffold-Notiz

Nicht erlaubt:

- separater dichter Symbolblock als zweite Hauptzone

## Blueprint-Reviewfragen

Vor jeder spaeteren Umsetzung muessen diese Fragen mit `ja`
beantwortet sein:

1. Gibt es genau einen primaeren Blickanker?
2. Traegt der Screen genau eine mathematische Idee?
3. Sind Fokus- und Scaffold-Zone klar untergeordnet?
4. Kommen die Handlungen erst nach Idee und Orientierung?
5. Kann ein Recovery-Screen kleiner statt groesser werden?

## Naechste Ableitung

Wenn dieser Blueprint akzeptiert ist, folgt danach erst:

- eine `Learning Screen Sequence Spec`
  oder
- ein `Wire Contract` fuer einen einzelnen Lernfall

und noch nicht:

- Mockup
- Styling
- UI-Implementation
