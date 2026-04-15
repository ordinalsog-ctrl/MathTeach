# Pilot Module Throughplay Script: Lineare Gleichungen

## Zweck

Dieses Dokument ist das konkrete Durchspielskript fuer das erste echte
MathTeach-Pilotmodul
[pilot-module-linear-equations.md](/Users/jonasweiss/MathTeach/docs/pilot-module-linear-equations.md).

Es beantwortet nicht mehr nur:

- was das Modul leisten soll

sondern:

- was der Tutor in welcher Station konkret sagt
- was der Screen dabei zeigt
- welche Illustration genau gebraucht wird
- welche Lernreaktion wir erwarten
- an welchem Punkt wir ueber UI-, Asset- oder Modulrichtung
  entscheiden

## Rolle im Testprozess

Dieses Script ist der operative Testpfad zwischen:

- fachlichem Modul-Blueprint
- Illustrationsbrief
- spaeterem echtem Schuelertest

Es ist damit das erste Dokument, das wir unmittelbar “durchspielen”
koennen.

## Quellenbasis

Dieses Throughplay-Script ist direkt aus diesen Repo-Artefakten
abgeleitet:

- [pilot-module-linear-equations.md](/Users/jonasweiss/MathTeach/docs/pilot-module-linear-equations.md)
- [pilot-module-linear-equations-illustration-brief.md](/Users/jonasweiss/MathTeach/docs/pilot-module-linear-equations-illustration-brief.md)
- [device-learningscreen-contract.md](/Users/jonasweiss/MathTeach/docs/device-learningscreen-contract.md)
- [device-learningscreen-blueprint.md](/Users/jonasweiss/MathTeach/docs/device-learningscreen-blueprint.md)
- [device-ui-evidence-matrix.md](/Users/jonasweiss/MathTeach/docs/device-ui-evidence-matrix.md)
- [pedagogical-strategy-matrix.md](/Users/jonasweiss/MathTeach/docs/pedagogical-strategy-matrix.md)
- [universal-round-u1-program.md](/Users/jonasweiss/MathTeach/docs/universal-round-u1-program.md)

## Nicht verhandelbare Spielregeln

Bei jedem Durchspiel dieses Moduls gilt:

- genau eine mathematische Idee pro Station
- Bedeutung oder Struktur vor Symbolverdichtung
- kein Testton
- keine Beschamung
- Recovery verkleinert den Schritt
- Illustration ist Lerntraeger, nicht Hintergrund

## Durchspielmodus fuer Pilot 1

Fuer den ersten echten Test wird dieses Modul so gespielt:

- Unterrichtsmodus: `school_scaffolded_mode`
- Schrittgroesse: `micro`
- Notationsdichte: `minimal` bis `reduced`
- Beispieltyp: `single_numeric` und spaeter `guided_symbolic`
- Historieneinsatz: `supporting`
- Feedback-Rhythmus: `every_step`
- Interventionsstil: `guiding`

## Teststruktur

Der Test hat `7` Kernstationen und `3` Entscheidungstore.

Die Entscheidungstore sind nicht Teil des Lernflusses fuer den
Lernenden, sondern interne Evaluationspunkte fuer uns.

## Station 1: Beziehung statt Formel

### Tutor sagt

`Wir schauen zuerst nur darauf, dass beide Seiten zusammengehoeren.`

`Noch keine Regel. Noch keine Umformung. Erst die Beziehung.`

### Screen muss zeigen

- eine ruhige Hauptflaeche
- eine visuelle Beziehung zwischen zwei Seiten
- noch keinen Operationsschritt

### Illustration muss zeigen

- zwei Seiten gehoeren zusammen
- keine Seite ist “wichtiger”
- die Beziehung ist stabil und ruhig

### Lernreaktion, die wir erwarten

- der Lernende versteht, dass Gleichung nicht nur aus Symbolen besteht
- keine Angst vor “ich kann das noch nicht”

### Warnsignal

- der Lernende sagt oder zeigt, dass `=` nur wie ein Trennzeichen wirkt

## Station 2: Gleichung in einfacher Symbolform

### Tutor sagt

`Jetzt schreiben wir dieselbe Beziehung als kleine Gleichung.`

`Links steht etwas Unbekanntes und noch drei dazu. Rechts steht sieben.`

### Screen muss zeigen

- die gleiche Beziehung wie in Station 1
- jetzt mit `x + 3 = 7`
- keine zweite Hauptidee

### Illustration muss zeigen

- `x` als unbekannte Groesse
- `+ 3` als reale Zusatzmenge oder Zusatzlast
- `7` als klares Gegenueber

