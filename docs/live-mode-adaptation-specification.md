# Live Mode Adaptation Specification

## Zweck

Dieses Dokument konkretisiert Phase `H` von MathTeach auf
Implementierungsniveau.

Es beantwortet die offenen Fragen aus den Reviews:

- was genau beobachtet wird
- wann ein Moduswechsel ueberhaupt geprueft wird
- wo diese Logik in der Architektur lebt
- wie Hysterese technisch gedacht ist
- wie ruhige Uebergangssprache erzeugt werden soll

## Kernentscheidung

Phase `H` fuehrt **keine zweite freie Mode-Auswahl** ein, sondern eine
kontrollierte `runtime mode adaptation` auf Basis des bereits gewaehlten
Startmodus.

Die Reihenfolge bleibt:

1. `mode_selector` waehlt den Startmodus
2. `runtime_mode_adapter` prueft spaeter blockweise, ob dieser Modus
   beibehalten oder sanft verschoben werden soll

## Neue Architekturkomponente

Die operative Logik von Phase `H` soll in einer neuen Komponente leben:

- `src/mathteach/services/runtime_mode_adapter.py`

Nicht im:

- `mode_selector.py`

weil dort die **Startentscheidung** getroffen wird,

und auch nicht direkt im:

- `conflict_resolver.py`

weil dort Supportkonflikte und Prioritaetslogik liegen, nicht
Laufzeitbeobachtung.

## Was ist ein Block

Fuer Phase `H.1` ist ein `Block` die kleinste Einheit, nach der ein
Moduswechsel geprueft werden darf.

Ein Block ist genau eine dieser Formen:

- ein kurzer Erklaerabschnitt mit anschließendem Verstaendnischeck
- ein worked example mit Abschlussfrage
- eine ueberschaubare Uebungsrunde mit Rueckmeldung
- ein prerequisite repair segment

Ein Block ist **nicht**:

- ein einzelner Rechenschritt
- ein einzelner Token oder Satz
- jede kleine Nutzerreaktion fuer sich

## Observation Signals

### Designprinzip

Observation Signals sollen:

- textbasiert auswertbar bleiben
- support-sensitiv interpretierbar sein
- nicht klinisch oder diagnostisch wirken
- als beobachtete Lernsignale formuliert werden

### Vorgeschlagenes Datenobjekt

```python
@dataclass
class ObservationSignal:
    signal_type: str
    strength: float
    evidence: list[str]
    support_context: list[str]
    block_index: int
```

### Primäre Signaltypen

#### 1. `confusion_signal`

Hinweise:

- gleiche Fehlrichtung wiederholt sich
- Rueckfrage zeigt unveraendertes Missverstaendnis
- Lernende Antwort weicht vom Kernziel sichtbar ab

#### 2. `overload_signal`

Hinweise:

- zu viele Elemente gleichzeitig werden verwechselt
- Antwort bricht mitten in der Struktur weg
- Symbolik oder Textlast ueberfordert den aktuellen Block

#### 3. `stagnation_signal`

Hinweise:

- keine sichtbare Bewegung ueber mehrere Versuche
- immer dieselbe Hilfe fuehrt nicht weiter
- gleiche Aufgabe bleibt trotz Rueckmeldung unverstanden

#### 4. `breakthrough_signal`

Hinweise:

- Lernender erkennt Muster selbst
- Antwort wird kuerzer und sicherer
- Transfer auf aehnliche Aufgabe gelingt

#### 5. `confidence_recovery_signal`

Hinweise:

- Lernender formuliert wieder aktiver
- Selbstkorrektur gelingt
- sichtbar weniger rueckweichende Sprache

## Support-Sensitive Interpretation

Dasselbe Oberflaechensignal kann je nach Supportprofil anders gewichtet
werden.

### Beispiele

#### ADHD-aware support

- langsame Antwort allein ist **kein** starker Ueberforderungshinweis
- abruptes Abbrechen eines Musters zaehlt staerker
- wiederholter Kontextverlust zaehlt staerker

#### Dyscalculia-aware support

- langsameres Arbeiten im konkreten Modus ist oft normal
- gleicher Mengenfehler in mehreren Bloecken zaehlt staerker
- Symbolfehler ohne Mengenverstaendnis zaehlen staerker als Tippfehler

#### Dyslexia-aware support

- Lesefehler duerfen nicht vorschnell als Mathematikfehler gelesen werden
- Textueberlastung zaehlt staerker als reine Bearbeitungszeit

#### Autism-spectrum-aware support

- abrupter Leistungsabfall nach Strukturbruch zaehlt staerker
- Reiz- und Layoutwechsel koennen Signale beeinflussen

#### Language-sensitive support

- Begriffsmissverstaendnisse sind nicht automatisch Konzeptmissverstaendnisse
- Rueckfragen zu Vokabular zaehlen nicht sofort als Stagnation

#### Scarcity-aware support

- Ausstieg nach fehlender Erfolgslinie zaehlt staerker
- kleine sichtbare Erfolge haben hoeheren positiven Signalwert

## Triggerlogik

### Grundregel

