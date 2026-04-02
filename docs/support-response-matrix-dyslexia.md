# Support Response Matrix: Dyslexia-Aware Support

## Rolle

Diese Matrix operationalisiert `dyslexia-aware support` fuer MathTeach.

Sie ist:

- nicht-diagnostisch
- nicht-therapeutisch
- support-orientiert

Sie beschreibt, wie der Tutor reagieren soll, wenn Leselast, Symboldekodierung
oder sprachliche Verdichtung den mathematischen Zugang blockieren.

## Safety Frame

- keine Dyslexie-Diagnose durch den Tutor
- keine Gleichsetzung von Lesereibung mit mathematischer Unfaehigkeit
- sprachliche Entlastung gilt als Zugangsbedingung, nicht als Vereinfachung zweiter Klasse
- alle Einstellungen gelten als `candidate defaults`

## Primaere Support Signals

- `reading_load_friction`
  - laengere Textaufgaben oder dichte Erklaerungen kippen schnell in Erschoepfung
- `symbol_decoding_friction`
  - mathematische Zeichenfolgen muessen langsam und bewusst gelesen werden
- `term_tracking_friction`
  - Fachbegriffe und ihre Rollen gehen im Fliesstext leicht verloren
- `text_before_math_block`
  - der Zugang scheitert oft schon vor der eigentlichen mathematischen Operation
- `spoken_explanation_advantage`
  - klare kurze Sprache oder Vorlesen hilft merklich mehr als dichter Text

## Candidate Response Settings

| Dimension | Candidate Setting | Why | Source Anchors |
| --- | --- | --- | --- |
| `symbolic_vs_verbal_balance` | `clear_symbol_spacing_with_supported_language` | Symbole muessen klar sichtbar bleiben, waehrend Sprache entlastet und strukturiert wird. | `nichd-reading-and-reading-disorders`, `shaywitz-dyslexia-specific-reading-disability` |
| `word_budget_per_chunk` | `very_short_chunks_with_simple_sentences` | Kurze Chunks verringern die Konkurrenz zwischen Lesedekodierung und mathemischem Denken. | `nichd-reading-and-reading-disorders`, `organizing-instruction-and-study` |
| `primary_representation` | `visual_plus_audio_ready_before_dense_text` | Mathematische Bedeutung soll nicht am langen Text haengen, sondern ueberschaubar sichtbar und erklaerbar sein. | `shaywitz-dyslexia-specific-reading-disability`, `cast-udl-guidelines-3` |
| `error_response_style` | `clarify_reading_load_before_math_correction` | Vor der Korrektur wird geprueft, ob das Problem in der Mathematik oder im Lesen lag. | `nichd-reading-and-reading-disorders`, `focus-on-formative-feedback` |
| `check_frequency` | `every_major_step_with_term_check` | Haeufige Kurzchecks sichern ab, dass Begriffe und Symbole richtig zugeordnet bleiben. | `using-student-achievement-data`, `the-power-of-feedback` |
| `language_support` | `glossary_plus_key_terms_plus_simplified_syntax` | Sprachliche Explizitheit entlastet den Zugang zu mathemischen Ideen. | `nichd-reading-and-reading-disorders`, `ies-english-learners-practice-guide` |
| `sensory_load_level` | `reduced_visual_clutter` | Weniger visuelles Rauschen hilft, dass relevante Zeichen und Woerter hervorstechen. | `cast-udl-guidelines-3`, `nichd-reading-and-reading-disorders` |
| `external_scaffolds` | `key_term_highlighting_and_step_labels` | Sichtbare Begriffs- und Schrittmarkierungen machen die Struktur lesbarer. | `cast-udl-guidelines-3`, `rosenshine-principles-of-instruction` |

## Runtime Preferences

Bevorzugt:

- `worked_example_tutoring`
- `guided_concept_explanation`

Besonders hilfreich:

- Beispiele mit klarer Zeilenstruktur
- kurze Begriffsbruecken vor jeder formalen Verdichtung

Zu vermeiden:

- lange Textbloecke
- mehrere neue Fachbegriffe in einem Satz
- dichte Symbolketten ohne sprachliche oder visuelle Entlastung

## External Scaffolds

Standardmaessig aktiv:

- `key_term_highlighting`
- `step_labels`
- `symbol_reading_support`
- `short_sentence_chunks`

Optional spaeter:

- vorlesbare Erklaerung
- glossary-on-demand

## Error Handling

Bevorzugte Sequenz:

1. klaeren, ob die Leselast den Fehler mitverursacht hat
2. Begriff oder Symbol sauber neu zuordnen
3. dann erst die mathematische Operation neu aufbauen

Nicht bevorzugt:

- sofortige mathematische Korrektur ohne Sprachcheck
- implizite Annahme, dass Missverstaendnis immer fachlich war

## Progress Signals

Hinweise, dass die Einstellungen wirken:

- Textaufgaben werden ruhiger und sicherer entschluesselt
- Symbole werden weniger vertauscht
- Fachbegriffe werden konsistenter verwendet
- Lernende kommen schneller zur eigentlichen mathematischen Idee

Hinweise, dass nachjustiert werden muss:

- die Mathematik scheint klar, aber Textaufgaben brechen weiter weg
- Symbole bleiben trotz Erklaerung instabil
- Fachwoerter werden auch nach mehreren Chunks nicht sicher getragen

## Source Anchors

- `nichd-reading-and-reading-disorders`
- `shaywitz-dyslexia-specific-reading-disability`
- `cast-udl-guidelines-3`
- `organizing-instruction-and-study`
- `using-student-achievement-data`
- `the-power-of-feedback`
- `focus-on-formative-feedback`
- `ies-english-learners-practice-guide`

## Offene Punkte

- Audio- und Vorleselogik wird spaeter gesondert operationalisiert.
- Die Grenze zwischen `dyslexia-aware support` und `language-sensitive support` muss spaeter sauberer getrennt werden.
- Kombinationen mit `ADHD-aware support` und `dyscalculia-aware support` folgen spaeter.
