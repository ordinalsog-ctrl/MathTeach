# Profile Conflict Resolution

## Rolle

Dieses Dokument definiert die erste explizite Konfliktaufloesung fuer
`mixed support profiles` in MathTeach.

Es ist die Bruecke zwischen:

- einzelnen Support-Matrizen
- realen Lernprofilen mit mehreren gleichzeitigen Bedarfen
- einer transparenten und testbaren Tutorentscheidung

## Warum diese Schicht notwendig ist

Ein realer Lernender bringt selten nur eine einzige Supportlinie mit.

Typische Kombinationen sind zum Beispiel:

- `ADHD-aware support` plus `scarcity-aware support`
- `dyscalculia-aware support` plus `language-sensitive support`
- `ADHD-aware support` plus `autism-spectrum-aware support`

Ohne explizite Konfliktregeln wuerde das System sonst stillschweigend von
Applikationsreihenfolge oder Zufallsdetails abhaengen.

## Architekturprinzip

MathTeach nutzt in dieser ersten Phase:

1. `deterministic application order`
2. `compatibility matrix`
3. `explicit pairwise conflict rules`
4. `triads and priority ladders`
5. spaeter `broader mixed-profile prioritization`

Die Reihenfolge lautet absichtlich:

- erst Einzelprofile stabilisieren
- dann Paar-Konflikte explizit aufloesen
- dann erste Triads mit Priority Ladders tragen
- erst danach komplexere Mehrfachprofile tiefer operationalisieren

## Nicht genutzte Strategien

Bewusst nicht verwendet werden:

- reine globale Dominanzhierarchien
- gewichtete Black-Box-Aggregation
- implizite Mittelwerte zwischen widerspruechlichen Empfehlungen

MathTeach priorisiert hier:

- Erklaerbarkeit
- Testbarkeit
- Quellennaehe
- paedagogische Plausibilitaet

## Deterministic Application Order

Die aktuelle Grundreihenfolge lautet:

1. `adhd_aware_support`
2. `dyscalculia_aware_support`
3. `dyslexia_aware_support`
4. `autism_spectrum_aware_support`
5. `language_sensitive_support`
6. `scarcity_aware_support`

Diese Reihenfolge ist nur die erste Schicht.

Sie entscheidet noch nicht den Endzustand.
Danach prueft der `conflict_resolver`, ob aktive Profilpaare eine explizite
Konfliktregel brauchen.

## Compatibility Matrix

### Konfliktpaare in der ersten Resolver-Runde

| Pair | Konfliktachsen |
| --- | --- |
| `ADHD + Dyscalculia` | `session_duration`, `break_pattern`, `worked_example_ratio`, `fading_speed`, `primary_representation` |
| `ADHD + Autism` | `session_duration`, `break_pattern`, `check_frequency` |
| `ADHD + Scarcity` | `worked_example_ratio`, `check_frequency`, `language_support` |
| `Dyscalculia + Language-Sensitive` | `symbolic_vs_verbal_balance`, `primary_representation`, `language_support` |
| `Dyscalculia + Scarcity` | `session_duration`, `worked_example_ratio`, `check_frequency` |

### Vorlaeufig kompatible Paare

Diese Paare werden in der ersten Runde noch ohne eigene Konfliktregel
ueber Zusammenspiel und additive Scaffolds getragen:

- `ADHD + Dyslexia`
- `ADHD + Language-Sensitive`
- `Dyscalculia + Dyslexia`
- `Dyscalculia + Autism`
- `Dyslexia + Autism`
- `Dyslexia + Language-Sensitive`
- `Dyslexia + Scarcity`
- `Autism + Language-Sensitive`
- `Autism + Scarcity`
- `Language-Sensitive + Scarcity`

## Erste Konfliktregeln

### 1. ADHD + Dyscalculia

Leitidee:

- Dyskalkulie braucht die laengere konkrete Linie
- ADHD braucht Abwechslung und Regulationsrhythmus innerhalb dieser Linie

Finale Tendenz:

- laengerer konkreter Fokusblock
- ultradiane Mikropausen
- hohe Beispielquote mit variierten Kontexten
- konkrete Materialien mit wechselnden Zugangsformen

Source Anchors:

- `barkley-executive-functions-adhd`
- `butterworth-varma-laurillard-dyscalculia-science`

### 2. ADHD + Autism

Leitidee:

- ADHD braucht Regulationsbewegung
- Autismusspektrum braucht Vorhersagbarkeit und Reizkontrolle

Finale Tendenz:

- kurze, aber vorhersagbare Fokusbloecke
- planbare Regulationspausen
- stabile Uebergaenge
- minimale sensorische Last

Source Anchors:

- `barkley-executive-functions-adhd`
- `rutherford-visual-supports-autism-scoping-review`

### 3. ADHD + Scarcity

Leitidee:

- ADHD braucht Neuheits- und Rueckkopplungssignale
- Scarcity-aware support braucht Relevanz und sichtbare kleine Erfolge

Finale Tendenz:

- kurze Erfolgsschleifen
- sehr fruehe Relevanzmarkierung
- sichtbarer Fortschritt nach wenigen Schritten
- Erfolgskriterien ohne verdeckte Huerden

Source Anchors:

- `barkley-executive-functions-adhd`
- `mani-mullainathan-shafir-zhao-poverty-cognition`
- `ryan-deci-self-determination-theory`

### 4. Dyscalculia + Language-Sensitive

Leitidee:

- Zahlbedeutung muss sichtbar bleiben
- Sprache muss Bedeutung tragen, statt neue Barriere zu werden

Finale Tendenz:

- Mengen- und Alltagsbedeutung vor Symbolkompression
- Glossar und Begriffsbruecken
- kontrollierte Wortlast
- termgestuetzte konkrete oder visuelle Darstellung

Source Anchors:

- `butterworth-varma-laurillard-dyscalculia-science`
- `ies-english-learners-practice-guide`
- `sharma-sharma-multilingual-math-meta-analysis`

### 5. Dyscalculia + Scarcity

Leitidee:

- tiefe konkrete Arbeit darf nicht in unsichtbarer Anstrengung verschwinden
- jeder Block braucht sichtbaren Kompetenzgewinn

Finale Tendenz:

- etwas laengerer konkreter Erfolgsblock
- hohe Beispielquote mit kleinen Erfolgszyklen
- klare Ziel- und Relevanzsprache
- expliziter Wiedereinstieg nach Unterbrechung

Source Anchors:

- `butterworth-varma-laurillard-dyscalculia-science`
- `mani-mullainathan-shafir-zhao-poverty-cognition`
- `ryan-deci-self-determination-theory`

## Resolver-Verhalten

Die erste Resolver-Version arbeitet so:

1. Einzelprofile werden deterministisch angewandt.
2. Aktive Profilpaare werden gegen die Compatibility Matrix geprueft.
3. Fuer Konfliktpaare werden explizite Paar-Regeln auf das Ergebnis gelegt.
4. Das Endergebnis enthaelt:
   - `conflict_pairs`
   - `conflict_resolution_notes`
   - aktualisierte `source_anchors`

Damit ist die Aufloesung nicht nur intern, sondern auch spaeter im API-Pfad
nachvollziehbar.

## Guardrails

- `explicit rules beat accidental override order`
- `accessibility before elegance`
- `conceptual grounding before formal compression`
- `safety before acceleration`
- `small wins must not become patronizing framing`

## Triads and Priority Ladders

In der aktuellen Runde sind jetzt die ersten expliziten Triads operationalisiert.

### Unterstuetzte Triads

| Triad | Priority Ladder |
| --- | --- |
| `ADHD + Dyscalculia + Scarcity` | `conceptual_grounding_before_speed`, `visible_progress_before_problem_volume`, `regulation_cadence_before_long_unbroken_work` |
| `ADHD + Autism + Scarcity` | `predictable_structure_before_novelty`, `sensory_stability_before_task_volume`, `immediate_relevance_before_formal_depth` |
| `Dyscalculia + Language-Sensitive + Scarcity` | `quantity_meaning_before_symbol_compression`, `language_bridge_before_formal_vocabulary`, `visible_success_before_session_density` |

Resolver-Wirkung:

- `triad_groups` machen die erkannte Triad-Konstellation sichtbar
- `priority_ladders` machen die Priorisierung explizit
- Triad-Regeln koennen Paar-Ergebnisse gezielt nachschaerfen

## Noch offen

Diese Runde loest bewusst noch nicht alles:

- keine globale Priorisierung ueber vier oder mehr konkurrierende Profile
- keine intensitaetsgewichtete Modulation
- keine echte Pilotvalidierung mit Lernenden
- noch keine support-sensitive Moduswahl im Planner

## Naechste Ausbaulinie

Nach dieser ersten Resolver-Runde folgen:

1. `triad coverage erweitern`
2. `priority ladders fuer weitere Mischlagen`
3. `planner-level mode selection under conflict`
4. spaetere Pilotierung
