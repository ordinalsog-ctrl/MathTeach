# Device Startscreen Wire Contract: Kein Verlauf

## Zweck

Dieses Dokument ist die zweite konkrete Wire-Ebene fuer den
MathTeach-Startscreen im Zustand:

- `kein Verlauf vorhanden`

Es legt nicht das Design fest, sondern die exakte strukturelle
Verdrahtung des Screens:

- welche inhaltlichen Slots es in diesem Zustand geben darf
- welche Slots bewusst nicht existieren
- welche Daten in welchem Slot auftauchen duerfen
- wie der erste Einstieg ohne Reibung und ohne Druck gebaut wird

## Quellenbasis

Dieser Wire Contract ist direkt abgeleitet aus:

- [device-ui-evidence-matrix.md](/Users/jonasweiss/MathTeach/docs/device-ui-evidence-matrix.md)
- [device-startscreen-contract.md](/Users/jonasweiss/MathTeach/docs/device-startscreen-contract.md)
- [device-startscreen-blueprint.md](/Users/jonasweiss/MathTeach/docs/device-startscreen-blueprint.md)

## Geltungsbereich

Dieser Wire Contract gilt nur fuer den Startscreen-Fall:

- es gibt noch keinen letzten Lernstand
  oder
- der Lernende hat noch keine echte Session-Historie

Er gilt nicht fuer:

- Resume vorhanden
- letzter Stand unsicher / defekt

## Hauptabsicht

Der Screen muss auf einen Blick diese Aussage transportieren:

`Du kannst ohne Huerde klein anfangen.`

Nicht transportieren:

- `Du musst erst etwas einrichten`
- `Du musst dich erst entscheiden, was fuer ein Lerntyp du bist`
- `Du bist noch ganz am Anfang und musst viel aufholen`

## Wire Slots

Der Screen besteht in diesem Zustand aus genau sechs Slots.

## Slot 1: Screen-Label

### Rolle

- schwache Orientierung

### Inhalt

- kleiner Screen-Kontext wie `MathTeach local tutor`

### Gewicht

- sehr schwach

### Darf nicht

- Titelcharakter bekommen
- als Navigationsleiste wachsen

## Slot 2: Begruessung

### Rolle

- Sicherheit und Zugehoerigkeit

### Inhalt

- eine kurze ruhige Begruessung
- optional ein zweiter kurzer Satz zum Startcharakter

### Beispielstruktur

- `Schoen, dass du da bist.`
- `Wir koennen klein und ruhig anfangen.`

### Budget

- maximal `2` kurze Zeilen

### Darf nicht

- fehlenden Verlauf problematisieren
- Leistungsframe enthalten

## Slot 3: Start-Kern

### Rolle

- den ersten Einstieg konkret und klein machen

### Inhalt

- ein kurzer Satz, was jetzt als erster Schritt passiert

### Beispielstruktur

- `Wir beginnen mit einer ersten ruhigen Erklaerung.`
- `Du musst noch nichts koennen oder vorbereiten.`

### Budget

- `1` kurzer Satz

### Darf nicht

- Themenkatalog sein
- mehrere Startwege aufmachen
- Produktuebersicht geben

## Slot 4: Primaerer CTA

### Rolle

- den ersten Lernschritt oeffnen

### Inhalt

- genau ein primaerer Start-CTA

### Beispielstruktur

- `Jetzt anfangen`
- `Ersten Schritt starten`

### Gewicht

- der einzige dominante Handlungsanker des Screens

### Darf nicht

- mit Onboarding oder Settings konkurrieren
- wie Registrierung oder Setup wirken

## Slot 5: Schwache Neben-Zeile

### Rolle

- eine einzige schwache Alternative oder Entlastung

### Inhalt

Genau eins von:

- kurzer entlastender Satz
  oder
- schwache Sekundaerhandlung wie `Profil einrichten`

### Gewicht

- deutlich schwächer als der Start-CTA

### Darf nicht

- zweite Hauptentscheidung werden
- mehrere Alternativen enthalten

## Slot 6: Start-Hinweis

### Rolle

- Reibung weiter senken

### Inhalt

- ein sehr kurzer Hinweis, dass der Einstieg klein und sicher ist

### Beispielstruktur

- `Ein kleiner erster Schritt reicht.`
- `Wir passen die Erklaerung spaeter an.`

### Gewicht

- schwach

### Darf nicht

- Profil- oder Diagnosesprache enthalten
- technische Erklaerung werden

## Verbotene Slots

Diese Slots sind in diesem Zustand nicht vorhanden:

- Resume-Titel
- Resume-Satz
- Verlaufskarte
- Themenraster
- grosse Themenwahl
- Statistik
- Erfolgssystem
- Account-/Setup-Module

## Lesereihenfolge

Die beabsichtigte Reihenfolge ist streng:

1. Begruessung
2. Start-Kern
3. primaerer CTA
4. schwache Neben-Zeile
5. Start-Hinweis

Der Screen ist falsch, wenn:

- ein fehlender Verlauf als Mangel wirkt
- Slot 5 oder 6 den CTA ueberstrahlt
- Slot 3 wie ein Menue statt wie ein erster Schritt gelesen wird

## Datenmapping

## Aus Runtime / Session

### Begruessung

- optional `learnerName`, wenn vorhanden

### Start-Kern

- statischer erster Startsatz
  oder
- leicht kontextualisierter Einstiegssatz

### Primaerer CTA

- fuehrt direkt in den ersten kleinen Lernpfad
  oder
- in das minimal noetige Onboarding

### Neben-Zeile

- eine einzige schwache Alternative

### Start-Hinweis

- statische entlastende Formulierung

## Nicht aus Runtime ziehen

Diese Daten duerfen in diesem Zustand nicht sichtbar werden:

- fehlende History als Defizit
- technische Systemzustände
- Outcome- oder Verlaufsdaten
- Support-Labels
- nicht benoetigte Profilparameter

## Zustandssicherheit

Wenn noch gar keine personenbezogenen Daten vorliegen, gilt:

- Begruessung bleibt allgemein
- Start-Kern bleibt maximal einfach
- CTA oeffnet den kleinstmoeglichen sicheren Einstieg

Der Screen darf nicht groesser oder erklaerungslauter werden, nur weil
noch nichts bekannt ist.

## Akzeptanzkriterien

Dieser Wire Contract gilt nur dann als korrekt umgesetzt, wenn:

1. alle sechs Slots klar zuordenbar sind
2. kein Resume-Slot auftaucht
3. der fehlende Verlauf nirgends als Mangel erscheint
4. es genau einen dominanten Start-CTA gibt
5. keine Wahl- oder Themenuebersicht entsteht
6. keine Setup- oder Diagnoseoptik entsteht

## Naechste Ableitung

Wenn dieser Wire Contract akzeptiert ist, folgt danach erst:

- eine `State-to-UI Mapping Spec` fuer den Erststart
  oder
- eine sehr rohe Layout-Skizze in Textform

und noch nicht:

- Mockup
- visuelle Gestaltung
- UI-Implementation
