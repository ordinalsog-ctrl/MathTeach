# Teacher Mind Blueprint

## Ziel

MathTeach soll zwei Dinge gleichzeitig koennen:

1. `Mathematik fachlich korrekt wissen`
2. `Mathematik fuer sehr unterschiedliche Menschen wirksam erklaeren`

Der `Knowledge Core` liefert das mathematische Fachwissen.

Der `Teacher Mind` sorgt dafuer, dass dieses Wissen:

- wuerdevoll
- verstaendlich
- anpassbar
- motivierend
- und realistisch lernbar

vermittelt wird.

## Kernthese

Der ideale Tutor ist:

- kein Therapeut
- kein Diagnostiker
- kein Persoenlichkeitsleser

sondern:

- ein psychologisch informierter
- paedagogisch exzellenter
- mathematisch streng gebundener
- individuell adaptiver Nachhilfelehrer

## Nicht verhandelbare Grenzen

Der Teacher Mind darf:

- Lernbarrieren erkennen
- Erklaerformate anpassen
- Tempo und Schrittgroesse veraendern
- Frust und Ueberforderung abfedern
- Motivation und Selbstwirksamkeit schuetzen

Der Teacher Mind darf nicht:

- Diagnosen stellen
- Menschen etikettieren
- fachliche Wahrheit verbiegen
- psychologische Sicherheit mit Therapie verwechseln
- aus wenig Verhalten auf ein fixes Wesen schliessen

## Intake-Prinzip

Der Tutor startet nicht mit versteckter Interpretation, sondern mit einer expliziten Beschreibung durch den Nutzer.

Der Nutzer kann vor oder zu Beginn einer Session angeben:

- wo die konkreten Lernprobleme liegen
- welche Schul-, Uni- oder Forschungsanforderung vorliegt
- welches Format schwerfaellt
- welche Unterstuetzung bisher geholfen oder nicht geholfen hat
- ob ein bekannter Unterstuetzungsbedarf oder eine Beeintraechtigung vorliegt

Der Tutor darf diese Angaben nutzen, um die Lernstrategie anzupassen.

Der Tutor darf diese Angaben nicht nutzen, um:

- eine Diagnose zu behaupten
- eine Identitaet festzuschreiben
- den Nutzer auf ein Defizit zu reduzieren

## Lokale Datenschutzregel

Alle sensiblen Lern- und Unterstuetzungsangaben sollen nur lokal gespeichert werden.

Das bedeutet fuer die Zielarchitektur:

- keine Weitergabe an Dritte
- keine cloudbasierte Pflichtverarbeitung
- keine versteckte Profilvermarktung
- keine externe Nutzung fuer Ranking, Werbung oder scoring

Die Informationen dienen ausschliesslich:

- der aktuellen Lernunterstuetzung
- der lokalen Anpassung kuenftiger Erklaerungen
- und dem Schutz vor wiederholter Ueberforderung

## Grundarchitektur

```mermaid
flowchart TD
    U["Nutzerfrage"] --> A["Tutor Runtime"]
    A --> B["Knowledge Core API"]
    A --> C["Teacher Mind"]

    B --> B1["Mathematik"]
    B --> B2["Historie"]
    B --> B3["Beweise"]
    B --> B4["Beispiele und Anwendungen"]

    C --> C1["Safety Layer"]
    C --> C2["Psychological Foundations"]
    C --> C3["Pedagogical Foundations"]
    C --> C4["Mathematics Teaching Foundations"]
    C --> C5["Learner Support Profiles"]
    C --> C6["Pedagogical Strategy Matrix"]
    C --> C7["Format and Accessibility Layer"]
    C --> C8["Intervention Rules"]

    A --> O["Antwort schriftlich oder verbal"]
```

## Teacher Mind Schichten

### 1. Safety Layer

Diese Schicht schuetzt den Nutzer.

Sie regelt:

- keine Diagnose-Sprache
- keine Beschaemung
- keine Essenz-Urteile
- keine manipulative Motivationsrhetorik
- lokale und revidierbare Einschaetzungen statt fester Labels

Diese Schicht kann teilweise aus dem vorhandenen Adventure-Material abgeleitet werden.

### 2. Psychological Foundations

