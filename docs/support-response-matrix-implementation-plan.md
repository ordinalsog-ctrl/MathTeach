# Support Response Matrix Implementation Plan

## Ziel

Dieser Plan uebersetzt die aktuelle Review-Lage in einen konkreten
Arbeitsablauf fuer die naechste Implementationsphase.

Der Fokus liegt auf:

- `ADHD-aware support`
- `dyscalculia-aware support`
- `dyslexia-aware support`
- `autism-spectrum-aware support`
- `language-sensitive support`
- `scarcity-aware support`
- spaeterer Code-Integration in Planner und Runtime

## Arbeitsprinzip

Die Reihenfolge lautet:

1. `structure before code`
2. `single profiles before mixed profiles`
3. `candidate defaults before hard rules`
4. `explainable rules before opaque adaptation`

## Phase A: Documentation Pass

Zeitrahmen:

- `weeks 1 to 3`

Deliverables:

- [support-response-matrix-structure.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-structure.md)
- [support-response-matrix-template.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-template.md)
- [support-response-matrix-adhd.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-adhd.md)
- [support-response-matrix-dyscalculia.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-dyscalculia.md)
- [support-response-matrix-dyslexia.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-dyslexia.md)
- [support-response-matrix-autism.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-autism.md)
- [support-response-matrix-language-sensitive.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-language-sensitive.md)
- [support-response-matrix-scarcity.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-scarcity.md)

Exit criteria:

- alle primaeren Response Dimensions sind fest
- sechs Einzelprofile sind operational beschrieben
- jede Matrix hat erkennbare Quellenanker

## Phase B: Code Skeleton

Zeitrahmen:

- `weeks 4 to 6`

Geplante Dateien:

- `src/mathteach/response_matrix.py`
- `src/mathteach/services/response_engine.py`
- spaeter `src/mathteach/services/profiler.py`
- `tests/test_response_matrix.py`

Mindestumfang:

- Datenmodelle fuer `support signal profile`
- Datenmodelle fuer `response settings`
- einfache regelbasierte Evaluation
- erste Tests fuer ADHD-, Dyscalculia-, Dyslexia-, Autism-, Language-Sensitive- und Scarcity-Pfade

## Phase C: Planner Integration

Zeitrahmen:

- `weeks 7 to 9`

Ziel:

- Response Settings in den bestehenden Planner ziehen

Geplante Wirkung:

- `planner.py` bekommt response-aware Entscheidungen
- Runtime-Modi werden nicht nur thematisch, sondern auch support-sensitiv gewaehlt
- `TeachingPlan` bekommt spaeter konkrete Response-Felder

## Phase D: Pilot and Validation

Zeitrahmen:

- `weeks 10 to 12`

Nur unter diesen Bedingungen:

- lokale Speicherung bleibt gewahrt
- Datensparsamkeit ist klar geregelt
- keine diagnostische oder therapeutische Selbstdarstellung des Systems

Beobachtungsfelder:

- Engagement
- Verstaendnisfortschritt
- Fehlererholung
- Abbruchpunkte
- wahrgenommene Sicherheit

## Technische Zwischenziele

### 1. Support Signal Profile

Braucht spaeter mindestens:

- cognitive signals
- support-family signals
- motivation signals
- emotional safety signals
- context signals
- domain-specific signals

### 2. Response Settings

Braucht spaeter mindestens:

- pacing
- step_size
- notation_density
- text_load
- visualization
- error_handling
- language_support
- self_check_rhythm
- external_scaffolds

### 3. Evidence Traceability

Jede spaetere Regel soll rueckfuehrbar bleiben auf:

- Matrix-Dokument
- Quellenanker
- spaetere Testfaelle

## Unmittelbar Naechste Aufgaben

1. ADHD-Matrix weiter verfeinern
2. Dyscalculia-Matrix weiter verfeinern
3. Dyslexia-Matrix weiter verfeinern
4. Autism-Matrix weiter verfeinern
5. Language-Sensitive-Matrix weiter verfeinern
6. Scarcity-Matrix weiter verfeinern
7. `response_matrix.py` weiter stabilisieren
8. `response_engine` von sechs Profilen auf gemischte Support-Familien ausbauen

## Nicht-Ziele Des Naechsten Sprints

- noch keine Vollabdeckung aller Support-Familien
- noch keine gemischten Profile als Hauptpfad
- noch keine vollstaendige UI-Neugestaltung
- noch keine klinisch anmutenden Frageboegen
