# Epoch Asset Family Sheet: Antiquity

## Zweck

Dieses Dokument uebersetzt den
[epoch-antiquity-visual-brief.md](/Users/jonasweiss/MathTeach/docs/epoch-antiquity-visual-brief.md)
in konkrete visuelle Asset-Familien fuer die antike Epoche.

Es ist kein Styleboard.

Es legt fest:

- welche Asset-Familien fuer Antiquity gebraucht werden
- welche mathematische Funktion sie haben
- welche psychologische Wirkung sie tragen
- was extern frei bleibt
- was intern fest bleibt

## Hauptregel

Auch in Antiquity gilt:

- jedes Asset ist Lehrwerkzeug
- kein Asset ist bloßer Epochen-Schmuck

## Asset A1: Counting and Grouping Carrier

### Einsatz

- fruehe Zahlverstaendnis-Themen
- Rhind / fruehe Arithmetik / Gruppierung
- Vorstufen von Stellen- und Mengenverstaendnis

### Muss sichtbar machen

- Zahl als Gruppe oder Anordnung
- gleiche Einheiten als zählbare Struktur
- Vergleich von Gruppen

### Muss vermeiden

- nur moderne Ziffernwand
- dekorative Alttextur ohne Mengensicht

### Extern frei

- Markerform
- Linien- und Materialanmutung

## Asset A2: Ratio and Shape Carrier

### Einsatz

- Pythagoreische oder geometrische Verhaeltnisse
- Seiten- und Flaechenbeziehungen

### Muss sichtbar machen

- Formbeziehung
- Teil-Ganzes-Ordnung
- Vergleich von Längen, Flaechen oder Segmenten

### Muss vermeiden

- Formel zuerst
- Zahlenetiketten ohne Formtraeger

## Asset A3: Euclidean Proof Carrier

### Einsatz

- Euclid
- Propositionen
- Beweisordnung

### Muss sichtbar machen

- Figur
- markierte Teilrelationen
- begrenzte Beweisschrittfolge

### Muss vermeiden

- moderne Schulbeweistafel
- ueberladene Vollfigur mit allen Hilfslinien gleichzeitig

### Intern fest

- Proof Carrier bleibt der Haupttraeger
- Schrittfolge muss begrenzt und lesbar bleiben

## Asset A4: Construction Carrier

### Einsatz

- Konstruktionsschritte
- Zirkel-/Linealnahe Sequenzen
- geometrische Erzeugung statt nur fertige Figur

### Muss sichtbar machen

- was konstruiert wird
- welcher neue Schritt hinzukommt
- dass Konstruktion geordnet und nachvollziehbar ist

### Muss vermeiden

- reine Werkzeugromantik
- dekorative Zirkel- oder Pergamentszene

## Asset A5: Exhaustion / Archimedean Approximation Carrier

### Einsatz

- Archimedes
- Flaeche, Volumen, Erschoepfung
- Vorformen spaeterer Integralideen

### Muss sichtbar machen

- Annaeherung
- Zerlegung oder Einpassung
- kontrollierte Grenznaehe

### Muss vermeiden

- moderne Analysis-Notation als primaere Darstellung
- fertige Integralgleichung als Einstieg

## Asset A6: Quiet Historical Sidecar

### Einsatz

- optionale historische Wuerdeebene
- Ueberlieferung / Kommentar / mathematische Kultur

### Muss sichtbar machen

- Kontext nur als leise Zusatzebene
- Denken und Weitergabe, nicht Heldenbild

### Muss vermeiden

- Tempelkulisse
- Buesten-/Philosophenportrait als Hauptszene
- museale Distanz statt Lernfunktion

## Carrier-State Mapping fuer Antiquity

Die wichtigsten Antike-Assets brauchen mindestens diese Zustandslogik:

- `intro`
- `proof_step`
- `repeat`
- `example` oder `variant`
- optional `history_sidecar`

### Antiquity-spezifisch wichtig

- `repeat` bedeutet:
  - weniger Teilrelationen gleichzeitig
  - klarere Markierung derselben Figur
  - kleinere Beweisspanne

- `example` bedeutet:
  - gleiche Formidee
  - andere konkrete Figur oder andere Groessenrelation

## Erste Produktionsreihenfolge

Fuer Antiquity sollte zuerst produziert werden:

1. `A1` Counting and Grouping
2. `A2` Ratio and Shape
3. `A3` Euclidean Proof
4. `A5` Exhaustion / Approximation
5. `A4` Construction
6. `A6` Quiet Historical Sidecar

## Begruendung

- `A1` bis `A3` tragen den fruehen antiken Kern unmittelbar
- `A5` oeffnet die Bruecke zur spaeteren Analysislinie
- `A4` vertieft Konstruktion
- `A6` bleibt semantisch Zusatz
