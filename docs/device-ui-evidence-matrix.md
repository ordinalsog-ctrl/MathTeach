# Device UI Evidence Matrix

## Zweck

Dieses Dokument ist die harte Uebersetzung der vorhandenen
MathTeach-Quellen in verbindliche UI-Regeln fuer das Device.

Es ist absichtlich:

- kein Mockup
- kein Moodboard
- kein Styleguessing

Es beantwortet nur diese Frage:

`Welche sichtbaren UI-Regeln muessen gelten, wenn MathTeach die
psychologischen und paedagogischen Quellen ernst nimmt?`

## Quellenbasis

Diese Matrix ist direkt aus den bereits vorhandenen Repo-Dokumenten
gezogen:

- [universal-round-u1-program.md](/Users/jonasweiss/MathTeach/docs/universal-round-u1-program.md)
- [support-response-matrix-adhd.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-adhd.md)
- [support-response-matrix-dyscalculia.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-dyscalculia.md)
- [support-response-matrix-dyslexia.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-dyslexia.md)
- [support-response-matrix-autism.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-autism.md)
- [support-response-matrix-scarcity.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-scarcity.md)
- [pedagogical-strategy-matrix.md](/Users/jonasweiss/MathTeach/docs/pedagogical-strategy-matrix.md)
- [rpi-touch-ui-lastenheft.md](/Users/jonasweiss/MathTeach/docs/rpi-touch-ui-lastenheft.md)

## Hauptregel

MathTeach-UI wird nicht von Stilideen aus gebaut.

Sie wird von vier Risiken aus gebaut:

- Ueberforderung
- Beschamung
- Desorientierung
- Bedeutungsverlust

Jede sichtbare UI-Entscheidung muss mindestens eines dieser Risiken
reduzieren.

## Globale psychologische Verpflichtungen

Aus `U.1`, den Support-Matrizen und dem Lastenheft folgen diese
globalen Pflichten:

### 1. Autonomie

Die UI muss Wahl und eigenes Tempo spuerbar lassen.

Deshalb:

- keine automatische Fortsetzung
- kein versteckter Zwang zum Weitergehen
- Handlungen muessen klar und gleichwertig lesbar sein

### 2. Sicherheit

Die UI darf nicht wie Bewertung, Pruefung oder Zeitdruck wirken.

Deshalb:

- kein Rot als Fehlercode
- keine Countdowns
- keine Leistungsanzeigen
- keine harte Erfolgs-/Misserfolgsdramaturgie

### 3. Zugehoerigkeit

Die erste Ansprache muss zeigen, dass der Lernende hier richtig ist.

Deshalb:

- ruhiger Ton
- keine Defizit- oder Diagnosesprache
- kein implizites "das solltest du koennen"

### 4. Fokus

Die UI darf nicht mehr konkurrierende Dinge zeigen, als das
Arbeitsgedaechtnis sicher tragen kann.

Deshalb:

- ein Gedanke pro Bildschirm
- maximal drei Hauptaktionen
- sichtbare Hierarchie statt Panel-Stapel

### 5. Bedeutungsprioritaet

Mathematik muss zuerst als Handlung, Beziehung oder Menge lesbar sein,
nicht nur als Symbolkette.

Deshalb:

- Bedeutung vor Symbolverdichtung
- Bild/Beispiel vor dichter Notation
- bei Zahlthemen Menge oder Struktur zuerst

## Harte globale Verbote

Diese Muster sind fuer MathTeach-UI nicht zulaessig:

- generische Dashboard- oder Kartenwand als Grundlayout
- mehr als drei gleichzeitige Hauptentscheidungen
- ein Onboarding, das mehrere Fragenbloecke gleichzeitig stapelt
- dense Sidebar-/Panel-Architektur mit konkurrierenden Informationssaeulen
- rein dekorative Illustration ohne mathematische Funktion
- Timer, Prozentbalken, Streaks, Badges, Punkte
- rote Fehlerflaechen oder strafende Zustandsfarben
- Diagnose- oder Identitaetssprache gegenueber Lernenden
- Browser-/Desktop-/Dateisystem-Anmutung

## Screen-Budgets

`800x480` ist klein.

Darum bekommt jeder Screen ein hartes Kompositionsbudget.

### Globales Screen-Budget

- genau `1` primaere Idee pro Screen
- genau `1` primaerer Blickanker
- hoechstens `3` Hauptaktionen
- hoechstens `2` unterstuetzende Textbloecke zusaetzlich zur Hauptidee
- keine Scrollpflicht im Kernfluss

## Matrix nach Screen

## 1. Startscreen / Ruhezustand

### Psychologische Aufgabe

- Sicherheit beim Wiedereinstieg
- minimale Einstiegshuerde
- klares "hier geht es weiter"

### Muss

- Begruessung ohne Leistungston
- letzter Stand oder letzter sinnvoller Wiedereinstieg
- genau eine dominant sichtbare primaere Handlung
- sichtbarer Wiedererkennungsanker fuer den Lernenden

### Darf

- eine ruhige zusaetzliche Sekundaerhandlung
- ein kleiner Hinweis, warum der naechste Schritt ueberschaubar ist

### Darf nicht

- Themenwahl, Einstellungen, Verlauf und Ziele gleichzeitig zeigen
- mehrere grosse Karten mit gleichem Wichtigkeitsgrad
- UI-Chrome, Menues oder "App"-Navigation in den Vordergrund holen
- eine Illustration nutzen, die nur Stimmung macht, aber nichts traegt

### Hartes Inhaltsbudget

- `1` Hauptsatz
- `1` Resume-Block
- `1` primaerer Button
- optional `1` schwache Sekundaerhandlung

