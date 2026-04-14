# Device Startscreen Blueprint

## Zweck

Dieses Dokument ist die erste konkrete Ableitung des
`device-startscreen-contract`.

Es beschreibt den Startscreen als strukturellen Bauplan.

Es ist bewusst:

- kein Mockup
- kein CSS-Plan
- keine Farb- oder Illustrationsanweisung

Es beantwortet nur:

- welche Zonen der Startscreen braucht
- in welcher Reihenfolge sie wahrgenommen werden sollen
- welche Inhalte in welche Zone duerfen
- welche Inhalte dort nicht auftauchen duerfen

## Quellenbasis

Dieser Blueprint ist direkt aus folgenden Repo-Dokumenten abgeleitet:

- [device-ui-evidence-matrix.md](/Users/jonasweiss/MathTeach/docs/device-ui-evidence-matrix.md)
- [device-startscreen-contract.md](/Users/jonasweiss/MathTeach/docs/device-startscreen-contract.md)
- [rpi-touch-ui-lastenheft.md](/Users/jonasweiss/MathTeach/docs/rpi-touch-ui-lastenheft.md)

## Primaere Bildschirmlogik

Der Startscreen ist kein Uebersichtsbildschirm.

Er ist ein `Wiedereinstiegsbildschirm`.

Darum gilt:

- der Screen hat nur einen primaeren Lesepfad
- der Screen hat nur einen primaeren CTA
- der Resume-Kern ist wichtiger als jede visuelle Zutat

## Wahrnehmungsreihenfolge

Die beabsichtigte Reihenfolge des ersten Blicks ist:

1. `Begruessung`
2. `letzter sinnvoller Stand`
3. `primaere Handlung`
4. `optionale entlastende Notiz`

Nicht erlaubt:

- dass zuerst ein dekoratives Objekt gelesen wird
- dass zuerst eine Sekundaerhandlung ins Auge springt
- dass zuerst mehrere gleich starke Informationsflaechen konkurrieren

## Zonen des Screens

Der Startscreen besteht aus genau vier moeglichen Zonen.

## Zone A: Begruessungszone

### Aufgabe

- Zugehoerigkeit und Ruhe signalisieren
- den Ton fuer die Session setzen

### Inhalt

- kurze Begruessung
- optional Name des Lernenden

### Muss

- sehr knapp sein
- nicht leistungsorientiert sein

### Darf nicht

- Resume-Details enthalten
- Zielsysteme oder Fortschritt erzaehlen
- mehrere Saetze stapeln

### Inhaltsbudget

- `1` kurze Begruessungszeile
- optional `1` personifizierende Ergaenzung

## Zone B: Resume-Zone

### Aufgabe

- den letzten sicheren Stand sichtbar machen
- den Wiedereinstieg entschlacken

### Inhalt

- letzter Lerngegenstand oder letzter sicherer Schritt
- kurzer Satz zum naechsten kleinen Wiedereinstieg

### Muss

- die wichtigste Inhaltszone des Screens sein
- als erstes inhaltlich verstaendlich werden

### Darf nicht

- Verlaufsliste werden
- mehrere Themen gleichzeitig zeigen
- Statistik oder Bewertung enthalten

### Inhaltsbudget

- `1` Resume-Titel
- `1` Resume-Satz

## Zone C: Primaere Handlungszone

### Aufgabe

- den naechsten sicheren Zug freigeben

### Inhalt

- genau ein primaerer CTA

### Muss

- dominant lesbar sein
- sprachlich ruhig sein
- direkt zum Wiedereinstieg fuehren

### Darf nicht

- mit anderen grossen Handlungen konkurrieren
- technisch oder systemisch formuliert sein

### Inhaltsbudget

- `1` primaerer Button

## Zone D: Schwache Neben-Zone

### Aufgabe

- nur bei Bedarf entlasten oder eine schwache Alternative anbieten

### Zulaessige Inhalte

- eine ruhige Sekundaerhandlung
- eine kurze entlastende Notiz

### Darf nicht

- gleich stark wie Resume oder Haupt-CTA werden
- mehrere Alternativen aufmachen
- den ersten Lesepfad stoeren

### Inhaltsbudget

- entweder `1` Sekundaerhandlung
- oder `1` entlastende Notiz
- nicht beides mehrfach gestapelt

## Nicht zulaessige Zonen

Folgende Zonen darf der Startscreen nicht enthalten:

- Themenraster
- Verlaufsliste
- Statistikflaeche
- Settings-Zone
- Dashboard-Navigation
- Leistungs- oder Zielzone

## Textmengenregeln

Der gesamte Startscreen darf in seiner Kernebene nicht mehr tragen als:

- `1` Begruessungszeile
- `1` Resume-Satz
- `1` CTA
- optional `1` kurze Zusatzzeile

Wenn mehr Text noetig scheint, ist die Screen-Idee zu gross und muss
verkleinert werden.

## Strukturregeln

### 1. Ein primaerer Inhaltsblock

Es darf nur einen Block geben, der wie "das Zentrum dieses Screens"
wirkt.

Das ist der Resume-Kern.

### 2. Keine konkurrierenden Karten

Es duerfen nicht zwei oder drei gleich wichtige Flaechen nebeneinander
stehen.

### 3. Keine Uebersichtsarchitektur

Der Screen darf nicht den Eindruck erzeugen, man muesse zuerst waehlen,
wo man ueberhaupt anfängt.

## Zustandsblueprint

## Zustand A: Kein Verlauf

### Reihenfolge

1. Begruessung
2. ruhiger Satz fuer ersten Start
3. primaerer CTA in den ersten Einstieg

### Was fehlt bewusst

- kein leeres Resume-Modul
- keine Platzhalterstatistik

## Zustand B: Resume vorhanden

### Reihenfolge

1. Begruessung
2. letzter Schritt
3. CTA `Weiterlernen`
4. optional entlastende Notiz

### Fokus

Der ganze Screen arbeitet auf diesen einen Wiedereinstieg hin.

## Zustand C: Letzter Stand unsicher

### Reihenfolge

1. Begruessung
2. letzter sicherer Schritt
3. CTA fuer sicheren Wiedereinstieg

### Verbot

- keine technische Fehlersprache
- kein Warnzustand

## Illustrationsposition

Eine Illustration ist im Startscreen-Blueprint nicht Pflichtbestandteil.

Falls spaeter eine Illustration eingesetzt wird:

- sie liegt ausserhalb des primaeren Resume-Kerns
- sie darf den Lesepfad nicht ueberschreiben
- sie muss semantisch leise bleiben

Die Illustration darf niemals die Resume-Zone ersetzen.

## Blueprint-Reviewfragen

Vor jeder spaeteren Umsetzung des Startscreens muessen diese Fragen mit
`ja` beantwortet sein:

1. Ist der Resume-Kern klar die wichtigste Inhaltszone?
2. Gibt es genau eine dominante Handlung?
3. Wird der Screen nicht zur Uebersicht oder Themenwahl umgedeutet?
4. Bleibt die Informationsmenge innerhalb des Budgets?
5. Ist eine Illustration, falls vorhanden, semantisch leiser als Resume
   und CTA?

## Naechste Ableitung

Wenn dieser Blueprint akzeptiert ist, folgt erst danach:

- ein `Startscreen Wire Contract` oder eine strukturierte
  Implementationsskizze

und noch nicht:

- Mockup
- Styling
- Illustrationswahl
