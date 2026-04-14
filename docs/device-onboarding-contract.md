# Device Onboarding Contract

## Zweck

Dieses Dokument beschreibt das `Onboarding` des MathTeach-Devices als
verbindlichen Screen- und Fluss-Contract.

Es legt fest:

- welche psychologische Aufgabe Onboarding in MathTeach hat
- welche Entscheidungen dort ueberhaupt erlaubt sind
- wie klein ein Onboarding-Schritt bleiben muss
- welche Muster ausdruecklich verboten sind

Es ist bewusst:

- kein Formularentwurf
- kein Wireframe
- keine visuelle Gestaltungsvorgabe

## Quellenbasis

Dieser Contract ist direkt aus folgenden Repo-Dokumenten abgeleitet:

- [device-ui-evidence-matrix.md](/Users/jonasweiss/MathTeach/docs/device-ui-evidence-matrix.md)
- [rpi-touch-ui-lastenheft.md](/Users/jonasweiss/MathTeach/docs/rpi-touch-ui-lastenheft.md)
- [universal-round-u1-program.md](/Users/jonasweiss/MathTeach/docs/universal-round-u1-program.md)
- [support-response-matrix-adhd.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-adhd.md)
- [support-response-matrix-dyscalculia.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-dyscalculia.md)
- [support-response-matrix-dyslexia.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-dyslexia.md)
- [support-response-matrix-autism.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-autism.md)
- [support-response-matrix-scarcity.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-scarcity.md)

## Psychologische Hauptaufgabe

Das Onboarding hat genau eine Hauptaufgabe:

`die erste didaktische Orientierung mit minimaler Last und ohne
Pathologisierung zu gewinnen`

Es ist nicht da fuer:

- Diagnose
- Profilkategorisierung gegenueber dem Lernenden
- Vollerhebung von Vorlieben
- Setup-Komplettierung

## Primaere Risiken, die Onboarding reduzieren muss

### 1. Beschamung

Der Lernende darf nicht das Gefuehl bekommen:

- geprueft zu werden
- eingeordnet zu werden
- ein Problemfall zu sein

### 2. Ueberforderung

Onboarding darf nicht mehrere Entscheidungen oder Signalkanäle
gleichzeitig verlangen.

### 3. Friktion

Onboarding darf nicht so gross werden, dass der erste Lerneinstieg
dadurch gebremst wird.

### 4. Falsche Endgueltigkeit

Die Antworten im Onboarding duerfen nicht wie starre Wahrheit wirken.

## Harte Funktionsaufgabe

Onboarding darf nur diese drei Dinge leisten:

1. einen ersten Lernwunsch oder Startgegenstand klaeren
2. die Darstellungsform fuer den ersten Einstieg grob ausrichten
3. den ersten Lernschritt schnell freigeben

Alles Weitere ist spaeter oder adaptiv im Betrieb zu klaeren.

## Was Onboarding ausdruecklich nicht ist

Onboarding ist nicht:

- Profiltest
- Support-Bedarfsbogen
- Accessibility-Center
- Settings-Seite
- Interessen- und Historienformular

## Grundregel fuer die Flusslogik

`Ein Onboarding-Screen = eine kleine Entscheidung`

Nicht erlaubt:

- mehrere Fragebloecke auf derselben Flaeche
- mehrere Entscheidungstypen auf einmal
- Textfeld + Chips + Checkboxgruppen gleichzeitig

## Erlaubte Entscheidungstypen

Im fruehen Device-Onboarding sind nur diese Typen zulaessig:

### 1. Startwunsch

Beispielcharakter:

- "Womit willst du zuerst anfangen?"
- "Was willst du gerade verstehen?"

### 2. Darstellungsstart

Beispielcharakter:

- "Soll ich mit einem Bild beginnen oder mit Worten?"

### 3. Schrittgroesse

Beispielcharakter:

- "Sollen wir in kleinen Schritten starten?"

### 4. Optionale Unterstuetzung in Alltagssprache

Beispielcharakter:

- "Hilft es dir, wenn ich weniger Text auf einmal zeige?"
- "Hilft es dir, wenn ich oefter kurz anhalte?"

