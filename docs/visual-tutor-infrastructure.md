# Visual Tutor Infrastructure

## Zweck

Dieses Dokument beschreibt die eigentliche grafische Infrastruktur fuer
MathTeach.

Es beantwortet nicht:

- wie ein einzelnes Bild aussehen koennte
- welche Farbe gerade gefaellt
- welcher Illustrationsstil “huebsch” wirkt

Es beantwortet:

- wie das vorhandene mathematische Fundamentwissen
- das paedagogische Tutorwissen
- und das psychologische Sicherheitswissen

in eine belastbare visuelle Lehrstruktur uebersetzt werden.

## Ausgangspunkt

MathTeach hat das `Gehirn` bereits:

- mathematisches Fundamentwissen
- historische Linien
- Tutor-Sprache
- psychologische Schutzlogik
- paedagogische Moduswahl

Der fehlende Layer ist nicht einfach “mehr Illustration”.

Der fehlende Layer ist:

`Wie wird dieselbe Tutor-Intelligenz systematisch sichtbar?`

## Nicht verhandelbare Hauptregel

MathTeach illustriert nicht von Bildern aus.

MathTeach illustriert von `Lehrfunktionen` aus.

Das bedeutet:

- zuerst Tutor-Absicht
- dann visuelle Semantik
- dann epochale Einfärbung
- dann modulbezogene Asset-Produktion

Nicht umgekehrt.

## Uebersetzungskette

Die richtige Pipeline ist:

1. `Tutor brain`
2. `didaktische Funktion`
3. `visueller Carrier`
4. `Carrier-Zustand`
5. `epochale Darstellungslogik`
6. `modulspezifisches Asset`
7. `grafische Ausfuehrung`

## Layer 1: Invariante psychologische Regeln

Diese Regeln gelten ueber alle Themen und Epochen hinweg:

- Bedeutung vor Symbol
- ein Gedanke pro Screen
- Recovery verkleinert den Schritt
- kein Testton
- keine Beschamung
- keine dekorative Illustration ohne mathematische Funktion
- sichtbare Autonomie ohne Navigationschaos
- ruhiger, wuerdevoller Carrier statt App- oder Dashboard-Anmutung

Diese Regeln kommen direkt aus:

- [universal-round-u1-program.md](/Users/jonasweiss/MathTeach/docs/universal-round-u1-program.md)
- [pedagogical-strategy-matrix.md](/Users/jonasweiss/MathTeach/docs/pedagogical-strategy-matrix.md)
- [device-ui-evidence-matrix.md](/Users/jonasweiss/MathTeach/docs/device-ui-evidence-matrix.md)
- [rpi-touch-ui-lastenheft.md](/Users/jonasweiss/MathTeach/docs/rpi-touch-ui-lastenheft.md)

## Layer 2: Visuelle Carrier-Grammatik

MathTeach braucht nicht nur Bilder, sondern eine kleine Familie
wiederkehrender visueller Carrier.

Jeder Carrier steht fuer eine bestimmte Lehrfunktion.

## Carrier A: Relationship Carrier

### Funktion

- Zugehoerigkeit zweier Seiten
- Struktur vor Regel
- Beziehung vor Symbol

### Geeignet fuer

- fruehe Algebra
- Gleichungen
- Verhaeltnisse
- Gegenüberstellungen

### Psychologische Wirkung

- Sicherheit
- keine Ueberrumpelung
- “ich darf erst sehen, bevor ich rechnen muss”

## Carrier B: Quantity Carrier

### Funktion

- Menge, Groesse, Gruppierung, Zusatz

### Geeignet fuer

- Arithmetik
- Dyskalkulie-nahe Unterstuetzung
- Zahlverstaendnis
- Stellenwert

### Psychologische Wirkung

- konkrete Verankerung
- weniger Symbolangst

## Carrier C: Operation Carrier

### Funktion

- kontrollierter Eingriff
- sichtbarer gleicher Zug
- kein Trickeffekt

### Geeignet fuer

- Umformung
- Ableitung kleiner Rechenschritte
- Transformationen

### Psychologische Wirkung

- Verstehbarkeit statt Magie

## Carrier D: Result Carrier

### Funktion

- Ergebnis als Folge
- sichtbarer Endzustand aus derselben Struktur

### Geeignet fuer

