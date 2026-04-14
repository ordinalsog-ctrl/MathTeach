# Device Onboarding Wire Contract: Startfreigabe

## Zweck

Dieses Dokument beschreibt den dritten konkreten Onboarding-Screen im
Device-Fluss:

- `Startfreigabe`

Es legt nicht das Design fest, sondern die exakte strukturelle
Verdrahtung dieses Screens:

- welche Slots sichtbar sein duerfen
- wie die Startfreigabe klein bleibt
- welche Ueberfrachtung auf diesem Abschluss-Schritt verboten ist

## Quellenbasis

Dieser Wire Contract ist direkt abgeleitet aus:

- [device-onboarding-contract.md](/Users/jonasweiss/MathTeach/docs/device-onboarding-contract.md)
- [device-onboarding-flow-blueprint.md](/Users/jonasweiss/MathTeach/docs/device-onboarding-flow-blueprint.md)
- [device-onboarding-screen-sequence-spec.md](/Users/jonasweiss/MathTeach/docs/device-onboarding-screen-sequence-spec.md)

## Geltungsbereich

Dieser Wire Contract gilt nur fuer den dritten kleinen Onboarding-
Schritt:

- den Fluss ruhig schliessen
- den ersten Lernschritt freigeben

Er gilt nicht fuer:

- neue Fragen
- Profil- oder Supporterhebung
- grosse Antwortzusammenfassung

## Hauptabsicht

Der Screen muss auf einen Blick diese Aussage transportieren:

`Gut, wir beginnen genau so.`

Nicht transportieren:

- `Hier ist deine komplette Konfiguration`
- `Bitte pruefe jetzt alle Angaben`
- `Bevor wir starten, fehlen noch weitere Angaben`

## Wire Slots

Der Screen besteht in diesem Zustand aus genau sechs Slots.

## Slot 1: Screen-Label

### Rolle

- schwache Orientierung

### Inhalt

- kleiner Flusskontext wie `Dann starten wir`

### Gewicht

- sehr schwach

### Darf nicht

- wie grosse Abschlussmarke oder Belohnung wirken

## Slot 2: Bestaetigungszeile

### Rolle

- den Fluss ruhig schliessen

### Inhalt

- eine kurze bestaetigende Zeile

### Beispielstruktur

- `Gut, wir beginnen genau so.`

### Budget

- `1` kurzer Satz

### Darf nicht

- dramatisch oder motivatorisch ueberhoeht werden

## Slot 3: Mini-Zusammenfassung

### Rolle

- genau die kleine Startfreigabe sichtbar machen

### Inhalt

- eine kurze Ein-Zeilen-Zusammenfassung

### Beispielstruktur

- `Lineare Gleichungen, zuerst mit Bild.`

### Budget

- `1` kurze Zeile

### Darf nicht

- Liste aller Antworten werden
- Support-, Profil- oder Niveaudaten zeigen

## Slot 4: Primaerer Start-CTA

### Rolle

- direkt in die erste Session fuehren

### Inhalt

- genau ein primaerer Start-CTA

### Beispielstruktur

- `Jetzt starten`

### Gewicht

- einziger dominanter CTA

### Darf nicht

- wie Abschluss eines langen Formulars wirken

## Slot 5: Schwache Rueck-Aktion

### Rolle

- ruhige Korrektur des letzten kleinen Schritts

### Inhalt

- eine schwache Rueck-Aktion

### Beispielstruktur

- `Zurueck`

### Gewicht

- deutlich schwaecher als der Start-CTA

### Darf nicht

- mit dem Start konkurrieren

## Slot 6: Entlastungs-Satz

### Rolle

- bestaetigen, dass der erste Lernschritt klein bleibt

### Inhalt

- sehr kurze entlastende Formulierung

### Beispielstruktur

- `Wir koennen den Einstieg spaeter jederzeit anpassen.`

### Gewicht

- schwach

### Darf nicht

- neue Entscheidungen oeffnen

## Verbotene Slots

Folgende Slots sind auf diesem Screen nicht vorhanden:

- grosse Antwortzusammenfassung
- Profil- oder Supportlisten
- Name/Niveau/Uebersichten
- Checkboxen oder weitere Auswahlfelder
- mehrere Haupt-CTAs

## Lesereihenfolge

Die beabsichtigte Reihenfolge ist streng:

1. Bestaetigungszeile
2. Mini-Zusammenfassung
3. primaerer Start-CTA
4. schwache Rueck-Aktion
5. Entlastungs-Satz

Der Screen ist falsch, wenn:

- die Zusammenfassung groesser wirkt als die Startfreigabe
- ploetzlich neue Informationen oder neue Wahlmoeglichkeiten auftauchen
- der letzte Schritt wie Formular-Abschluss statt wie Startfreigabe
  gelesen wird

## Datenmapping

## Aus Runtime / Device-State

### Mini-Zusammenfassung

- Startgegenstand aus Screen 1
- Darstellungsstart aus Screen 2

### Primaerer CTA

- fuehrt direkt in den ersten Lernscreen / erste Session

### Rueck-Aktion

- fuehrt auf `Darstellungsstart`

## Nicht aus Runtime ziehen

Diese Daten duerfen auf diesem Screen nicht sichtbar werden:

- Support-Checkboxwerte
- Niveau
- Diagnose- oder Profilbezeichnungen
- Verlaufs- oder Resume-Daten