### Quellenbegruendung

- `scarcity`: geringe Friktion, klarer Wiedereinstieg, sichtbarer Nutzen
- `U.1`: Autonomie ohne Kontrolle
- `belonging/safety`: sicher statt pruefungsartig

## 2. Onboarding

### Psychologische Aufgabe

- didaktische Orientierung, nicht Diagnose
- keine Beschamung
- geringe kognitive Last

### Muss

- in kleine Einzelschritte zerlegt sein
- pro Screen nur eine kleine Entscheidung tragen
- erklaeren, warum gefragt wird
- natuerliche Sprache statt klinischer Begriffe nutzen

### Darf

- binäre oder kleine Auswahlfragen zeigen
- kurze Beispielantworten geben
- erklaeren, dass Antworten nur die Darstellungsform aendern

### Darf nicht

- mehrere Fragenbloecke gleichzeitig auf einen Screen stapeln
- Checkbox-Waende zeigen
- den Eindruck eines Tests oder Diagnosebogens erzeugen
- mehr als `3` Optionen auf einmal gleichgewichtig zeigen

### Hartes Inhaltsbudget

Pro Onboarding-Screen:

- `1` Frage
- `1` kurzer Grund dafuer
- `2` bis `3` Antwortoptionen
- `1` klare Weiter-Aktion

### Quellenbegruendung

- `ADHD`: short chunks, max three core points
- `Autism`: explicit structure, predictable shifts
- `Dyslexia`: reduced clutter, very short chunks
- `U.1`: never frame struggle as identity failure

## 3. Lernscreen

### Psychologische Aufgabe

- eine mathematische Idee sicher tragen
- Fokus halten
- naechsten Schritt explizit machen

### Muss

- genau eine mathematische Hauptidee zeigen
- genau einen mathematischen visuellen Traeger haben
- Uebergang explizit markieren: jetzt / danach / naechster Schritt
- den naechsten kleinen Schritt sichtbar machen
- bei Fehlern oder Stockung die Idee verkleinern statt die Flaeche zu vergroessern

### Darf

- eine kurze Randnotiz fuer Fokus
- eine kurze Randnotiz fuer Scaffolds
- zwei bis drei klar unterscheidbare Handlungen

### Darf nicht

- mehrere Panels mit gleichem Aufmerksamkeitsanspruch nebeneinander stellen
- gleichzeitig Ziel, Theorie, Historie, Beispiel, Uebung und Meta-Infos stapeln
- eine Illustration zeigen, die mathematisch nichts erklaert
- Dense Symbolik vor Handlung oder Bedeutung setzen

### Hartes Inhaltsbudget

- `1` visuelle Hauptdarstellung
- `1` kurze Hauptaussage
- `1` kurzer Relevanz- oder Uebergangssatz
- `1` Fokusblock
- `1` Scaffoldblock
- `2` bis `3` Aktionen

### Quellenbegruendung

- `ADHD`: verbal + visual before dense symbolic
- `Dyscalculia`: quantity visual first, simple and quantity explicit
- `Dyslexia`: visual plus supported language before dense text
- `Autism`: stable visual structure, explicit transition cues
- `Scarcity`: why this matters now, small wins sequence
- `Pedagogical strategy matrix`: Bedeutung vor Symbol, Schritt fuer Schritt

## Farb- und Kontrastregeln

Dieses Dokument definiert keine Palette nach Geschmack, aber klare
Wirkungsregeln:

### Muss

- ruhige, warme Grundflaechen
- klarer Lesekontrast
- sehr sparsame Akzentfarbe
- Farbgebrauch nur mit Funktion

### Darf nicht

- Alarmrot fuer Korrektur oder Fehler
- mehrere starke Akzentfarben gleichzeitig
- dunkle, dichte, dramatische Flaechen ohne didaktischen Grund
- Farbwechsel als Ersatz fuer Struktur

### Quellenbegruendung

- `SAMHSA`-Linie im Lastenheft: Sicherheit vor Bedrohungssignalen
- `Autism`: minimal and high contrast
- `Dyslexia`: reduced visual clutter

## Illustrationsregeln

### Muss

- mathematische Funktion haben
- auf die aktuelle Idee verweisen
- simpel genug sein, um auf `800x480` sofort lesbar zu bleiben

### Darf nicht

- dekorative Platzhalter sein
- "Lernstimmung" simulieren, ohne mathematische Arbeit zu leisten
- mehrere konkurrierende Blickanker erzeugen

### Prioritaet fuer fruehe Algebra

Fuer lineare Gleichungen gilt:

- Balance- oder Mengenmodell vor freier Werkbank-Illustration
- Handlung "auf beiden Seiten gleich" muss sichtbar sein
- Ergebnis muss als reduzierte Reststruktur lesbar werden

## Konsequenz fuer die naechste UI-Arbeit

Bevor ein neuer Screen gezeichnet oder implementiert wird, muss er in
dieser Reihenfolge beschrieben werden:

1. psychologische Hauptaufgabe des Screens
2. primaere Quelle(n)
3. hartes Screen-Budget
4. klare Verbote fuer diesen Screen
5. erst danach Layout

## Minimaler Review-Check

Ein Device-Screen darf nur gebaut werden, wenn alle Fragen mit `ja`
beantwortet werden:

1. Reduziert der Screen Ueberforderung?
2. Vermeidet der Screen Beschamung?
3. Ist der naechste Schritt explizit?
4. Hat die Illustration mathematische Funktion?
5. Ist die Menge sichtbarer Dinge fuer `800x480` hart begrenzt?
