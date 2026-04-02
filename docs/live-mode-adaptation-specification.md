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

## Beobachtungstakt

### Wann wird beobachtet

Beobachtet wird waehrend eines Blocks fortlaufend, aber ein formaler
Adaptionscheck findet nur statt:

- am Ende jedes abgeschlossenen Blocks

### Default-Fenster fuer H.1

Die erste Version bewertet:

- den aktuellen Block
- plus den direkt vorherigen Block fuer Vergleich und Hysterese

### Nicht vorgesehen in H.1

- sekundenbasierte Feinanalyse
- Wechselpruefung nach jedem einzelnen Rechenschritt
- lange gleitende Fenster ueber viele Bloecke

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

### Support-sensitive Interpretation Layer

Rohe Beobachtungen sollen nicht direkt in die Modusentscheidung gehen.

Dazwischen liegt fuer `H.1` ein eigener Interpretationsschritt:

```python
@dataclass
class RawBlockObservation:
    block_index: int
    evidence: list[str]
    current_mode: str


class SignalInterpreter:
    def interpret(
        self,
        raw_observation: RawBlockObservation,
        profile: SupportSignalProfile,
    ) -> list[ObservationSignal]:
        ...
```

Die Aufgabe dieses Schritts ist:

- rohe Evidenz sammeln
- Evidenz support-sensitiv gewichten
- erst danach formale `ObservationSignal`-Objekte ableiten

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

## Schwellenwerte Fuer H.1

Die erste Version arbeitet mit drei Signalstaerken:

- `weak`
- `meaningful`
- `strong`

### `confusion_signal`

- `weak`
  - ein einzelner konzeptioneller Fehler, der nach Hinweis verschwindet
- `meaningful`
  - derselbe konzeptionelle Fehler taucht zweimal in einem Block auf
  - oder dieselbe Rueckfrage bleibt nach einer Klaerung bestehen
- `strong`
  - derselbe konzeptionelle Fehler zieht sich ueber zwei aufeinanderfolgende
    Bloecke

### `overload_signal`

- `weak`
  - ein Lastindikator im Block
  - Beispiel: Antwort bricht ab oder ein Zwischenschritt faellt weg
- `meaningful`
  - zwei Lastindikatoren im selben Block
  - Beispiel: Symbolmix plus Strukturabbruch
- `strong`
  - Ueberlastung bleibt trotz Zusatzstruktur oder Vereinfachung im naechsten
    Block bestehen

### `stagnation_signal`

- `weak`
  - wenig Fortschritt in einem Block
- `meaningful`
  - kein sichtbarer Fortschritt ueber zwei Bloecke
- `strong`
  - kein Fortschritt ueber drei Bloecke trotz gleichbleibender Hilfe

### `breakthrough_signal`

- `weak`
  - richtige Antwort mit starker Fuehrung
- `meaningful`
  - richtiges Muster wird mit geringerer Hilfe selbst wiedererkannt
- `strong`
  - Transfer auf aehnliche Aufgabe gelingt in zwei Bloecken hintereinander

### `confidence_recovery_signal`

- `weak`
  - weniger rueckweichende Sprache in einem Block
- `meaningful`
  - Selbstkorrektur plus aktive Fortsetzungsbereitschaft
- `strong`
  - der Lernende erklaert den naechsten Schritt selbst und bleibt stabil

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

## Adaptation Decision Matrix

Die erste Phase nutzt eine kleine, feste Wechselmatrix.

