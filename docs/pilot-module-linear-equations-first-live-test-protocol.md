# Pilot Module First Live Test Protocol: Lineare Gleichungen

## Zweck

Dieses Dokument ist das erste echte Beobachtungs- und
Auswertungsprotokoll fuer einen realen Lerndurchlauf des Pilotmoduls
[pilot-module-linear-equations.md](/Users/jonasweiss/MathTeach/docs/pilot-module-linear-equations.md).

Es ist kein allgemeiner Usability-Test.

Es dient dazu, nach einem ersten echten Durchlauf sauber zu trennen:

- traegt die Moduldramaturgie?
- traegt die Tutor-Sprache?
- traegt die aktuelle Device-UI?
- oder fehlt vor allem ein staerkerer illustrativer Carrier?

## Rolle im Entscheidungsprozess

Dieses Protokoll ist der letzte innere Baustein vor einem echten Test.

Es verbindet:

- Throughplay-Script
- Asset Mapping
- Tutor Utterance Pack
- spaetere Produktentscheidung

Es ist bewusst so gebaut, dass wir nach dem ersten Test nicht nur
“Eindruecke” haben, sondern eine belastbare Richtungsentscheidung.

## Quellenbasis

Dieses Protokoll ist abgeleitet aus:

- [pilot-module-linear-equations.md](/Users/jonasweiss/MathTeach/docs/pilot-module-linear-equations.md)
- [pilot-module-linear-equations-throughplay-script.md](/Users/jonasweiss/MathTeach/docs/pilot-module-linear-equations-throughplay-script.md)
- [pilot-module-linear-equations-asset-mapping-sheet.md](/Users/jonasweiss/MathTeach/docs/pilot-module-linear-equations-asset-mapping-sheet.md)
- [pilot-module-linear-equations-tutor-utterance-pack.md](/Users/jonasweiss/MathTeach/docs/pilot-module-linear-equations-tutor-utterance-pack.md)
- [device-ui-evidence-matrix.md](/Users/jonasweiss/MathTeach/docs/device-ui-evidence-matrix.md)
- [pedagogical-strategy-matrix.md](/Users/jonasweiss/MathTeach/docs/pedagogical-strategy-matrix.md)

## Testziel

Der erste Live-Test soll noch nicht beweisen, dass das Modul “fertig”
ist.

Er soll beantworten:

1. Versteht eine reale Lernperson die Grundbeziehung von `x + 3 = 7`?
2. Wird `derselbe Zug auf beiden Seiten` als Sinn und nicht als Trick
   erlebt?
3. Wirkt `Nochmal` als Hilfe und nicht als Rueckstufung?
4. Wirkt `Beispiel` als Strukturtransfer und nicht als Themenwechsel?
5. Fehlt im Kern vor allem Illustration oder schon frueher die
   didaktische Sequenz?

## Geeignete erste Testperson

Fuer den ersten Durchlauf ist geeignet:

- eine reale Lernperson mit Schulnaehe
- bevorzugt mit leichtem oder mittlerem Strukturbedarf
- keine Person, die schon sehr sicher in Gleichungen ist

Nicht ideal fuer Test 1:

- stark pruefungsgetriebene Evaluation
- mehrere Testpersonen gleichzeitig
- Vergleichstest mit zwei UI-Varianten

## Testmodus fuer Pilot 1

- Device oder Device-nahe 800x480-Darstellung
- ein Tutorfluss, kein freies Explorieren
- ruhiger 1:1-Durchgang
- Dauerziel:
  `10 bis 20 Minuten`
- History-Sidecar nur, wenn der Kernfluss bis Station 6 stabil war

## Vor dem Test

Vor dem Start muss intern klar sein:

- welche Version der UI gezeigt wird
- welche Tutor-Saetze benutzt werden
- welche Asset-Platzhalter oder Carrier bereits vorhanden sind
- ob der Test live moderiert oder halbmoderiert ist

## Waehren des Tests nicht tun

- keine spontane Umformulierung aus Nervositaet
- keine zweite Erklaerspur parallel aufmachen
- keine mathematische Zusatzidee einschieben
- keine Erfolge bewerten statt sie zu verstehen
- keinen defensiven Produktpitch geben