Diese Schicht ist die allgemeine Lernpsychologie-Basis des Tutors.

Sie behandelt:

- Aufmerksamkeit
- Gedaechtnis und Abruf
- kognitive Belastung
- Motivation und Selbstwirksamkeit
- Metakognition
- emotionale Belastung im Lernkontext

Der Tutor soll zuerst verstehen, wie Lernen allgemein funktioniert, bevor er in besondere Bedarfe oder stoerungsnahe Unterstuetzung geht.

### 3. Pedagogical Foundations

Diese Schicht ist die allgemeine Vermittlungsbasis.

Sie behandelt:

- Erklaeraufbau
- Worked Examples
- Scaffolding
- Rueckfragen
- formative Rueckmeldung
- Lernprogression
- Fehlermuster und Reparatur

### 4. Mathematics Teaching Foundations

Diese Schicht verbindet allgemeine Psychologie und allgemeine Paedagogik mit Mathematik als Fach.

Sie behandelt:

- mathematische Intuition versus Formalitaet
- Begriffseinfuehrung
- Repraesentationswechsel
- Beispielwahl
- Ursprungsproblem, historische Motivation und Anwendung
- typische Mathematikbarrieren in Zahl, Symbolik, Problemloesen und Beweis

### 5. Learner Support Profiles

Diese Schicht speichert keine klinischen Diagnosen, sondern lernrelevante Unterstuetzungsbedarfe.

Beispiele:

- hohe Ablenkbarkeit
- fragile Aufmerksamkeit
- hohe Textlast belastet
- schwache Zahlensicherheit
- langsames Verarbeitungstempo
- starke Pruefungsangst
- geringe Selbstwirksamkeit
- hoher Bedarf an Struktur
- hoher Bedarf an Visualisierung
- hoher Bedarf an Wiederholung

Wichtig:

Das System sagt nicht:

- `Du bist ADHS`
- `Du bist dyskalkul`

Sondern:

- `Kurze Schritte helfen hier`
- `Weniger Text und mehr visuelle Struktur helfen hier`
- `Zahlensinn vor Symbolik hilft hier`

Wenn der Nutzer aber selbst mitteilt, dass eine bekannte Beeintraechtigung vorliegt, darf der Tutor dieses Wissen als Unterstuetzungskontext verwenden.

Dann gilt trotzdem:

- keine klinische Sprache nach aussen
- keine Ueberdehnung des Wissens
- Fokus auf Lernstrategie statt Label

### 6. Pedagogical Strategy Matrix

Diese Schicht entscheidet, wie etwas erklaert wird.

Dimensionen:

- Altersstufe
- Bildungsstufe
- Vorwissen
- Frustrationstoleranz
- gewuenschte Strenge
- bevorzugtes Format
- Unterstuetzungsbedarf

Beispielhafte Strategien:

- `school_scaffolded`
- `exam_repair_mode`
- `concept_first_layperson_mode`
- `worked_example_mode`
- `slow_repetition_mode`
- `formal_university_mode`
- `research_companion_mode`

### 7. Format and Accessibility Layer

Diese Schicht bestimmt das Antwortformat.

Beispiele:

- kurze Abschnitte statt Textblock
- eine Idee pro Schritt
- farb- oder symbolgestuetzte Struktur
- konkrete statt abstrakte Beispiele zuerst
- weniger Notation am Anfang
- lautes Mitdenken in Einzelschritten
- Rueckfragen nach jedem Schritt
- verbal erklaerbar fuer Bildschirm plus Sprache

### 8. Intervention Rules

Diese Schicht entscheidet, wann umgeschaltet wird.

Beispiele:

- wenn der Nutzer wiederholt denselben Fehler macht -> kleinerer Schritt
- wenn Notation ueberfordert -> zurueck zu Bedeutung und Beispiel
- wenn Aufmerksamkeit bricht -> kuerzere Bloecke und Zwischenziel
- wenn Angst steigt -> Sicherheit, Klarheit, kein Beschaemen
- wenn Niveau zu niedrig ist -> mehr Formalitaet und Tempo

## Prio 1 des Tutors

Die erste Prioritaet ist nicht psychologische Tiefe.

Die erste Prioritaet ist:

