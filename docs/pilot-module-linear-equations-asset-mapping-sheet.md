# Pilot Module Asset Mapping Sheet: Lineare Gleichungen

## Zweck

Dieses Dokument uebersetzt das
[pilot-module-linear-equations-throughplay-script.md](/Users/jonasweiss/MathTeach/docs/pilot-module-linear-equations-throughplay-script.md)
in eine operative Asset-Zuordnung.

Es beantwortet fuer jede Kernstation:

- welches Asset oder welche Asset-Familie gebraucht wird
- in welchem Carrier-Zustand das Asset erscheint
- welche mathematische Funktion das Asset genau traegt
- was spaeter extern produziert werden darf
- und welche Teile intern fest bleiben muessen

## Rolle im Produktionsfluss

Dieses Mapping sitzt zwischen:

- Modul-Blueprint
- Throughplay-Script
- Illustrationsbrief
- spaeterem externem Asset-Track

Es ist bewusst kein Stilboard.

Es ist ein didaktisches Produktionsdokument.

## Quellenbasis

Dieses Asset Mapping ist abgeleitet aus:

- [pilot-module-linear-equations.md](/Users/jonasweiss/MathTeach/docs/pilot-module-linear-equations.md)
- [pilot-module-linear-equations-illustration-brief.md](/Users/jonasweiss/MathTeach/docs/pilot-module-linear-equations-illustration-brief.md)
- [pilot-module-linear-equations-throughplay-script.md](/Users/jonasweiss/MathTeach/docs/pilot-module-linear-equations-throughplay-script.md)
- [device-learningscreen-contract.md](/Users/jonasweiss/MathTeach/docs/device-learningscreen-contract.md)
- [device-ui-evidence-matrix.md](/Users/jonasweiss/MathTeach/docs/device-ui-evidence-matrix.md)

## Nicht verhandelbare Mapping-Regeln

- ein Asset muss immer eine mathematische Funktion tragen
- `Standard`, `Nochmal` und `Beispiel` duerfen nie nur farblich
  unterschieden sein
- keine Asset-Entscheidung darf `Bedeutung -> Symbolik -> Handlung`
  umkehren
- Recovery benutzt dieselbe Struktur, aber kleiner und expliziter
- Historie bleibt Sidecar und nie Haupttraeger

## Asset-Familien-Referenz

Fuer Pilot 1 werden diese Asset-Familien verwendet:

- `A` Beziehungs-/Balance-Traeger
- `B` Unknown-plus-Quantity
- `C` Same-Operation-Both-Sides
- `D` Resultat-Traeger
- `E` Aehnliches Beispiel
- `F` Optionales History-Sidecar

Sie sind in
[pilot-module-linear-equations-illustration-brief.md](/Users/jonasweiss/MathTeach/docs/pilot-module-linear-equations-illustration-brief.md)
definiert.

## Station Mapping

## Station 1: Beziehung statt Formel

- Throughplay-Referenz:
  [pilot-module-linear-equations-throughplay-script.md](/Users/jonasweiss/MathTeach/docs/pilot-module-linear-equations-throughplay-script.md)
- Primaeres Asset: `A`
- Carrier-Zustand: `relationship_intro`
- Screen-Rolle:
  nur Beziehung, noch kein Operations- oder Resultatpfad
- Muss sichtbar sein:
  - zwei Seiten gehoeren zusammen
  - Stabilitaet ohne Effektlogik
  - kein Eindruck von Pruefung oder Aufgabe
- Intern fest:
  - Gleichgewicht ist die Kernidee
  - keine Seite dominiert
  - keine Umformung wird vorweggenommen
- Extern frei:
  - wie die ruhige Beziehung formal gezeichnet wird
  - welche Material- und Linienanmutung die Beziehung traegt

## Station 2: Gleichung in einfacher Symbolform

- Throughplay-Referenz:
  [pilot-module-linear-equations-throughplay-script.md](/Users/jonasweiss/MathTeach/docs/pilot-module-linear-equations-throughplay-script.md)
- Primaeres Asset: `A + B`
- Carrier-Zustand: `standard`
- Screen-Rolle:
  dieselbe Beziehung jetzt mit `x + 3 = 7`
- Muss sichtbar sein:
  - `x` ist eine unbekannte Groesse
  - `+3` ist Zusatz zur linken Seite
  - `7` ist Gegenueber derselben Beziehung
- Intern fest:
  - die Bildstruktur bleibt direkt rueckbindbar auf die Symbolzeile
  - noch kein eigener Operationskanal
- Extern frei:
  - Markierung der unbekannten Groesse
  - konkrete Form der drei Zusatz-Einheiten

## Station 3: Derselbe Zug auf beiden Seiten

- Throughplay-Referenz:
  [pilot-module-linear-equations-throughplay-script.md](/Users/jonasweiss/MathTeach/docs/pilot-module-linear-equations-throughplay-script.md)
- Primaeres Asset: `C`
- Carrier-Zustand: `repeat_seed`
- Screen-Rolle:
  Hauptgleichung bleibt, Operationsspur kommt dazu
- Muss sichtbar sein:
  - `-3` links
  - `-3` rechts
  - derselbe Eingriff auf beiden Seiten
- Intern fest:
  - die Operation wirkt klein und kontrolliert
  - die Beziehung bleibt Hauptsache
- Extern frei:
  - ob der Zug als Markieren, Abheben, Entfernen oder Ausgrauen
    gezeigt wird

## Station 4: Resultat aus derselben Struktur

- Throughplay-Referenz:
  [pilot-module-linear-equations-throughplay-script.md](/Users/jonasweiss/MathTeach/docs/pilot-module-linear-equations-throughplay-script.md)
