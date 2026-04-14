# Device Onboarding Wire Contract: Startgegenstand

## Zweck

Dieses Dokument beschreibt den ersten konkreten Onboarding-Screen im
Device-Fluss:

- `Startgegenstand`

Es legt nicht das Design fest, sondern die exakte strukturelle
Verdrahtung dieses Screens:

- welche Slots sichtbar sein duerfen
- welche eine kleine Entscheidung dieser Screen wirklich traegt
- welche Inhalte ausdruecklich nicht auf diesen Schritt gehoeren

## Quellenbasis

Dieser Wire Contract ist direkt abgeleitet aus:

- [device-onboarding-contract.md](/Users/jonasweiss/MathTeach/docs/device-onboarding-contract.md)
- [device-onboarding-flow-blueprint.md](/Users/jonasweiss/MathTeach/docs/device-onboarding-flow-blueprint.md)
- [device-onboarding-screen-sequence-spec.md](/Users/jonasweiss/MathTeach/docs/device-onboarding-screen-sequence-spec.md)

## Geltungsbereich

Dieser Wire Contract gilt nur fuer den ersten kleinen Onboarding-
Schritt:

- den ersten Lerngegenstand klaeren

Er gilt nicht fuer:

- Darstellungswahl
- Schrittgroesse
- Supportlisten
- Abschluss oder Zusammenfassung

## Hauptabsicht

Der Screen muss auf einen Blick diese Aussage transportieren:

`Sag mir nur, womit wir anfangen sollen.`

Nicht transportieren:

- `Erzaehle mir alles ueber dich`
- `Wir richten jetzt dein ganzes Profil ein`
- `Du musst zuerst viele Dinge ausfuellen`

## Wire Slots

Der Screen besteht in diesem Zustand aus genau sechs Slots.

## Slot 1: Screen-Label

### Rolle

- schwache Orientierung

### Inhalt

- kleiner Flusskontext wie `Erster Schritt`

### Gewicht

- sehr schwach

### Darf nicht

- wie Titel oder Fortschrittsdrama wirken

## Slot 2: Entlastungs-Satz

### Rolle

- Druck rausnehmen
- den Sinn der Frage ruhig klaeren

### Inhalt

- ein sehr kurzer Erklaersatz

### Beispielstruktur

- `Ich frage nur, womit wir ruhig beginnen sollen.`

### Budget

- `1` kurzer Satz

### Darf nicht

- Profilsprache enthalten
- Diagnose- oder Leistungslogik andeuten

## Slot 3: Hauptfrage

### Rolle

- die einzige kleine Entscheidung dieses Screens benennen

### Inhalt

- die Startfrage

### Beispielstruktur

- `Was willst du gerade verstehen?`

### Budget

- `1` Frage

### Darf nicht

- mehrere Fragen auf einmal stellen
- auf Niveau, Diagnose oder Verlauf ausweiten

## Slot 4: Eingabefeld

### Rolle

- den ersten Lerngegenstand erfassen

### Inhalt

- genau `1` kurzes Eingabefeld

### Muss

- direkt lernrelevant sein
- auf ein Thema, einen Begriff oder eine Aufgabe zielen

### Darf nicht

- aus mehreren Feldern bestehen
- Name, Niveau oder Support parallel erfassen

## Slot 5: Primaerer Weiter-CTA

### Rolle

- zum naechsten kleinen Schritt fuehren

### Inhalt

- genau ein primaerer CTA

### Beispielstruktur

- `Weiter`

### Gewicht

- der einzige dominante Handlungsanker des Screens

### Darf nicht

- wie Absenden eines Formulars wirken
- mit weiteren primaeren Aktionen konkurrieren

## Slot 6: Schwache Rueck-Aktion

### Rolle

- nur bei Bedarf Orientierung halten

### Inhalt

- eine ruhige Rueck- oder Abbruchalternative

### Beispielstruktur

- `Zurueck`

### Gewicht

- deutlich schwaecher als der primaere CTA

### Darf nicht

- als zweite Hauptentscheidung auftreten

## Verbotene Slots

Folgende Slots sind auf diesem Screen nicht vorhanden:

- Namensfeld
- Niveau-/Klassenstufenfeld
- Darstellungswahl
- Schrittgroessenwahl
- Support-Checkboxen
- Zusammenfassungskarte

## Lesereihenfolge

Die beabsichtigte Reihenfolge ist streng:

1. Entlastungs-Satz
2. Hauptfrage
3. Eingabefeld
4. primaerer CTA
5. schwache Rueck-Aktion

Der Screen ist falsch, wenn:

- das Eingabefeld wie Teil eines grossen Formulars wirkt
- mehrere Entscheidungen sichtbar gleichzeitig konkurrieren
- der CTA wie `Profil speichern` oder `Setup abschicken` gelesen wird

## Datenmapping

## Aus Runtime / Device-State

### Eingabefeld

- schreibt den ersten Startgegenstand
- spaeter Zielwert fuer `objective`

### Primaerer CTA

- fuehrt direkt auf `Darstellungsstart`

### Rueck-Aktion

- fuehrt ruhig auf den Startscreen zurueck
  oder
- bleibt auf dem ersten Screen unsichtbar

## Nicht aus Runtime ziehen

Diese Daten duerfen auf diesem Screen nicht gezeigt werden:

- Support-Labels
- Verlaufsdaten
- Session- oder Resume-Status
- Outcome- oder Bewertungswerte
