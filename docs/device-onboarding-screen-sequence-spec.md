# Device Onboarding Screen Sequence Spec

## Zweck

Dieses Dokument legt die konkrete Reihenfolge der ersten echten
Onboarding-Screens fuer das Device fest.

Es ist die direkte Ableitung aus:

- [device-onboarding-contract.md](/Users/jonasweiss/MathTeach/docs/device-onboarding-contract.md)
- [device-onboarding-flow-blueprint.md](/Users/jonasweiss/MathTeach/docs/device-onboarding-flow-blueprint.md)
- [device-ui-evidence-matrix.md](/Users/jonasweiss/MathTeach/docs/device-ui-evidence-matrix.md)

Es beantwortet nur:

`Welche Onboarding-Screens darf die erste Device-Implementierung
ueberhaupt haben, in welcher Reihenfolge kommen sie und welche einzige
kleine Entscheidung traegt jeder Screen?`

Es ist absichtlich:

- kein Mockup
- kein CSS-Briefing
- kein UI-Code

## Hauptregel

Die erste Device-Onboarding-Implementierung benutzt die `Kurzform`.

Der Grund ist fachlich, nicht nur pragmatisch:

- geringste Einstiegslast
- schnellster Weg zum ersten echten Lernschritt
- geringstes Risiko fuer Formular- oder Profilbogen-Charakter

Darum ist die erste verbindliche Zielsequenz:

1. `Womit willst du anfangen?`
2. `Soll ich mit Bild oder mit Worten starten?`
3. `Dann starten wir`

## Warum nicht die grosse Variante

Die laengere Standardfolge aus dem Flow-Blueprint bleibt fachlich
zulaessig, ist aber nicht die bevorzugte erste Device-Umsetzung.

Fuer die erste Version wird bewusst ausgeschlossen:

- eigener Erklaerscreen nur fuer `Warum ich frage`
- eigener Screen fuer `Schrittgroesse`
- jede fruehe Support-Mehrfachabfrage

Begruendung:

- der erste Device-Prototyp braucht einen moeglichst kurzen Pfad zur
  ersten Session
- `Schrittgroesse` und feinere Support-Anpassung koennen spaeter adaptiv
  oder in ruhiger Nachkonfiguration folgen

## Verbindliche Sequenz

## Screen 1: Startgegenstand

### Leitfrage

`Womit willst du anfangen?`

### Einzige kleine Entscheidung

- erster Lerngegenstand

### Erlaubte Eingabeform

- genau `1` kurzes Eingabefeld

### Muss

- direkt lernrelevant sein
- den ersten Startgegenstand klaeren
- einen kurzen Erklaersatz tragen, warum gefragt wird

### Darf nicht

- Themenkatalog werden
- mehrere Felder parallel zeigen
- Niveau, Profil, Support oder Verlauf gleichzeitig abfragen

### Sichtbares Minimalbudget

- `1` Frage
- `1` kurzer Erklaersatz
- `1` Eingabefeld
- `1` primaerer Weiter-CTA
- optional `1` schwache Zurueck-Aktion

### Beispielcharakter

- Frage:
  `Was willst du gerade verstehen?`
- Erklaersatz:
  `Ich frage nur, womit wir ruhig beginnen sollen.`

## Screen 2: Darstellungsstart

### Leitfrage

`Soll ich mit Bild oder mit Worten starten?`

### Einzige kleine Entscheidung

- erste Darstellungsform

### Erlaubte Eingabeform

- genau `2` gleichartige Optionen

### Muss

- nur diese eine Entscheidung enthalten
- alltagssprachlich bleiben
- sichtbar machen, dass es nur um den Start der Erklaerung geht

### Darf nicht

- gleichzeitig Schrittgroesse abfragen
- Supportlisten oder Checkboxen anzeigen
- klinische oder diagnostische Sprache tragen

### Sichtbares Minimalbudget

- `1` Frage
- `1` kurzer Erklaersatz
- `2` Antwortoptionen
- `1` primaerer Weiter-CTA
- optional `1` schwache Zurueck-Aktion

