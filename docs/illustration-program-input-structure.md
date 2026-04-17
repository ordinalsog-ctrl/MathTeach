# Illustration Program Input Structure

## Zweck

Dieses Dokument liefert **nicht** die mathematische Erklaerung selbst.

Text, Formeln, Schrittfolge und Tutor-Sprache bleiben in MathTeach.

Dieses Dokument liefert die Struktur, die an ein grafisches
Illustrationsprogramm uebergeben werden kann, damit die **grafische
Huelle** und der **primaere visuelle Carrier** den vorhandenen
mathematischen, paedagogischen und psychologischen Regeln entsprechen.

Kurz:

- MathTeach liefert `Gehirn`
- das Illustrationsprogramm liefert `sichtbare Carrier-Ausfuehrung`

## Hauptregel

Ein externes Illustrationsprogramm darf fuer MathTeach **nicht**
entscheiden:

- was mathematisch erklaert wird
- in welcher Reihenfolge erklaert wird
- welche Formel oder welcher Text auf dem Screen steht
- welche Recovery-Logik gilt

Ein externes Illustrationsprogramm darf nur ausfuehren:

- Grundflaeche
- Carrier-Form
- Atmosphaere
- historische Einfaerbung
- visuelle Ruhe
- freie Flaechen fuer Text-/Formel-Overlay

## Was das Grafikprogramm produzieren soll

Fuer MathTeach soll ein Grafikprogramm im Normalfall **keinen
fertig beschrifteten Screen** erzeugen.

Es soll stattdessen einen Asset-Typ aus einer von vier Klassen
erzeugen:

1. `Base Surface`
2. `Primary Carrier`
3. `Sidecar Carrier`
4. `State Variant Set`

### 1. Base Surface

Die ruhige Gesamtflaeche:

- Hintergrund
- Tonalitaet
- Materialanmutung
- visuelle Wuerde
- negative Flaeche fuer spaetere Text-/Formel-Overlay

### 2. Primary Carrier

Der eigentliche mathematische Traeger:

- Beziehung
- Menge
- Operation
- Beweis
- Notationsentwicklung
- Transmission
- Anwendung

### 3. Sidecar Carrier

Eine kleine sekundäre Zusatzspur:

- historische Wuerdeebene
- Kommentarspur
- ruhige Kontextverankerung

Nie:

- Hauptbild
- Biografieposter
- Dekoersatz fuer Mathematik

### 4. State Variant Set

Varianten desselben Assets fuer:

- `intro`
- `standard`
- `repeat`
- `example`
- optional `history_sidecar`

Wichtig:

- `repeat` bedeutet kleiner, klarer, ruhiger
- `example` bedeutet gleiche Struktur, andere Instanz

## Nicht verhandelbare psychologische Regeln

Jeder Input an ein Grafikprogramm muss diese Regeln tragen:

- Bedeutung vor Symbol
- ein Gedanke pro Screen
- kein Testton
- keine Beschamung
- keine dekorative Illustration ohne mathematische Funktion
- Recovery verkleinert den Schritt
- Wuerde statt Spielzeuganmutung
- Zugehoerigkeit statt Distanz
- Ruhe statt App-Hektik

## Nicht verhandelbare visuelle Regeln

Das Grafikprogramm darf **nicht** produzieren:

- Dashboard-Layout
- Kartenstapel
- Floating-Box-Komponenten
- Smartphone-App-Optik
- Gamification
- rote Warnsignale
- ueberfuellte Komposition
- Figuren-/Personenszenen als mathematischen Ersatz
- eingebetteten UI-Text oder Buttons
- eingebrannte Formeln, wenn Formel spaeter dynamisch aus MathTeach
  kommt

## Empfohlene Layer-Struktur pro Asset

Jeder Text-Input an das Grafikprogramm soll diese Layer klar trennen:

### Layer A: Emotional Base

- ruhig
- wuerdevoll
- konzentriert
- nicht kalt
- nicht verspielt

### Layer B: Epoch Inflection

- antik
- mittelalterlich
- fruehneuzeitlich
- modern

Aber:

- niemals als Kulisse
- immer als mathematische Denkform

### Layer C: Primary Mathematical Carrier

Der zentrale bildliche Traeger.

Hier liegt die eigentliche mathematische Funktion.

### Layer D: Overlay Safe Zones

