# Tutor Runtime Modes

## Ziel

MathTeach soll nicht jede Lernfrage im selben Stil beantworten.

Es gibt mindestens zwei zentrale Hauptfaelle:

1. `Worked Example Tutoring`
2. `Origin Story Explanation`

Und einen Mischfall:

3. `Origin Then Example`

## 1. Worked Example Tutoring

Typische Nutzerfrage:

- `Erklaere mir Differentialgleichungen anhand dieses Beispiels.`
- `Hilf mir bei dieser Aufgabe.`

Was der Agent tun soll:

- Problemtyp erkennen
- Voraussetzungen knapp pruefen
- Beispiel Schritt fuer Schritt loesen
- jeden Schritt lokal begruenden
- Ergebnis kontrollieren

Historie:

- nur unterstuetzend
- nur wenn sie das Verstehen wirklich verbessert

## 2. Origin Story Explanation

Typische Nutzerfrage:

- `Erklaere mir als Mathe-Laie die Differentialgleichung.`
- `Warum brauchte man das?`
- `Wie ist das entstanden und wozu dient es?`

Was der Agent tun soll:

- mit dem urspruenglichen Problem beginnen
- erklaeren, warum das mathematische Objekt notwendig wurde
- erst dann die formale Sprache einfuehren
- ein einfaches Mini-Beispiel zeigen
- die moderne Anwendung anschliessen

Historie:

- ist hier nicht Zusatzmaterial
- ist der eigentliche Einstiegspfad

## 3. Origin Then Example

Typische Nutzerfrage:

- `Erklaere mir kurz, woher Differentialgleichungen kommen, und rechne dann mein Beispiel vor.`

Was der Agent tun soll:

- historische und intuitive Motivation zuerst
- dann direkt in das konkrete Beispiel des Lernenden wechseln
- am Ende die allgemeine Struktur benennen

## Routing-Regel

Der Planner soll deshalb nicht nur Alter und Niveau beachten, sondern auch die Form der Frage:

- enthaelt sie Beispiel- oder Aufgabensprache
- enthaelt sie Laien-, Warum- oder Ursprungs-Sprache
- verlangt sie eher Problemloesung oder Begriffserklaerung

## Beispiel Differentialgleichung

### Worked Example

Antwortbogen:

1. Was ist hier gegeben?
2. Welche Art Differentialgleichung ist das?
3. Welches Verfahren passt?
4. Rechenschritte
5. Probe

### Origin Story

Antwortbogen:

1. Welches reale Problem fuehrte zu Differentialgleichungen?
2. Warum reichen normale Gleichungen dafuer nicht?
3. Was bedeutet "Ableitung haengt von der Funktion ab" in Alltagssprache?
4. Einfachstes Beispiel
5. Moderne Anwendungen

## Repo-Artefakte

- [src/mathteach/services/planner.py](/Users/jonasweiss/MathTeach/src/mathteach/services/planner.py)
- [src/mathteach/models.py](/Users/jonasweiss/MathTeach/src/mathteach/models.py)
- [tests/test_api.py](/Users/jonasweiss/MathTeach/tests/test_api.py)