## Beobachtungslogik

Pro Station wird getrennt beobachtet:

1. `Verstehen`
2. `Blick und Aufmerksamkeit`
3. `Sprachreaktion`
4. `Carrier-Wirkung`
5. `Stoerquelle`

## Stoerquellen-Kategorien

Jede Schwierigkeit wird nach dem Test einer Hauptursache zugeordnet:

- `M` Modulstruktur
- `T` Tutor-Sprache
- `U` UI-/Layoutstruktur
- `I` Illustration / Carrier zu schwach
- `H` History-Gewichtung
- `P` persoenlicher Vorwissens- oder Belastungsfaktor

## Stationsprotokoll

## Station 1: Beziehung statt Formel

### Beobachten

- schaut die Lernperson auf beide Seiten als zusammengehoerig?
- wirkt die Szene ruhig oder schon wie eine Aufgabe?
- fragt die Person sofort nach “was muss ich tun?” statt nach Beziehung?

### Positives Signal

- `=` wird als Beziehung oder Zusammengehoeren beschrieben

### Kritisches Signal

- `=` wird nur als Trennstrich gelesen

### Wahrscheinliche Ursache bei Bruch

- `I`, wenn die Beziehung optisch nicht traegt
- `U`, wenn der Screen zu sehr wie Bedienoberflaeche wirkt
- `T`, wenn der Tutor zu frueh auf Regelton kippt

## Station 2: Gleichung in einfacher Symbolform

### Beobachten

- kann die Lernperson `x + 3 = 7` auf das Sichtbare zurueckbinden?
- wird `x` als unbekannte Groesse oder als beliebiger Buchstabe erlebt?

### Positives Signal

- `x` wird als “das, was wir noch nicht kennen” verstanden

### Kritisches Signal

- `x` steht sprachlich leer im Raum

### Wahrscheinliche Ursache bei Bruch

- `I`, wenn die Bild-Symbol-Bruecke nicht traegt
- `T`, wenn der Tutor zu technisch spricht
- `M`, wenn der Sprung von Station 1 zu 2 zu gross ist

## Station 3: Derselbe Zug auf beiden Seiten

### Beobachten

- wird der doppelte Zug als sinnvoll erlebt?
- oder nur als nachzusprechende Regel?

### Positives Signal

- die Lernperson kann sagen, warum links und rechts derselbe Zug noetig
  ist

### Kritisches Signal

- Formulierungen wie:
  - `weil man das so macht`
  - `weil es die Regel ist`

### Wahrscheinliche Ursache bei Bruch

- `I`, wenn der Carrier den doppelten Zug nicht sichtbar macht
- `T`, wenn der Tutor die Begruendung nicht klein genug haelt
- `M`, wenn der Regelgedanke zu frueh kommt

## Station 4: Resultat aus derselben Struktur

### Beobachten

- wirkt `x = 4` hergeleitet oder abrupt?
- kann die Lernperson den Endzustand in eigenen Worten rueckbinden?

### Positives Signal

- `Jetzt bleibt links nur x und rechts vier` kommt als eigener Sinnsatz
  der Lernperson

### Kritisches Signal

- das Ergebnis wird akzeptiert, aber nicht nachvollzogen

### Wahrscheinliche Ursache bei Bruch

- `I`, wenn Resultatspur nicht aus demselben Carrier kommt
- `U`, wenn der Screen neue Flaechen oder zu viele Metaelemente oeffnet
- `T`, wenn der Tutor das Resultat zu schnell schliesst

## Station 5: Recovery / Nochmal

### Beobachten

- fuehlt sich `Nochmal` kleiner oder ruecksetzender an?
- entspannt sich der Blick oder steigt die Unsicherheit?

### Positives Signal

- `Nochmal` wird ohne Scham angenommen

### Kritisches Signal

- die Person wirkt defensiver oder sagt sinngemaess:
  - `Ich habe es wohl falsch gemacht`
  - `Dann habe ich es nicht verstanden`

### Wahrscheinliche Ursache bei Bruch