Ein Moduswechsel wird nur geprueft, wenn:

1. ein Block abgeschlossen ist
2. mindestens ein relevantes Signal ueber dem Schwellwert liegt
3. Hysterese den Wechsel nicht blockiert

### Erste Schwellenlogik

Die erste Phase soll noch nicht numerisch feinoptimiert sein.

Sie arbeitet mit drei Klassen:

- `weak`
- `meaningful`
- `strong`

Ein Wechsel wird nur bei mindestens `meaningful` geprueft,
und nur bei `strong` ohne weiteres Zusatzsignal empfohlen.

## Adaptation Rules

### Form

```python
@dataclass
class ModeAdaptationRule:
    current_mode: str
    triggering_signal: str
    support_context: tuple[str, ...]
    target_mode: str
    reason: str
```

### Erste Wechselregeln

#### Ueberforderung

- `origin_then_example -> worked_example_tutoring`
- `guided_concept_explanation -> worked_example_tutoring`
- `formal_compact_explanation -> guided_concept_explanation`

#### Stabiler Fortschritt

- `worked_example_tutoring -> guided_concept_explanation`
- `guided_concept_explanation -> origin_then_example`

### Wichtige Begrenzung

Phase `H.1` erlaubt nur Wechsel zu **nahe liegenden** Modi.

Nicht erlaubt:

- `formal_compact_explanation -> origin_story_explanation`
- mehrere Spruenge in einem einzigen Adaptionsschritt

## Hysteresis Model

### Zweck

Hysterese soll verhindern:

- Modusflattern
- hektische Rueckwechsel
- Ueberreaktion auf einzelne schwache Signale

### Vorgeschlagenes Datenobjekt

```python
@dataclass
class ModeAdaptationState:
    current_mode: str
    blocks_in_current_mode: int
    mode_changes_in_session: int
    last_change_reason: str | None
    cooldown_blocks_remaining: int
```

### Erste Guardrails

- `min_blocks_in_mode = 2`
- `max_mode_changes_per_session = 3`
- `cooldown_blocks_after_change = 1`

### Wirkung

Das System darf also nicht:

- nach jedem Block springen
- direkt im naechsten Block wieder zurueckspringen
- eine Sitzung in staendige Moduskorrektur verwandeln

## Transition Messaging

### Prinzip

Uebergangsmeldungen sind:

- kurz
- ruhig
- lernendenzentriert
- nicht technisch
- nicht beschämend

### Drei Grundfamilien

#### 1. Simplifying Transition

Wenn das System vereinfacht:

- "Lass mich einen Schritt zurueckgehen und es klarer zeigen."
- "Wir machen das jetzt direkter und in kleineren Schritten."

#### 2. Confidence-Building Transition

Wenn das System nach Stagnation neu ansetzt:

- "Das ist eine Stelle, an der viele haengen bleiben. Wir nehmen einen anderen Zugang."
- "Wir bleiben bei derselben Idee, aber ich zeige sie dir jetzt anders."

#### 3. Stretch Transition

Wenn das System bei Erfolg etwas oeffnet:

- "Das klappt schon gut. Ich gebe dir jetzt etwas mehr Eigenraum."
- "Du hast das Muster gut erfasst. Lass uns einen Schritt weitergehen."

### Nicht erlaubt

- "Ich wechsle jetzt den Modus."
- interne Modusnamen gegenueber Lernenden
- Formulierungen, die Defizite oder Scheitern zuschreiben

## Rueckwaertskompatibilitaet mit Phase G

Phase `G` bleibt die gueltige Startentscheidung.

Phase `H` bedeutet **nicht**, dass `G` falsch war.

Stattdessen gilt:

- `G` waehlt den besten Startmodus auf Basis des bekannten Profils
- `H` reagiert spaeter auf neu beobachtete Laufzeitsignale

Damit ist `H` eine **zustandsbasierte Fortsetzung** von `G`, nicht deren
Widerspruch.

## Teststrategie fuer H.1

### Neue Testfamilien

- `test_observation_signal_interpretation.py`
- `test_runtime_mode_adapter.py`
- `test_transition_language.py`

### Mindestens zu pruefen

1. Ueberforderung fuehrt blockweise zu Vereinfachung
2. Erfolg fuehrt blockweise zu vorsichtiger Oeffnung
3. Hysterese blockiert zu fruehe Rueckwechsel
4. Transition Messaging bleibt nicht-technisch
5. Phase-G-Startmodus bleibt unbeschaedigt

## Erwartete erste Codeartefakte

- `src/mathteach/services/runtime_mode_adapter.py`
- Erweiterung in [models.py](/Users/jonasweiss/MathTeach/src/mathteach/models.py)
- spaetere Planner-Integration in [planner.py](/Users/jonasweiss/MathTeach/src/mathteach/services/planner.py)

## H.1 Exit Criteria

Phase `H.1` ist erfolgreich, wenn:

- Beobachtungssignale explizit modelliert sind
- blockweise Moduspruefung existiert
- Hysterese einfache Oszillation verhindert
- Uebergangssprache sauber generiert werden kann
- bestehende Phase-G-Tests nicht regressieren

