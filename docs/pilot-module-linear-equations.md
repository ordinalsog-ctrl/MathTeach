# Pilot Module: Lineare Gleichungen

## Zweck

Dieses Dokument definiert das erste echte MathTeach-Pilotmodul, an dem
wir die weitere Produkt- und UI-Richtung pruefen.

Es ist kein allgemeiner Themenentwurf, sondern ein bewusster
Entscheidungstest.

Es soll zeigen:

- ob die aktuelle Tutorlogik ein reales Lernmodul schon tragen kann
- welche Teile fachlich, paedagogisch und psychologisch zwingend intern
  bleiben muessen
- welche Teile des illustrierten Lerntraegers sauber auslagerbar sind,
  ohne die Lehrentscheidung aus der Hand zu geben

## Warum dieses Modul

Als erster Testkorridor wird `lineare Gleichungen` gewaehlt.

Begruendung:

- das Thema liegt im `P0`-Kern aus
  [math-corpus-blueprint.md](/Users/jonasweiss/MathTeach/docs/math-corpus-blueprint.md)
- es passt direkt zur aktuellen Device-Lernansicht
- es braucht Illustration nicht als Dekoration, sondern als echten
  Beziehungstraeger
- es erlaubt eine saubere Verbindung von
  - frueher Algebra
  - symbolischer Uebersetzung
  - psychologischer Stabilisierung
  - optionaler historischer Vertiefung

## Quellenbasis

Dieser Modul-Blueprint ist aus diesen Repo-Grundlagen abgeleitet:

- [pedagogical-strategy-matrix.md](/Users/jonasweiss/MathTeach/docs/pedagogical-strategy-matrix.md)
- [universal-round-u1-program.md](/Users/jonasweiss/MathTeach/docs/universal-round-u1-program.md)
- [device-ui-evidence-matrix.md](/Users/jonasweiss/MathTeach/docs/device-ui-evidence-matrix.md)
- [device-learningscreen-contract.md](/Users/jonasweiss/MathTeach/docs/device-learningscreen-contract.md)
- [device-learningscreen-blueprint.md](/Users/jonasweiss/MathTeach/docs/device-learningscreen-blueprint.md)
- [rpi-touch-ui-lastenheft.md](/Users/jonasweiss/MathTeach/docs/rpi-touch-ui-lastenheft.md)
- [math-history-program.md](/Users/jonasweiss/MathTeach/docs/math-history-program.md)
- [math-corpus-blueprint.md](/Users/jonasweiss/MathTeach/docs/math-corpus-blueprint.md)

## Kernentscheidung dieses Moduls

Dieses Modul behandelt Illustration als `didaktischen Kern`, nicht als
optisches Finish.

Deshalb gilt:

- die Auswahl der visuellen Funktion bleibt intern
- die fachliche Sequenz bleibt intern
- die psychologische Wirkung bleibt intern
- die zeichnerische und asset-seitige Ausarbeitung kann ausgelagert
  werden

## Mathematisches Lernziel

Am Ende des Moduls soll der Lernende fuer einfache lineare Gleichungen
vom Typ

- `x + a = b`

verstehen:

1. warum beide Seiten einer Gleichung zusammengehoeren
2. warum dieselbe Operation auf beiden Seiten ausgefuehrt wird
3. wie aus einer zugrunde liegenden Beziehung eine kontrollierte
   Symbolumformung wird
4. wie ein einfacher Loesungsschritt sichtbar und nicht nur
   merkwuerdig-manipulativ erscheint

## Nicht-Ziele

Dieses Pilotmodul soll noch nicht:

- komplette Gleichungsfamilien erschlagen
- Textaufgaben voll behandeln
- negative Zahlen, Klammern und mehrere Umformungsschritte mischen
- Historie in einen eigenen Erzaehlpfad aufblasen
- Assessment- oder Pruefungsmodus simulieren

## Primaere Zielgruppen

Dieses Modul muss mindestens fuer diese drei Nutzungslagen tragen:

### 1. Fragile Aufmerksamkeit

Braucht:

- micro steps
- klaren Blickanker
- sichtbar kleine Veraenderungen
- keine Textwand vor dem mathematischen Kern

### 2. Symbolische Uebersetzungsprobleme

Braucht:

- Bedeutung vor Symbol
- Beziehung vor Regel
- Regel vor Umformung
- wiederholbare Rueckuebersetzung zwischen Bild und Gleichung

### 3. Lernen ohne Rueckendeckung

Braucht:

- hohe Vorhersagbarkeit
- wuerdevollen Ton
- null Beschamung
- sofort sichtbaren Sinn des naechsten Schritts

## Strategischer Lehrmodus

Aus der
[pedagogical-strategy-matrix.md](/Users/jonasweiss/MathTeach/docs/pedagogical-strategy-matrix.md)
folgt fuer diesen Seed standardmaessig:

