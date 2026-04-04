# Triad Conflict Resolution Rules

Stand: 2026-04-04

## Ziel

Die blockweise Konfliktaufloesung soll bei Mehrprofil-Situationen nicht
nur eine Reihenfolge von `support_moves` liefern, sondern bekannte
Konflikte auch semantisch abfedern. H.2e fuehrt deshalb neben
`priority_ladder` zwei weitere sichtbare Schichten ein:

- `generated_moves`
- `move_dependencies_applied`

Dadurch bleibt nachvollziehbar, wann eine Regel nicht nur priorisiert,
sondern neue Block-Hinweise erzeugt hat.

## Aktive Pair-Regeln

| Pair | Typische Konfliktlage | Beispiel-Anpassung |
| --- | --- | --- |
| `ADHD + Dyscalculia` | Speed-Signal kollidiert mit Konzept-Reparatur | `increase_pacing_after_stable_success` -> `increase_pacing_monitor_only_after_concept_recovery` |
| `ADHD + Language-Sensitive` | Tempo kollidiert mit Sprachlast | `increase_pacing_after_stable_success` -> `increase_pacing_gently_after_language_clarification` |
| `Dyscalculia + Autism-Spectrum` | Variation kollidiert mit Layout-Stabilitaet | `stabilize_layout_before_variation` -> `stabilize_layout_before_new_quantity_variation` |
| `ADHD + Dyslexia` | Tempo kollidiert mit Lesbarkeit | `increase_pacing_after_stable_success` -> `increase_pacing_after_text_clarity` |
| `Dyscalculia + Language-Sensitive` | Konzept-Reparatur braucht Sprachbruecke | `stop_retry_loop_and_reframe_concept` -> `reframe_concept_with_everyday_language_bridge` |
| `Language-Sensitive + Autism-Spectrum` | Sprachhilfe braucht konsistente Rahmung | `bridge_everyday_language_and_math_terms` -> `bridge_language_with_consistent_patterning` |

## Aktive Triad-Regeln

| Triad | Priority Ladder | Beispiel-Anpassung |
| --- | --- | --- |
| `ADHD + Dyscalculia + Language-Sensitive` | `dyscalculia -> language_sensitive -> adhd` | `reframe_concept_with_simple_language_and_quantity_support` |
| `ADHD + Dyslexia + Autism-Spectrum` | `dyslexia -> autism_spectrum -> adhd` | `split_problem_text_into_shorter_predictable_chunks` |
| `Dyscalculia + Language-Sensitive + Scarcity` | `dyscalculia -> language_sensitive -> scarcity` | `reframe_concept_with_minimal_language_overhead` |

## Generierte Kombinations-Moves

Die H.2e-Schicht erzeugt nur wenige, bewusst explizite Kombinationen:

- `pair_visual_explanation_with_simple_language`
  entsteht aus Mengen-/Quantitaets-Sichtbarkeit plus sprachlicher
  Klaerung
- `pair_shorter_text_with_clear_reading_path`
  entsteht aus Dyslexia-Lesbarkeit plus ADHD-Mikrostruktur
- `use_predictable_visual_reading_sequence`
  entsteht aus vorhersehbaren Text-Chunks plus stabilen visuellen
  Leseankern
- `use_consistent_bilingual_patterns`
  entsteht aus sprachlicher Bruecke plus literal-konsistenter Rahmung
- `keep_concept_repair_within_visible_resource_limits`
  entsteht aus minimal-sprachiger Konzept-Reparatur plus klaren kleinen
  Erfolgskriterien

## Guardrails

- Keine implizite Magie: jede Move-Transformation ist als String-Regel
  explizit im Resolver hinterlegt.
- Keine Vollabdeckung aller Profile: H.2e erweitert nur bekannte
  Konfliktlagen mit klarer Testabdeckung.
- Keine Laufzeit-Sequenzierung: die Resolver-Schicht entscheidet fuer
  einen Block, nicht fuer eine ganze mehrstufige Unterrichtsfolge.

## Naechster Schritt

H.2f soll dieselben Regeln staerker an `lesson_mode` und konkretere
Evidence-Kombinationen koppeln, damit z.B. dieselbe Triad in
`worked_example_tutoring` andere Anpassungen bekommt als in
`origin_story_explanation`.