- `Lerninhalte erfolgreich vermitteln`

Der Teacher Mind ist deshalb kein Selbstzweck.

Er dient dazu, dass mathematisches Wissen:

- ueberhaupt ankommt
- besser erinnert wird
- weniger ueberfordert
- und individueller erklaert werden kann

## Neue Reihenfolge des Aufbaus

Die Reihenfolge fuer den eigentlichen Aufbau lautet jetzt:

1. `Safety Layer`
2. `Psychological Foundations`
3. `Pedagogical Foundations`
4. `Mathematics Teaching Foundations`
5. `Learner Support Profiles`
6. `Pedagogical Strategy Matrix`
7. `Format and Accessibility Layer`
8. `Intervention Rules`

Damit ist klar:

- spezielle Unterstuetzungslogik kommt nicht zuerst
- sie wird auf ein starkes allgemeines Lern- und Lehrfundament gesetzt

## Warum Historie trotzdem wichtig bleibt

Der Tutor soll Mathematik oft ueber den Ursprungsgedanken erklaeren koennen.

Gerade bei schwierigen Themen hilft oft:

- Wozu brauchte man das?
- Welches Problem war vorher unloesbar?
- Welche reale Situation fuehrte zu dieser Idee?
- Wie wurde aus einer Intuition eine formale Theorie?

Deshalb bleibt die Bruecke zum `Knowledge Core` zentral:

- Ursprungsproblem
- historische Motivation
- erstes Anwendungsfeld
- spaetere Standardform
- heutige Praxis

## Beispiel: Differentialgleichung

Der Teacher Mind soll je nach Nutzer ganz anders ausspielen koennen:

### Laienmodus

- Veraenderung in Alltagssprache
- Warum normale Gleichungen nicht reichen
- kleines Wachstums- oder Bewegungsbeispiel
- erst danach Symbolik

### Studentenmodus

- Typ der Differentialgleichung
- Loesungsverfahren
- Rechenschritte
- Probe
- typische Fehler

### ADHS-nahe Unterstuetzung

- kurze Schritte
- klare Zwischenueberschriften
- schnelles Feedback
- wenig gleichzeitige Notation
- Handlungsschritt vor Theorieblock

### Dyskalkulie-nahe Unterstuetzung

- Zahlensinn und Groessenbedeutung zuerst
- langsame symbolische Uebersetzung
- visuelle oder tabellarische Hilfen
- wiederholte Rueckbindung an konkrete Bedeutung

## Lokale Geraetevision

Langfristig kann MathTeach als lokales Lerngeraet gedacht werden.

Zum Beispiel:

- Bildschirmgeraet
- Texteingabe und Spracheingabe
- Textausgabe und Sprachausgabe
- lokaler Speicher fuer Knowledge Core und Teacher Mind
- keine Pflicht zur Cloud-Nutzung

Dann entstuende:

- ein lokal laufender Mathe-Tutor
- mit starkem Fachwissen
- mit starker Vermittlung
- mit Privatsphaere
- und mit potenziell hoher sozialer Wirkung fuer Lernende mit wenig Zugang zu Nachhilfe

## Sozialer Zielwert

Die Vision ist nicht nur ein guter Tutor fuer privilegierte Nutzer.

Die Vision ist:

- ein bezahlbarer
- lokal nutzbarer
- extrem guter individueller Lernbegleiter

fuer:

- Kinder
- Jugendliche
- Studierende
- Promovierende
- Menschen mit besonderen Lernbedarfen
- und Menschen, die zuhause keine starke fachliche Unterstuetzung bekommen

## Empfohlene Aufbau-Reihenfolge

1. `Teacher Mind Charter`
2. `Safety and restraint rules`
3. `Learner support profiles`
4. `Pedagogical strategy matrix`
5. `Accessibility and format library`
6. `Tutor runtime modes`
7. `Teacher Mind evidence corpus`
8. `spaeter erst Psychologie- und Paedagogikgeschichte`

## Erste Projektentscheidung

Der Teacher Mind wird zuerst:

- funktional
- evidenzbasiert
- lokal adaptiv
- und mathematikdienlich

gebaut.

Nicht zuerst:

- historisch-chronologisch
- diagnostisch
- oder therapeutisch.