- Unterrichtsmodus: `school_scaffolded_mode` mit Anteilen von
  `worked_example_mode`
- Tempo: `slow`
- Schrittgroesse: `micro` bis `small`
- Notationsdichte: `minimal` bis `reduced`
- Beispieltyp: `single_numeric` und `guided_symbolic`
- Historieneinsatz: `supporting`
- Feedback-Rhythmus: `every_step`
- Interventionsstil: `guiding`

## Historischer Einsatz

Die Historie ist in diesem Modul `supporting`, nicht primaer.

Das folgt aus:

- [pedagogical-strategy-matrix.md](/Users/jonasweiss/MathTeach/docs/pedagogical-strategy-matrix.md)
- [math-history-program.md](/Users/jonasweiss/MathTeach/docs/math-history-program.md)

Funktion der Geschichte hier:

- Gleichungen als kulturell entstandene Sprache zeigen
- die Idee von `balancing` und `restoring` nicht als reine
  Schulsynthaxe erscheinen lassen
- Interesse und Wuerde steigern, ohne die Hauptspur zu ueberladen

Empfohlener historischer Mini-Einsatz:

- sehr spaet im Modul oder als optionale Zusatzkarte
- al-Khwarizmi als Bruecke zur algebraischen Verfahrenssprache
- Fokus nicht auf Jahreszahlen, sondern auf:
  - welches Problem wurde bearbeitet
  - wie wurde Gleichung als Verfahren gedacht
  - wie wurde daraus unsere spaetere Standardform

## Screen-Korridor

Der erste echte Durchspielkorridor soll `7` Stationen haben.

## Station 1: Beziehung statt Formel

### Mathematische Hauptidee

Eine Gleichung ist eine Beziehung zwischen zwei Seiten.

### Psychologische Funktion

- Sicherheit durch sehr klare Ausgangsidee
- kein Eindruck, dass der Lernende schon eine Umformungsregel kennen
  muesste

### Paedagogische Funktion

- `Bedeutung vor Symbol`
- `Visual Bridge Strategy`

### Illustration muss leisten

- zwei Seiten als zusammengehoerig zeigen
- Gleichgewicht als ruhige Beziehung, nicht als hektisches Gadget
- keine dekorative Schuelerszene, sondern echte mathematische Struktur

### Ohne gute Illustration droht

- Symbolik startet zu frueh
- die Gleichung wirkt wie ein Code statt wie eine Beziehung

## Station 2: Erstes konkretes Beispiel

### Mathematische Hauptidee

`x + 3 = 7` ist dieselbe Beziehung in einfacher Symbolform.

### Psychologische Funktion

- kleiner erster Erfolg
- kein ueberraschender Formalisierungssprung

### Paedagogische Funktion

- Rueckbindung von Bild zu Symbol
- kontrollierte Einfuehrung von `x`

### Illustration muss leisten

- linke Seite als `unbekannt plus drei`
- rechte Seite als `sieben`
- beide Seiten muessen als dieselbe Situation lesbar bleiben

### Ohne gute Illustration droht

- `x` wird als willkuerliches Zeichen erlebt
- `+3` und `7` stehen beziehungslos nebeneinander

## Station 3: Warum derselbe Zug auf beiden Seiten

### Mathematische Hauptidee

Wenn wir die Beziehung erhalten wollen, behandeln wir beide Seiten mit
demselben Zug.

### Psychologische Funktion

- Fehlervermeidung durch Explizitheit
- keine Magie, kein “so macht man das eben”

### Paedagogische Funktion

- Regel wird aus Struktur begruendet
- nicht zuerst als auswendig zu lernende Vorschrift

### Illustration muss leisten

- denselben Zug links und rechts zeigen
- klein genug bleiben, damit der Blick nicht zerstreut
- idealerweise mit expliziter Operationszeile

### Ohne gute Illustration droht

- Umformen erscheint wie formale Trickserei
- Wiederholung wird sprachlich, aber nicht strukturell gestuetzt

## Station 4: Ergebniszeile

### Mathematische Hauptidee

Aus `x + 3 = 7` wird ueber denselben Zug `x = 4`.

### Psychologische Funktion

- echtes Kompetenzsignal
- sichtbare Loesung ohne Testcharakter

### Paedagogische Funktion

- Resultat als nachvollziehbarer Endzustand
- nicht als ploeztliches Endergebnis

### Illustration muss leisten

- Ergebnisspur aus demselben Traeger herleiten
- nicht neues Bild, sondern konsequente Fortsetzung

### Ohne gute Illustration droht

- das Resultat wirkt abgeschnitten oder “hingesprungen”

## Station 5: Nochmal-Korridor

### Mathematische Hauptidee

Dasselbe Problem kann kleiner gemacht werden, ohne ein neues Thema zu
starten.

### Psychologische Funktion

