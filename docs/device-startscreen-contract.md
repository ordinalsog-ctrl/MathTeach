# Device Startscreen Contract

## Zweck

Dieses Dokument beschreibt den `Startscreen / Ruhezustand` des
MathTeach-Devices als verbindlichen Screen-Contract.

Es ist bewusst:

- kein Mockup
- kein CSS-Briefing
- kein Moodboard

Es legt nur fest:

- welche psychologische Aufgabe dieser Screen hat
- welche Inhalte er tragen muss
- welche Inhalte er nicht tragen darf
- welche Zustandslogik er braucht
- wann der Screen als korrekt umgesetzt gilt

## Quellenbasis

Dieser Contract ist direkt aus folgenden Repo-Dokumenten abgeleitet:

- [device-ui-evidence-matrix.md](/Users/jonasweiss/MathTeach/docs/device-ui-evidence-matrix.md)
- [rpi-touch-ui-lastenheft.md](/Users/jonasweiss/MathTeach/docs/rpi-touch-ui-lastenheft.md)
- [universal-round-u1-program.md](/Users/jonasweiss/MathTeach/docs/universal-round-u1-program.md)
- [support-response-matrix-adhd.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-adhd.md)
- [support-response-matrix-autism.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-autism.md)
- [support-response-matrix-scarcity.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-scarcity.md)
- [pedagogical-strategy-matrix.md](/Users/jonasweiss/MathTeach/docs/pedagogical-strategy-matrix.md)

## Psychologische Hauptaufgabe

Der Startscreen hat genau eine Hauptaufgabe:

`einen ruhigen, wuerdevollen Wiedereinstieg mit minimaler Entscheidungslast ermoeglichen`

Das bedeutet:

- kein Screen fuer Orientierung ueber das ganze Produkt
- kein Screen fuer Einstellungen
- kein Screen fuer Motivationsspielerei
- kein Screen fuer Leistungsauswertung

## Primaere Risiken, die dieser Screen reduzieren muss

### 1. Ueberforderung beim Einstieg

Der Lernende darf beim ersten Blick nicht entscheiden muessen:

- welches Thema
- welcher Modus
- welche Einstellung
- welcher Verlauf

sondern nur:

- `kann ich jetzt sicher weitermachen?`

### 2. Beschamung

Der Screen darf keinerlei Ton oder Struktur tragen, die sagt:

- du bist hinten
- du hast zu wenig geschafft
- du bist noch nicht weit

### 3. Unterbrechungsbruch

Nach Unterbrechung muss der Faden wieder sichtbar werden, ohne dass der
Lernende den gesamten Kontext neu aufbauen muss.

### 4. Institutionelle Reibung

Der Screen darf nicht wie Login, Schulportal, App-Startseite oder
Lernplattform-Dashboard wirken.

## Harte Funktionsaufgabe

Der Startscreen hat nur drei legitime Funktionen:

1. den letzten sinnvollen Stand sichtbar machen
2. den naechsten sicheren Wiedereinstieg anbieten
3. einen alternativen Neustart nur schwach und kontrolliert anbieten

Alles andere ist fuer diesen Screen nachrangig.

## Verbindliches Inhaltsbudget

Der Startscreen darf maximal diese Inhaltsmenge tragen:

- `1` Begruessung
- `1` Resume-Block
- `1` primaere Handlung
- optional `1` schwache Sekundaerhandlung
- optional `1` kurze entlastende Notiz

Nicht erlaubt:

- mehrere Resume-Bloecke
- mehrere gleichgewichtige Themenvorschlaege
- Verlauf + Ziele + Einstellungen + Historie gleichzeitig

## Pflichtinhalte

### 1. Zugehoerige Begruessung

Muss:

- ruhig
- nicht diagnostisch
- nicht leistungsorientiert

Beispielcharakter:

- "Schoen, dass du da bist."
- "Wir gehen in deinem Tempo weiter."

Nicht erlaubt:

- "Du bist bereit fuer Level 2"
- "Heute schaffst du mehr"
- "Du bist hinter deinem Ziel"

### 2. Resume-Kern

Muss sichtbar machen:

- wo der Lernende zuletzt war
- was der naechste kleine Schritt ist

Muss nicht sichtbar machen:

- komplette Session-Historie
- Bewertung
- Statistiken

Resume-Form:

- Thema oder letzter Lernschritt
- kurzer Wiedereinstiegssatz

### 3. Primaere Handlung

Muss:

- eindeutig dominant sein
- sprachlich ruhig sein
- direkt zum Wiedereinstieg fuehren

Bevorzugte Form:

- `Weiterlernen`
- `Hier weitermachen`

