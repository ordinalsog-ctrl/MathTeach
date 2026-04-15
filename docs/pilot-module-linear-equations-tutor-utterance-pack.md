# Pilot Module Tutor Utterance Pack: Lineare Gleichungen

## Zweck

Dieses Dokument definiert die konkrete Tutor-Stimme fuer das erste echte
Pilotmodul
[pilot-module-linear-equations.md](/Users/jonasweiss/MathTeach/docs/pilot-module-linear-equations.md).

Es ist kein allgemeiner Sprachleitfaden fuer MathTeach, sondern die
operative Sprechschicht fuer den ersten realen Durchspielpfad.

Es beantwortet:

- was der Tutor pro Station in der Standardspur sagt
- was der Tutor in `Nochmal` sagt
- was der Tutor im `Beispiel` sagt
- welche Uebergangssaetze erlaubt sind
- welche Tonalitaeten und Formulierungen verboten sind

## Rolle im Produktionsfluss

Dieses Utterance Pack sitzt zwischen:

- Throughplay-Script
- Asset Mapping
- spaeterem Live-Test-Protokoll

Es sorgt dafuer, dass unsere fachliche und paedagogische Struktur nicht
spaeter durch beliebige UI-Copy oder zufaellige Tutor-Texte verwischt
wird.

## Quellenbasis

Dieses Dokument ist direkt abgeleitet aus:

- [pilot-module-linear-equations.md](/Users/jonasweiss/MathTeach/docs/pilot-module-linear-equations.md)
- [pilot-module-linear-equations-throughplay-script.md](/Users/jonasweiss/MathTeach/docs/pilot-module-linear-equations-throughplay-script.md)
- [pilot-module-linear-equations-asset-mapping-sheet.md](/Users/jonasweiss/MathTeach/docs/pilot-module-linear-equations-asset-mapping-sheet.md)
- [pilot-module-linear-equations-illustration-brief.md](/Users/jonasweiss/MathTeach/docs/pilot-module-linear-equations-illustration-brief.md)
- [pedagogical-strategy-matrix.md](/Users/jonasweiss/MathTeach/docs/pedagogical-strategy-matrix.md)
- [device-ui-evidence-matrix.md](/Users/jonasweiss/MathTeach/docs/device-ui-evidence-matrix.md)

## Nicht verhandelbare Sprachregeln

- der Tutor spricht ruhig, knapp und fuehrend
- der Tutor spricht nie pruefend
- der Tutor erklaert zuerst Sinn, dann Regel
- der Tutor verkleinert bei Unsicherheit den Schritt
- der Tutor sagt nie, dass etwas “doch einfach” sei
- der Tutor spricht Fehler nie als Defizit des Lernenden aus
- der Tutor nutzt keine motivierende Lautstaerke als Ersatz fuer Klarheit

## Sprachcharakter fuer Pilot 1

Die Tutor-Stimme fuer dieses Modul ist:

- `guiding`
- `stabilizing`
- `school_scaffolded`

Das bedeutet konkret:

- kurze Saetze
- eine Aussage pro Satz
- wenige Fachwoerter auf einmal
- keine rhetorischen Doppelbewegungen
- kein schulischer Testton

## Globale Muss-Regeln

- pro Station maximal `2` bis `3` Kernsätze
- ein Uebergangssatz darf nie eine zweite mathematische Idee einfuehren
- `Nochmal` darf nur denselben Schritt kleiner machen
- `Beispiel` darf nur dieselbe Struktur mit anderen Zahlen zeigen
- History bleibt sprachlich leise und optional

## Globale Verbote

Nicht benutzen:

- `Das ist doch einfach.`
- `Das musst du dir merken.`
- `Das ist die Regel, fertig.`
- `Falsch.`
- `Nein, so nicht.`
- `Das solltest du eigentlich schon koennen.`
- `Wir loesen das jetzt schnell.`
- `Pass auf, das ist wichtig.`

