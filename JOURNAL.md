# MathTeach Journal

Stand: 2026-04-02

## Review-Einarbeitung 2026-04-02

Der externe Journal-Review wurde als naechste Prioritaetskorrektur uebernommen.

Wichtigste Konsequenzen:

- der bisherige Stand wird als `solide und strategisch sauber` bestaetigt
- die Hauptluecke liegt jetzt in der `Operationalisierung`
- der naechste Hauptschritt ist nicht neue Allgemeintheorie, sondern die `Support Response Matrix`
- die aktive Zielarchitektur wird jetzt klarer als `lokal-first`, `geschlossen` und `rule-based` gefasst
- die Support-Matrix arbeitet mit `support signals` statt mit diagnostischen Prozentmodellen

Neue Referenzdokumente aus dieser Review-Einarbeitung:

- [docs/journal-review-triage-2026-04-02.md](/Users/jonasweiss/MathTeach/docs/journal-review-triage-2026-04-02.md)
- [docs/support-response-matrix-structure.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-structure.md)
- [docs/architecture-v2.md](/Users/jonasweiss/MathTeach/docs/architecture-v2.md)

## Projektkern

MathTeach ist aktuell als `geschlossenes lokales Mathematik-Lernsystem` angelegt.

Zielbild:

- kompletter lokaler Mathematik-Korpus
- lokaler `Teacher Mind`
- keine Cloud-Pflicht
- nutzbar als App oder eigenes Geraet
- stark fuer armutsbetroffene Lernende, aber ebenso fuer Schule, Studium und erwachsene Selbstlerner

Die Architektur trennt weiterhin:

- `Knowledge Core`
- `Teacher Mind`
- `Teaching Intelligence Engine`

## Aktueller Mathematik-Korpus

Die mathematische Grundsammlung ist fuer die erste grosse Projektphase ueber vier Epochen aufgebaut und als stabiler Kern zu betrachten.

### Antiquity

- `Euclid: Elements`
- `Archimedes: On the Sphere and Cylinder`
- `Archimedes: The Method`
- `Apollonius: Conics`
- `Diophantus: Arithmetica`
- `Heron: Metrica`
- `Pappus: Collection`
- `Hipparchus: commentary and chord-table tradition`
- `Theon of Alexandria: Euclid and Ptolemy commentary tradition`
- `Hypatia: commentary tradition on Arithmetica and Conics`
- `Eutocius of Ascalon: commentaries on Archimedes and Apollonius`
- `Aryabhata: Aryabhatiya`

### Medieval Transmission and Synthesis

- `Brahmasphutasiddhanta`
- `Al-Khwarizmi: Book on Addition and Subtraction after the Method of the Indians`
- `Al-Khwarizmi: Al-jabr`
- `Fibonacci: Liber Abaci`
- `Bhaskara II: Lilavati`
- `Bhaskara II: Bijaganita`
- `Omar Khayyam: Demonstration concerning problems of algebra`
- `Adelard of Bath: Euclid translation tradition`
- `Al-Karaji: Al-Fakhri`
- `Nicole Oresme: Tractatus de configurationibus qualitatum et motuum`
- `Regiomontanus: De triangulis omnimodis`
- `Nasir al-Din al-Tusi: Treatise on the Quadrilateral`

### Early Modern Analysis and Chance

- `Newton: Method of Fluxions`
- `Leibniz: Nova Methodus pro Maximis et Minimis`
- `Pascal and Fermat correspondence on games of chance`
- `Descartes: La Geometrie`
- `Cavalieri: Geometria indivisibilibus continuorum nova quadam ratione promota`
- `Wallis: Arithmetica infinitorum`
- `Huygens: De Ratiociniis in Ludo Aleae`
- `Viete: In artem analyticam isagoge`
- `Stevin: De Thiende`
- `Napier: Mirifici logarithmorum canonis descriptio`
- `Jacob Bernoulli: Ars Conjectandi`
- `Kepler: Astronomia nova`
- `Fermat: Methodus ad disquirendam maximam et minimam`
- `Barrow: Lectiones geometricae`
- `Henry Briggs: Arithmetica logarithmica`
- `Gregory of Saint-Vincent: Opus geometricum`

### Modern Mathematics

