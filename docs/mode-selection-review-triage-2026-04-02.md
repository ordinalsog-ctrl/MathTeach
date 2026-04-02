# Mode Selection Review Triage 2026-04-02

## Zweck

Dieses Dokument verarbeitet die Reviews zum aktuellen Journal-Stand
`Support-Sensitive-Mode-Selection 2026-04-02 G`.

Es fixiert:

- was an der neuen `mode_selector`-Schicht jetzt als bestaetigt gilt
- welche Risiken trotz des Erfolgs offen bleiben
- welche naechste Phase jetzt aktiv vorbereitet werden soll

## Validierter Stand

Die Reviews bestaetigen drei zentrale Architekturentscheidungen:

1. `requested_mode` und `selected_mode` muessen getrennt bleiben.
2. `mode selection` gehoert als eigene Schicht zwischen
   `conflict_resolver` und `planner`.
3. Triads und Prioritaetsleitern duerfen echte `mode overrides`
   ausloesen, solange diese sichtbar, begruendbar und testbar bleiben.

Damit gilt Phase `G` jetzt als erfolgreicher Uebergang von:

- support-sensitiver Antwortkonfiguration

zu:

- support-sensitiver Moduswahl

## Was noch nicht geloest ist

Der aktuelle Stand waehlt den Modus nur zu Beginn einer Sitzung.

Noch nicht geloest sind:

- Moduswechsel waehrend einer laufenden Sitzung
- adaptive Reaktion auf Ermuedung, Frustration oder schnellen Fortschritt
- Schutz gegen hektisches Hin- und Herschalten zwischen Modi
- spaetere Nutzung von Lernerhistorie fuer Modusentscheidungen

## Aktive naechste Phase

Die naechste echte Ausbauphase ist jetzt:

- `planner-level live mode adaptation`

Diese Phase soll den Schritt leisten von:

- `statisch-adaptiv`

zu:

- `dynamisch-adaptiv`

## Leitregeln fuer Phase H

### 1. Moduswechsel nicht auf jedem Schritt

Live-Anpassung soll zunaechst nur auf `Block-Ebene` erfolgen, nicht nach
jedem einzelnen Rechenschritt.

Begruendung:

- haeufige Wechsel destabilisieren das Lernen
- Lernende brauchen kurzfristige Vorhersagbarkeit
- Paedagogik braucht sanfte, nicht hektische Umsteuerung

### 2. Hysterese statt nervoeser Reaktion

Das System soll einen Modus nicht schon bei kleinen Schwankungen wechseln.

Braucht spaeter:

- Mindestdauer pro Modus
- Schwellenwerte fuer Frustration oder Ermuedung
- Mindestvertrauen vor Rueckwechsel

### 3. Sanfte Uebergaenge statt harter Spruenge

Wenn ein Moduswechsel noetig ist, soll der Planner ihn als
`strukturierte Verschiebung` behandeln.

Beispiel:

- von `origin_then_example`
- zu `worked_example_tutoring`

nicht abrupt, sondern mit kurzer Bruecke:

- "Wir wechseln jetzt von der Idee zum konkreten Muster."

### 4. Explainability bleibt Pflicht

Auch Live-Anpassung muss spaeter lesbar bleiben.

Braucht spaeter:

- welches Signal den Wechsel ausgeloest hat
- welcher Modus verlassen wurde
- welcher Modus aktiviert wurde
- welche Schutzregel den Wechsel begrenzt hat

### 5. Mode-Explosion vermeiden

Die Reviews bestaetigen implizit: MathTeach soll nicht in immer neue
Spezialmodi zerfallen.

Deshalb bleibt die Regel:

- wenige stabile Modi
- mehr Variation ueber `constraints`
- Live-Anpassung zuerst als Uebergang zwischen bestehenden Modi

## Erste Arbeitspakete fuer Phase H

1. `live adaptation signals` definieren
   Beispiele:
   - wiederholte Fehler
   - verlangsamter Fortschritt
   - sichtbare Erfolgslinie
   - Ueberlastung im aktuellen Block

2. `mode shift thresholds` definieren
   Beispiele:
   - wann von `origin_then_example` zu `worked_example_tutoring`
   - wann von `worked_example_tutoring` zu `guided_concept_explanation`

3. `transition language` definieren
   Das System braucht spaeter kurze, ruhige Uebergangsformeln.

4. `planner memory hooks` vorbereiten
   Damit spaeter Modusgeschichte und Ruecksprungschutz moeglich werden.

## Nicht-Ziele der naechsten Phase

- noch keine voll offene Modusgenerierung
- noch keine Nutzeroberflaechen fuer manuelle Modusueberschreibung
- noch keine lernhistorische Volladaption ueber viele Sitzungen
- noch keine klinisch klingenden Belastungs- oder Emotionsmodelle

## Repo-Konsequenz

Die Reviews bestaetigen den jetzigen Repo-Stand ausdruecklich als
architektonisch sauber.

Die aktive Reihenfolge lautet jetzt:

1. `Support Response Matrix`
2. `Mixed Profiles and Priority Ladders`
3. `Support-Sensitive Mode Selection`
4. `Planner-Level Live Mode Adaptation`

