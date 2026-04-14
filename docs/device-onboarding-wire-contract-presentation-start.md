# Device Onboarding Wire Contract: Darstellungsstart

## Zweck

Dieses Dokument beschreibt den zweiten konkreten Onboarding-Screen im
Device-Fluss:

- `Darstellungsstart`

Es legt nicht das Design fest, sondern die exakte strukturelle
Verdrahtung dieses Screens:

- welche Slots sichtbar sein duerfen
- welche einzige kleine Entscheidung dieser Screen tragen darf
- welche Inhalte hier ausdruecklich nicht erscheinen duerfen

## Quellenbasis

Dieser Wire Contract ist direkt abgeleitet aus:

- [device-onboarding-contract.md](/Users/jonasweiss/MathTeach/docs/device-onboarding-contract.md)
- [device-onboarding-flow-blueprint.md](/Users/jonasweiss/MathTeach/docs/device-onboarding-flow-blueprint.md)
- [device-onboarding-screen-sequence-spec.md](/Users/jonasweiss/MathTeach/docs/device-onboarding-screen-sequence-spec.md)

## Geltungsbereich

Dieser Wire Contract gilt nur fuer den zweiten kleinen Onboarding-
Schritt:

- wie die erste Erklaerung beginnen soll

Er gilt nicht fuer:

- den Startgegenstand selbst
- Schrittgroesse
- Supportlisten
- Abschluss oder Zusammenfassung

## Hauptabsicht

Der Screen muss auf einen Blick diese Aussage transportieren:

`Sag mir nur, wie ich anfangen soll zu erklaeren.`

Nicht transportieren:

- `Waehle jetzt dein Lernprofil`
- `Stelle mehrere Praeferenzen gleichzeitig ein`
- `Wir machen jetzt eine Detailkonfiguration`

## Wire Slots

Der Screen besteht in diesem Zustand aus genau sechs Slots.

## Slot 1: Screen-Label

### Rolle

- schwache Orientierung

### Inhalt

- kleiner Flusskontext wie `Naechster Schritt`

### Gewicht

- sehr schwach

### Darf nicht

- wie Fortschrittsdruck wirken

## Slot 2: Entlastungs-Satz

### Rolle

- den Sinn der Frage ruhig rahmen

### Inhalt

- ein sehr kurzer Satz

### Beispielstruktur

- `Ich richte nur den ersten Zugang fuer dich aus.`

### Budget

- `1` kurzer Satz

### Darf nicht

- klinisch, technisch oder testhaft wirken

## Slot 3: Hauptfrage

### Rolle

- die einzige kleine Entscheidung dieses Screens benennen

### Inhalt

- die Darstellungsfrage

### Beispielstruktur

- `Soll ich mit Bild oder mit Worten starten?`

### Budget

- `1` Frage

### Darf nicht

- Schrittgroesse oder Support parallel fragen

## Slot 4: Antwortoptionen

### Rolle

- die eine kleine Wahl sichtbar machen

### Inhalt

- genau `2` gleichartige Optionen

### Beispielstruktur

- `Mit einem Bild`
- `Mit Worten`

### Muss

- gleichwertig sichtbar sein
- dieselbe Entscheidungsebene tragen

### Darf nicht

- `3+` Optionen zeigen
- Chips fuer weitere Praeferenzen daneben tragen
- Checkboxlogik benutzen

## Slot 5: Primaerer Weiter-CTA

### Rolle

- in den Abschluss- und Startschritt fuehren

### Inhalt

- genau ein primaerer CTA

### Beispielstruktur

- `Weiter`

### Gewicht

- der einzige dominante CTA

### Darf nicht

- wie finaler Setup-Save wirken

## Slot 6: Schwache Rueck-Aktion

### Rolle

- ruhiger Rueckschritt

### Inhalt

- eine schwache Rueck-Aktion

### Beispielstruktur

- `Zurueck`

### Gewicht

- klar schwaecher als der primaere CTA

### Darf nicht

- mit der Bild-/Wort-Wahl konkurrieren

## Verbotene Slots

Folgende Slots sind auf diesem Screen nicht vorhanden:

- Namensfeld
- Niveau-/Klassenstufe
- Schrittgroessenwahl
- Support-Checkboxen
- Mehrfachwahl fuer mehrere Darstellungsmodi
- Abschlusszusammenfassung

## Lesereihenfolge

Die beabsichtigte Reihenfolge ist streng:

1. Entlastungs-Satz
2. Hauptfrage
3. die zwei Antwortoptionen
4. primaerer CTA
5. schwache Rueck-Aktion

Der Screen ist falsch, wenn:

- die zwei Optionen nicht wie dieselbe Entscheidungsebene gelesen werden
- ein zusaetzlicher Wahlblock danebensteht
- die Rueck-Aktion oder der CTA lauter werden als die eigentliche
  Bild-/Wort-Entscheidung

## Datenmapping

## Aus Runtime / Device-State

### Optionen

- `Mit einem Bild` -> spaeter `wantsVisuals = true`
- `Mit Worten` -> spaeter `wantsVisuals = false`

### Primaerer CTA

- fuehrt direkt auf `Startfreigabe`

### Rueck-Aktion

- fuehrt auf `Startgegenstand`

## Nicht aus Runtime ziehen

Diese Daten duerfen auf diesem Screen nicht sichtbar werden:

- Diagnose- oder Support-Labels
- Verlauf oder Resume-Daten
- Niveau
- Schrittgroesse