### Lernreaktion, die wir erwarten

- der Lernende kann die Symbolzeile auf die sichtbare Beziehung zurueckbinden

### Warnsignal

- `x` wird als willkuerlicher Buchstabe erlebt
- `3` und `7` stehen fuer den Lernenden nur nebeneinander

## Station 3: Derselbe Zug auf beiden Seiten

### Tutor sagt

`Wenn wir die Beziehung erhalten wollen, machen wir auf beiden Seiten denselben Zug.`

`Wir nehmen nicht nur irgendwo etwas weg. Wir halten die Beziehung im Gleichgewicht.`

### Screen muss zeigen

- Hauptgleichung bleibt sichtbar
- Operationsspur wird eingefuehrt
- Blick bleibt auf genau einem Zug

### Illustration muss zeigen

- `-3` links und `-3` rechts
- dieselbe Operation auf beiden Seiten
- keine aggressive Pfeil- oder Effektlogik

### Lernreaktion, die wir erwarten

- der Lernende kann die Regel begruenden, nicht nur nachsprechen

### Warnsignal

- der Lernende erlebt den Schritt als “Zaubertrick”

## Station 4: Resultat aus derselben Struktur

### Tutor sagt

`Jetzt sehen wir, was nach diesem einen Zug uebrig bleibt.`

`Links bleibt nur noch x. Rechts bleibt vier.`

### Screen muss zeigen

- Hauptgleichung
- Operationsspur
- Resultatspur

### Illustration muss zeigen

- das Ergebnis kommt aus demselben Traeger
- keine neue Szene

### Lernreaktion, die wir erwarten

- sichtbarer Verstehensmoment
- der Endzustand fuehlt sich hergeleitet an

### Warnsignal

- der Lernende akzeptiert `x = 4`, kann aber nicht sagen warum

## Entscheidungstor A: Traegt der Kern ohne Historie?

Nach Station 4 pruefen wir intern:

1. War die mathematische Hauptidee in allen vier ersten Stationen klar?
2. War die Illustration in jeder Station funktional oder nur hilfreich?
3. Koennte man irgendeine dieser vier Stationen ohne starke Illustration
   mit gleichem Lernwert tragen?

Wenn `nein`, ist der Illustrationspfad fuer das Modul kein Nebenpfad,
sondern Kernproduktion.

## Station 5: Recovery / Nochmal

### Ausloeser

- der Lernende stockt
- der Lernende will `Nochmal`
- Blick oder Sprache zeigen Unsicherheit

### Tutor sagt

`Wir machen genau diesen einen Schritt noch kleiner.`

`Wir bleiben bei derselben Gleichung. Wir machen nur die Operation deutlicher.`

### Screen muss zeigen

- dieselbe Gleichung
- explizitere Operationszeile
- explizitere Resultatzeile
- kein neues Thema

### Illustration muss zeigen

- dieselbe Struktur
- weniger implizite Logik
- kleinere, deutlichere Teilhandlung

### Lernreaktion, die wir erwarten

- der Lernende erlebt Recovery als Hilfe, nicht als Rueckstufung

### Warnsignal

- Recovery fuehlt sich wie “Zurueck auf Anfang” an
- oder vergroessert den Screen statt den Schritt

## Station 6: Aehnliches Beispiel

### Ausloeser

- der Lernende will ein Beispiel
- Struktur ist noch nicht stabil

### Tutor sagt

`Wir sehen dieselbe Regel jetzt an einer aehnlichen Gleichung.`

`Nicht neues Thema. Nur dieselbe Struktur mit anderen Zahlen.`

### Screen muss zeigen

- `5 + 2 = 7`
- `-2 / -2`
- `5 = 5`

### Illustration muss zeigen

- gleiche Form, andere Zahlen
- gleiche Regel, andere sichtbare Instanz

### Lernreaktion, die wir erwarten

- der Lernende erkennt dieselbe Regel wieder

### Warnsignal

- das Beispiel fuehlt sich wie Themenwechsel an

## Entscheidungstor B: Reicht unsere aktuelle UI-Struktur?

Nach Station 6 pruefen wir intern:

1. Wirkt der primäre Träger schon wie ein echter illustrativer Lerntraeger?
2. Oder wirkt er immer noch wie eine UI-Flaeche, die bloss guten Text
   traegt?
3. Sind `Standard`, `Nochmal`, `Beispiel` ausreichend unterscheidbar?
4. Oder braucht das Modul zwingend einen separaten, staerkeren
   Asset-Track, bevor es wirklich lebendig wird?

