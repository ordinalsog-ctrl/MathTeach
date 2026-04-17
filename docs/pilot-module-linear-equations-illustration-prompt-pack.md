# Pilot Module Illustration Prompt Pack: Lineare Gleichungen

## Zweck

Dieses Dokument uebersetzt das vorhandene mathematische Fundament,
das paedagogische Moduldesign und die psychologisch gebundenen
UI-Regeln in produktive Prompts fuer einen externen
Illustrations- oder Grafik-Workflow.

Es ist kein Stilspiel.

Es ist die operative Bruecke zwischen:

- [pilot-module-linear-equations-illustration-brief.md](/Users/jonasweiss/MathTeach/docs/pilot-module-linear-equations-illustration-brief.md)
- [pilot-module-linear-equations-asset-mapping-sheet.md](/Users/jonasweiss/MathTeach/docs/pilot-module-linear-equations-asset-mapping-sheet.md)
- [pilot-module-linear-equations-throughplay-script.md](/Users/jonasweiss/MathTeach/docs/pilot-module-linear-equations-throughplay-script.md)
- [device-ui-evidence-matrix.md](/Users/jonasweiss/MathTeach/docs/device-ui-evidence-matrix.md)
- [device-learningscreen-contract.md](/Users/jonasweiss/MathTeach/docs/device-learningscreen-contract.md)

## Nicht verhandelbare Hauptregel

Die Prompts duerfen nie nur auf `schoen`, `warm` oder `einladend`
zielen.

Jeder Prompt muss ein `Lehrproblem` loesen:

- Bedeutung vor Symbol sichtbar machen
- denselben Zug links und rechts erklaeren
- Recovery kleiner statt lauter machen
- aehnliches Beispiel als Strukturtransfer zeigen
- Historie als leise Wuerdeebene tragen

## Wie der Pack benutzt wird

Ein produktiver externer Track sollte pro Asset immer mit drei Teilen
arbeiten:

1. `Locked instruction block`
2. `Stage prompt`
3. `Negative block`

Der `Locked instruction block` kommt immer zuerst.

Der `Stage prompt` ist je nach Station verschieden.

Der `Negative block` kommt immer dazu, damit typische generische
KI-Illustrationsmuster nicht hereinkippen.

## Locked Instruction Block

Diesen Block immer unveraendert vor den eigentlichen Stage-Prompt
stellen:

```text
Create a mathematically functional learning illustration for a local-first tutoring device.
This is not decoration and not marketing art.
The image must support one single mathematical idea only.
The scene must feel calm, dignified, safe, non-testing, and low-pressure.
Meaning must be visible before dense symbolic notation.
The composition must work on an 800x480 landscape learning device.
Keep generous breathing room and a clear primary carrier.
The illustration must avoid shame, overload, urgency, and gamification.
```

## Negative Block

Diesen Block immer am Ende anhaengen:

```text
No dashboard layout, no app cards, no floating UI boxes, no menu chrome, no smartphone app styling, no gamification, no badges, no trophies, no countdowns, no red error states, no glossy 3D icons, no mascot characters, no children in a classroom, no school desk scene, no random decorative formulas, no exaggerated arrows, no chaotic background objects, no museum portrait scene, no visual clutter, no second main idea.
```

## Global Style Guidance

Diese Punkte duerfen in einem externen Track variiert werden, solange
die mathematische Funktion stabil bleibt:

- ruhige handgemachte Linien
- warmes, nicht steriles Papier- oder Druckgefuehl
- klare, reduzierte Formen
- lesbare Gruppierung
- leichte Materialtextur

Diese Punkte duerfen nicht variiert werden:

- Reihenfolge der Information
- mathematische Beziehung der beiden Seiten
- Unterschied zwischen `relationship_intro`, `standard`, `repeat`,
  `example`
- Recovery als `kleiner und expliziter`, nicht `groesser und dramatischer`

## Prompt 1: Relationship Intro

### Funktion

- vor der Gleichung
- vor der Operation
- vor dem Ergebnis

### Prompt