Leer- oder Ruheflaechen fuer:

- Titel
- kurze Tutor-Zeile
- Formel
- kleiner Hinweis

Diese Zonen muessen grafisch mitgedacht, aber **nicht** beschriftet
werden.

### Layer E: Optional Quiet Sidecar

Kleiner Zusatzkontext:

- historische Spur
- Kommentarspur
- Uebertragung

Immer visuell untergeordnet.

## 800x480 Device-Safe-Zone-Regel

Wenn das Asset fuer das Device gedacht ist, soll der Input immer sagen:

- Format: `800x480 landscape`
- kein Vollflaechen-Text
- keine harte Mittellinie
- keine vier gleich starken Zonen
- eine klare primaere Bildflaeche
- mindestens eine ruhige Overlay-Zone fuer MathTeach-Text

Empfohlene funktionale Aufteilung:

- `10-15%` ruhige obere Zone fuer Titel/Status
- `50-65%` primaere Carrier-Flaeche
- `15-25%` ruhige Zusatz-/Hinweiszone
- `15-20%` freie oder weich gefuehrte Aktionsnaehe

Diese Werte sind keine Pixelpflicht, sondern Kompositionspflicht.

## Struktur fuer den Text-Input an ein Grafikprogramm

Jeder produktive Input soll aus genau diesen Blocken bestehen.

## Block 1: Asset Identity

- `Project`: MathTeach
- `Module`:
- `Epoch`:
- `Stage`:
- `State Variant`:
- `Output Type`: base surface / primary carrier / sidecar / variant set

## Block 2: Didactic Role

Hier nur:

- was dieser Asset-Typ mathematisch leisten muss
- nicht wie der Tutor es sprachlich erklaert

Beispiel:

- "Make a pre-symbolic relationship visible before equation notation."
- "Make a local operation visible as the same move on both sides."

## Block 3: Psychological Contract

Hier steht:

- wie sich das Asset psychologisch anfuehlen muss

Beispiel:

- calm
- dignified
- low-pressure
- non-testing
- focused
- safe
- not childish

## Block 4: Primary Carrier Type

Genau ein Carrier:

- Relationship Carrier
- Quantity Carrier
- Operation Carrier
- Result Carrier
- Transfer Carrier
- Proof Carrier
- Notation Evolution Carrier
- Transmission Carrier
- Application Bridge Carrier

## Block 5: What Must Be Visible

Nur die mathematisch zwingenden Bildelemente.

Beispiel:

- one unknown whole
- three identical added units
- seven total units
- both sides visibly belonging together

Keine UI-Elemente.
Keine Textelemente.
Keine Buttons.

## Block 6: What Must Stay Empty

Hier werden die Flaechen definiert, die bewusst frei bleiben fuer
MathTeach:

- title safe zone
- formula safe zone
- explanation safe zone
- action-safe breathing room

## Block 7: Epoch Inflection

Hier steht:

- wie die Epoche die Darstellung faerbt
- ohne den mathematischen Kern zu ersetzen

Beispiel:

- "Show transmission and procedure, not orientalist scenery."
- "Show proof order and form, not temple aesthetics."

## Block 8: Forbidden Distortions

Hier steht alles, was das Grafikprogramm nicht tun darf.

Beispiel:

- no cards
- no dashboard
- no decorative manuscript wallpaper
- no scholar portrait
- no embedded text
- no glossy 3D icon look

## Block 9: Output Constraints

- vector-first or raster-first
- transparent background or full surface
- single asset or asset family
- state variants required or not
- readable at 800x480

## Block 10: Deliverable Form

Beispiel:

- one primary SVG
- one simplified fallback SVG
- repeat variant
- example variant
- optional sidecar variant

## Tool-Ready Prompt Skeleton

Der folgende Block ist bewusst in Englisch gehalten, damit er direkt in
Grafikprogramme uebergeben werden kann.