- Primaeres Asset: `D` mit Rueckbindung an `A + C`
- Carrier-Zustand: `repeat`
- Screen-Rolle:
  Gleichung, Operation und Resultat in einem Traeger
- Muss sichtbar sein:
  - `x = 4` kommt aus derselben Struktur
  - kein harter Szenenwechsel
- Intern fest:
  - Resultatspur ist Folge, nicht neue Szene
  - die Ableitung bleibt lesbar
- Extern frei:
  - visuelle Verdichtung der Ergebniszone
  - Material- und Lichtlogik des Endzustands

## Station 5: Recovery / Nochmal

- Throughplay-Referenz:
  [pilot-module-linear-equations-throughplay-script.md](/Users/jonasweiss/MathTeach/docs/pilot-module-linear-equations-throughplay-script.md)
- Primaeres Asset: `C + D`
- Carrier-Zustand: `repeat`
- Screen-Rolle:
  dieselbe Gleichung, explizitere Teilhandlung
- Muss sichtbar sein:
  - gleiche Zahlen
  - gleiche Struktur
  - klarere Operations- und Resultatspur
- Intern fest:
  - Recovery verkleinert den Schritt
  - Recovery fuehrt nicht zu neuer Szene
  - Recovery bleibt wuerdevoll und nicht remedial
- Extern frei:
  - wie Explizitheit visualisiert wird
  - wie Teilhandlungen voneinander lesbar gemacht werden

## Station 6: Aehnliches Beispiel

- Throughplay-Referenz:
  [pilot-module-linear-equations-throughplay-script.md](/Users/jonasweiss/MathTeach/docs/pilot-module-linear-equations-throughplay-script.md)
- Primaeres Asset: `E`
- Carrier-Zustand: `example`
- Screen-Rolle:
  gleiche Regel an `5 + 2 = 7`
- Muss sichtbar sein:
  - neue Zahlen
  - gleiche Struktur
  - `-2` auf beiden Seiten
  - `5 = 5` als Resultat
- Intern fest:
  - Beispiel ist Strukturtransfer, kein Themenwechsel
  - Differenz nur so gross wie noetig
- Extern frei:
  - wie die Varianz sichtbar wird
  - wie die neue Zahlenkonstellation formal gewaehlt aussieht

## Station 7: History-Sidecar

- Throughplay-Referenz:
  [pilot-module-linear-equations-throughplay-script.md](/Users/jonasweiss/MathTeach/docs/pilot-module-linear-equations-throughplay-script.md)
- Primaeres Asset: `F`
- Carrier-Zustand: `history_sidecar`
- Screen-Rolle:
  optionale Zusatzstation oder leiser Zusatzblock
- Muss sichtbar sein:
  - Problem -> Verfahren -> Notation
  - Algebra als entstandene Sprache
- Intern fest:
  - historische Szene bleibt semantisch leise
  - sie darf den Kernpfad nicht verdrängen
- Extern frei:
  - visuelle Verdichtung der historischen Referenz
  - Textur, Rahmung, Materialitaet

## Carrier-State Mapping

Die aktuelle Device-UI und ein spaeterer Asset-Track muessen mindestens
diese Zustandslogik tragen:

- `relationship_intro`
  - nur Beziehungs-Traeger
- `standard`
  - Hauptgleichung ohne explizite Operationsspur
- `repeat_seed`
  - dieselbe Gleichung mit eingefuehrter Operationslogik
- `repeat`
  - gleiche Gleichung, explizite Operation und Resultat
- `example`
  - aehnliche Gleichung, gleiche Struktur
- `history_sidecar`
  - optionaler Zusatz, nie Hauptzustand

## Aktuelle UI-Grenze

Mit dem heutigen Stand in
[device.html](/Users/jonasweiss/MathTeach/src/mathteach/ui/device.html) und
[device.js](/Users/jonasweiss/MathTeach/src/mathteach/ui/static/device.js)
koennen wir bereits tragen:

- `standard`
- `repeat`
- `example`

Noch nicht stark genug ausgebaut fuer einen vollwertigen Modultest sind:

- `relationship_intro` als eigener ruhiger Beziehungszustand vor Symbolik
- `history_sidecar` als wirklich leiser historischer Zusatztraeger
- ein eigener Asset-Track, der die didaktische Carrier-Funktion sichtbar
  staerker macht als die aktuelle UI-Bordstruktur

## Produktionsschnitt fuer einen externen Illustrationstrack

Wenn dieser Pilot nach externen Assets ruft, sollte der Auftrag in
dieser Reihenfolge laufen:

1. `A + B`
   - Beziehung und erste Gleichung
2. `C + D`
   - derselbe Zug auf beiden Seiten und Resultat
3. `E`
   - aehnliches Beispiel
4. `F`
   - History-Sidecar

Begruendung:

- `A` bis `D` tragen den eigentlichen Lehrkern
- `E` prueft, ob Strukturtransfer visuell stark genug wird
- `F` ist wichtig, aber nicht gate-entscheidend fuer Pilot 1

## Abnahmefragen pro Asset

Jedes Asset gilt erst als tragfaehig, wenn wir intern `ja` sagen koennen
zu:

1. Ist die mathematische Funktion ohne Zusatztext sichtbar?
2. Ist die Reihenfolge `Bedeutung -> Symbolik -> Handlung` intakt?
3. Traegt das Asset `repeat` wirklich kleiner statt lauter?
4. Ist `example` gleich genug fuer Transfer und anders genug fuer ein
   echtes Beispiel?
5. Wuerde die Szene ohne dekorative Figuren immer noch lehren?

## Naechster sinnvoller Baustein

Auf dieses Mapping sollte direkt folgen:

1. `Tutor utterance pack`
2. `First live test protocol`

Erst danach lohnt sich es, einen externen Asset-Track konkret zu
briefen oder zu beauftragen.
