# Mode-Evidence Coupling

Stand: 2026-04-04

## Ziel

H.2f erweitert die bestehende Pair-/Triad-Aufloesung so, dass
Mehrprofil-Regeln nicht mehr nur auf `active_supports` und globale
Evidence reagieren, sondern auf den aktuellen `lesson_mode`.

Das heisst praktisch:

- dieselbe Profilkombination kann in
  `worked_example_tutoring` andere Moves erhalten als in
  `origin_story_explanation`
- die sichtbare Erklaerung dafuer bleibt im bestehenden
  `conflict_resolution_summary`

## Sichtbare Felder

Die Block-Zusammenfassung enthaelt jetzt zusaetzlich:

- `lesson_mode_applied`
- `mode_evidence_adjustments`

Damit kann die API zeigen, dass eine Anpassung nicht nur wegen der
Support-Kombination, sondern auch wegen des aktuellen Unterrichtsmodus
passiert ist.

## Aktuelle H.2f-Regeln

### `worked_example_tutoring`

- `ADHD + Dyscalculia`
  - Konzept-Reparatur wird zu
    `worked_example_rebuild_with_pacing_pause`
  - stabile Erfolgs-Signale koennen zu
    `worked_example_release_after_two_stable_steps` fuehren

- `ADHD + Dyscalculia + Language-Sensitive`
  - Konzept-Reparatur wird zu
    `worked_example_visual_concept_with_minimal_text`
  - Freigabe wird zu
    `worked_example_release_after_concept_check`
  - daraus kann zusaetzlich
    `worked_example_check_after_each_micro_step` entstehen

- `ADHD + Dyslexia + Autism-Spectrum`
  - Lesepfade werden zu
    `worked_example_predictable_visual_reading_sequence`
  - bei stabilen Erfolgssignalen kann die Freigabe zu
    `worked_example_release_after_readable_step` werden

### `origin_story_explanation`

- `ADHD + Dyscalculia + Language-Sensitive`
  - die Regel verschiebt sich auf einen knappen Bruecken-Move:
    `origin_story_bridge_with_concise_math_language`
  - Tempo wird dabei erst spaeter freigegeben:
    `delay_pacing_until_story_bridge_lands`

### `guided_concept_explanation`

- `ADHD + Dyscalculia + Language-Sensitive`
  - Konzept-Reparatur wird zu
    `guided_concept_rebuild_with_simple_language`
  - daraus kann
    `guided_concept_single_check_after_rebuild` entstehen

- `Dyscalculia + Language-Sensitive + Scarcity`
  - Konzept-Reparatur wird zu
    `guided_concept_rebuild_with_tiny_language_load`
  - der Block kann ebenfalls
    `guided_concept_single_check_after_rebuild` erzeugen

## Reihenfolge der Anwendung

1. Basis-Pair-Regeln
2. Basis-Triad-Regeln
3. Mode-Evidence-Kopplung
4. kleine Dependency-/Generated-Move-Schicht
5. Sortierung nach `priority_ladder`

## Nicht-Ziele

- noch keine vollstaendige Blocktyp-Erkennung
- noch keine sequentielle Move-Ausfuehrung ueber mehrere Bloecke
- noch keine Confidence-gewichtete Ausloesung

## Weiterfuehrung

H.2g ist jetzt als eigene Folgeschicht umgesetzt und koppelt diese
modus-sensitiven Regeln weiter an explizite Blocktypen und
Evidence-Kombinationsmuster. Der Anschluss ist dokumentiert in
[blocktype-evidence-coupling.md](/Users/jonasweiss/MathTeach/docs/blocktype-evidence-coupling.md).
