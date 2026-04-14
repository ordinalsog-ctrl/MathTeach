# RPi Touch UI Lastenheft

## Zweck

Dieses Lastenheft uebersetzt die bereits vorhandenen MathTeach-
Grundlagen aus `Teacher Mind`, `Universal Round U.1`,
`Learner Support Profiles` und `architecture-v2` in konkrete
Anforderungen fuer die erste lokale Geraete-UI auf dem
`RPi Touch Display 2 (7")`.

Es ist bewusst kein Pixel-Styleguide.

Die harte Quelle-fuer-Regel-Uebersetzung fuer einzelne Screens liegt
zusaetzlich in:

- [device-ui-evidence-matrix.md](/Users/jonasweiss/MathTeach/docs/device-ui-evidence-matrix.md)

Es definiert:

- welche psychologischen und paedagogischen Wirkungen die UI erzeugen
  muss
- welche Barrieren sie aktiv vermeiden muss
- wie ein erster Schueler-Prototyp auf dem 800x480-Touchscreen
  funktionieren soll

## Quellenbasis in diesem Repo

Die Anforderungen unten sind aus bereits vorhandenen MathTeach-
Grundlagen destilliert, nicht frei erfunden:

- [architecture-v2.md](/Users/jonasweiss/MathTeach/docs/architecture-v2.md)
- [universal-round-u1-program.md](/Users/jonasweiss/MathTeach/docs/universal-round-u1-program.md)
- [learner-support-profiles.md](/Users/jonasweiss/MathTeach/docs/learner-support-profiles.md)
- [teacher-mind-foundation-stack.md](/Users/jonasweiss/MathTeach/docs/teacher-mind-foundation-stack.md)
- [support-response-matrix-adhd.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-adhd.md)
- [support-response-matrix-dyscalculia.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-dyscalculia.md)
- [support-response-matrix-scarcity.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-scarcity.md)

Implizite Leitquellen innerhalb dieser Dokumente sind unter anderem:

- `Self-Determination Theory`
- `Walton/Cohen Belonging`
- `SAMHSA Trauma-Informed`
- `CAST UDL`
- Scarcity-/Equity-Literatur

## Zielgeraet

Das erste Zielgeraet ist nicht Smartphone und nicht Browser-App im
Alltag, sondern ein lokales Lern-Geraet auf:

- `Raspberry Pi 5`
- `RPi Touch Display 2 (7")`
- `800x480`
- Querformat
- Touch-Bedienung
- offline-first

Konsequenzen:

- es gibt wenig vertikalen Platz
- Scrollen soll im Kernfluss vermieden werden
- Touch-Ziele muessen gross und fehlertolerant sein
- die UI wird auf ruhige, direkte 1-Gedanke-pro-Bildschirm-Fuehrung
  optimiert

## Primaere Nutzungslagen

Die erste UI muss fuer mindestens drei reale Nutzungslagen taugen:

### 1. Fragile Aufmerksamkeit / ADHS-nahe Nutzung

Braucht:

- geringe Reizlast
- klares Tempo
- sichtbare Zwischenorientierung
- keine langen Textwaende
- kein Gefuehl von Zeitdruck

### 2. Lernen ohne Rueckendeckung zu Hause

Braucht:

- sehr geringe Einstiegshuerde
- keine Eltern- oder Account-Abhaengigkeit
- klares Gefuehl von Sicherheit und Wuerde
- Tutor-Ton ohne Beschamung
- Wiederaufnahme genau dort, wo zuletzt gearbeitet wurde

### 3. Neugierige Selbstlerner

Brauchen:

- Zugang zu Tiefe, wenn gewuenscht
- keine kindische Gamification
- ernstnehmende Sprache
- das Gefuehl, dass das Geraet sie nicht klein haelt

## Nicht verhandelbare Wirkungen

Die UI muss spuerbar erzeugen:

- `Autonomie`: der Schueler erlebt echte Wahl und eigenes Tempo
- `Kompetenz`: der Schueler erlebt fruehe, sichtbare Verstehensmomente
- `Sicherheit`: die Oberflaeche wirkt vorhersagbar, nicht bedrohlich
- `Zugehoerigkeit`: die erste Ansprache signalisiert "Du gehoerst hier
  hin"
- `Fokus`: nichts konkurriert mit dem aktuellen Lernschritt

## Was die UI aktiv vermeiden muss

Diese Punkte sind fuer den ersten Prototypen bewusst ausgeschlossen:

- rote Fehlerbotschaften
- Timer, Countdowns oder sichtbarer Zeitdruck
- Prozent-Fortschrittsbalken
- Streaks, Badges, Punkte oder Ranglogik
- versteckte Navigation
- mehr als drei gleichzeitige Hauptoptionen
- klinische Profil- oder Diagnose-Sprache gegenueber Lernenden
- Browser-, Desktop- oder Dateisystem-Anmutung

## Visuelle Grundprinzipien

### 1. Ruhige, nicht sterile Flaeche

Die UI soll ruhig wirken, aber nicht wie generische KI- oder Business-
Software.

Das bedeutet:

- warmer Hintergrund statt hartem Reinweiss
- hohe Lesbarkeit ohne aggressive Kontraste
- klare Hierarchie statt bunter Reize
- Illustration oder visuelle Lernstuetze als echtes didaktisches
  Element, nicht als Dekoration

### 2. Illustration ist Kernbestandteil

Illustrationen sind fuer den ersten Prototypen kein Bonus.

Sie sind Teil der Lernstrategie:

- Idee zuerst sehen, dann sprachlich und symbolisch fassen
- besonders wichtig fuer Visualisierungsbedarf, fragile Aufmerksamkeit
  und symbolische Uebersetzungsprobleme
- Illustrationen werden als separate Assets eingebunden, nicht als
  improvisierte Inline-SVG-Konstrukte zur Laufzeit

### 3. Wenige, grosse Touch-Flächen

Richtwerte fuer 800x480:

- Hauptaktionen mindestens `72x72 px`
- nur `2-3` Hauptaktionen gleichzeitig
- der wichtige naechste Schritt muss ohne Suchblick antippbar sein

### 4. Typografie als Beruhigungsfaktor

Die Typografie muss lesbar, warm und nicht technisch wirken.

Anforderungen:

- grosszuegige Schriftgroessen
- kurze Zeilen
- klare Absaetze
- keine ueberladene Symbolhaeufung
- bei Bedarf spaeter optionale dyslexiefreundliche Font-Variante

## Sprachprinzipien

Der Tutor spricht:

- auf Augenhoehe
- nie vorwurfsvoll
- nie ueberrascht von Fehlern
- nie diagnostisch

Bevorzugte Form:

- `Wir schauen gemeinsam auf den naechsten Schritt.`
- `Lass uns das noch einmal ruhiger ansehen.`
- `Viele brauchen hier einen zweiten Blick.`

Zu vermeiden:

- `Falsch`
- `Das war leicht`
- `Du solltest das koennen`
- `Du bist noch nicht weit genug`

## Screen-Anforderungen fuer Prototyp 1

### 1. Ruhezustand / Startbildschirm

Der erste Bildschirm nach dem Einschalten muss:

- sofort sicher und ruhig wirken
- die letzte Lernstelle sichtbar machen
- genau eine primaere Handlung anbieten
- keine Menuewand erzeugen

Pflichtinhalte:

- Begruessung
- Name oder Profilbezeichnung des Geraets / Lernenden
- Hinweis auf letzten Stand
- primaerer Button `Weiterlernen`

Optional spaeter:

- `Neues Thema`
- `Heute nur kurz wiederholen`

Nicht auf diesem Bildschirm:

- Prozentfortschritt
- Leistungsbewertung
- viele Einstellungen