- `Gauss: Disquisitiones Arithmeticae`
- `Fourier: Theorie analytique de la chaleur`
- `Abel: Memoire sur les equations algebriques, ou l'on demontre l'impossibilite de la resolution de l'equation generale du cinquieme degre`
- `Cauchy: Cours d'analyse de l'Ecole Royale Polytechnique`
- `Weierstrass: Mathematische Werke`
- `Galois: Memoire sur les conditions de resolubilite des equations par radicaux`
- `Hamilton: Elements of Quaternions`
- `Cayley: The collected mathematical papers of Arthur Cayley`
- `Kronecker: Werke`
- `Riemann: Ueber die Hypothesen welche der Geometrie zu Grunde liegen`
- `Dedekind: Was sind und was sollen die Zahlen?`
- `Peano: Arithmetices principia, nova methodo exposita`
- `Cantor: Beitrage zur Begrundung der transfiniten Mengenlehre`
- `Zermelo: Untersuchungen ueber die Grundlagen der Mengenlehre I`
- `Hausdorff: Grundzuege der Mengenlehre`
- `Klein: Vergleichende Betrachtungen ueber neuere geometrische Forschungen`
- `Poincare: Analysis Situs`
- `Russell and Whitehead: Principia Mathematica`
- `Hilbert: Grundlagen der Geometrie`
- `Hilbert and Ackermann: Grundzuege der theoretischen Logik`
- `John von Neumann and Oskar Morgenstern: Theory of Games and Economic Behavior`
- `Nicolas Bourbaki: Elements of Mathematics (Theory of Sets)`
- `Emmy Noether: Idealtheorie in Ringbereichen`
- `Lebesgue: Integrale, longueur, aire`
- `Alonzo Church: An Unsolvable Problem of Elementary Number Theory`
- `Gerhard Gentzen: Untersuchungen ueber das logische Schliessen I and II`
- `Kolmogorov: Grundbegriffe der Wahrscheinlichkeitsrechnung`
- `Godel: Ueber formal unentscheidbare Saetze der Principia Mathematica und verwandter Systeme I`
- `Turing: On Computable Numbers, with an Application to the Entscheidungsproblem`
- `Alexander Grothendieck: Sur quelques points d'algebre homologique`
- `Jean-Pierre Serre: Geometrie algebrique et geometrie analytique`

## Aktueller Teacher-Mind-Stand

Der Teacher Mind ist jetzt als gestufter lokaler Wissensaufbau dokumentiert.

Reihenfolge:

1. `Safety and Restraint`
2. `Psychological Foundations`
3. `Pedagogical Foundations`
4. `Universal Round U.1`
5. `Universal Round U.2`
6. `Universal Round U.3`
7. `Universal Round U.4`
8. spaeter `Mathematics Teaching Foundations`
9. spaeter konkrete Runtime- und Response-Matrizen

### Psychological Foundations

- `How People Learn II: Learners, Contexts, and Cultures`
- `How People Learn: Brain, Mind, Experience, and School`
- `Improving Students' Learning With Effective Learning Techniques: Promising Directions From Cognitive and Educational Psychology`
- `Test-Enhanced Learning: Taking Memory Tests Improves Long-Term Retention`
- `The Critical Importance of Retrieval for Learning`
- `Organizing Instruction and Study to Improve Student Learning`
- `Using Student Achievement Data to Support Instructional Decision Making`
- `Learning Styles: Concepts and Evidence`

### Pedagogical Foundations

- `Organizing Instruction and Study to Improve Student Learning`
- `Using Student Achievement Data to Support Instructional Decision Making`
- `Principles of Instruction: Research-Based Strategies That All Teachers Should Know`
- `The Power of Feedback`
- `Focus on Formative Feedback`
- `Self-Explanations: How Students Study and Use Examples in Learning to Solve Problems`
- `Why Minimal Guidance During Instruction Does Not Work`

### Universal Round U.1

- `Self-Determination Theory and the Facilitation of Intrinsic Motivation, Social Development, and Well-Being`
- `A Question of Belonging: Race, Social Fit, and Achievement`
- `Psychological Safety and Learning Behavior in Work Teams`
- `Learning from Errors`
- `Poverty Impedes Cognitive Function`
- `Stereotype Threat and the Intellectual Test Performance of African Americans`
- `Inclusion and Education: All Means All`
- `CAST Universal Design for Learning Guidelines 3.0`

### Universal Round U.2

- `When and Where Do We Apply What We Learn? A Taxonomy for Far Transfer`
- `Toward a Model of Transfer as Sense-Making`
- `Reasoning and Learning by Analogy`
- `Situated Learning: Legitimate Peripheral Participation`
- `Mind in Society: The Development of Higher Psychological Processes`
- `Cognitive Apprenticeship: Teaching the Craft of Reading, Writing, and Mathematics`
- `An Educational Psychology Success Story: Social Interdependence Theory and Cooperative Learning`
- `The Adult Learner`
- `Learning in Adulthood: A Comprehensive Guide`

### Universal Round U.3

- `ADHD in the Classroom: Helping Children Succeed in School`
- `Learning Disabilities`
- `Reading and Reading Disorders`
- `Infographic: Does your child struggle with Math? Dyscalculia could be the reason.`
- `CAST Universal Design for Learning Guidelines 3.0`
- `SAMHSA's Concept of Trauma and Guidance for a Trauma-Informed Approach`
- `How People Learn II: Learners, Contexts, and Cultures`
- `The Adult Learner`
- `Learning Styles: Concepts and Evidence`
- `Why Minimal Guidance During Instruction Does Not Work`
- `Neuroscience and Education: Myths and Messages`