| Current Mode | Primary Trigger | Threshold | Target Mode | Notes |
| --- | --- | --- | --- | --- |
| `origin_then_example` | `confusion_signal` oder `overload_signal` | `meaningful` | `worked_example_tutoring` | Weniger Vorlauf, mehr direkte Struktur |
| `guided_concept_explanation` | `confusion_signal` oder `stagnation_signal` | `meaningful` | `worked_example_tutoring` | Mehr Beispielbindung und engere Fuehrung |
| `formal_compact_explanation` | `overload_signal` | `meaningful` | `guided_concept_explanation` | Weniger Verdichtung, mehr Zwischenschritte |
| `worked_example_tutoring` | `breakthrough_signal` | `strong` | `guided_concept_explanation` | Nur bei stabiler Sicherheit oeffnen |
| `guided_concept_explanation` | `breakthrough_signal` plus `confidence_recovery_signal` | `strong` | `origin_then_example` | Etwas mehr Eigenraum, aber nicht zu schnell |

### Support-sensitive modifiers

#### ADHD-aware support

- `stagnation_signal` allein reicht nicht schnell fuer einen Wechsel
- `overload_signal` plus Kontextverlust wiegt staerker

#### Dyscalculia-aware support

- langsames Arbeiten im konkreten Modus zaehlt nicht automatisch als
  `stagnation_signal`
- Wechsel nach oben braucht eher `strong breakthrough`, nicht nur Tempo

#### Dyslexia-aware support

- Textfehler muessen zuerst als Sprach- oder Leselast geprueft werden
- `confusion_signal` ist schwaecher, wenn die Mathematik an sich plausibel ist

#### Autism-spectrum-aware support

- Strukturbruch verstaerkt `overload_signal`
- Wechsel duerfen seltener und erklaerter stattfinden

#### Language-sensitive support

- Vokabularprobleme sollen eher den Block vereinfachen als sofort den Modus
  wechseln

#### Scarcity-aware support

- fehlende Erfolgslinie ueber zwei Bloecke verstaerkt `stagnation_signal`
- sichtbare kleine Erfolge verstaerken `confidence_recovery_signal`

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

## Rueckkehrregeln

Ein Rueckwechsel in einen frueheren Modus ist in H.1 nur erlaubt, wenn:

1. der aktuelle Modus mindestens `min_blocks_in_mode` gehalten wurde
2. kein Cooldown mehr aktiv ist
3. ein erneutes `meaningful` oder `strong` Signal den Rueckwechsel stuetzt

Das verhindert:

- `A -> B -> A` in kurzer Folge
- scheinbar nervoeses Tutorverhalten

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

### Pseudocode

```python
def consider_mode_shift(
    state: ModeAdaptationState,
    current_mode: str,
    suggested_mode: str,
) -> tuple[bool, str]:
    if suggested_mode == current_mode:
        return False, current_mode

    if state.cooldown_blocks_remaining > 0:
        return False, current_mode

    if state.blocks_in_current_mode < 2:
        return False, current_mode

    if state.mode_changes_in_session >= 3:
        return False, current_mode

    return True, suggested_mode
```

### Wirkung

Das System darf also nicht:

- nach jedem Block springen
- direkt im naechsten Block wieder zurueckspringen
- eine Sitzung in staendige Moduskorrektur verwandeln

## MVP Default Calibration Fuer H.1

Fuer die erste Runtime-Implementierung gelten feste Startwerte.

Diese Werte sind bewusst konservativ und spaeter kalibrierbar.

| Parameter | Startwert | Zweck |
| --- | --- | --- |
| `observation_window_blocks` | `2` | aktueller Block plus ein Vergleichsblock |
| `minimum_signal_strength_for_shift` | `meaningful` | einzelne schwache Signale loesen keinen Wechsel aus |
| `min_blocks_in_mode` | `2` | mindestens zwei Bloecke pro Modus |
| `cooldown_blocks_after_change` | `1` | kein sofortiger Rueckwechsel |
| `max_mode_changes_per_session` | `3` | Sitzung bleibt stabil |

Diese Kalibrierung gilt fuer `H.1` als MVP-Default, nicht als Endzustand.

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

## Transition Template Structure

Die erste Version soll mit festen Template-Bausteinen arbeiten.

### Template-Form

1. `stabilize`
   - kurze Normalisierung oder Beruhigung