```text
Project: MathTeach
Module: [MODULE]
Epoch: [EPOCH]
Stage: [STAGE]
State Variant: [STATE]
Output Type: [base surface / primary carrier / sidecar / variant set]

Didactic Role:
[ONE CLEAR SENTENCE ABOUT THE MATHEMATICAL JOB OF THE ASSET]

Psychological Contract:
calm, dignified, low-pressure, non-testing, focused, safe, not childish, not gamified

Primary Carrier Type:
[EXACTLY ONE CARRIER]

What Must Be Visible:
- [VISIBLE MATHEMATICAL ELEMENT 1]
- [VISIBLE MATHEMATICAL ELEMENT 2]
- [VISIBLE MATHEMATICAL ELEMENT 3]

What Must Stay Empty:
- safe zone for title
- safe zone for formula
- safe zone for short explanation
- breathing room for action area

Epoch Inflection:
[HOW THE EPOCH SHOULD SHAPE THE VISUAL LOGIC WITHOUT BECOMING DECORATIVE]

Forbidden Distortions:
- no dashboard layout
- no floating cards
- no smartphone app styling
- no gamification
- no red warning cues
- no embedded UI buttons
- no embedded final text blocks
- no decorative historical scenery without teaching function
- no second main idea

Output Constraints:
- 800x480 landscape readability
- one primary carrier only
- text and formulas will be added later by MathTeach
- keep visual hierarchy quiet and readable
- produce [vector-first / raster-first] output
- include [repeat/example/history sidecar] variants if requested

Deliverable:
[EXACT OUTPUT PACKAGE]
```

## Beispiel 1: Relationship-Intro fuer lineare Gleichungen

```text
Project: MathTeach
Module: linear equations
Epoch: cross-epoch neutral learning carrier
Stage: relationship_intro
State Variant: intro
Output Type: primary carrier

Didactic Role:
Make a pre-symbolic relationship visible before equation notation.

Psychological Contract:
calm, dignified, low-pressure, non-testing, focused, safe, not childish, not gamified

Primary Carrier Type:
Relationship Carrier

What Must Be Visible:
- one unknown whole as one calm distinct part
- three added identical units on the same side
- seven total units on the other side
- visible belonging of both sides without using flashy balance gimmicks

What Must Stay Empty:
- quiet top zone for title
- quiet mid or lower zone for later formula insertion
- small explanation-safe zone
- breathing room near the future action area

Epoch Inflection:
Keep the carrier historically neutral and pedagogically direct. This is not a historical scene.

Forbidden Distortions:
- no dashboard layout
- no floating cards
- no embedded equation text
- no cartoon mascots
- no classroom scene
- no decorative objects
- no second main idea

Output Constraints:
- 800x480 landscape readability
- one primary carrier only
- text and formulas will be added later by MathTeach
- vector-first preferred
- prepare standard and repeat variants

Deliverable:
one SVG primary carrier, one simplified repeat SVG
```

## Beispiel 2: Medieval place-value carrier

```text
Project: MathTeach
Module: place value and zero
Epoch: Medieval Transmission and Synthesis
Stage: place_value_intro
State Variant: standard
Output Type: primary carrier

Didactic Role:
Make positional value visible before formal rule compression.

Psychological Contract:
calm, dignified, low-pressure, non-testing, focused, safe, not childish, not gamified

Primary Carrier Type:
Quantity Carrier

What Must Be Visible:
- same numeral shape in different positions
- one place held or stabilized by zero or empty-position logic
- visible difference in mathematical role through position

What Must Stay Empty:
- safe zone for title
- safe zone for later explanation text
- breathing room for formula or notation overlay

Epoch Inflection:
Show procedure, positional structure, and transmission logic, not decorative manuscript nostalgia.

Forbidden Distortions:
- no orientalist scenery
- no scholar portrait
- no decorative manuscript wallpaper
- no dense number table without meaning
- no second main idea

Output Constraints:
- 800x480 landscape readability
- one primary carrier only
- vector-first preferred
- keep text and numerals mostly for later overlay except where carrier structure truly needs placeholder marks

Deliverable:
one SVG primary carrier, one repeat variant with reduced complexity
```

## Praktische Arbeitsregel

Wenn ein Grafikprogramm fuer MathTeach gebrieft wird, dann immer in
dieser Reihenfolge:

1. `Carrier zuerst`
2. `psychologische Wirkung`
3. `mathematische Muss-Elemente`
4. `freie Overlay-Zonen`
5. `epochale Einfaerbung`
6. `Verbote`
7. `Output-Paket`

Nicht in dieser Reihenfolge:

1. Stil
2. Stimmung
3. Dekoration
4. danach Mathematik

Denn genau dann kippt das Ergebnis wieder in generischen oder falschen
Illustrationsmuell.
