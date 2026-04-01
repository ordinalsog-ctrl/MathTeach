# Math Corpus Blueprint

## Ziel

Wir beginnen nicht mit beliebigen Mathetexten, sondern mit einer kontrollierten Grundsammlung.

Diese Sammlung soll:

- fachlich breit genug fuer spaetere Schul-, Hochschul- und Expertenpfade sein
- zitierbar und segmentierbar bleiben
- historische Linien spaeter erweiterbar machen
- auf Standardquellen aufbauen, bevor Spezialliteratur hinzukommt

## Was wir zuerst sammeln

Die erste Mathe-Datenbank beginnt mit dem Kern, nicht mit der Vollstaendigkeit.

Prioritaet `P0`:

- Arithmetik und Zahlverstaendnis
- Algebraische Grundlagen
- Geometrie und Messen
- Funktionen und Vorkalkuel

Prioritaet `P1`:

- Analysis und Differentialrechnung
- Lineare Algebra
- Diskrete Mathematik
- Wahrscheinlichkeit und Statistik

Prioritaet `P2`:

- Differentialgleichungen
- Zahlentheorie
- Abstrakte Algebra

Prioritaet `P3`:

- Topologie
- Differentialgeometrie
- Mass- und Funktionalanalysis
- Forschungsspezifische Spezialgebiete

## Quellenfamilien

Wir sammeln nicht nur "Buecher", sondern klar getrennte Quellenfamilien:

- historische Primaerwerke
- moderne Standardlehrbuecher
- Problem- und Uebungssammlungen
- Survey- und Referenztexte
- Curriculum- und Lehrplanreferenzen

## Warum diese Reihenfolge?

Die spaetere Lehrerfigur braucht ein starkes stabiles Fundament.

Darum sammeln wir zuerst Quellen, die:

- Begriffe sauber definieren
- Voraussetzungsketten sichtbar machen
- Standardnotation stabil halten
- viele spaetere Themen tragen

## Nicht im ersten Schritt

Noch nicht Teil dieser ersten Sammlung:

- paedagogische Literatur
- psychologische Literatur
- motivationale und coaching-orientierte Literatur
- freie Erklaerblogs ohne klaren Quellenstatus

Diese Bereiche kommen spaeter in den `Teacher Mind`, nicht in den `Knowledge Core`.

## Technische Sammelreihenfolge

1. Quellenfamilien definieren
2. Domainen und Prioritaeten definieren
3. Collection-Queue anlegen
4. Quellenkandidaten sammeln
5. Dokumente segmentieren
6. Begriffe, Gleichungen, Theoreme und Anwendungen extrahieren
7. Zitationspfade und Wissenskanten aufbauen

## Artefakte im Repo

- [data/math_core/foundation_manifest.json](/Users/jonasweiss/MathTeach/data/math_core/foundation_manifest.json)
- [sql/002_math_corpus_collection.sql](/Users/jonasweiss/MathTeach/sql/002_math_corpus_collection.sql)
- [src/mathteach/services/corpus.py](/Users/jonasweiss/MathTeach/src/mathteach/services/corpus.py)
