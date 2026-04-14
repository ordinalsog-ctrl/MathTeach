# Device Startscreen Wire Contract: Letzter Stand Unsicher

## Zweck

Dieses Dokument ist die dritte konkrete Wire-Ebene fuer den
MathTeach-Startscreen im Zustand:

- `letzter Stand unsicher`
  oder
- `letzte Session unvollstaendig / defekt`

Es legt nicht das Design fest, sondern die exakte strukturelle
Verdrahtung des Screens:

- welche Slots in diesem Sonderzustand erlaubt sind
- wie Wiedereinstieg trotz unsicherem Verlauf ruhig und wuerdevoll
  bleibt
- welche technischen oder systemischen Inhalte ausdruecklich nicht
  sichtbar werden duerfen

## Quellenbasis

Dieser Wire Contract ist direkt abgeleitet aus:

- [device-ui-evidence-matrix.md](/Users/jonasweiss/MathTeach/docs/device-ui-evidence-matrix.md)
- [device-startscreen-contract.md](/Users/jonasweiss/MathTeach/docs/device-startscreen-contract.md)
- [device-startscreen-blueprint.md](/Users/jonasweiss/MathTeach/docs/device-startscreen-blueprint.md)
- [support-response-matrix-scarcity.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-scarcity.md)
- [universal-round-u1-program.md](/Users/jonasweiss/MathTeach/docs/universal-round-u1-program.md)

## Geltungsbereich

Dieser Wire Contract gilt nur fuer den Startscreen-Fall:

- es gibt Verlauf
  aber
- der letzte Zustand ist nicht stabil genug, um direkt als Resume-Kern
    verwendet zu werden

Typische Ursachen koennen spaeter intern sein:

- abgebrochene Session
- defekter Datensatz
- unsicherer letzter Block

Diese Ursachen sind fuer den Lernenden jedoch nicht sichtbar.

## Hauptabsicht

Der Screen muss auf einen Blick diese Aussage transportieren:

`Wir steigen beim letzten sicheren Schritt wieder ein.`

Nicht transportieren:

- `Etwas ist kaputt`
- `Deine letzte Sitzung ist fehlerhaft`
- `Du hast etwas verloren`

## Harte psychologische Aufgabe

Dieser Zustand muss drei Dinge zugleich leisten:

1. Unsicherheit entdramatisieren
2. den Wiedereinstieg weiter klein halten
3. technische Komplexitaet voll aus dem Blick des Lernenden nehmen

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

- Hinweis auf Fehler, Quarantaene oder Systemstatus enthalten

## Slot 2: Begruessung

### Rolle

- Sicherheit und Zugehoerigkeit halten

### Inhalt

- kurze ruhige Begruessung

### Beispielstruktur

- `Schoen, dass du da bist.`
- `Wir steigen ruhig wieder ein.`

### Budget

- maximal `2` kurze Zeilen

### Darf nicht

- Problem- oder Fehlersprache enthalten

## Slot 3: Sicherer Wiedereinstiegs-Kern

### Rolle

- den letzten sicheren Punkt benennen

### Inhalt

- letzter sicherer Schritt
  oder
- letzter sicherer Themenpunkt

### Beispielstruktur

- `Wir machen bei dem letzten sicheren Schritt weiter.`
- `Wir schauen noch einmal auf das Gleichgewicht beider Seiten.`

### Budget

- `1` kurzer Satz

### Darf nicht

- technischen Grund nennen
- auf verlorene oder defekte Daten verweisen
- mehrere Alternativen anbieten

## Slot 4: Primaerer CTA

### Rolle

- den sicheren Wiedereinstieg oeffnen

### Inhalt

- genau ein ruhiger Wiedereinstiegs-CTA

### Beispielstruktur

- `Sicher weitermachen`
- `Beim letzten sicheren Schritt weitermachen`

### Gewicht

- einziger dominanter CTA

### Darf nicht

- wie Reparatur oder Wiederherstellung wirken
- technische Bedeutung tragen

## Slot 5: Schwache Neben-Zeile

### Rolle

- eine schwache Alternative oder Entlastung

### Inhalt

Genau eins von:

- kurze entlastende Notiz
  oder
- schwache Alternative wie `Neu beginnen`

### Gewicht

- deutlich schwächer als der sichere Wiedereinstiegs-CTA

### Darf nicht

- Problemframing verstaerken
- mehrere Alternativen enthalten

## Slot 6: Entdramatisierungs-Hinweis

### Rolle

- den Zustand ohne Technik und ohne Schuld framings abfedern

### Inhalt

- sehr kurze entlastende Formulierung

### Beispielstruktur

- `Ein sicherer Wiedereinstieg reicht fuer jetzt.`
- `Wir nehmen einfach den letzten stabilen Schritt.`

### Gewicht

- schwach

### Darf nicht

- erklaeren, was technisch passiert ist
- Alarm oder Warnung tragen

## Verbotene Slots

Diese Slots sind in diesem Zustand nicht vorhanden:

- Fehler- oder Warnbanner
- technische Statusbox
- Quarantaenehinweis
- Datenverlust-Hinweis
- Verlaufsliste
- Reparaturoptionen
- Support- oder Diagnosehinweise

## Lesereihenfolge

Die beabsichtigte Reihenfolge ist streng:

1. Begruessung
2. sicherer Wiedereinstiegs-Kern
3. primaerer CTA
4. schwache Neben-Zeile
5. Entdramatisierungs-Hinweis

Der Screen ist falsch, wenn:

- ein Problem oder Fehler zuerst gelesen wird
- Slot 5 oder 6 lauter wird als Slot 3 oder 4
- der CTA wie technische Problembehebung gelesen wird

## Datenmapping

## Aus Runtime / Session

### Begruessung

- optional `learnerName`

### Sicherer Wiedereinstiegs-Kern

- letzter verifizierter stabiler Schritt
  oder
- letzte sichere Resume-Zusammenfassung

### Primaerer CTA

- fuehrt direkt in einen sicheren, kleineren Lernwiedereinstieg

### Neben-Zeile

- eine einzige schwache Alternative

### Entdramatisierungs-Hinweis

- statische entlastende Formulierung

## Nicht aus Runtime ziehen

Diese Daten duerfen in diesem Zustand nicht sichtbar werden:

- Fehlercodes
- Quarantaene-Status
- Defektbeschreibung
- technische Resume-Quellen
- Session-Integrity-Details
- interne Systembegriffe

## Zustandssicherheit

Wenn auch der sichere letzte Schritt nur grob bestimmbar ist, gilt:

- der sichere Wiedereinstiegs-Kern wird weiter vereinfacht
- der CTA fuehrt in den kleinsten moeglichen stabilen Schritt
- der Screen wird nicht technischer oder voller

## Akzeptanzkriterien

Dieser Wire Contract gilt nur dann als korrekt umgesetzt, wenn:

1. alle sechs Slots klar zuordenbar sind
2. kein Fehler- oder Warnslot sichtbar wird
3. der Wiedereinstieg als Schutz und nicht als Problem gelesen wird
4. es genau einen dominanten CTA gibt
5. technische Ursachen komplett unsichtbar bleiben
6. der Zustand nicht beschaemend und nicht alarmierend wirkt

## Naechste Ableitung

Wenn dieser Wire Contract akzeptiert ist, folgt danach erst:

- eine gemeinsame `Startscreen State Mapping Spec`

und noch nicht:

- Mockup
- UI-Design
- konkrete Implementation
