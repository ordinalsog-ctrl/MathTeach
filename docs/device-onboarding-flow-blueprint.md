# Device Onboarding Flow Blueprint

## Zweck

Dieses Dokument ist die erste konkrete Ableitung des
`device-onboarding-contract`.

Es beschreibt den Onboarding-Fluss als strukturellen Bauplan.

Es legt fest:

- welche Schritte der Fluss ueberhaupt haben darf
- in welcher Reihenfolge diese Schritte kommen
- welche Information in welchem Schritt geklaert wird
- was in diesem Fluss ausdruecklich nicht passieren darf

Es ist bewusst:

- kein Mockup
- kein Wizard-Design
- kein Formularlayout

## Quellenbasis

Dieser Blueprint ist direkt aus folgenden Repo-Dokumenten abgeleitet:

- [device-ui-evidence-matrix.md](/Users/jonasweiss/MathTeach/docs/device-ui-evidence-matrix.md)
- [device-onboarding-contract.md](/Users/jonasweiss/MathTeach/docs/device-onboarding-contract.md)
- [rpi-touch-ui-lastenheft.md](/Users/jonasweiss/MathTeach/docs/rpi-touch-ui-lastenheft.md)

## Hauptregel

Das Device-Onboarding ist kein Erhebungsfluss.

Es ist ein `kurzer Einstiegspfad zur ersten passenden Erklaerung`.

Darum gilt:

- so wenig Schritte wie moeglich
- so wenig Entscheidungen wie noetig
- erster Lernschritt wichtiger als vollstaendige Konfiguration

## Maximaler Flussumfang

Der fruehe Device-Onboarding-Fluss darf hoechstens `4` Schritte haben.

Bevorzugt:

- `3` Schritte

Nicht erlaubt:

- lange Mehrschritt-Serien
- Unterpfade mit vielen Sonderfragen

## Verbindliche Reihenfolge

Der Onboarding-Fluss folgt dieser Reihenfolge:

1. `Warum ich frage`
2. `Womit willst du anfangen?`
3. `Wie soll ich anfangen?`
4. `Dann starten wir`

Wenn weniger noetig ist, darf Schritt 3 entfallen.

## Schritt 1: Warum ich frage

### Aufgabe

- Druck rausnehmen
- den Sinn des Onboardings klar machen

### Inhalt

- sehr kurzer Erklaersatz
- keine Entscheidung
- nur Freigabe fuer den restlichen Fluss

### Muss

- klar sagen, dass es um die Darstellungsform geht
- klar sagen, dass nichts bewertet wird

### Darf nicht

- Profilsprache verwenden
- Supportbegriffe aufzählen
- mehrere Erklaerblaecke tragen

### Output dieses Schritts

- Lernende verstehen:
  `ich werde nicht getestet; ich sage nur, wie ich starten will`

## Schritt 2: Womit willst du anfangen?

### Aufgabe

- ersten Lerngegenstand klaeren

### Inhalt

- ein kurzer Startwunsch oder Lernwunsch

### Erlaubte Form

- ein einzelnes kurzes Eingabefeld
- oder eine sehr kleine Auswahl vorbereiteter Startthemen

### Muss

- klein bleiben
- sofort lernrelevant sein

### Darf nicht

- Interessenprofil werden
- Themenkatalog werden
- mehrere Eingaben gleichzeitig verlangen

### Output dieses Schritts

- ein erster Startgegenstand

## Schritt 3: Wie soll ich anfangen?

### Aufgabe

- die erste Erklaerform grob ausrichten

### Erlaubte Entscheidungstypen

- `Bild oder Worte zuerst`
- `kleine Schritte oder direkt`

### Muss

- nur eine dieser Entscheidungen pro Screen
- nur `2` bis `3` Optionen

### Darf nicht

- mehrere Entscheidungsebenen gleichzeitig zeigen
- Checkbox-Logik verwenden
- Supportlisten anbieten

### Output dieses Schritts

- eine grobe Darstellungsrichtung fuer die erste Session

## Schritt 4: Dann starten wir

### Aufgabe

- den Fluss abschliessen
- die erste Lernsession oeffnen

### Inhalt

- sehr kurze Bestaetigung
- ein primaerer Start-CTA

### Muss

- direkt in den Lernscreen fuehren
- keine weitere Abfrage oeffnen

### Darf nicht

- als Zusammenfassungsformular auftreten
- Rueckblick in alle Antworten aufblasen

## Alternative Kurzform

Wenn der Einstieg extrem niedrigschwellig bleiben soll, ist auch diese
Kurzform zulaessig:

1. `Womit willst du anfangen?`
2. `Soll ich mit Bild oder Worten starten?`
3. `Los geht's`

Die Entscheidung zwischen Standard- und Kurzform ist eine
Produktentscheidung, keine freie Screen-Erweiterung.

## Nicht zulaessige Flussbestandteile

Diese Bestandteile darf der Onboarding-Fluss nicht enthalten:

- Support-Bedarfsliste mit vielen Haken
- Diagnose- oder Label-Fragen
- persoenliche Hintergrundabfragen ohne direkten Lernwert
- Settings-Schritte
- Account-, Cloud- oder Sync-Schritte
- Motivationserfassung
- grosse Abschlusszusammenfassung

## Fortschrittslogik

Der Fluss darf Orientierung geben, aber keinen Druck.

Darum:

- jeder Schritt muss klar als kleiner Einzelschritt wirken
- Fortschritt nur schwach markieren
- kein Prozentbalken
- keine Zeitsprache

## Rueckwaertslogik

Ein Zurueck ist erlaubt, aber:

- nur ruhig
- ohne Verlustdramaturgie
- ohne dass mehrere alte Antworten erneut geprueft werden muessen

## Fehler- oder Stockungslogik

Wenn ein Lernender in Onboarding stockt, wird der Fluss nicht erweitert.

Stattdessen:

- Frage vereinfachen
- Beispiel geben
- Schritt kleiner machen

Nicht erlaubt:

- Zusatzfragen einfuegen
- Sonderdialoge aufmachen
- Supportlisten nachschieben

## Akzeptanzkriterien

Der Onboarding-Fluss gilt nur dann als korrekt, wenn:

1. er in maximal vier kleinen Schritten bleibt
2. jeder Schritt genau eine Entscheidung traegt
3. kein Schritt wie Diagnose, Test oder Formular wirkt
4. der erste Lernschritt schnell erreichbar bleibt
5. der Fluss keine Checkbox-Wand oder Setup-Optik entwickeln kann

## Naechste Ableitung

Wenn dieser Blueprint akzeptiert ist, folgt erst danach:

- ein `Onboarding Screen Sequence Spec`

und noch nicht:

- Mockup
- CSS
- Implementation