- Gleichungsergebnis
- Zwischenresultate
- kleinere Kompetenzsignale

### Psychologische Wirkung

- Kompetenz ohne Testcharakter

## Carrier E: Transfer Carrier

### Funktion

- gleiche Struktur, andere Instanz
- Beispiel ohne Themenwechsel

### Geeignet fuer

- `Nochmal`
- `Beispiel`
- Generalisierung

### Psychologische Wirkung

- Wiedererkennen statt Neubedrohung

## Carrier F: Proof Carrier

### Funktion

- Beweisarchitektur
- Schrittfolge
- Warum statt nur Was

### Geeignet fuer

- Geometrie
- axiomatische Linien
- klassische Beweise
- moderne Strukturbeweise

### Psychologische Wirkung

- Ernsthaftigkeit
- Orientierung
- Wuerde des Denkens

## Carrier G: Notation Evolution Carrier

### Funktion

- historische Entwicklung einer Schreibweise sichtbar machen

### Geeignet fuer

- Algebra
- Differentialnotation
- Integralnotation
- Wahrscheinlichkeitsnotation

### Psychologische Wirkung

- Symbole sind gemacht, nicht natürlich vom Himmel gefallen

## Carrier H: Transmission Carrier

### Funktion

- Weitergabe, Uebersetzung, Kommentar, Tradition

### Geeignet fuer

- historische Mathematik
- Epochenwechsel
- kulturelle Bruecken

### Psychologische Wirkung

- Zugehoerigkeit zur Mathematik als Kulturleistung

## Carrier I: Application Bridge Carrier

### Funktion

- mathematische Idee -> reale oder spaetere Anwendung

### Geeignet fuer

- Analysis
- Wahrscheinlichkeit
- moderne Mathematik

### Psychologische Wirkung

- Sinn
- Relevanz
- Motivation

## Carrier-Zustaende

Jeder Carrier braucht mindestens diese Zustandslogik:

- `intro`
- `standard`
- `repeat`
- `example`
- optional `history_sidecar`

Wichtig:

- `repeat` ist nie nur farblich anders
- `example` ist nie nur dieselbe Szene mit anderer Farbe
- `history_sidecar` ist nie Haupttraeger

## Layer 3: Epochenlogik

Carrier allein reichen nicht.

Dieselbe Mathematik wird je nach Epoche anders sichtbar:

- andere Problemform
- andere Materialitaet
- andere Notationslage
- andere historische Wuerdeebene

Darum braucht MathTeach fuer jede Epoche eine eigene visuelle
Uebersetzungsschicht.

Diese liegt nicht unterhalb der Carrier, sondern oberhalb:

`Carrier bleibt gleich, Epoche faerbt ihn historisch und inhaltlich ein.`

## Layer 4: Modul- und Erklaerungslogik

Erst nach Carrier und Epoche kommt das einzelne Modul.

Beispiel `lineare Gleichungen`:

- Relationship Carrier
- Quantity Carrier
- Operation Carrier
- Result Carrier
- Transfer Carrier
- optional History Sidecar

Beispiel `Integral` spaeter:

- Problem-/Flaechen-Carrier
- Approximation Carrier
- Notation Evolution Carrier
- Application Bridge Carrier

## Produktionsschnitt

Die Reihenfolge fuer reale Produktion sollte immer sein:

1. visuelle Infrastruktur festlegen
2. Epoche festlegen
3. Modul bestimmen
4. Stationen bestimmen
5. Asset-Familien bestimmen
6. erst dann extern illustrieren

## Was intern bleiben muss

Intern bleiben zwingend:

- welche Carrier es gibt
- wann welcher Carrier benutzt wird
- wann `repeat` statt `example` gilt
- wann Historie Sidecar ist
- welche mathematische Beziehung sichtbar sein muss
- welche psychologische Wirkung noetig ist

## Was extern produziert werden darf

Extern produziert werden darf:

- Liniencharakter
- Materialanmutung
- Farbtextur
- Formenfamilie
- Vektorproduktion
- Bewegungsvarianten

## Naechster richtiger Schritt

Aus dieser Infrastruktur muessen jetzt zwei operative Dokumente folgen:

1. `Epoch Visual Translation Program`
2. `Topic / Module Visual Production Sheet`

Erst dann macht ein grosser externer Illustrationstrack wirklich Sinn.
