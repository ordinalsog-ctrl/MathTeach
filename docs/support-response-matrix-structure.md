# Support Response Matrix Structure

## Zweck

Die `Support Response Matrix` uebersetzt:

- `Learner Input`
- `Teacher Mind`
- `Support Profiles`

in konkrete Tutorentscheidungen.

Sie ist die Bruecke zwischen allgemeinem paedagogisch-psychologischem Wissen
und sichtbar adaptivem Tutorverhalten.

## Sicherheitsprinzipien

Die Matrix arbeitet nur unter diesen Regeln:

- kein therapeutisches System
- kein Diagnosesystem
- keine Identitaetsurteile
- selbstbeschriebene Bedarfe haben Vorrang
- beobachtete Lernreibung darf nur zu `Tutoranpassung`, nie zu Zuschreibung fuehren
- jede Reaktion muss fachlich korrekt bleiben

## Kernlogik

Der Fluss lautet:

1. `learner intake`
2. `support signal profile`
3. `response settings`
4. `runtime mode selection`
5. `session plan`
6. `live adaptation`

## Support Signal Profile

Statt medizinischer Diagnostik verwendet MathTeach ein `support signal profile`.

Es besteht aus diesen Hauptachsen.

### 1. Cognitive Dimension

- `working_memory_load`
- `processing_speed`
- `attention_regulation`
- `symbolic_processing`
- `spatial_visual_processing`

Empfohlene Werte:

- `fragile`
- `supported`
- `typical`
- `strong`

### 2. Support Signal Dimension

Diese Felder erfassen, welche Supportlinien fuer die Vermittlung relevant sind.

- `adhd_aware_support`
- `dyscalculia_aware_support`
- `dyslexia_aware_support`
- `autism_spectrum_aware_support`
- `language_sensitive_support`
- `scarcity_aware_support`

Empfohlene Werte:

- `none`
- `possible`
- `declared`
- `highly_relevant`

### 3. Motivation Dimension

- `autonomy_need`
- `competence_belief`
- `relatedness_need`
- `relevance_need`
- `persistence_state`

### 4. Emotional Safety Dimension

- `math_anxiety`
- `psychological_safety`
- `confidence_stability`
- `error_sensitivity`
- `stereotype_threat_risk`

### 5. Context Dimension

- `language_context`
- `school_experience`
- `support_availability`
- `scarcity_pressure`
- `time_pressure`

### 6. Domain-Specific Dimension

- `prior_knowledge_map`
- `misconception_flags`
- `transfer_readiness`
- `target_formality`
- `requested_runtime_mode`

## Response Dimensions

Die erste Matrix-Version steuert diese Tutorvariablen.

### 1. Pacing

- `session_duration`
- `break_pattern`
- `transition_buffer`

### 2. Step Size

- `conceptual_increment`
- `worked_example_ratio`
- `fading_speed`

### 3. Notation Density

- `symbolic_vs_verbal_balance`
- `formula_complexity`
- `notation_introduction_speed`

### 4. Text Load

- `word_budget_per_chunk`
- `sentence_length_budget`
- `chunk_limit`

### 5. Visualization

- `primary_representation`
- `concrete_duration`
- `diagram_complexity`
- `sensory_load_level`

### 6. Error Handling

- `error_detection_speed`
- `error_response_style`
- `misconception_targeting`

### 7. Language Support

- `key_term_support`
- `syntax_simplification`
- `glossary_depth`

### 8. Self-Check Rhythm

- `check_frequency`
- `check_method`
- `corrective_escalation`

### 9. External Scaffolds

- `checklists`
- `timers`
- `step_labels`
- `visual_progress_markers`

## Primaere Profilfamilien

Die erste konkrete Matrixrunde fokussiert sechs Profilfamilien.

### ADHD-Aware Support

Typische Tutorverschiebungen:

- kuerzere Einheiten
- haeufigere Uebergaenge
- schnellere Rueckkopplung
- staerkere externe Struktur
- weniger Suchlast, mehr klare Schritte

### Dyscalculia-Aware Support

Typische Tutorverschiebungen:

- laengere konkrete Phase
- langsamere Symbolisierung
- staerkere Mengen- und Groessenbruecken
- explizitere Fehleranalyse
- kleinere konzeptuelle Schritte

### Dyslexia-Aware Support

Typische Tutorverschiebungen:

- geringere Textdichte
- kuerzere Saetze
- klarere Begriffsfuehrung
- bessere Sichtbarkeit mathematischer Symbole
- mehr sprachliche Entlastung

### Autism-Spectrum-Aware Support

Typische Tutorverschiebungen:

- mehr Vorhersagbarkeit
- stabilere Sitzungsstruktur
- explizitere Schrittfolgen
- geringere Reizlast
- staerkeres Nutzen von Musterstaerken

### ELL / Language-Sensitive Support

Typische Tutorverschiebungen:

- einfachere Syntax
- explizite Fachbegriffe
- kontrollierte Wortlast
- Begriffserklaerung vor komplexen Operationen
- mehr Uebersetzungsbruecken zwischen Alltagssprache und Fachsprache

### Scarcity-Aware Support

Typische Tutorverschiebungen:

- schnellere Relevanzherstellung
- geringere unnoetige Komplexitaet
- klarere Erfolgskriterien
- kleinere erreichbare Lernschritte
- stabilere Motivation durch sichtbaren Fortschritt

## Kombinierte Profile

Kombinierte Profile werden erst nach stabilen Einzelprofilen operationalisiert.

Vorrangregeln:

1. `safety before acceleration`
2. `accessibility before elegance`
3. `conceptual grounding before formal compression`
4. `clarity before variety`

Beispiele:

- `ADHD + dyslexia`: kurze Bloecke plus reduzierte Textlast
- `dyscalculia + math anxiety`: konkrete Phase plus sehr sanfte Fehlernormalisierung
- `autism-spectrum + ELL`: explizite Struktur plus sprachliche Vereinfachung

## Verbindung Zur Runtime

Die Matrix speist spaeter:

- `planner.py`
- einen eigenen `response_engine`
- spaetere `session_plan`-Objekte

Die Runtime entscheidet dann nicht mehr nur:

- `worked_example_tutoring`
- `origin_story_explanation`
- `origin_then_example`

sondern auch:

- in welchem Tempo
- mit welcher Symbolik
- mit welcher Fehlerlogik
- mit welcher Checkfrequenz
- mit welcher externen Struktur

## Erste Implementierungsreihenfolge

### Sprint 1

- Struktur der Matrix fixieren
- Response Dimensions finalisieren
- aktive Architektur auf lokal-first ausrichten

### Sprint 2

- `ADHD-aware support` voll ausarbeiten
- `dyscalculia-aware support` voll ausarbeiten

### Sprint 3

- `dyslexia-aware support`
- `autism-spectrum-aware support`
- `ELL / language-sensitive support`
- `scarcity-aware support`

### Sprint 4

- Datenmodell fuer Matrix
- `response_engine`
- Planner-Integration

## Nicht-Ziele Dieser Phase

- keine medizinische Diagnostik
- keine Therapie-Logik
- keine vollautomatische Persoenlichkeitsklassifikation
- keine Black-Box-Entscheidungen ohne erklaerbare Regeln
