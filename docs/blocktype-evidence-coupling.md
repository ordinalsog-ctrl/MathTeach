# Blocktype-Evidence Coupling

Stand: 2026-04-04

## Ziel

H.2g fuehrt eine zusaetzliche Schicht ueber H.2f ein: bekannte
Mehrprofil-Regeln reagieren jetzt nicht nur auf `lesson_mode`, sondern
auch auf den konkreten Blockkontext und verdichtete Evidence-Muster.

Das heisst praktisch:

- ein `worked_example`-Block kann andere Konfliktmoves tragen als ein
  `concept_introduction`- oder `error_recovery`-Block
- der Planner muss dafuer nicht mehr nur indirekt ueber
  `lesson_mode` raten, sondern bekommt einen expliziten `block_type`
- mehrere Rohsignale werden als wiederverwendbare
  `EvidenceCombinationPattern`-Muster sichtbar

## Neue sichtbare Felder

`PlannedTeachingBlock` traegt jetzt:

- `block_type`
- `evidence_combination`

`conflict_resolution_summary` traegt jetzt zusaetzlich:

- `block_type_applied`
- `evidence_patterns_applied`
- `evidence_combination_rules_applied`
- `blocktype_adjustments_applied`

## Evidence-Muster

Die neue Detektorschicht verdichtet rohe Beobachtungsevidenz in
stabilere Muster:

- `rapid_consecutive_success`
- `stagnation_pattern`
- `inconsistent_success`
- `vocabulary_gap`
- `confidence_buildup`
- `concept_confusion`

Diese Muster bleiben im API-Output sichtbar ueber
`evidence_combination.patterns`.

## Blocktypen

Die aktuelle H.2g-Heuristik nutzt:

- `concept_introduction`
- `worked_example`
- `guided_practice`
- `error_recovery`
- `concept_check`
- `bridge_to_application`
- `reflection`

Die Zuordnung geschieht aktuell im Planner ueber `lesson_mode` plus
starke Evidence-Hinweise wie Konzeptfehler, Stagnation, Transfer oder
Textueberlastung.

## Aktuelle H.2g-Regeln

### Evidence-Kombinationsregeln

- `rapid_consecutive_success + vocabulary_gap`
  - generiert `reduce_text_density_while_maintaining_pacing`
  - bei sprachsensiblen oder dyslexiebezogenen Supports zusaetzlich
    `embed_vocabulary_in_rapid_flow`

- `concept_confusion + vocabulary_gap`
  - bei `dyscalculia_aware_support + language_sensitive_support`
    zusaetzlich `preemptively_clarify_key_terms`

- `inconsistent_success + stagnation_pattern`
  - bei `adhd_aware_support + dyscalculia_aware_support`
    zusaetzlich `identify_and_reinforce_success_patterns`

### Blocktyp-Regeln

- `worked_example + rapid_consecutive_success + ADHD + Dyscalculia`
  - generiert `worked_example_accelerated_with_pacing_checks`
  - generiert `use_concrete_example_as_anchor`

- `worked_example + concept_confusion + vocabulary_gap + Dyscalculia + Language`
  - generiert `worked_example_concept_clarification_sequence`

- `error_recovery + stagnation_pattern + Dyscalculia + Autism`
  - generiert `structured_error_analysis_with_prediction`
  - generiert `error_recovery_with_concept_reframing`

- `concept_introduction + vocabulary_gap + Dyscalculia + Language`
  - generiert `visual_concept_intro_minimal_text`

- `guided_practice + inconsistent_success + ADHD + Dyscalculia`
  - generiert `practice_with_embedded_concept_checks`

- `concept_check + confidence_buildup + ADHD + Autism`
  - generiert `extended_concept_check_with_positive_feedback`

## Reihenfolge der Anwendung

1. Basis-Pair-/Triad-Aufloesung
2. H.2f `lesson_mode`-Kopplung
3. H.2g Evidence-Kombinationsanpassungen
4. H.2g Blocktyp-Anpassungen
5. finale Sortierung und API-Sichtbarkeit

## Testanker

Die neue Schicht ist aktuell abgesichert ueber:

- [tests/test_evidence_pattern_detector.py](/Users/jonasweiss/MathTeach/tests/test_evidence_pattern_detector.py)
- [tests/test_blocktype_evidence_coupling.py](/Users/jonasweiss/MathTeach/tests/test_blocktype_evidence_coupling.py)
- [tests/test_planner_runtime_flow.py](/Users/jonasweiss/MathTeach/tests/test_planner_runtime_flow.py)
- [tests/test_api.py](/Users/jonasweiss/MathTeach/tests/test_api.py)

## Weiterfuehrung

H.3 ist jetzt als eigene Folgeschicht umgesetzt und nutzt diese
Blocktyp-/Evidence-Signale fuer die Wahl des naechsten Blocktyps. Der
Anschluss ist dokumentiert in
[block-sequence-planning.md](/Users/jonasweiss/MathTeach/docs/block-sequence-planning.md).