### Beispielcharakter

- Frage:
  `Wie soll ich anfangen?`
- Optionen:
  `Mit einem Bild`
  `Mit Worten`

## Screen 3: Startfreigabe

### Leitfrage

Keine neue echte Frage.

### Einzige kleine Entscheidung

- `jetzt starten`

### Funktion

- den Onboarding-Fluss schliessen
- die erste Session freigeben

### Muss

- sehr kurz bleiben
- nicht wie Zusammenfassungsformular wirken
- direkt in den ersten Lernschritt fuehren

### Darf nicht

- alle Antworten noch einmal als Liste aufblasen
- weitere Entscheidungen oeffnen
- nachtraeglich Support- oder Profillogik einfuegen

### Sichtbares Minimalbudget

- `1` kurze Bestaetigungszeile
- `1` primaerer Start-CTA
- optional `1` ruhige Zurueck-Aktion

### Beispielcharakter

- Bestaetigung:
  `Gut, wir beginnen genau so.`
- CTA:
  `Jetzt starten`

## Was in der ersten Sequenz bewusst fehlt

Folgende Inhalte sind fuer die erste Device-Onboarding-Sequenz
ausdruecklich ausgeschlossen:

- Name als eigener Pflichtschritt
- Niveau-/Klassenstufen-Auswahl
- `kleine Schritte / ausgewogen / direkt` als eigener Screen
- Support-Checkboxgruppen
- Mehrfachauswahl ueber Hilfsformen
- grosse Abschlusszusammenfassung

## Begruendung dieser Ausschluesse

Diese Inhalte sind nicht wertlos, aber fuer den ersten Onboarding-Pfad
nicht primaer.

Sie wuerden das Risiko erhoehen fuer:

- Formularcharakter
- Diagnose-/Profilbogen-Gefuehl
- zu hohe Einstiegslast
- falsche Endgueltigkeit

## Fortschrittslogik

Die Sequenz darf nur eine sehr schwache Orientierung tragen.

Erlaubt:

- ruhiger Schrittindikator wie `1 von 3`

Nicht erlaubt:

- Prozentbalken
- "fast geschafft"
- Leistungs- oder Tempo-Sprache

## Rueckwaertslogik

Auf jedem Schritt ist nur eine schwache Rueck-Aktion zulaessig.

Sie darf:

- ruhig sein
- nicht wie Abbruch wirken

Sie darf nicht:

- als zweite Hauptentscheidung konkurrieren

## Aktueller Gap zum bestehenden UI-Stand

Der aktuelle Onboarding-Screen in
[device.html](/Users/jonasweiss/MathTeach/src/mathteach/ui/device.html)
verletzt diese Sequence Spec deutlich, weil er heute gleichzeitig
enthaelt:

- Name
- Niveau
- Startgegenstand
- Darstellungswahl
- Schrittgroesse
- Support-Checkboxen

Das ist fuer die erste evidenzgebundene Onboarding-Implementierung zu
viel.

## Konsequenz fuer den naechsten echten UI-Schritt

Der naechste Onboarding-Umbau darf nicht "ein bisschen aufraeumen".

Er muss die aktuelle Ein-Flaechen-Onboarding-Ansicht strukturell in
diese drei kleinen Schritte zerlegen.

## Akzeptanzkriterien

Die erste Onboarding-Sequenz gilt nur dann als korrekt, wenn:

1. sie genau drei kleine Screens hat
2. jeder Screen genau eine kleine Entscheidung traegt
3. kein Screen wie Formular oder Profilbogen wirkt
4. keine Support-Checkboxen oder Mehrfachlisten sichtbar sind
5. der erste Lernschritt direkt nach Screen 3 beginnt

## Folgeschritt

Der naechste saubere Schritt ist jetzt:

- `Onboarding Step Wire Contracts`

Also:

- je ein Wire Contract fuer Screen 1, 2 und 3
- noch ohne UI-Code
- erst danach der echte Onboarding-Umbau