### Universal Round U.4

- `ADHD in the Classroom: Helping Children Succeed in School`
- `Non-pharmacological interventions for attention-deficit/hyperactivity disorder (ADHD) delivered in school settings: systematic reviews of quantitative and qualitative research`
- `Genetics of childhood disorders: XVII. ADHD, Part 1: The executive functions and ADHD`
- `Dyscalculia: from brain to education`
- `Developmental dyscalculia and basic numerical capacities: a study of 8-9-year-old students`
- `Infographic: Does your child struggle with Math? Dyscalculia could be the reason.`
- `Reading and Reading Disorders`
- `Dyslexia (specific reading disability)`
- `Treatment and Intervention for Autism Spectrum Disorder`
- `Visual supports at home and in the community for individuals with autism spectrum disorders: A scoping review`
- `Issues in the use of visual supports to promote communication in individuals with autism spectrum disorder`
- `Teaching Academic Content and Literacy to English Learners in Elementary and Middle School`
- `Successful teaching practices for English language learners in multilingual mathematics classrooms: a meta-analysis`

## Runtime-Stand

Neben dem Dokumentationsstand gibt es jetzt auch einen ersten offenen Runtime-Zweig, der in diesem Commit mitgesichert wird:

- `Tutor Runtime Modes` als eigene Doku
- erster Planner-Routing-Ansatz fuer:
  - `worked_example_tutoring`
  - `origin_story_explanation`
  - `origin_then_example`
- erweiterte `TeachingPlan`- und `RetrievalPlan`-Modelle
- erste API-Tests fuer den Unterschied zwischen Beispielmodus und Ursprungserklaerung

Betroffene Dateien:

- [docs/tutor-runtime-modes.md](/Users/jonasweiss/MathTeach/docs/tutor-runtime-modes.md)
- [docs/architecture.md](/Users/jonasweiss/MathTeach/docs/architecture.md)
- [docs/roadmap.md](/Users/jonasweiss/MathTeach/docs/roadmap.md)
- [src/mathteach/models.py](/Users/jonasweiss/MathTeach/src/mathteach/models.py)
- [src/mathteach/services/planner.py](/Users/jonasweiss/MathTeach/src/mathteach/services/planner.py)
- [tests/test_api.py](/Users/jonasweiss/MathTeach/tests/test_api.py)

## Wichtige Spannung im Repo

Es gibt aktuell noch eine bewusst nicht aufgeloeste Spannung:

- die Produktvision ist inzwischen stark `lokal`, `geschlossen` und notfalls `ohne AI`
- die [README.md](/Users/jonasweiss/MathTeach/README.md) enthaelt noch einen aelteren Modell-Stack mit Cloud-LLMs

Das ist kein Fehler dieses Journal-Schritts, sondern eine offene Architektur-Aufraeumarbeit fuer die naechste oder eine spaetere Session.

Mit dem Review vom `2026-04-02` ist diese Spannung jetzt enger gefasst:

- `architecture-v2` ist die aktive Richtung
- die aelteren Cloud- und Modellpassagen in der README gelten als `Legacy-/Explorationsstand`
- die naechste groessere Repo-Bereinigung sollte README und Runtime explizit an die lokale Zielarchitektur angleichen

## Letzte groessere Commit-Linie

- `7d5ee28` Add universal round U4 program
- `ff995e9` Add universal round U3 program
- `a3e3923` Add universal round U2 program
- `0ad7674` Add universal round U1 program
- `542d690` Triage universal tutor system review
- `7846931` Triage teacher mind foundations review
- `f8b7491` Add pedagogical foundations program
- `7fe991a` Add psychological foundations program
- `792f538` Reorder teacher mind around core foundations
- `a618ff5` Add teacher mind evidence program
- `57036bd` Define pedagogical strategy matrix
- `1cafc85` Define learner support profiles

## Empfohlener naechster Schritt

Der logisch naechste starke Schritt ist:

- keine neue allgemeine Literatur-Runde
- sondern die erste echte `Support Response Matrix`

also die Uebersetzung von:

- `ADHD-aware support`
- `dyscalculia-aware support`
- `dyslexia-aware support`
- `autism-spectrum-aware support`
- `ELL / language-sensitive support`

in konkrete Tutorentscheidungen ueber:

- `pacing`
- `step_size`
- `notation_density`
- `text_load`
- `visualization`
- `error_handling`
- `language_support`
- `self_check_rhythm`
- `external_scaffolds`

Empfohlene erste Ausbaureihenfolge:

1. `ADHD-aware support`
2. `dyscalculia-aware support`
3. `dyslexia-aware support`
4. `autism-spectrum-aware support`
5. `ELL / language-sensitive support`
6. `scarcity-aware support`