Nicht erlaubt:

- "Hast du ADHS?"
- "Bist du dyslexisch?"
- "Welche Diagnose trifft zu?"

## Verbindliches Inhaltsbudget pro Onboarding-Screen

Jeder Onboarding-Screen darf maximal enthalten:

- `1` Frage
- `1` kurzer Satz, warum gefragt wird
- `2` bis `3` Antwortoptionen
- `1` primaere Weiter-Aktion
- optional `1` schwache Zurueck-Aktion

Nicht erlaubt:

- mehr als `3` gleichzeitige Optionen
- Checkbox-Waende
- mehr als `1` Eingabefeld auf einem Schritt
- mehrere primaere Handlungen

## Sprachregeln

Onboarding spricht:

- natuerlich
- nicht klinisch
- nicht testhaft
- nicht technisch

Muss vermeiden:

- Diagnosebegriffe
- Defizit-Sprache
- institutionellen Formular-Ton
- Suggestion, dass die Antwort etwas ueber Wert oder Faehigkeit sagt

Zulaessiger Erklaersatz:

- "Ich frage nur, wie ich am besten erklaere."

Nicht zulaessig:

- "Diese Angaben bestimmen dein Profil."
- "Diese Einschraenkung wird gespeichert."

## Fortschrittslogik

Onboarding darf Orientierung geben, aber nicht Druck erzeugen.

Darum:

- Schrittzahl nur schwach und ruhig
- kein Prozentbalken
- keine "fast geschafft"-Dramatik
- kein Tempo-Signal

Wenn Fortschritt sichtbar gemacht wird, dann nur als:

- diskreter Schrittindikator
- ruhige Benennung des aktuellen Schritts

## Screen-spezifische Verbote

Folgendes ist im Onboarding nicht zulaessig:

- ein einziger grosser Screen mit allen Fragen
- Rollen- oder Diagnosezuschreibungen
- grosse Formularflaechen
- Settings-Optik
- Bewertungs- oder Pruefungston
- mehrere Farbakzente mit konkurrierenden Bedeutungen
- dekorative Illustration, die die Frage nicht stuetzt

## Zustandslogik

Das Onboarding braucht minimal diese Zustandsunterscheidung:

### Zustand A: Erster Einstieg

Pflicht:

- sehr niedrige Last
- keine Rueckfragen zur Vergangenheit
- sofortiger Startcharakter

### Zustand B: spaetere Anpassung

Falls Onboarding spaeter erneut betreten wird:

- als ruhige Aenderung der Darstellungsform
- nicht als kompletter Reset
- keine Neuabfrage bereits stabiler Dinge ohne Grund

## Illustrationsregel fuer Onboarding

Wenn spaeter eine Illustration eingesetzt wird, dann nur:

- zur Unterstuetzung der aktuellen Frage
- nicht als Deko
- nicht als Clipart fuer "Lernen"
- nicht als konkurrierender Blickanker

Beispiel:

- fuer `Bild oder Worte?` darf eine einfache Gegenueberstellung
  unterschiedlicher Zugangsformen helfen
- fuer `kleine Schritte` darf eine ruhige Sequenzidee helfen

Nicht erlaubt:

- allgemeine Schueler-, Heft- oder Symbol-Illustration ohne Bezug zur
  aktuellen Entscheidung

## Akzeptanzkriterien

Das Onboarding gilt nur dann als korrekt, wenn:

1. jeder Screen nur eine kleine Entscheidung traegt
2. keine Diagnose- oder Defizit-Sprache sichtbar ist
3. der Lernende nie mehr als drei Optionen gleichzeitig abwaegen muss
4. der erste Lernschritt schnell erreichbar bleibt
5. die UI eher wie ein ruhiger Dialog als wie ein Formular wirkt
6. keine Screen-Struktur an Umfrage, Schulportal oder Setup-Wizard
   erinnert

## Naechste Ableitung

Wenn dieser Contract akzeptiert ist, folgt erst danach:

- ein `Onboarding Flow Blueprint`

und noch nicht:

- Mockup
- Screen-Design
- Implementierung