Vermeiden:

- ueberlange Meta-Einleitungen
- abstrakte Rechtfertigungen ohne sichtbaren mathematischen Bezug
- zwei Erklaerbilder in einem Satz
- Scham- oder Defizit-Ton

## Standard-Uebergangssprache

Diese Uebergangsformen sind fuer Pilot 1 erlaubt:

- `Wir schauen zuerst nur auf ...`
- `Jetzt sehen wir dieselbe Beziehung als ...`
- `Jetzt kommt genau ein Zug dazu.`
- `Wir bleiben bei derselben Gleichung.`
- `Jetzt sehen wir, was nach diesem Zug uebrig bleibt.`
- `Wir nehmen dieselbe Struktur noch einmal in klein.`
- `Jetzt dieselbe Idee mit anderen Zahlen.`

## Station 1: Beziehung statt Formel

### Standard

- `Wir schauen zuerst nur darauf, dass beide Seiten zusammengehoeren.`
- `Noch keine Regel. Erst die Beziehung.`

### Wenn Blick oder Stimme unsicher werden

- `Du musst hier noch nichts umformen.`
- `Es reicht zuerst zu sehen: links und rechts gehoeren zusammen.`

### Nicht sagen

- `Das ist einfach nur eine Waage.`
- `Spaeter rechnen wir das dann richtig.`

## Station 2: Gleichung in einfacher Symbolform

### Standard

- `Jetzt schreiben wir dieselbe Beziehung als kleine Gleichung.`
- `Links steht etwas Unbekanntes und noch drei dazu. Rechts steht sieben.`

### Wenn Rueckbindung an das Bild noetig ist

- `Das x steht fuer den Teil, den wir noch nicht kennen.`
- `Die drei kommen links dazu. Die sieben stehen rechts gegenueber.`

### Nicht sagen

- `x ist einfach die unbekannte Variable.`
- `Links haben wir den Term, rechts den Wert.`

## Station 3: Derselbe Zug auf beiden Seiten

### Standard

- `Wenn die Beziehung erhalten bleiben soll, machen wir auf beiden Seiten denselben Zug.`
- `Wir nehmen nicht irgendwo etwas weg. Wir halten die Beziehung im Gleichgewicht.`

### Wenn die Regel als Satz, aber noch nicht als Sinn ankommt

- `Der Zug ist links und rechts derselbe.`
- `Genau das haelt die Beziehung stabil.`

### Nochmal

- `Wir machen genau diesen einen Zug noch kleiner sichtbar.`
- `Links minus drei. Rechts auch minus drei.`

### Nicht sagen

- `Wir kuerzen jetzt einfach die drei weg.`
- `Das macht man bei Gleichungen eben so.`

## Station 4: Resultat aus derselben Struktur

### Standard

- `Jetzt sehen wir, was nach diesem einen Zug uebrig bleibt.`
- `Links bleibt nur noch x. Rechts bleibt vier.`

### Wenn das Resultat akzeptiert, aber nicht verstanden wird

- `Das Ergebnis kommt aus demselben Schritt.`
- `Wir haben nichts Neues angefangen. Wir haben dieselbe Beziehung weitergefuehrt.`

### Nochmal

- `Wir schauen noch einmal genau auf denselben Weg.`
- `Erst der gleiche Zug auf beiden Seiten. Dann bleibt x gleich vier.`

### Nicht sagen

- `Also ist die Loesung einfach vier.`
- `Damit sind wir fertig.`

## Station 5: Recovery / Nochmal

### Standard-Recovery

- `Wir bleiben bei derselben Gleichung und machen nur den Schritt kleiner.`
- `Nichts Neues. Nur derselbe Zug deutlicher.`

### Wenn Unsicherheit hoch ist

- `Wir gehen nicht zurueck. Wir schauen nur naeher hin.`
- `Es ist dieselbe Idee, nur in kleineren Teilen.`

### Mini-Bestaetigung nach Recovery

