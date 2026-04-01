# Universal Tutor System Review Triage 2026-04-01

## Ergebnis

Der neue Review wird in seinem Kern angenommen.

Er praezisiert das Projektziel deutlich:

- MathTeach ist nicht nur ein mathematischer Tutor
- MathTeach ist ein `universelles, lokales, armutssensibles und inklusives Mathematik-Lernsystem`

Die Zielgruppen sind damit ausdruecklich:

- Kinder und Jugendliche
- armutsbetroffene Lernende
- Lernende mit ADHS-, Dyskalkulie-, Dyslexie- oder anderen relevanten Unterstuetzungsbedarfen
- Studierende
- erwachsene Selbstlerner

## Was sich dadurch strategisch aendert

Bisher war die Architektur logisch so geordnet:

1. allgemeine psychologische Grundlagen
2. allgemeine paedagogische Grundlagen
3. spaeter spezialisierte Unterstuetzung

Diese Reihenfolge bleibt im Grundsatz richtig.

Aber:

`Neurodiversitaet, Equity und Inklusion duerfen jetzt nicht mehr als spaete Zusatzschicht behandelt werden.`

Sie werden ab jetzt als:

- `fruehe Design-Constraints`
- und `parallele Grundlagenanforderungen`

behandelt.

Das bedeutet:

- sie kommen nicht vor den allgemeinen Lern- und Lehrgrundlagen
- aber sie duerfen auch nicht erst ganz am Ende erscheinen

## Neue strategische Einordnung

Fuer das Projekt ergibt sich jetzt folgende Struktur:

### Tier A. System Invariants

Diese Punkte sind nicht optional und keine spaeten Features:

- `geschlossenes lokales System`
- `keine Cloudpflicht`
- `kostenguenstige Bereitstellung`
- `nutzbar als App oder Geraet`
- `lokale Speicherung sensibler Lerndaten`
- `Eignung auch fuer armutsbetroffene Lernende`

### Tier B. Universal Foundations

Diese Schicht bleibt der erste Wissensaufbau:

- `Psychological Foundations`
- `Pedagogical Foundations`
- spaeter `Mathematics Teaching Foundations`

### Tier C. Early Universal Design Constraints

Diese Schicht wird ab jetzt parallel frueh aufgebaut und nicht auf spaeter verschoben:

- `Universal Design for Learning`
- `Inclusion and Equity`
- `Neurodiversity-aware design`
- `poverty and scarcity aware design`
- `trauma-informed safety`
- `lifespan awareness`
- `multimodal and sensory accessibility`

### Tier D. Specific Support Logic

Erst danach folgen die ausdifferenzierten Regelwerke fuer:

- ADHS-nahe Unterstuetzung
- Dyskalkulie-nahe Unterstuetzung
- Dyslexie-nahe Unterstuetzung
- Autismusspektrum-nahe Unterstuetzung
- ELL- oder sprachsensible Unterstuetzung
- weitere spezifische Profile

## Was aus dem Review sofort hochgestuft wird

### 1. Neurodiversity is not optional

Dieser Punkt wird inhaltlich angenommen.

Wenn das Ziel ein universeller Tutor ist, duerfen ADHS, Dyskalkulie, Dyslexie und Autismusspektrum-nahe Anforderungen nicht als ferne Erweiterung behandelt werden.

Sie werden ab jetzt:

- nicht als reine spaete Spezialfunktion
- sondern als `fruehe Designanforderung`

gefuehrt.

Wichtig:

Das heisst nicht, dass sofort klinische Volltiefe gebaut wird.

Es heisst:

- fruehe Einplanung in Format, Pacing, Struktur, Feedback und Reizlast
- spaetere Vertiefung in die spezifischen Unterstuetzungslogiken

### 2. Equity and Poverty Sensitivity

Dieser Punkt wird deutlich hochgestuft.

Da der soziale Zielwert explizit armutsbetroffene Lernende einschliesst, darf `poverty-aware design` nicht nur eine spaetere soziale Zusatzperspektive sein.

Er wird ab jetzt verstanden als:

- Komplexitaetsreduktion
- hohe Transparenz
- geringe Eintrittshuerden
- hohe Vertrauenswuerdigkeit
- und minimierte Abhaengigkeit von externer Infrastruktur

### 3. Lifespan Scope

Der Review trifft auch hier einen echten Punkt.

Wenn das System fuer Kinder, Studierende und Erwachsene gedacht ist, dann muss `Adult Learning` frueher kommen als bisher geplant.

Es wird deshalb aus der spaeteren dritten Welle in die fruehe zweite Welle vorgezogen.

### 4. Multimodal Representation and Accessibility

Dieser Punkt wird sofort angenommen.

Ein universeller Mathe-Tutor darf nicht stillschweigend davon ausgehen, dass:

- alle gleich gut mit dichter Notation umgehen
- alle problemlos zwischen verbal, numerisch, algebraisch und geometrisch uebersetzen
- oder alle dieselbe sensorische Toleranz haben

Diese Linie wird daher frueh mit UDL und Mathematikdidaktik verbunden.