- Beschamung vermeiden
- Stockung als normal behandeln

### Paedagogische Funktion

- `verkleinern statt vergroessern`
- Wiederholung direkt am Kernschritt

### Illustration muss leisten

- dieselbe Struktur, aber expliziter
- Operationszeile und Resultatzeile noch deutlicher

### Ohne gute Illustration droht

- Recovery bleibt nur Text
- Wiederholung fuehlt sich wie Rueckschritt statt Hilfe an

## Station 6: Aehnliches Beispiel

### Mathematische Hauptidee

Dieselbe Regel kann an einer aehnlichen Gleichung wiedererkannt werden.

### Psychologische Funktion

- Transfer ohne Ueberforderung
- Variation ohne Themenbruch

### Paedagogische Funktion

- Struktur sehen, nicht nur Einzelfall merken

### Illustration muss leisten

- dieselbe Form an anderer Zahlensituation
- hinreichend aehnlich, aber nicht identisch

### Ohne gute Illustration droht

- Beispiel wirkt wie neues Thema
- Transfer wird sprachlich behauptet, aber nicht gesehen

## Station 7: Optionale History-/Wuerdekarte

### Mathematische Hauptidee

Gleichungen sind eine historische Problemlosesprache, nicht bloß
Schulsymbolik.

### Psychologische Funktion

- Wuerde
- Sinn
- Zugehoerigkeit zur Mathematik als Kulturleistung

### Paedagogische Funktion

- Interesse oeffnen, nicht Kernwissen verdraengen

### Illustration muss leisten

- kein Museumsornament
- sondern eine ruhige Bruecke von Problem, Sprache und Verfahren

### Ohne gute Illustration droht

- Geschichte wird bloße Zierde
- oder sie frisst die Hauptspur auf

## Modul-Pflichtregel fuer Illustrationen

Dieses Modul bestaetigt explizit die Regel aus
[rpi-touch-ui-lastenheft.md](/Users/jonasweiss/MathTeach/docs/rpi-touch-ui-lastenheft.md):

`Illustration ist Kernbestandteil`

Fuer lineare Gleichungen heisst das:

- Balance- oder Mengenmodell vor freier Charakter- oder Szenenillustration
- die Illustration muss eine mathematische Operation tragen
- dieselbe Illustration muss in Wiederholung und Beispiel variieren
  koennen
- sie ist kein Hintergrundbild, sondern Lerntraeger

## Interne vs. externe Verantwortung

## Muss intern bleiben

- Modulziel
- Screen-Reihenfolge
- mathematische Idee pro Station
- psychologische Funktion pro Station
- paedagogische Funktion pro Station
- Entscheidung, welche Illustration was leisten muss
- Entscheidung, welche Variationen `repeat` und `example` brauchen
- Entscheidung, wie viel Historie erlaubt ist

## Kann ausgelagert werden

- zeichnerischer Stil
- Vektor- und Farbproduktion
- Asset-Sauberkeit
- formale Varianten desselben didaktischen Motivs
- finale Animation oder Micro-Motion, falls spaeter gewuenscht

## Darf nicht ausgelagert werden

- ob Illustration nur Stimmung oder mathematische Funktion hat
- welche Struktur im Bild sichtbar sein muss
- welche Fehlvorstellung die Illustration korrigieren soll
- welche Recovery-Stufe die Illustration tragen muss

## Entscheidungstest nach dem Durchspiel

Nach dem ersten echten Durchspiel dieses Moduls muessen wir diese Fragen
beantworten:

1. Trägt die aktuelle Tutorlogik bereits einen echten Lernkorridor?
2. Welche Screens brechen ohne starke Illustration sofort ein?
3. Reicht es, nur Asset-Produktion auszulagern?
4. Oder ist die aktuelle UI-Struktur fuer illustrativen Lerninhalt noch
   zu arm?
5. Wie gross darf der historische Anteil sein, ohne den Kernkorridor zu
   schaedigen?

## Go/No-Go-Signale

### Go fuer externen Illustrations-Track

- wenn die didaktische Funktion je Screen intern klar benennbar ist
- wenn die mathematische Struktur im Storyboard stabil ist
- wenn der Unterschied zwischen `Standard`, `Nochmal` und `Beispiel`
  fachlich klar spezifiziert werden kann

### No-Go fuer blosse Auslagerung

- wenn wir noch nicht sagen koennen, was die Illustration pro Screen
  genau lehren soll
- wenn Historie und Kernlernen noch nicht sauber getrennt sind
- wenn der aktuelle UI-Traeger noch keine klare Asset-Funktion hat

## Empfohlener naechster Arbeitsschritt

Direkt aus diesem Dokument folgt:

1. eine `Illustration Brief` fuer dieses Modul
2. danach ein `Module Throughplay Script`
3. erst dann die Entscheidung, wie weit der Illustrations-Track extern
   wird