```text
Show a calm pre-symbolic relationship for an introductory algebra lesson.
Left side: one unknown whole or covered quantity plus exactly three identical small units.
Right side: exactly seven identical units as the full matching total.
Both sides must feel equally important and clearly connected.
No equation symbols yet, no minus operation, no result row.
The unknown part should be visible as one calm distinct shape, not a mystery gimmick.
The three added units must read as an addition to the left side, not as a separate list.
The seven units on the right must read as the total counterpart.
The visual relationship must suggest stability, balance, and togetherness without using a flashy scale gimmick.
The learner should immediately feel: these two sides belong together.
```

### Locked Math Constraints

- unknown quantity on the left
- `+3` still visible as quantity, not only text
- total `7` visible on the right
- no algebra notation yet

## Prompt 2: Equation Form

### Funktion

- dieselbe Beziehung jetzt als kleine lesbare Gleichung
- noch keine Operationsspur

### Prompt

```text
Show the same calm relationship now translated into a first algebra line.
Keep the same left-right structure from the pre-symbolic carrier.
Introduce exactly one simple equation: x + 3 = 7.
The learner must still be able to see that x stands for the unknown whole on the left.
The three must remain visibly grouped as an addition to the unknown on the left side.
The seven must remain the total counterpart on the right side.
Do not add any operation marks yet.
Do not create a second scene.
The image should help the learner feel: this equation is the same relationship, only now written down.
```

### Locked Math Constraints

- show `x + 3 = 7`
- no `-3`
- no result row
- bind symbol directly back to quantity structure

## Prompt 3: Same Operation On Both Sides

### Funktion

- derselbe Zug links und rechts
- kein Trick, kein Zauber

### Prompt

```text
Show the same equation carrier with one calm operation introduced on both sides.
Keep x + 3 = 7 as the main line.
Add exactly the same subtraction on both sides: minus 3 on the left and minus 3 on the right.
The operation must feel small, controlled, and relationship-preserving.
It must not feel like a dramatic strike-through or a magic reveal.
The learner should see that the same action happens on both sides to preserve the relationship.
Use the same carrier and the same structural layout as before.
Do not jump to the result yet.
```

### Locked Math Constraints

- main line `x + 3 = 7`
- operation line `-3` and `-3`
- no `x = 4` result yet

## Prompt 4: Result From The Same Structure

### Funktion

- Ergebnis kommt aus derselben Struktur
- keine neue Szene

### Prompt

```text
Show the equation, the same-operation row, and the resulting simplified relationship in one single connected carrier.
Keep the original equation x + 3 = 7 visible.
Keep the operation row -3 and -3 visible.
Now show the derived result x = 4 as the consequence in the same structure, not as a separate scene.
The result should feel earned, calm, and readable.
The learner should feel: this result comes from the exact same relationship and the same move, not from a jump.
```

### Locked Math Constraints

- top line `x + 3 = 7`
- operation line `-3` and `-3`
- result line `x = 4`
- one connected carrier only

## Prompt 5: Repeat / Recovery Variant

### Funktion

- dieselbe Struktur
- expliziter
- kleiner statt lauter

### Prompt

```text
Create a recovery version of the same linear-equation carrier.
Do not change the numbers and do not introduce a new example.
Use the same equation x + 3 = 7.
Use the same subtraction row -3 and -3.
Use the same result x = 4.
The difference must be structural clarity, not stronger drama.
Make the operation and result path more explicit and easier to follow.
Recovery must feel supportive and dignified, not remedial or childish.
It should feel like the same idea made clearer, not a reset to the beginning.
```

### Locked Math Constraints

- same numbers as standard
- same structure as standard
- more explicit path only

## Prompt 6: Similar Example

### Funktion

- gleiche Struktur
- andere Zahlen
- kein Themenwechsel

### Prompt

```text
Show a near-transfer version of the same algebra structure.
Use the example 5 + 2 = 7.
Show the same subtraction on both sides: -2 and -2.
Show the resulting equality 5 = 5.
The image must clearly feel like the same rule in another number situation.
It must not feel like a new chapter or a different topic.
The visual grammar should match the main carrier closely, while the numbers clearly differ.
The learner should feel: same structure, different numbers.
```