- `Genau dieser kleine Zug war wichtig.`
- `Jetzt ist der Weg besser sichtbar.`

### Nicht sagen

- `Dann machen wir es eben noch einmal ganz von vorne.`
- `Das war offenbar noch zu schwer.`

## Station 6: Aehnliches Beispiel

### Standard

- `Jetzt sehen wir dieselbe Regel an einer aehnlichen Gleichung.`
- `Nicht neues Thema. Dieselbe Struktur mit anderen Zahlen.`

### Beispielspur

- `Hier stehen fünf plus zwei gleich sieben.`
- `Wir machen wieder denselben Zug auf beiden Seiten: minus zwei.`
- `Dann bleibt fünf gleich fünf.`

### Wenn Transfer noch nicht stabil ist

- `Die Zahlen sind anders. Der Gedanke ist derselbe.`
- `Wichtig ist nicht die Zahl. Wichtig ist die gleiche Struktur.`

### Nicht sagen

- `Das ist genau dasselbe, nur einfacher.`
- `Wenn du das kannst, kannst du alle Gleichungen.`

## Station 7: History-Sidecar

### Standard

- `Diese Gleichungssprache ist nicht einfach vom Himmel gefallen.`
- `Menschen haben Wege gesucht, Probleme Schritt fuer Schritt in eine loesbare Form zu bringen.`

### Wenn Interesse da ist

- `Spaeter wurde daraus die Algebra, wie wir sie heute schreiben.`
- `Wichtig ist hier nicht der Name, sondern die Idee: Verfahren statt Ratespiel.`

### Nicht sagen

- `Das hat al-Khwarizmi erfunden.`
- `Das ist jetzt nur ein kleiner Exkurs.`

## Mini-Bestaetigungen

Diese kurzen Rueckmeldungen sind fuer Pilot 1 zulaessig:

- `Genau auf diese Beziehung schauen wir.`
- `Ja, das ist derselbe Zug.`
- `Genau dieser kleine Schritt zaehlt hier.`
- `So bleibt die Struktur gleich.`
- `Jetzt sieht man den Unterschied klarer.`

Nicht benutzen:

- `Super!`
- `Perfekt!`
- `Ganz toll!`
- `Richtig!`

Begruendung:

- Rueckmeldung soll Bedeutung stabilisieren, nicht Performance bewerten

## CTA-nahe Tutor-Sprache

Wenn die UI eine Aktion wie `Nochmal`, `Beispiel` oder `Weiter` traegt,
muessen die Tutor-Saetze dazu passen.

Erlaubte kurze Kopplung:

- `Wenn du willst, machen wir genau diesen Schritt noch kleiner.`
- `Wenn du willst, sehen wir dieselbe Idee an einem aehnlichen Beispiel.`
- `Wenn es klarer ist, gehen wir zum naechsten kleinen Schritt.`

Nicht benutzen:

- `Brauchst du noch Hilfe?`
- `Willst du testen, ob du es verstanden hast?`
- `Bist du bereit fuer das Naechste?`

## Live-Test-Beobachtungen fuer die Sprache

Beim ersten echten Durchspiel pruefen wir besonders:

1. Klingen die Tutor-Saetze zu schulisch?
2. Klingen sie zu abstrakt fuer die jeweilige Illustration?
3. Wird `Nochmal` sprachlich wirklich kleiner und nicht ruecksetzender?
4. Klingt `Beispiel` wie Transfer und nicht wie Themenwechsel?
5. Bleibt History sprachlich leise genug?

## Naechster sinnvoller Baustein

Nach diesem Utterance Pack folgt sinnvollerweise:

1. `First live test protocol`
2. spaeter ein gebundener externer Asset-Track

Erst dann lohnt sich eine belastbare Entscheidung, ob die aktuelle
Device-UI fuer Pilot 1 schon reicht oder ob der Illustrations-Track
sofort priorisiert werden muss.
