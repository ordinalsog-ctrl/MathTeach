# Data Foundation

## Ausgangsidee

Die Datenbasis von MathTeach besteht aus zwei streng getrennten Schichten:

1. `Knowledge Core`
2. `Teacher Mind`

Diese Trennung ist kein Detail, sondern ein Sicherheits- und Qualitaetsprinzip.

## 1. Knowledge Core

Der Knowledge Core enthaelt Mathematik in sachlicher, nuechterner Form.

Er speichert:

- Begriffe und Definitionen
- Gleichungen und Notationen
- Theoreme und Voraussetzungen
- Beweisideen
- historische Herkunft
- moderne Anwendungen
- Quellenketten bis auf Segmentebene
- Abhaengigkeiten zwischen Konzepten

Der Knowledge Core darf keine Motivationstricks, Zielgruppenrhetorik oder emotionalen Formulierungen enthalten.

Seine Regeln:

- fachliche Aussagen muessen zitierbar sein
- historische Aussagen muessen belegbar sein
- Unsicherheit wird markiert, nicht kaschiert
- verschiedene Darstellungen duerfen gespeichert werden, aber nicht mit Wahrheitsanspruch vermischt werden

## 2. Teacher Mind

Der Teacher Mind ist die psychologisch-paedagogische Vermittlungsschicht.

Er speichert:

- Unterrichtsstile
- Erklaerstrategien
- Motivationsmuster
- Fehlvorstellungs-Diagnostik
- Tonalitaet und Framing
- Anpassung an Alter, Vorwissen und Selbstvertrauen
- Interventionsregeln bei Frust, Ueberforderung oder Langeweile

Der Teacher Mind kennt also nicht "neue Mathematik", sondern Wege, dieselbe Mathematik wirksam zu lehren.

Seine Regeln:

- keine Veraenderung fachlicher Kernaussagen
- keine Erfindung von Quellen
- keine Vereinfachung, die mathematisch falsch wird
- didaktische Adaption nur innerhalb des vom Knowledge Core erlaubten Rahmens

## Handoff zwischen beiden Schichten

Der Laufzeitfluss sollte immer so aussehen:

1. Nutzerziel verstehen
2. Learner-Profil bestimmen
3. Fakten aus dem `Knowledge Core` abrufen
4. Vermittlungsstrategie aus dem `Teacher Mind` waehlen
5. Antwort erzeugen
6. Korrektheit und Passung pruefen

## Persistente Datenbereiche

### Knowledge Schema

- `source_document`
- `source_segment`
- `concept`
- `equation`
- `theorem`
- `application`
- `knowledge_edge`
- `claim_evidence`

### Teacher Schema

- `teacher_profile`
- `teaching_strategy`
- `teacher_rule`
- `misconception_pattern`
- `lesson_template`

## Erste Build-Reihenfolge

1. Quellenkatalog aufbauen
2. Segmente mit Zitationspfad speichern
3. Konzepte, Gleichungen und Theoreme extrahieren
4. Kanten fuer Voraussetzungen und Historie aufbauen
5. Lehrerregeln und Erklaerstrategien separat modellieren
6. Beide Schichten erst in der Laufzeit wieder zusammenfuehren

## Entscheidender Vorteil

Wenn diese Trennung sauber bleibt, kann MathTeach gleichzeitig:

- fachlich streng bleiben,
- didaktisch flexibel werden,
- Halluzinationen besser kontrollieren,
- neue Unterrichtsstile testen, ohne die Mathematik-Datenbasis zu beschaedigen.