Nicht erlaubt:

- mehrere gleich dominante Buttons
- primaerer CTA fuer Settings oder Profilbearbeitung

### 4. Optionale Sekundaerhandlung

Nur erlaubt, wenn sie die primaere Handlung nicht visuell konkurrenziert.

Zulaessig:

- `Neues Profil einrichten`
- `Thema wechseln` spaeter eventuell, aber nicht als gleich dominante Flaeche

Nicht zulaessig:

- mehrere Sekundaeroptionen gleichzeitig
- CTA-Cluster

### 5. Entlastende Notiz

Optional und nur kurz.

Funktion:

- signalisiert Sicherheit
- reduziert Scham
- bestaetigt, dass Wiedereinstieg klein beginnen darf

Beispielcharakter:

- "Ein kleiner Schritt reicht fuer jetzt."
- "Viele brauchen hier einen zweiten Blick."

## Verbotene Inhalte

Folgendes ist auf dem Startscreen nicht zulaessig:

- Prozentfortschritt
- Tagesziele
- Punkte, Badges, Streaks
- Test- oder Diagnosehinweise
- mehrere Themenkarten
- mehr als zwei sichtbare Handlungsrichtungen
- Menueleisten, Tabs oder Dashboard-Navigation
- dense Informationsflaechen
- Illustration ohne klare Funktion

## Zustandslogik

Der Startscreen braucht genau diese drei Zustaende.

### Zustand A: Kein Verlauf vorhanden

Pflicht:

- ruhige Erstbegruessung
- klares Signal, dass ein erster Start klein und sicher ist
- primaerer CTA fuehrt in das erste Onboarding oder direkt in einen
  ersten kleinen Einstieg

Nicht zeigen:

- leere Verlaufscontainer
- Systemstatus-Rauschen

### Zustand B: Resume verfuegbar

Pflicht:

- letzter sinnvoller Stand
- ein klarer Satz zum Wiedereinstieg
- primaerer CTA: `Weiterlernen`

Das ist der Normalzustand.

### Zustand C: Letzte Session defekt oder unvollstaendig

Pflicht:

- keine technische Sprache
- Wiedereinstieg ueber den letzten sicheren Punkt
- ruhiger Ausweichsatz

Beispielcharakter:

- "Wir steigen beim letzten sicheren Schritt wieder ein."

Nicht erlaubt:

- Fehlermeldungston
- technische Details
- rote Warnflaechen

## Sprachregeln

Der Startscreen spricht:

- auf Augenhoehe
- langsam
- nicht schulportalhaft
- nicht marketinghaft

Muss vermeiden:

- Leistungsdramatik
- Motivationsslogans
- Drucksprache
- Diagnosesprache

## Illustrationsregel fuer diesen Screen

Wenn eine Illustration spaeter eingesetzt wird, dann nur unter diesen
Bedingungen:

- sie darf den Resume-Kern nicht ueberstimmen
- sie muss Ruhe und Orientierung stuetzen
- sie darf keine zusaetzliche Deutungsaufgabe erzeugen
- sie muss fuer `800x480` auf einen Blick lesbar sein

Fuer den Startscreen ist eine Illustration optional.
Sie ist nicht wichtiger als Resume-Klarheit.

## Layoutfolgen ohne Designvorgabe

Dieser Contract schreibt kein Pixel-Layout vor, aber folgende
Wirkungsregeln:

- der primaere Blick muss zuerst auf Begruessung und Resume fallen
- die primaere Handlung muss ohne Suchblick auffindbar sein
- nichts darf gleich wichtig wirken wie `Weiterlernen`
- die Flaeche muss leer genug sein, um nicht wie eine App-Startseite zu
  wirken

## Akzeptanzkriterien

Der Startscreen gilt nur dann als korrekt umgesetzt, wenn alle Punkte
erfuellt sind:

1. Ein neuer Lernender versteht in unter drei Sekunden, was die
   Hauptaktion ist.
2. Ein wiederkehrender Lernender erkennt sofort, wo er zuletzt war.
3. Der Screen erzeugt keinen Eindruck von Bewertung oder Rueckstand.
4. Es gibt nie mehr als eine dominante Handlung.
5. Die sichtbare Inhaltsmenge bleibt innerhalb des Budgets.
6. Der Screen funktioniert ohne Scrollen.
7. Keine sichtbare Struktur erinnert primaer an Dashboard, Portal oder
   generische Lern-App.

## Naechste Ableitung

Wenn dieser Contract akzeptiert ist, folgt danach erst:

- ein `Startscreen Blueprint`

und noch nicht:

- ein Mockup
- eine Illustration
- eine Implementation
