# Support Response Matrix Review Triage 2026-04-02

## Ergebnis

Der Review bestaetigt die aktuelle Projektlage sehr klar:

- `Knowledge Core` ist fuer die naechste Phase stark genug
- `Teacher Mind` ist fuer die naechste Phase breit genug
- die eigentliche Luecke liegt jetzt in der `Operationalisierung`

MathTeach verschiebt sich damit von:

- `strategischer Grundlegung`

zu:

- `regelbasierter Tutorsteuerung`

## Uebernommen

Diese Punkte werden direkt als aktive Projektlogik uebernommen:

- Die `Support Response Matrix` ist jetzt der zentrale naechste Bauabschnitt.
- Die Matrix braucht drei Ebenen:
  - `support signal profile`
  - `response dimensions`
  - `profile-specific mappings`
- Die ersten beiden priorisierten Einzelprofile sind:
  - `ADHD-aware support`
  - `dyscalculia-aware support`
- Danach folgen:
  - `dyslexia-aware support`
  - `autism-spectrum-aware support`
  - `ELL / language-sensitive support`
  - `scarcity-aware support`
- Die naechste Phase braucht nicht primaer neue Allgemeintheorie, sondern:
  - Matrix-Dokumentation
  - spaeter ein `response_engine`
  - danach Planner-Integration

## Bewusst Angepasst

Der Review wird fuer MathTeach an mehreren Stellen bewusst in sicherere und
besser pruefbare Projektlogik uebersetzt:

- keine diagnostischen Prozentmodelle im Kernsystem
- keine klinischen Labels als Tutoroutput
- keine versteckte medizinische Klassifikation
- `support signals` statt Diagnosen
- `candidate defaults` statt unantastbarer fixer Zahlenwerte

Das bedeutet:

- Der Tutor darf sagen:
  - `shorter sessions help here`
  - `more concrete grounding helps here`
  - `we will use more external structure`
- Der Tutor darf nicht sagen:
  - `you have ADHD`
  - `your dyscalculia probability is 68 percent`

## Punkte Zurueckgestellt Oder Nur Teilweise Uebernommen

Einige Teile des Reviews sind plausibel, werden aber noch nicht als feste
Systemregel codiert:

- exakte Minutenvorgaben wie `17-minute ultradian cycle`
- harte numerische Schwellen wie `careless_error_rate > 30 percent`
- feinere klinische Unterfaktoren, die noch nicht separat im lokalen Korpus
  abgesichert sind
- Pilot- oder Screening-Logik mit Minderjaehrigen, bevor Datenschutz,
  Datensparsamkeit und Beobachtungsprotokolle sauber ausdefiniert sind

Diese Punkte bleiben moegliche spaetere Verfeinerungen.

## Neue Arbeitsdefinition

Die Matrix arbeitet ab jetzt mit:

- `support signal profile`
- `response settings`
- `candidate operational defaults`
- `evidence anchors`

Jede profilbezogene Matrixzeile soll spaeter enthalten:

- `dimension`
- `setting`
- `rationale`
- `source anchors`
- optional `validation note`

## Neue Sprintprioritaet

Der naechste Sprint gliedert sich jetzt in vier Stufen:

1. `Dokumentationsphase`
   - Matrixstruktur
   - Template
   - ADHD-Matrix
   - Dyscalculia-Matrix

2. `Code-Skeleton`
   - `response_matrix.py`
   - `response_engine.py`
   - spaeter `profiler.py`

3. `Planner-Integration`
   - Response Settings in `planner.py`
   - Sessionplanung mit Profilbezug

4. `Pilot and Validation`
   - erst nach sauberer lokaler und nicht-diagnostischer Rahmung

## Wichtigste Konsequenz

MathTeach hat jetzt genug Theorie gesammelt, um in ein erstes
`explainable operational tutoring core` ueberzugehen.

Der Massstab ab jetzt lautet nicht mehr:

- `haben wir genug Literatur`

sondern:

- `koennen wir aus dieser Literatur klare, wuerdevolle und testbare Tutorregeln ableiten`