Wenn `die UI-Flaeche traegt nicht`, ist die Antwort nicht mehr
“weiter CSS”, sondern `Illustrationsproduktion parallelisieren`.

## Station 7: History-Sidecar

### Optionalitaet

Diese Station ist optional und darf den Kernfluss nicht blockieren.

### Tutor sagt

`Diese Gleichungssprache ist nicht einfach vom Himmel gefallen.`

`Menschen haben Wege gesucht, Probleme Schritt fuer Schritt in eine loesbare Form zu bringen.`

### Screen muss zeigen

- kleine, leise Zusatzkarte oder Zusatzstation
- keine zweite Hauptszene
- keine Ueberladung

### Illustration muss zeigen

- Problem -> Verfahren -> Notation
- nicht primär Personenkult

### Historischer Kern

Empfohlene Mini-Referenz:

- al-Khwarizmi als Bruecke zur algebraischen Verfahrenssprache

### Lernreaktion, die wir erwarten

- Wuerde
- Sinn
- groessere Ernsthaftigkeit des Themas

### Warnsignal

- Historie verdrängt das Kernverstehen
- oder wirkt wie ein beliebiger Schulbuchkasten

## Entscheidungstor C: Auslagerungsentscheidung

Nach dem gesamten Durchspiel muessen wir diese Fragen beantworten:

### 1. Was bleibt intern?

Zwingend intern bleiben:

- Moduldramaturgie
- Tutor-Sprache
- Recovery-Logik
- mathematische Carrier-Struktur
- Historiengewichtung
- didaktische Funktion jeder Illustration

### 2. Was darf extern produziert werden?

Externe Produktion ist sinnvoll fuer:

- Linien- und Formensprache
- Asset-Familien
- SVG-/Vektorproduktion
- Variantenbildung
- spaetere Motion

### 3. Was darf nicht in externe Hande rutschen?

- welche Struktur im Bild sichtbar sein muss
- wie Recovery kleiner gemacht wird
- wie Beispielvariation aussieht
- welche historische Mini-Szene semantisch leiser bleiben muss

## Durchspielprotokoll fuer den ersten Test

Beim ersten echten Durchgang halten wir pro Station kurz fest:

1. `Verstanden?`
2. `Wo stockt es?`
3. `War Illustration tragend oder austauschbar?`
4. `War der Tutor-Ton stabil?`
5. `War die Station zu gross fuer einen Screen?`

## Aktuelle Konsequenz fuer unsere weitere Arbeit

Dieses Throughplay-Script ist bewusst auch ein Richtungsfilter fuer die
naechsten Wochen.

Wenn das Durchspiel zeigt, dass:

- die Sequenz fachlich und paedagogisch bereits traegt
- die aktuelle Device-UI den Kernfluss tragen kann
- aber die illustrierten Carrier noch nicht stark genug sind

dann ist die richtige Reaktion nicht:

- mehr freie UI-Politur

sondern:

- die Fach-, Psychologie- und Tutorarbeit intern weiter vertiefen
- den Illustrationstrack separat organisieren
- und die Asset-Produktion an einen klaren didaktischen Brief koppeln

Wenn das Durchspiel dagegen zeigt, dass schon die Sequenz selbst
stockt, muss zuerst das Modul intern nachgeschaerft werden, bevor
Illustrationsproduktion skaliert wird.

## Erfolgssignale

Das Modul ist auf gutem Weg, wenn:

- der Lernende die Beziehung hinter der Gleichung benennen kann
- `derselbe Zug auf beiden Seiten` nicht wie auswendig gelernter Satz
  wirkt
- `repeat` als Hilfe und nicht als Niederlage erlebt wird
- `example` als Strukturtransfer und nicht als Themenbruch erlebt wird
- Historie optional bleibt und trotzdem Wuerde erzeugt

## Abbruchsignale

Wir muessen die Richtung korrigieren, wenn:

- Illustration nur Stimmung liefert, aber keine Operation traegt
- die UI die Asset-Funktion sichtbar einengt
- Historie den Kernkorridor verwischt
- Recovery den Screen wieder lauter oder komplexer macht

## Naechste Artefakte nach diesem Script

Wenn dieses Throughplay-Script steht, folgen sinnvollerweise:

1. `Asset Mapping Sheet`
   - welches Asset an welche Station
2. `Tutor utterance pack`
   - feiner ausformulierte Tutor-Stimme
3. `First live test protocol`
   - Beobachtung und Auswertung fuer eine reale Lernperson
