# Cross Epoch Networking

## Ziel

Die Sammlung ist jetzt historisch breit genug. Der naechste Schritt ist daher nicht mehr `mehr Werke`, sondern `mehr Verbindung`.

MathTeach soll spaeter nicht nur sagen koennen, dass ein Werk existiert, sondern:

- aus welcher Linie ein Beweis stammt
- wie sich eine Gleichung sprachlich und symbolisch veraendert hat
- ueber welche Kommentare, Uebersetzungen und Lehrtexte Wissen weitergegeben wurde
- wie sich Fachgebiete ueber Epochen hinweg differenziert und wieder vernetzt haben
- welche spaeteren Anwendungen aus fruehen Ideen hervorgegangen sind

## Die erste Vernetzungsschicht

Die erste Schicht modelliert fuenf Typen von Linien:

1. `Proof Lines`
2. `Equation Lines`
3. `Transmission Paths`
4. `Domain Lines`
5. `Application Bridges`

Alle fuenf greifen auf denselben historischen Korpus zu, aber mit unterschiedlicher Frage.

## Line Types

### Proof Lines

Frage:

- Wie wurde etwas ueberhaupt beweisbar?

Beispiele:

- von Erschoepfung zu Integral
- von Gleichungsloesung zu Strukturbeweis
- von Axiomatik zu formaler Beweistheorie und Grenzen

### Equation Lines

Frage:

- Wie ist eine mathematische Form entstanden, notiert und standardisiert worden?

Beispiele:

- quadratische Gleichung
- Differential- und Integralnotation
- Wahrscheinlichkeits- und Mengen-Sprache

### Transmission Paths

Frage:

- Wer hat Wissen getragen, kommentiert, uebersetzt oder in Schulen verankert?

Beispiele:

- Euclid ueber Theon, Hypatia und Adelard
- indisch-arabische Zahlen ueber al-Khwarizmi und Fibonacci
- Archimedes ueber Eutocius in spaetere Analysisfamilien

### Domain Lines

Frage:

- Wie wurde aus einer Problemkultur ein Fachgebiet?

Beispiele:

- Algebra
- Geometrie
- Analysis
- Wahrscheinlichkeit
- Logik und Computation

### Application Bridges

Frage:

- Wie wurden mathematische Ideen spaeter zu Werkzeugen?

Beispiele:

- Himmelsmechanik
- Entscheidung und Spieltheorie
- algorithmische Verfahren bis Computability

## Laufzeitnutzen

Die Vernetzungsschicht ist kein Deko-Layer.

Sie soll spaeter direkt beeinflussen:

- Retrieval-Reihenfolge
- Auswahl historischer Beispiele
- Quellenpflicht pro Erklaerung
- Beweis- und Gleichungserzaehlungen
- adaptive Unterrichtspfade je nach Vorwissen

Wenn ein Lernender etwa nach dem Integral fragt, soll das System nicht nur eine Formel liefern, sondern bei Bedarf die Linie:

- `Archimedes -> Cavalieri -> Barrow -> Cauchy -> Lebesgue`

Wenn jemand nach Algorithmen fragt, soll das System die Linie:

- `al-Khwarizmi -> Viete -> Peano -> Church -> Turing`

ausspielen koennen.

## Repo-Artefakte

- [data/math_core/network_manifest.json](/Users/jonasweiss/MathTeach/data/math_core/network_manifest.json)
- [sql/005_cross_epoch_network.sql](/Users/jonasweiss/MathTeach/sql/005_cross_epoch_network.sql)
- [src/mathteach/services/corpus.py](/Users/jonasweiss/MathTeach/src/mathteach/services/corpus.py)
- [src/mathteach/main.py](/Users/jonasweiss/MathTeach/src/mathteach/main.py)

## Erste API

Die erste maschinenlesbare Vernetzung liegt unter:

- `GET /api/v1/corpus/network`

Diese API liefert zunaechst das Netzwerkmanifest.

Spaeter soll daraus ein echter traversierbarer Graph werden.
