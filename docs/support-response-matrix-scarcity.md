# Support Response Matrix: Scarcity-Aware Support

## Rolle

Diese Matrix operationalisiert `scarcity-aware support` fuer MathTeach.

Sie ist:

- nicht-diagnostisch
- nicht-therapeutisch
- support-orientiert

Sie beschreibt, wie der Tutor reagieren soll, wenn Knappheit, hohe Alltagslast,
unterbrochene Aufmerksamkeit oder geringe Planungsspielraeume den Lernzugang
merklich erschweren.

## Safety Frame

- keine Defiziterzaehlung ueber Armut oder Lebenslage
- keine moralische Deutung von Unterbrechung, Erschoepfung oder unregelmaessigem Lernen
- geringe Friktion, klare Relevanz und sichtbarer Fortschritt gelten als legitime Zugangsbedingungen
- alle Einstellungen gelten als `candidate defaults`

## Primaere Support Signals

- `immediate_relevance_need`
  - neue Inhalte muessen frueh zeigen, warum sie jetzt nuetzlich oder sinnvoll sind
- `interruption_risk`
  - Lernphasen koennen leicht von Alltag, Verpflichtungen oder Stress unterbrochen werden
- `low_bandwidth_for_overhead`
  - unnoetige Komplexitaet, lange Vorrede oder diffuse Aufgabenformate kosten zu viel Energie
- `success_visibility_need`
  - kleine Fortschritte muessen klar sichtbar werden, damit Motivation nicht wegkippt
- `institutional_friction_history`
  - unklare Erwartungen oder verdeckte Bewertungssignale koennen schnell entmutigen

## Candidate Response Settings

| Dimension | Candidate Setting | Why | Source Anchors |
| --- | --- | --- | --- |
| `transition_buffer` | `brief_explicit_transition_with_goal_reminder` | Kurze Zielerinnerungen helfen beim Wiedereinstieg und halten die Lernlinie trotz Unterbrechung sichtbar. | `mani-mullainathan-shafir-zhao-poverty-cognition`, `unesco-gem-inclusion-and-education` |
| `worked_example_ratio` | `examples_then_quick_success_practice` | Fruehe erfolgreiche Anwendung reduziert Suchlast und gibt schnell erlebbare Kompetenzsignale. | `rosenshine-principles-of-instruction`, `ryan-deci-self-determination-theory` |
| `symbolic_vs_verbal_balance` | `meaning_and_relevance_before_dense_formalism` | Formalisierung folgt erst, wenn Nutzen und Bedeutung lokal sichtbar geworden sind. | `mani-mullainathan-shafir-zhao-poverty-cognition`, `unesco-gem-inclusion-and-education` |
| `word_budget_per_chunk` | `short_clear_chunks_with_immediate_relevance` | Knappe, zielnahe Chunks senken Einstiegsfriktion unter hoher Alltagslast. | `mani-mullainathan-shafir-zhao-poverty-cognition`, `organizing-instruction-and-study` |
| `primary_representation` | `everyday_relevance_then_visual_or_symbolic` | Alltagsnahe Relevanz oder praktischer Nutzen oeffnen oft schneller den mathematischen Einstieg. | `unesco-gem-inclusion-and-education`, `cast-udl-guidelines-3` |
| `error_response_style` | `stabilize_then_strategy_with_progress_marker` | Fehler sollen nicht als Leistungsurteil wirken, sondern mit naechstem Schritt und sichtbarer Erholung verbunden werden. | `steele-aronson-stereotype-threat`, `the-power-of-feedback` |
| `check_frequency` | `every_major_step_with_progress_confirmation` | Haeufige kurze Bestaetigung hilft, dass Fortschritt sichtbar und Orientierung stabil bleibt. | `using-student-achievement-data`, `ryan-deci-self-determination-theory` |
| `language_support` | `plain_goal_and_relevance_framing` | Klare Ziel- und Nutzensprache reduziert institutionelle Reibung auch ohne eigentliche Sprachbarriere. | `unesco-gem-inclusion-and-education`, `ryan-deci-self-determination-theory` |
| `external_scaffolds` | `clear_success_criteria_and_small_wins_sequence` | Transparente Erfolgskriterien und kleine erreichbare Etappen schuetzen Motivation und Wiedereinstieg. | `mani-mullainathan-shafir-zhao-poverty-cognition`, `ryan-deci-self-determination-theory` |

## Runtime Preferences

Bevorzugt:

- `guided_concept_explanation`
- `worked_example_tutoring`
- `origin_then_example`

Besonders hilfreich:

- fruehe Antwort auf `Wozu brauche ich das jetzt?`
- sichtbare Teilziele
- kompakte Wiedereinstiege nach Unterbrechung

Zu vermeiden:

- lange Einleitungen ohne klaren Nutzen
- diffuse Erfolgskriterien
- formale Verdichtung, bevor Sinn und Richtung sichtbar sind

## External Scaffolds

Standardmaessig aktiv:

- `clear_success_criteria`
- `visible_progress_markers`
- `why_this_matters_now`
- `small_wins_sequence`
- `re_entry_summary_after_interruption`

Optional spaeter:

- ultra-kurzer Wiederaufnahme-Modus
- lernhistorische Wiedereinstiegskarten

## Error Handling

Bevorzugte Sequenz:

1. Fehler lokal entdramatisieren
2. naechsten kleinsten sinnvollen Schritt markieren
3. Fortschritt sofort wieder sichtbar machen

Nicht bevorzugt:

- Fehler als globales Leistungsurteil
- lange Rueckspruenge ohne Orientierung
- abstrakte Rechtfertigung ohne direkte Handlungsmoeglichkeit

## Progress Signals

Hinweise, dass die Einstellungen wirken:

- Lernende bleiben auch nach Unterbrechungen leichter im Faden
- kleine Erfolge werden schneller benannt und genutzt
- weniger Reibung an Aufgabenstart und Wiedereinstieg
- Relevanzfragen werden frueher beantwortet und blockieren weniger

Hinweise, dass nachjustiert werden muss:

- trotz korrekter Mathematik kippt Motivation frueh weg
- Unterbrechungen fuehren jedes Mal zu fast komplettem Neustart
- Lernende verstehen den Nutzen des Schritts weiterhin nicht

## Source Anchors

- `mani-mullainathan-shafir-zhao-poverty-cognition`
- `steele-aronson-stereotype-threat`
- `unesco-gem-inclusion-and-education`
- `ryan-deci-self-determination-theory`
- `cast-udl-guidelines-3`
- `organizing-instruction-and-study`
- `using-student-achievement-data`
- `the-power-of-feedback`
- `rosenshine-principles-of-instruction`

## Offene Punkte

- Kombinationen mit `language-sensitive support` und `ADHD-aware support` brauchen spaeter Priorisierungsregeln.
- Konkrete Wiedereinstiegsmodi nach echten Alltagsunterbrechungen folgen spaeter als Runtime-Schicht.
- Kontextsensibles Beispielmaterial kann spaeter noch staerker an Lebenswelt und Nutzenachsen gekoppelt werden.