## Was aus dem Review nur teilweise uebernommen wird

### 1. Jede genannte Quelle wird nicht automatisch Primaeranker

Der Review nennt viele relevante Namen, aber nicht alle eignen sich gleich gut als erste Evidenzspitze fuer MathTeach.

Fuer den Start priorisieren wir:

- offizielle oder institutionelle Leitquellen
- primaere oder stark rezipierte Forschungsarbeiten
- direkt in Unterrichtslogik uebersetzbare Quellen

Nicht automatisch als erste Primaeranker gesetzt werden:

- popularisierende Buecher
- zu breite sozialtheoretische Texte ohne direkte Uebersetzbarkeit in Tutorlogik
- Prestige-Neurowissenschaft ohne klare Designfolgen

### 2. Trauma-Informed Design wird angenommen, aber vorsichtig

Der Punkt ist fuer das Projekt hochrelevant.

Aber auch hier gilt:

- der Tutor bleibt `kein Therapeut`
- der Tutor simuliert keine Traumabehandlung

Uebernommen wird:

- Sicherheit
- Transparenz
- Wahlmoeglichkeit
- Nicht-Beschaemung
- vorhersehbare Interaktion

Nicht uebernommen wird:

- therapeutische Deutung
- klinische Sprache nach aussen

### 3. Poverty Literature wird selektiv gefiltert

`Scarcity` und inklusive Bildungsberichte sind fuer das Projekt klar relevant.

Einige oft genannte Armutsrahmen werden jedoch nicht automatisch als wissenschaftliche Kernanker gesetzt.

Fuer die erste Evidenzschicht priorisieren wir eher:

- `Mullainathan and Shafir`
- `UNESCO inclusion and equity`
- stereotype-threat- und belonging-Literatur

als primaere Leitachsen.

## Wichtiger Architekturkonflikt im Repo

Der Review macht auch einen internen Spannungsbogen sichtbar:

- die neue Produktvision ist `geschlossen, lokal und notfalls ohne AI`
- die aktuelle [README.md](/Users/jonasweiss/MathTeach/README.md) enthaelt noch einen frueheren `Empfohlenen Modell-Stack` mit Cloud-LLMs

Diese Spannung ist real und muss spaeter bereinigt werden.

Aktuelle Entscheidung:

- fuer die Wissens- und Foundations-Arbeit bleibt das Repo nutzbar
- fuer die langfristige Produktarchitektur gilt aber ab jetzt die lokale Systemvision als normative Richtung

## Neue Prioritaetsstruktur

### Universal Round U.1

- `Motivation Systems`
- `Belonging and Psychological Safety`
- `Learning from Errors`
- `Equity and Scarcity as design constraints`
- `UDL and multimodal accessibility as early architecture constraints`

### Universal Round U.2

- `Transfer and Generalization`
- `Situated Learning`
- `Collaborative Learning`
- `Zone of Proximal Development`
- `Adult Learning`

### Universal Round U.3

- `Neurodiversity-aware core design`
- `trauma-informed but non-therapeutic safety`
- `developmental and lifespan sequencing`
- `stronger myth and anti-pattern catalog`

### Universal Round U.4

- spezifische ADHS-, Dyskalkulie-, Dyslexie-, Autismusspektrum- und ELL-Regelwerke
- konkrete Learner-Profile mal Accessibility-Response Matrizen

## Konkrete Folgerung fuer MathTeach

Ab jetzt gilt:

- `Universalitaet` ist kein spaeteres Add-on
- `Inklusion und Equity` sind keine reinen Spezialfeatures
- `Neurodiversitaet` beeinflusst schon fruehe Architekturentscheidungen

Gleichzeitig bleibt methodisch wichtig:

- erst ernstes allgemeines Lern- und Lehrwissen
- dann fruehe Universal-Constraints
- dann tiefe spezifische Unterstuetzungslogik

## Quellenpolitik fuer die naechste Runde

Die naechsten Quellen sollen bevorzugt aus diesen Familien kommen:

- `CAST UDL`
- `UNESCO inclusion and equity`
- `CDC and NICHD` fuer lernrelevante offizielle Ueberblicke
- `SAMHSA` fuer trauma-informed principles
- primaere oder stark rezipierte Forschungsarbeiten zu motivation, belonging, stereotype threat und transfer

## Wichtige Repo-Beziehungen

- [closed-local-tutor-system-blueprint.md](/Users/jonasweiss/MathTeach/docs/closed-local-tutor-system-blueprint.md)
- [teacher-mind-foundation-stack.md](/Users/jonasweiss/MathTeach/docs/teacher-mind-foundation-stack.md)
- [teacher-mind-foundations-review-triage-2026-04-01.md](/Users/jonasweiss/MathTeach/docs/teacher-mind-foundations-review-triage-2026-04-01.md)
- [psychological-foundations-program.md](/Users/jonasweiss/MathTeach/docs/psychological-foundations-program.md)
- [pedagogical-foundations-program.md](/Users/jonasweiss/MathTeach/docs/pedagogical-foundations-program.md)
