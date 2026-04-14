# Device Startscreen Wire Contract: Resume Vorhanden

## Zweck

Dieses Dokument ist die erste konkrete Wire-Ebene fuer den
MathTeach-Startscreen im Zustand:

- `Resume vorhanden`

Es legt nicht das Design fest, sondern die exakte strukturelle
Verdrahtung des Screens:

- welche inhaltlichen Slots existieren
- in welcher Reihenfolge sie gelesen werden
- welche Daten in welchem Slot landen
- welche Slots bewusst leer oder gar nicht vorhanden sind

## Quellenbasis

Dieser Wire Contract ist direkt abgeleitet aus:

- [device-ui-evidence-matrix.md](/Users/jonasweiss/MathTeach/docs/device-ui-evidence-matrix.md)
- [device-startscreen-contract.md](/Users/jonasweiss/MathTeach/docs/device-startscreen-contract.md)
- [device-startscreen-blueprint.md](/Users/jonasweiss/MathTeach/docs/device-startscreen-blueprint.md)

## Geltungsbereich

Dieser Wire Contract gilt nur fuer den Startscreen-Fall:

- ein letzter sinnvoller Lernstand ist vorhanden
- der Lernende soll ohne Umweg genau dort wieder einsteigen koennen

Er gilt nicht fuer:

- Erststart ohne Verlauf
- letzter Stand unsicher / defekte Session

## Hauptabsicht

Der Screen muss auf einen Blick diese Aussage transportieren:

`Du kannst genau hier sicher weitermachen.`

Nicht transportieren:

- `Du musst jetzt waehlen`
- `Du solltest mehr schaffen`
- `Hier ist dein Lerncockpit`

## Wire Slots

Der Screen besteht in diesem Zustand aus genau sechs Slots.

## Slot 1: Screen-Label

### Rolle

- Orientierung, aber nicht inhaltlicher Fokus

### Inhalt

- kleiner Screen-Kontext wie `MathTeach local tutor`

### Gewicht

- sehr schwach

### Darf nicht

- dominanter Titel werden
- Produktnavigation enthalten

## Slot 2: Begruessung

### Rolle

- Zugehoerigkeit und Ruhe

### Inhalt

- eine kurze Begruessungszeile
- optional Lernendenname

### Beispielstruktur

- `Schoen, dass du da bist.`
- `Alex, wir gehen in deinem Tempo weiter.`

### Budget

- maximal `2` kurze Zeilen

### Darf nicht

- Resume-Info enthalten
- Leistungsframe enthalten

## Slot 3: Resume-Titel

### Rolle

- sofort klarmachen, worauf sich der Wiedereinstieg bezieht

### Inhalt

- letzter Lerngegenstand
  oder
- letzter sicherer Schritt

### Beispielstruktur

- `Lineare Gleichungen: x + 3 = 7`
- `Wir waren zuletzt bei: auf beiden Seiten gleich handeln`

### Budget

- `1` Titelzeile

### Darf nicht

- mehrere Themen nennen
- Kontextgeschichte erzaehlen

## Slot 4: Resume-Satz

### Rolle

- den naechsten kleinen Wiedereinstieg explizit machen

### Inhalt

- ein kurzer Satz, der den naechsten sicheren Schritt benennt

### Beispielstruktur

- `Wir steigen wieder dort ein, wo wir die 3 auf beiden Seiten wegnehmen.`

### Budget

- `1` kurzer Satz

### Darf nicht

- mehrere naechste Schritte enthalten
- Theorie oder Motivation mischen

## Slot 5: Primaerer CTA

### Rolle

- direkter Wiedereinstieg

### Inhalt

- `Weiterlernen`
  oder
- `Hier weitermachen`

### Gewicht

- der einzige dominante Handlungsanker des Screens

### Darf nicht

- mit weiteren grossen CTAs konkurrieren
- technisch formuliert sein

## Slot 6: Schwache Neben-Zeile

### Rolle

- entlasten oder eine einzige schwache Alternative anbieten

### Inhalt

Genau eins von:

- kurze entlastende Notiz
  oder
- schwache Sekundaerhandlung

### Beispielstruktur

- `Ein kleiner Schritt reicht fuer jetzt.`
  oder
- `Neues Profil einrichten`

### Gewicht

- klar schwächer als Resume und CTA

### Darf nicht

- zweite Hauptentscheidung werden
- mehrere Optionen enthalten

## Verbotene Slots

Folgende Slots sind in diesem Wire Contract nicht vorhanden:

- Statistikslot
- Themenraster
- Verlaufsverlauf
- Ziel- oder Erfolgsanzeige
- Settings-CTA
- Verlaufsliste
- zweite CTA-Reihe

## Lesereihenfolge

Die beabsichtigte Reihenfolge ist streng:

1. Begruessung
2. Resume-Titel
3. Resume-Satz
4. Primaerer CTA
5. schwache Neben-Zeile

Der Screen ist falsch, wenn:

- Slot 6 vor Slot 5 dominiert
- Slot 1 visuell lauter wird als Slot 2 bis 5
- Resume-Titel und Resume-Satz nicht zusammen gelesen werden

## Datenmapping

## Aus Runtime / Session

### Begruessung

- `learnerName` falls vorhanden

### Resume-Titel

- letzter `goal`
  oder
- letzter sicherer Block-Titel

### Resume-Satz

- letzte sichere Resume-Zusammenfassung
  oder
- systemseitig abgeleiteter Wiedereinstiegssatz

### Primaerer CTA

- fuehrt direkt in den naechsten Plan / Resume-Lernscreen

### Neben-Zeile

- statische entlastende Formulierung
  oder
- eine einzige schwache Alternative

## Nicht aus Runtime ziehen

Diese Daten duerfen in diesem Zustand nicht gezeigt werden:

- Anzahl vergangener Sessions
- Test-/Outcome-Werte
- Statistiken
- Profile oder Support-Labels
- technische Resume-Quellen

## Zustandssicherheit

Wenn einzelne Resume-Daten fehlen, gilt:

- Resume-Titel bleibt minimal
- Resume-Satz wird auf letzten sicheren Schritt vereinfacht
- der Screen darf nicht groesser oder technischer werden

## Akzeptanzkriterien

Dieser Wire Contract gilt nur dann als korrekt umgesetzt, wenn:

1. alle sechs Slots klar zuordenbar sind
2. keine weiteren Slots auftauchen
3. Resume-Titel und Resume-Satz zusammen den Wiedereinstieg klaeren
4. es genau einen dominanten CTA gibt
5. die Neben-Zeile visuell und inhaltlich schwach bleibt
6. keine Statistik-, Profil- oder Diagnoseinfo sichtbar wird

## Naechste Ableitung

Wenn dieser Wire Contract akzeptiert ist, folgt danach erst:

- eine `State-to-UI Mapping Spec`
  oder
- eine sehr rohe Layout-Skizze in Textform

und noch nicht:

- Mockup
- visuelle Gestaltung
- UI-Implementation