- `T`, wenn Recovery sprachlich rueckstufend klingt
- `U`, wenn der Screen durch Recovery lauter wird
- `I`, wenn der Carrier nicht wirklich kleiner, sondern nur voller wird

## Station 6: Aehnliches Beispiel

### Beobachten

- wird die Struktur wiedererkannt?
- oder fuehlt sich das Beispiel wie ein neues Thema an?

### Positives Signal

- die Person sagt sinngemaess:
  - `gleiche Idee, andere Zahlen`

### Kritisches Signal

- die Person startet wieder bei null oder fragt nach komplett neuer
  Regel

### Wahrscheinliche Ursache bei Bruch

- `I`, wenn Beispiel und Standard nicht strukturell verwandt wirken
- `T`, wenn Transfer sprachlich nicht klar markiert ist
- `M`, wenn das Beispiel zu frueh kommt

## Station 7: History-Sidecar

### Beobachten

- wirkt History wuerdig und leise?
- oder stoert sie den Kernfluss?

### Positives Signal

- mehr Ernsthaftigkeit und Sinn, ohne Ablenkung vom Kern

### Kritisches Signal

- die Person verliert den Faden oder erlebt Historie als Schulbuchkasten

### Wahrscheinliche Ursache bei Bruch

- `H`, wenn Gewichtung zu hoch ist
- `I`, wenn das Sidecar zu gross oder zu bildhaft dominant wird
- `T`, wenn die Sprache zu erklaerend statt verbindend ist

## Entscheidungsraster nach dem Test

## Fall A: Sequenz traegt, Illustration fehlt

Merkmale:

- Lernfluss funktioniert grundsaetzlich
- Tutor-Sprache wirkt stabil
- aber Beziehung, doppelter Zug oder Transfer bleiben visuell zu schwach

Konsequenz:

- Illustrations-Track separat priorisieren
- UI nur klein weiterfuehren

## Fall B: Sprache stoert mehr als Illustration

Merkmale:

- Lernperson stockt eher an Formulierungen als am Traeger
- rueckfragende Sprache hilft sofort

Konsequenz:

- Tutor Utterance Pack nachschaerfen
- noch keine groessere Asset-Produktion beauftragen

## Fall C: UI-Struktur schiebt sich vor die Mathematik

Merkmale:

- Lernperson schaut auf Oberflaeche statt auf Beziehung
- Aktionen, Hinweise oder Layout dominieren den Blick

Konsequenz:

- UI weiter entschlacken
- Asset-Produktion nur parallel, nicht als Erstreaktion

## Fall D: Moduldramaturgie selbst ist noch nicht stabil

Merkmale:

- Brueche schon vor Recovery oder Beispiel
- zu grosser Sprung zwischen Stationen

Konsequenz:

- Modul intern nachschneiden
- noch keine externe Visualproduktion priorisieren

## Kurzprotokoll fuer die Auswertung

Direkt nach dem Test halten wir knapp fest:

1. Welche Station war der erste echte Bruch?
2. Welche Stoerquellen-Kategorie war primaer?
3. War `Nochmal` psychologisch tragend?
4. War `Beispiel` echter Transfer?
5. Hat History genutzt oder gestört?
6. Ist der naechste Hebel `UI`, `Illustration`, `Sprache` oder `Modul`?

## Minimale Go-/No-Go-Entscheidung nach Test 1

### Go fuer naechsten Modultest

Wenn:

- Station 1 bis 4 grundsaetzlich tragen
- `Nochmal` nicht beschämend wirkt
- `Beispiel` als Strukturtransfer lesbar ist

### Sofortiger Illustrations-Track

Wenn:

- Struktur und Sprache tragen
- aber die Carrier wiederholt zu schwach fuer Beziehung und Operation
  sind

### Zuerst interner Rework

Wenn:

- Brueche schon im Grundfluss auftreten
- die Modulreihenfolge noch nicht stabil ist
- der Tutor-Ton die Sicherheit nicht haelt

## Naechster sinnvoller Baustein

Nach dem ersten echten Test sollten direkt folgen:

1. `Testauswertung 1`
2. daraus abgeleitet:
   - `UI-Rework`
   - oder `Illustrations-Track-Start`
   - oder `Modul-Rework`