### Locked Math Constraints

- equation `5 + 2 = 7`
- operation `-2` and `-2`
- result `5 = 5`

## Prompt 7: History Sidecar

### Funktion

- Problem -> Verfahren -> Notation
- Wuerde und Sinn
- semantisch leiser als der Hauptcarrier

### Prompt

```text
Create a quiet historical sidecar illustration for an early algebra lesson.
Do not make this a hero scene and do not make it a museum image.
The visual idea must show that algebra emerged as a way to turn problems into solvable procedures and readable notation.
Use a calm, secondary composition that stays clearly less dominant than the main learning carrier.
If a historical anchor is needed, suggest al-Khwarizmi as a bridge to procedural algebra, but without making the image into a portrait celebration.
The learner should feel dignity, meaning, and continuity of mathematical culture, not distraction.
```

### Locked Meaning Constraints

- no portrait-first image
- no person cult
- no giant historical tableau
- must stay secondary

## Prompt 8: Asset Family Sheet

### Funktion

- externer Track soll mehrere zusammengehoerige Assets entwickeln

### Prompt

```text
Create a coherent educational illustration family for a first module on linear equations.
The family must include:
1. relationship-before-formula carrier
2. unknown-plus-three to seven carrier
3. same-operation-on-both-sides carrier
4. result-from-same-structure carrier
5. similar-example carrier
6. optional quiet history sidecar
All assets must clearly belong together, but each one must solve a distinct mathematical teaching problem.
Do not flatten standard, repeat, and example into one generic visual treatment.
Deliver a system that supports progression: relationship, notation, operation, result, transfer, optional history.
```

## Prompt 9: State Variant Sheet

### Funktion

- externer Track soll `standard`, `repeat`, `example` sauber trennen

### Prompt

```text
Create state variants for a linear-equation teaching carrier:
standard, repeat, and example.
Standard must show one main equation without an expanded operation path.
Repeat must keep the same equation but make the operation row and result row more explicit.
Example must keep the same structure but switch to a nearby example with different numbers.
The differences must be structural and didactic, not only color-based.
Do not make repeat louder.
Do not make example feel like a new topic.
```

## Optional Tool Add-On: Vector-First

Wenn das Programm SVG oder editierbare Vektoren gut kann, diesen Block
anhaengen:

```text
Prefer flat editable vector shapes, clear layer separation, and safe export for SVG.
Keep the composition readable at 800x480.
Avoid ultra-fine texture that will break when vectorized.
```

## Optional Tool Add-On: Raster-First

Wenn das Programm eher rasterbasiert arbeitet, diesen Block anhaengen:

```text
Create clean separable foreground structure with minimal background noise.
Preserve clear silhouette and grouping so the image can later be translated into SVG or a simplified asset system.
```

## Produktionshinweis

Wenn wir mit einem externen Tool oder einer externen Person arbeiten,
sollte die Reihenfolge fuer Pilot 1 sein:

1. `Prompt 1` Relationship Intro
2. `Prompt 2` Equation Form
3. `Prompt 3` Same Operation
4. `Prompt 4` Result
5. `Prompt 6` Similar Example
6. `Prompt 5` Repeat Variant
7. `Prompt 7` History Sidecar
8. `Prompt 8` Asset Family Sheet
9. `Prompt 9` State Variant Sheet

## Abnahmefragen

Ein generiertes oder gezeichnetes Ergebnis ist nur dann brauchbar,
wenn wir intern mit `ja` antworten koennen:

1. Wird die mathematische Idee klarer statt nur attraktiver?
2. Ist die psychologische Wirkung ruhig, sicher und wuerdevoll?
3. Sieht man Beziehung vor Symbol?
4. Ist `repeat` kleiner und expliziter statt dramatischer?
5. Fuehlt sich `example` wie dieselbe Struktur und nicht wie neues
   Thema an?
6. Bleibt Historie, falls vorhanden, leiser als der Hauptcarrier?