### 2. Erst-Onboarding

Das Onboarding dient nicht der Diagnose, sondern nur der ersten
didaktischen Orientierung.

Pflichtregeln:

- kurze, natuerliche Fragen
- keine klinischen Begriffe
- pro Bildschirm nur eine kleine Entscheidung
- erklaeren, warum gefragt wird, ohne zu pathologisieren

Geeignete Fragetypen:

- `Willst du lieber mit einem Bild starten oder mit Worten?`
- `Soll ich eher in kleinen Schritten erklaeren?`
- `Moechtest du oefter kurz anhalten und pruefen?`

### 3. Lernansicht

Die Lernansicht ist das Herzstueck des Geraets.

Pflichtstruktur:

- ein Lernziel oder Gedanke pro Bildschirm
- eine starke visuelle oder beispielhafte Verankerung
- begrenzte Textmenge
- maximal drei Hauptaktionen

Empfohlene Hauptaktionen:

- `Nochmal`
- `Zeig mir ein Beispiel`
- `Ich bin bereit fuer den naechsten Schritt`

Nicht zulassen:

- automatische Fortsetzung ohne aktive Schuelerentscheidung
- ueberladene Multipanels
- fachliche und navigative Information in einem Block

### 4. Fehler- und Stockungszustand

Wenn ein Schueler haengen bleibt, darf der Bildschirm nicht kippen in:

- Rot
- Alarm
- Abwertung
- hektisches Reframing

Stattdessen:

- ruhige Wiederorientierung
- ein kleinerer naechster Schritt
- alternative Darstellung
- explizite Entlastungssprache

## Screen-Layout-Regeln fuer 800x480

Fuer das Zielgeraet gelten:

- kein Smartphone-Layout recyceln
- kein enger Hochformat-Denken-Import
- Querformat als zusammenhaengende Flaeche behandeln
- keine harte Mittelachse nur aus App-Gewohnheit
- Illustration und Text muessen auf derselben Flaeche zusammenarbeiten,
  nicht in starre Karten gesperrt werden

## Konflikte, die die UI spaeter adaptiv loesen muss

Einige Spannungen sind unvermeidlich:

- ADHS-nahe Nutzung braucht weniger Reiz; neugierige Nutzer wollen
  mehr Tiefe
- textarme Erklaerung hilft vielen; manche wollen mehr historischen
  Kontext
- klare Struktur hilft bei Ueberforderung; zu viel Struktur kann fuer
  selbstsichere Lernende einengend wirken

Konsequenz:

Der erste Prototyp soll nicht alle Konflikte perfekt loesen.
Er braucht aber ein Grundlayout, das spaeter adaptiv variiert werden
kann, ohne seine psychologische Sicherheit zu verlieren.

## Abbruchmomente, gegen die die UI aktiv arbeiten muss

Die UI gilt als schlecht, wenn sie diese Momente verstaerkt:

- `Frustration`: "Ich weiss nicht, was ich jetzt tun soll."
- `Scham`: "Ich fuehle mich dumm oder bewertet."
- `Ueberforderung`: "Es ist zu viel auf einmal."
- `Langeweile`: "Das ist tot, mechanisch oder belanglos."

Jeder neue Bildschirm soll gegen diese vier Risiken geprueft werden.

## Definition of Done fuer Prototyp 1

Der erste UI-Prototyp ist gut genug, wenn:

- ein Schueler ohne Einweisung den Startbildschirm versteht
- das Onboarding ohne Diagnose- oder Testgefuehl auskommt
- die Lernansicht auf 800x480 ohne Scrollen klar lesbar bleibt
- `Nochmal` sich gleichwertig und nicht wie ein Scheitern anfuehlt
- die Illustration fachlich stuetzt statt zu dekorieren
- das Geraet im Eindruck eher wie ein persoenliches Lernwerkzeug als
  wie eine App wirkt
