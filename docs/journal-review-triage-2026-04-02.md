# Journal Review Triage 2026-04-02

## Ergebnis

Der Review bestaetigt den bisherigen Projektstand als stark und strategisch konsistent:

- der `Mathematik-Korpus` ist als Wissensbasis tragfaehig
- der `Teacher Mind` ist sinnvoll in Foundations und Universal Rounds gestuft
- die ersten `Tutor Runtime Modes` sind paedagogisch plausibel

Die Hauptluecke liegt jetzt nicht mehr in allgemeiner Theorie, sondern in der
`Operationalisierung`:

- von `Learner Profile`
- zu `konkreten Tutorentscheidungen`
- zu `sichtbarem Tutorverhalten`

## Leitentscheidung

Der naechste Hauptschritt ist die `Support Response Matrix`.

Sie wird die Bruecke zwischen:

- `Teacher Mind`
- `Learner Support Profiles`
- `Planner / Runtime`

und konkreten Tutorentscheidungen bilden.

## Uebernommen Aus Dem Review

- Die aktuelle Phase braucht jetzt `Decision Rules`, nicht nur weitere allgemeine Theorie.
- Der Tutor braucht explizite `Response Dimensions` wie Tempo, Schrittgroesse, Notationsdichte und Fehlerbehandlung.
- Support-spezifische Regelwerke sollen zunaechst fuer wenige primaere Profile ausgearbeitet werden.
- Der README-Konflikt zwischen `lokal-first` Vision und aelterem `cloud-LLM` Framing muss offen markiert und schrittweise bereinigt werden.

## Bewusst Angepasst

Einige Teile des Reviews werden fuer MathTeach bewusst in sicherere Projektlogik uebersetzt:

- Keine diagnostischen Prozentwerte im Kernsystem.
- Keine versteckten medizinischen Inferenzmodelle.
- Statt `likelihood`-Diagnostik nutzt MathTeach `support signals` und `selbstbeschriebene Bedarfe`.
- Kontextsignale wie Armut, Angst, schlechte Schulerfahrung oder geringe Unterstuetzung duerfen nur als `paedagogische Anpassungsfaktoren` dienen, nicht als Identitaetsurteil.

## Erste Primaere Profile Fuer Die Matrix

Die erste Ausbaustufe der Matrix fokussiert:

- `ADHD-aware support`
- `dyscalculia-aware support`
- `dyslexia-aware support`
- `autism-spectrum-aware support`
- `ELL / language-sensitive support`
- `scarcity-aware support`

Kombinierte Profile folgen erst nach stabilen Einzelprofilen.

## Erste Response Dimensions

Die erste Matrix-Version arbeitet mit:

- `pacing`
- `step_size`
- `notation_density`
- `text_load`
- `visualization`
- `error_handling`
- `language_support`
- `self_check_rhythm`
- `external_scaffolds`

## Neue Architekturprioritaet

Die aktive Zielarchitektur ist jetzt explizit:

- `lokal-first`
- `geschlossen`
- `rule-based`
- `ohne Cloud-Pflicht`
- `ohne Diagnoseanspruch`

Lokale Modelle bleiben spaeter moeglich, sind aber nicht die Grundbedingung des Systems.

## Konkrete Naechste Deliverables

1. `docs/support-response-matrix-structure.md`
2. `docs/architecture-v2.md`
3. README- und Journal-Ausrichtung auf die aktive lokale Architektur
4. danach erste inhaltliche Matrix fuer `ADHD` und `Dyskalkulie`
5. danach Datenmodell und `response_engine`

## Sprint-Empfehlung

Der naechste saubere Sprint lautet:

- keine neue allgemeine Literaturexpansion
- keine neue grosse Runtime-Funktion
- sondern `Support Response Matrix Structure -> Profile Matrices -> Response Engine`

Damit verschiebt sich MathTeach von:

- `epistemischer Grundlegung`

zu:

- `operationalisierbarer Tutorsteuerung`