2. `reason`
   - lernendensicherer Grund ohne Defizitzuschreibung
3. `next_step`
   - was jetzt konkret anders geschieht

### Beispiele

#### Simplifying

- `stabilize`: "Das ist eine Stelle, an der viele kurz haengen bleiben."
- `reason`: "Ich nehme etwas Last raus."
- `next_step`: "Wir gehen jetzt in kleineren Schritten weiter."

#### Reframing

- `stabilize`: "Wir bleiben bei derselben Idee."
- `reason`: "Ich erklaere sie dir nur auf einem anderen Weg."
- `next_step`: "Danach pruefen wir sie wieder an einem Beispiel."

#### Stretching

- `stabilize`: "Das klappt schon gut."
- `reason`: "Du hast das Muster sicherer im Griff."
- `next_step`: "Ich gebe dir jetzt etwas mehr Eigenraum."

### Ownership

Die erste Version soll **nicht** frei generiert werden, sondern aus
regelgebundenen Templates kommen.

Damit bleibt die lokale Architektur gewahrt.

## API Zwischen Phase G, Planner Und Phase H

Die operative Schnittstelle fuer `H.1` soll klein und testbar bleiben.

### Zielobjekte

```python
@dataclass
class ModeAdaptationDecision:
    selected_mode: str
    changed: bool
    trigger_signals: list[str]
    transition_family: str | None
    transition_message: str | None
    notes: list[str]


class RuntimeModeAdapter:
    def check_and_adapt_mode(
        self,
        state: ModeAdaptationState,
        current_mode: str,
        block_observation: RawBlockObservation,
        profile: SupportSignalProfile,
    ) -> ModeAdaptationDecision:
        ...
```

### Rueckgabe-Faelle

- `changed = False`
  - derselbe Modus bleibt aktiv
  - keine Uebergangsmeldung notwendig
- `changed = True`
  - ein neuer Modus wird gewaehlt
  - `transition_family` bestimmt das Template
  - `transition_message` wird dem naechsten Block vorangestellt

## Planner Integration Flow

Die Integration in `planner.py` soll fuer `H.1` diesem Ablauf folgen:

1. `mode_selector` liefert den Startmodus fuer die Sitzung oder den neuen
   Anfragekontext
2. der Planner erzeugt einen ersten Block in diesem Modus
3. aus dem Blockverlauf wird eine `RawBlockObservation` aufgebaut
4. `SignalInterpreter` erzeugt daraus support-sensitive `ObservationSignal`
5. `runtime_mode_adapter` prueft am Blockende `stay` oder `shift`
6. bei `shift` wird zuerst `transition_message` ausgegeben
7. der naechste Block wird im neuen Modus geplant

## Rueckwaertskompatibilitaet mit Phase G

Phase `G` bleibt die gueltige Startentscheidung.

Phase `H` bedeutet **nicht**, dass `G` falsch war.

Stattdessen gilt:

- `G` waehlt den besten Startmodus auf Basis des bekannten Profils
- `H` reagiert spaeter auf neu beobachtete Laufzeitsignale

Damit ist `H` eine **zustandsbasierte Fortsetzung** von `G`, nicht deren
Widerspruch.

### Neue Nutzeranfrage waehrend einer Sitzung

Wenn eine neue, fachlich andere Anfrage startet, gilt:

- Phase `G` laeuft erneut
- ein neuer Startmodus wird gewaehlt
- Phase `H` beginnt fuer diese neue Sitzung wieder mit leerem
  Adaptionszustand

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

## Offene Restpunkte Nach Dieser Spezifikation

Trotz dieser Schaerfung bleiben fuer spaetere Feinarbeit offen:

- exakte Kalibrierung der Schwellenwerte im realen Einsatz
- support-spezifische Feinabstimmung mit echten Lernenden
- spaetere history-aware Adaptionspfade ueber mehrere Sitzungen
