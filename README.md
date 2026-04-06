# MathTeach

MathTeach ist die Grundlage fuer einen globalen Mathe-Lehrer-Agenten: fachlich tief in Mathematik, historisch praezise, didaktisch anpassungsfaehig und in der Lage, vom Grundschulkind bis zum Professor sinnvoll zu erklaeren.

## Kernprinzip

MathTeach trennt zwei Systeme bewusst voneinander:

- `Knowledge Core`: sachlich, nuechtern, zitierbar, historisch verankert
- `Teacher Mind`: paedagogisch, psychologisch, adaptiv, motivierend

Der Lehrer darf nie die Mathematik "umbiegen". Er darf nur entscheiden, wie dieselbe Mathematik fuer eine bestimmte Person am besten vermittelt wird.

## Produktthese

Die aktive Produktvision ist inzwischen `lokal-first`, `geschlossen` und `rule-based`.

Ein wirklich starker Mathe-Tutor braucht nicht zwingend Cloud-AI. Er braucht:

- einen lokalen Mathematik-Korpus mit Quellen, Herleitungen und Anwendungen,
- einen lokalen `Teacher Mind` mit psychologischer und paedagogischer Grundausbildung,
- eine explizite `Support Response Matrix`, die Lernbedarfe in Tutorentscheidungen uebersetzt,
- eine nachvollziehbare Retrieval- und Planungslogik,
- optional spaeter lokale Modelle oder weitere Intelligenzschichten, aber nicht als Grundbedingung.

## Architekturhinweis

`MathTeach` wird aktuell von einer frueheren cloud- und modellzentrierten Beschreibung
auf eine lokale Zielarchitektur umgestellt.

Aktive Richtung:

- vollstaendig lokal oder lokal-first
- kein Cloud-Zwang
- rule-based Teaching Intelligence als Kern
- lokale Werke, lokale Teacher-Mind-Regeln, lokale Lernerdaten

Fuer die aktive Richtung siehe:

- [JOURNAL.md](/Users/jonasweiss/MathTeach/JOURNAL.md)
- [docs/architecture-v2.md](/Users/jonasweiss/MathTeach/docs/architecture-v2.md)
- [docs/journal-review-triage-2026-04-02.md](/Users/jonasweiss/MathTeach/docs/journal-review-triage-2026-04-02.md)
- [docs/support-response-matrix-structure.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-structure.md)

Legacy- und Explorationsstand:

- fruehere Cloud-LLM-Orientierung
- modellzentrierte Ingestion- und Orchestrierungsempfehlungen
- weiterhin als Projekthistorie nutzbar, aber nicht mehr alleinige Zielrichtung

## Legacy Modell-Stack

Stand der Empfehlung: 2026-04-01, auf Basis offizieller Modelldokumentation.

- `gpt-5.4` als Hauptmodell fuer Tutor-Orchestrierung, Tool-Nutzung und komplexes fachliches Reasoning
- `gpt-5.4-mini` fuer schnelle, guenstigere Nebenaufgaben wie Klassifikation, Session-Routing und Hint-Generierung
- `gemini-2.5-pro` fuer Batch-Ingestion sehr grosser PDFs, Buecher und Dokumentkorpora mit Langkontext
- `claude-opus-4-6` als optionales Zweitmodell fuer harte Gegenpruefung bei schwierigen Forschungs- und Erklaerungsfaellen
- `text-embedding-3-large` fuer semantische Suche ueber mathematische Quellen

Warum diese Aufteilung:

- Ein einzelnes Modell ist fuer dieses Vorhaben zu schwach als alleinige Architektur.
- Lehrgespraeche brauchen andere Latenz-, Kosten- und Tool-Anforderungen als Offline-Korpusaufbau.
- Historische und fachliche Zuverlaessigkeit steigen, wenn Retrieval, Zitationspflicht und Cross-Checks systematisch eingebaut sind.

## Architektur in einem Satz

MathTeach ist ein `geschlossenes lokales Tutor-System aus Knowledge Core + Teacher Mind + Support Response Matrix + Tutor Runtime`.

## Aktueller Stand

MathTeach ist aktuell eine belastbare Tutor-Engine-Basis, noch kein
fertiges Endnutzerprodukt.

Heute bereits im Code:

- lokale, regelbasierte Tutorplanung mit klarer Trennung von
  Fachwissen und Vermittlungslogik
- support-sensitive Moduswahl, Mixed-Profile-Konfliktaufloesung und
  blockweise Runtime-Anpassung innerhalb einer Session
- mehrstufige Pfadplanung von H.3 bis H.5:
  Sequenzrouting, Lookahead-Pfade und Langfristziel-Kopplung
- empirische Kalibrierung von H.6 bis H.8:
  Outcome-Logging, persistente Gewichte ueber Sessions hinweg und
  profilspezifische Kalibrierung nach Support-Mix, Intent, Evidence und
  Blocktyp
- erster H.9-Start:
  datenarme exakte Profile koennen jetzt kontrolliert von aehnlichen,
  staerker gelernten Profilen profitieren; diese Transfers werden jetzt
  auch mit Quellanteilen, echter Gewichtsveraenderung und sauberer
  Outcome-Attribution historisiert
- H.9.1 Monitoring:
  Transfer-Netzwerk, schwache Transfer-Kanten, Profil-Dichte sowie
  profilbezogene Transfer-Historie und Transfer-Kandidaten sind jetzt
  ueber Admin-Endpunkte sichtbar; Donor-Ranking und `top_donors`
  werden dabei aus effektiver Transfer-Historie statt aus rohen
  Linkaggregaten abgeleitet, und `weak-transfers` respektiert seine
  Query-Schwellen jetzt auch wirklich zur Laufzeit
- H.9.2 Active Steering, Phase 1 und 2:
  Die Engine nutzt weak-transfer- und proven-donor-Signale jetzt direkt
  in der Donor-Auswahl, steuert zusaetzlich die Transfer-Intensitaet
  ueber donor-spezifische adaptive Blend-Caps und dokumentiert diese
  Signale bis in `enriched_paths`, `DecisionRecord` und
  `calibration_context`
- H.9.2 Steering Observability, Phase 3:
  read-only Admin-Endpunkte machen Steering-Entscheidungen und
  adaptive Cap-Trends jetzt historisch sichtbar, ohne in die Engine-
  Logik selbst einzugreifen
- H.9.2 Active Edge-Seeking, Phase 4:
  sparse und isolierte Zielprofile koennen jetzt engine-seitig
  vorsichtige Explorations-Boosts fuer datenarme oder zuvor schwache
  Kanten erhalten; diese Signale laufen ebenfalls bis in Audit und
  Observability durch
- H.9.2 Edge Policy Layer, Phase 5:
  die Engine klassifiziert Donor-Ziel-Kanten jetzt zusaetzlich in
  explizite Policy-Typen wie `trusted_edge`, `guarded_edge`,
  `explore_edge`, `recovery_edge` oder `cautious_edge`, nutzt diese
  Policies als leichte Orchestrierungsschicht ueber den bestehenden
  Steering-Signalen und macht ihren Mix jetzt auch in Runtime und
  Steering-Log sichtbar
- H.9.2 Policy Trends and Profile Families, Phase 6:
  der Admin-Layer kann Edge-Policies jetzt historisch nach `policy`,
  `source_family`, `target_family` oder `family_pair` aggregieren; der
  Steering-Log traegt zusaetzlich Source-/Target-Familien pro Decision
  und macht Policy-Muster zwischen Profilfamilien sichtbar
- H.9.2 Live Family Transfer Policies, Phase 7:
  die Engine nutzt die sichtbaren Profilfamilien jetzt auch live bei
  der Donor-Auswahl; sie unterscheidet zwischen
  `trusted_family_pair`, `same_family_preference`,
  `guarded_family_pair` und `cross_family_probe_guard`, schreibt diese
  Regeln pro Source in die Steering-Faktoren und zeigt ihren Mix in
  Runtime und Steering-Log
- H.9.2 Persistent Family Snapshots, Phase 8:
  Family-Labels werden jetzt zusaetzlich im `DecisionRecord`
  gesnapshottet; historische Trends und Steering-Logs bevorzugen diese
  persistierten Werte und fallen nur fuer Alt-Daten ohne Snapshot auf
  die bisherige Computed-on-Read-Rekonstruktion zurueck
- H.9.2 Cross-Family Probe Budgets, Phase 9:
  wiederholte Cross-Family-Probes bekommen jetzt ein kleines Budget pro
  Family-Pair; wenn juengste Probe-Entscheidungen fuer dasselbe Pair
  keinen positiven Outcome geliefert haben, wird weiterer Probe-Boost
  blockiert und als `cross_family_probe_budget_guard` auditierbar
  markiert
- Session-Persistenz, Resume, Checkpoint-Migration, Quarantaene und
  Audit-Pfade fuer defekte Sessions
- eine lauffaehige FastAPI-Schicht fuer Planerstellung, Outcome-Updates
  und Admin-Inspektion

Verifizierter Stand:

- `ruff check --no-cache src tests`
- `pytest -q` -> `239 passed, 1 warning`

Der naechste groessere technische Schritt innerhalb von `H.9` ist jetzt
die naechste Ausbaustufe fuer feinere Informationsgewinn-Steuerung auf
dieser Basis, etwa Family-Pair-spezifische Probe-Priorisierung,
adaptive Budgetgroessen nach beobachtetem Outcome oder staerker
zeitgewichtete Transfer-Raten innerhalb stabil gesnapshotteter
Family-Historien.

## Repository-Inhalt

- [JOURNAL.md](/Users/jonasweiss/MathTeach/JOURNAL.md): Laufender Session- und Projektstand mit Mathematikwerken, Teacher-Mind-Quellen, Runtime-Handoff und naechsten Schritten
- [docs/architecture.md](/Users/jonasweiss/MathTeach/docs/architecture.md): Zielarchitektur und Komponenten
- [docs/architecture-v2.md](/Users/jonasweiss/MathTeach/docs/architecture-v2.md): Aktive lokale Zielarchitektur fuer das geschlossene Tutorsystem
- [docs/journal-review-triage-2026-04-02.md](/Users/jonasweiss/MathTeach/docs/journal-review-triage-2026-04-02.md): Prioritaetskorrektur nach dem Review des aktuellen Journals
- [docs/support-response-matrix-structure.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-structure.md): Erste Struktur fuer Learner-Signale, Response Dimensions und Support-Matrizen
- [docs/support-response-matrix-review-triage-2026-04-02.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-review-triage-2026-04-02.md): Operative Prioritaetskorrektur fuer den Uebergang von Theorie zu Decision Rules
- [docs/support-response-matrix-template.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-template.md): Standardform fuer alle spaeteren Profil-Matrizen
- [docs/support-response-matrix-adhd.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-adhd.md): Erste operative Matrix fuer ADHD-aware support
- [docs/support-response-matrix-dyscalculia.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-dyscalculia.md): Erste operative Matrix fuer dyscalculia-aware support
- [docs/support-response-matrix-dyslexia.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-dyslexia.md): Dritte operative Matrix fuer dyslexia-aware support
- [docs/support-response-matrix-autism.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-autism.md): Vierte operative Matrix fuer autism-spectrum-aware support
- [docs/support-response-matrix-language-sensitive.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-language-sensitive.md): Fuenfte operative Matrix fuer language-sensitive support
- [docs/support-response-matrix-scarcity.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-scarcity.md): Sechste operative Matrix fuer scarcity-aware support
- [docs/profile-conflict-resolution.md](/Users/jonasweiss/MathTeach/docs/profile-conflict-resolution.md): Erste Konfliktaufloesungsarchitektur fuer gemischte Supportprofile
- [docs/mixed-profile-scenarios.md](/Users/jonasweiss/MathTeach/docs/mixed-profile-scenarios.md): Konkrete Mischprofil-Szenarien als Test- und Review-Basis
- [docs/profile-prioritization.md](/Users/jonasweiss/MathTeach/docs/profile-prioritization.md): Erste Priority-Ladder-Logik fuer Triads und spaetere groessere Mischlagen
- [docs/mode-selection-strategy.md](/Users/jonasweiss/MathTeach/docs/mode-selection-strategy.md): Erste Strategie fuer support-sensitive Moduswahl unter Konfliktlagen und Triads
- [docs/mode-selection-review-triage-2026-04-02.md](/Users/jonasweiss/MathTeach/docs/mode-selection-review-triage-2026-04-02.md): Prioritaetskorrektur nach dem Review der neuen `mode_selector`-Schicht
- [docs/live-mode-adaptation-program.md](/Users/jonasweiss/MathTeach/docs/live-mode-adaptation-program.md): Erstes Arbeitsprogramm fuer Phase `H` mit Beobachtungssignalen, Wechselregeln und Hysterese
- [docs/live-mode-adaptation-specification.md](/Users/jonasweiss/MathTeach/docs/live-mode-adaptation-specification.md): Operative Spezifikation fuer Beobachtungssignale, `runtime_mode_adapter`, Hysterese und Transition-Messaging
- [docs/live-mode-adaptation-readiness-review-2026-04-02.md](/Users/jonasweiss/MathTeach/docs/live-mode-adaptation-readiness-review-2026-04-02.md): Readiness-Triage fuer den Uebergang von Phase-H-Spezifikation zu erster Runtime-Implementierung
- [docs/live-mode-adaptation-final-assessment-2026-04-02.md](/Users/jonasweiss/MathTeach/docs/live-mode-adaptation-final-assessment-2026-04-02.md): Abschlussbewertung, dass Phase `H.1` jetzt startbereit fuer die erste Runtime-Implementierung ist
- [docs/live-mode-adaptation-h1-code-review-2026-04-02.md](/Users/jonasweiss/MathTeach/docs/live-mode-adaptation-h1-code-review-2026-04-02.md): Review-Triage nach dem ersten H.1-Codecheckpoint mit Fokus auf den naechsten Block-Loop im Planner
- [docs/live-mode-adaptation-persistence-review-2026-04-02.md](/Users/jonasweiss/MathTeach/docs/live-mode-adaptation-persistence-review-2026-04-02.md): Review-Triage, die den Engpass von Runtime-Logik auf Persistenz und Resume-Semantik verschiebt
- [docs/mode-adaptation-checkpoint-contract.md](/Users/jonasweiss/MathTeach/docs/mode-adaptation-checkpoint-contract.md): Versionierter API- und Persistenzvertrag fuer `mode_adaptation_checkpoint`
- [docs/session-storage-architecture.md](/Users/jonasweiss/MathTeach/docs/session-storage-architecture.md): Anschlussarchitektur fuer `session_id`, `SessionStore` und spaeter `SessionManager`
- [docs/session-validation-and-migration.md](/Users/jonasweiss/MathTeach/docs/session-validation-and-migration.md): Erste Validierungs- und Fehlersemantik fuer unbekannte, ungueltige und migrationsbeduerftige Sessions
- [docs/checkpoint-migrator.md](/Users/jonasweiss/MathTeach/docs/checkpoint-migrator.md): Erste echte Migrationslogik fuer bekannte Alt-Checkpoints
- [docs/session-quarantine-and-audit.md](/Users/jonasweiss/MathTeach/docs/session-quarantine-and-audit.md): Erste Betriebs-Haertung fuer defekte Sessions und Audit-Trail
- [docs/support-response-matrix-implementation-plan.md](/Users/jonasweiss/MathTeach/docs/support-response-matrix-implementation-plan.md): Sprint- und Implementierungsplan fuer Response Engine und Planner-Integration
- [docs/mode-evidence-coupling.md](/Users/jonasweiss/MathTeach/docs/mode-evidence-coupling.md): H.2f-Ausbau fuer modus-sensible Pair-/Triad-Regeln
- [docs/blocktype-evidence-coupling.md](/Users/jonasweiss/MathTeach/docs/blocktype-evidence-coupling.md): H.2g-Ausbau fuer blocktyp- und evidence-kombinationssensible Blockauflosung
- [docs/block-sequence-planning.md](/Users/jonasweiss/MathTeach/docs/block-sequence-planning.md): H.3-Ausbau fuer adaptive Wahl des naechsten Blocktyps
- [docs/lookahead-path-planning.md](/Users/jonasweiss/MathTeach/docs/lookahead-path-planning.md): H.4-Ausbau fuer bewertete Lookahead-Pfade statt nur einer direkten Naechstblock-Wahl
- [docs/long-term-integration.md](/Users/jonasweiss/MathTeach/docs/long-term-integration.md): H.5-Ausbau fuer Lernziele, Session-Historie und pilotdatengestuetzte Pfadbewertung
- [docs/h6-calibration.md](/Users/jonasweiss/MathTeach/docs/h6-calibration.md): H.6-Ausbau fuer Entscheidungs-Logging, Outcome-Updates und empirische Gewichtsanpassung
- [docs/h7-persistent-calibration.md](/Users/jonasweiss/MathTeach/docs/h7-persistent-calibration.md): H.7-Ausbau fuer persistente Kalibrierung ueber Sessions und Prozessstarts hinweg
- [docs/h8-profile-calibration.md](/Users/jonasweiss/MathTeach/docs/h8-profile-calibration.md): H.8-Ausbau fuer profilspezifische und kontextsensitive Gewichtsanpassung
- [docs/h9-meta-calibration.md](/Users/jonasweiss/MathTeach/docs/h9-meta-calibration.md): H.9-Start fuer Transfer zwischen verwandten Kalibrierungsprofilen
- [docs/math-corpus-blueprint.md](/Users/jonasweiss/MathTeach/docs/math-corpus-blueprint.md): Startplan fuer die mathematische Quellensammlung
- [docs/math-history-program.md](/Users/jonasweiss/MathTeach/docs/math-history-program.md): Chronologisches Sammelprogramm fuer die erste Mathegeschichte
- [docs/modern-math-baseline-audit-2026-04-01.md](/Users/jonasweiss/MathTeach/docs/modern-math-baseline-audit-2026-04-01.md): Startaudit fuer die neue Epoche Moderne Mathematik
- [docs/modern-math-review-triage-2026-04-01.md](/Users/jonasweiss/MathTeach/docs/modern-math-review-triage-2026-04-01.md): Priorisierung nach dem ersten externen Review der modernen Epoche
- [docs/modern-math-post-round-m1-audit-2026-04-01.md](/Users/jonasweiss/MathTeach/docs/modern-math-post-round-m1-audit-2026-04-01.md): Folgeaudit nach Runde M.1 der modernen Epoche
- [docs/modern-math-second-review-triage-2026-04-01.md](/Users/jonasweiss/MathTeach/docs/modern-math-second-review-triage-2026-04-01.md): Priorisierung nach dem zweiten externen Review der modernen Epoche
- [docs/modern-math-post-round-m2-audit-2026-04-01.md](/Users/jonasweiss/MathTeach/docs/modern-math-post-round-m2-audit-2026-04-01.md): Folgeaudit nach Runde M.2 der modernen Epoche
- [docs/modern-math-third-review-triage-2026-04-01.md](/Users/jonasweiss/MathTeach/docs/modern-math-third-review-triage-2026-04-01.md): Prioritaetskorrektur nach dem Review von Runde M.2
- [docs/modern-math-post-round-m3-audit-2026-04-01.md](/Users/jonasweiss/MathTeach/docs/modern-math-post-round-m3-audit-2026-04-01.md): Folgeaudit nach Runde M.3 der modernen Epoche
- [docs/modern-math-final-assessment-2026-04-01.md](/Users/jonasweiss/MathTeach/docs/modern-math-final-assessment-2026-04-01.md): Abschlussbewertung der modernen Epoche innerhalb des definierten Kanons
- [docs/full-corpus-final-assessment-2026-04-01.md](/Users/jonasweiss/MathTeach/docs/full-corpus-final-assessment-2026-04-01.md): Abschlussbewertung des historischen Gesamtkorpus vor der Vernetzungsphase
- [docs/cross-epoch-networking.md](/Users/jonasweiss/MathTeach/docs/cross-epoch-networking.md): Erste Architektur fuer Proof Lines, Equation Lines und Transmission Paths ueber alle Epochen
- [docs/literature-gap-audit-2026-04-01.md](/Users/jonasweiss/MathTeach/docs/literature-gap-audit-2026-04-01.md): Vergleich unseres Stands mit kanonischer Literatur fuer Antike bis Fruehe Neuzeit
- [docs/literature-gap-audit-2026-04-01-post-round-a.md](/Users/jonasweiss/MathTeach/docs/literature-gap-audit-2026-04-01-post-round-a.md): Folgeaudit nach der ersten Brueckenwerk-Runde
- [docs/literature-gap-audit-2026-04-01-post-round-b.md](/Users/jonasweiss/MathTeach/docs/literature-gap-audit-2026-04-01-post-round-b.md): Folgeaudit nach Runde B
- [docs/literature-gap-audit-2026-04-01-post-round-c.md](/Users/jonasweiss/MathTeach/docs/literature-gap-audit-2026-04-01-post-round-c.md): Folgeaudit nach Runde C
- [docs/literature-gap-audit-2026-04-01-post-round-c1.md](/Users/jonasweiss/MathTeach/docs/literature-gap-audit-2026-04-01-post-round-c1.md): Folgeaudit nach Runde C.1
- [docs/external-feedback-triage-2026-04-01.md](/Users/jonasweiss/MathTeach/docs/external-feedback-triage-2026-04-01.md): Einordnung externer LLM-Rueckmeldungen in kommende Runden
- [docs/external-feedback-triage-2026-04-01-second-assessment.md](/Users/jonasweiss/MathTeach/docs/external-feedback-triage-2026-04-01-second-assessment.md): Prioritaetskorrektur nach der zweiten externen Bewertung
- [docs/curation-loop.md](/Users/jonasweiss/MathTeach/docs/curation-loop.md): Fester Arbeitszyklus aus Audit, Werk-Ergaenzung und Folgeaudit
- [docs/source-access-program.md](/Users/jonasweiss/MathTeach/docs/source-access-program.md): Wie historische Quellen gelesen, beschafft und lokal abgelegt werden
- [docs/data-foundation.md](/Users/jonasweiss/MathTeach/docs/data-foundation.md): Trennung von Knowledge Core und Teacher Mind
- [docs/knowledge-system.md](/Users/jonasweiss/MathTeach/docs/knowledge-system.md): Mathematik-Korpus, Graphmodell und Retrieval
- [docs/teacher-mind-blueprint.md](/Users/jonasweiss/MathTeach/docs/teacher-mind-blueprint.md): Grundmodell der paedagogischen und psychologischen Lehrerschicht
- [docs/teacher-mind-charter.md](/Users/jonasweiss/MathTeach/docs/teacher-mind-charter.md): Verbindliche Regeln fuer selbstbeschriebene Lernbedarfe, lokale Speicherung und Nicht-Therapie-Rolle
- [docs/teacher-mind-foundation-stack.md](/Users/jonasweiss/MathTeach/docs/teacher-mind-foundation-stack.md): Reihenfolge des Tutor-Aufbaus: erst psychologische und paedagogische Grundlagen, dann Support- und Accessibility-Schichten
- [docs/teacher-mind-foundations-review-triage-2026-04-01.md](/Users/jonasweiss/MathTeach/docs/teacher-mind-foundations-review-triage-2026-04-01.md): Prioritaetskorrektur nach dem ersten umfassenden Review der psychologisch-paedagogischen Grundausbildung
- [docs/universal-tutor-system-review-triage-2026-04-01.md](/Users/jonasweiss/MathTeach/docs/universal-tutor-system-review-triage-2026-04-01.md): Prioritaetskorrektur fuer Universalitaet, Inklusion, Neurodiversitaet, Equity und lokale Systemarchitektur
- [docs/universal-round-u1-program.md](/Users/jonasweiss/MathTeach/docs/universal-round-u1-program.md): Erste universelle Designrunde fuer Motivation, Belonging, Errors, Equity/Scarcity und UDL
- [docs/universal-round-u2-program.md](/Users/jonasweiss/MathTeach/docs/universal-round-u2-program.md): Zweite universelle Designrunde fuer Transfer, situiertes Lernen, Zusammenarbeit, ZPD und Adult Learning
- [docs/universal-round-u3-program.md](/Users/jonasweiss/MathTeach/docs/universal-round-u3-program.md): Dritte universelle Designrunde fuer neurodiversitaetsbewusste Kernarchitektur, trauma-informed safety, Lifespan-Sequencing und Guardrails
- [docs/universal-round-u4-program.md](/Users/jonasweiss/MathTeach/docs/universal-round-u4-program.md): Erste support-spezifische Runde fuer ADHD, Dyskalkulie, Dyslexie, Autismusspektrum und sprachsensible Unterstuetzung
- [docs/psychological-foundations-program.md](/Users/jonasweiss/MathTeach/docs/psychological-foundations-program.md): Erster Teacher-Mind-Korpus fuer Lernen, Gedaechtnis, Abruf, Motivation und Anti-Myth-Guardrails
- [docs/pedagogical-foundations-program.md](/Users/jonasweiss/MathTeach/docs/pedagogical-foundations-program.md): Allgemeine Tutor-Grundausbildung fuer Erklaeraufbau, Scaffolding, Worked Examples, Feedback und Lernprogression
- [docs/learner-support-profiles.md](/Users/jonasweiss/MathTeach/docs/learner-support-profiles.md): Erste nicht-diagnostische Support-Profile fuer Lernbarrieren und Unterstuetzungsbedarfe
- [docs/pedagogical-strategy-matrix.md](/Users/jonasweiss/MathTeach/docs/pedagogical-strategy-matrix.md): Uebersetzung von Profilmix in Unterrichtsmodus, Tempo, Schrittgroesse und Interventionsstil
- [docs/teacher-mind-evidence-program.md](/Users/jonasweiss/MathTeach/docs/teacher-mind-evidence-program.md): Lokales Evidenzprogramm fuer serioese Leitquellen, Practice Guides und spaetere Einzelstudien des Teacher Mind
- [docs/closed-local-tutor-system-blueprint.md](/Users/jonasweiss/MathTeach/docs/closed-local-tutor-system-blueprint.md): Zielbild eines geschlossenen lokalen Tutorsystems als App oder eigenes Geraet
- [docs/roadmap.md](/Users/jonasweiss/MathTeach/docs/roadmap.md): MVP- und Ausbauphasen
- [data/math_core/foundation_manifest.json](/Users/jonasweiss/MathTeach/data/math_core/foundation_manifest.json): Erstes Sammelmanifest fuer mathematische Quellen
- [data/math_core/chronology_manifest.json](/Users/jonasweiss/MathTeach/data/math_core/chronology_manifest.json): Historischer Startkatalog fuer Antike bis Moderne Mathematik
- [data/math_core/source_access_manifest.json](/Users/jonasweiss/MathTeach/data/math_core/source_access_manifest.json): Register mit Werken, Zugriffspfaden und Ablagehinweisen
- [data/math_core/network_manifest.json](/Users/jonasweiss/MathTeach/data/math_core/network_manifest.json): Erstes Netzwerkmanifest fuer Proof Lines, Equation Lines, Transmission Paths und Domain Lines
- [data/teacher_mind/evidence_manifest.json](/Users/jonasweiss/MathTeach/data/teacher_mind/evidence_manifest.json): Startmanifest fuer die lokale Teacher-Mind-Evidenzbasis
- [data/teacher_mind/psychological_foundations_manifest.json](/Users/jonasweiss/MathTeach/data/teacher_mind/psychological_foundations_manifest.json): Startmanifest fuer die erste psychologische Grundausbildung des Tutors
- [data/teacher_mind/pedagogical_foundations_manifest.json](/Users/jonasweiss/MathTeach/data/teacher_mind/pedagogical_foundations_manifest.json): Startmanifest fuer die allgemeine paedagogische Grundausbildung des Tutors
- [data/teacher_mind/universal_round_u1_manifest.json](/Users/jonasweiss/MathTeach/data/teacher_mind/universal_round_u1_manifest.json): Startmanifest fuer die erste universelle Designrunde des Tutors
- [data/teacher_mind/universal_round_u2_manifest.json](/Users/jonasweiss/MathTeach/data/teacher_mind/universal_round_u2_manifest.json): Startmanifest fuer die zweite universelle Designrunde des Tutors
- [data/teacher_mind/universal_round_u3_manifest.json](/Users/jonasweiss/MathTeach/data/teacher_mind/universal_round_u3_manifest.json): Startmanifest fuer die dritte universelle Designrunde des Tutors
- [data/teacher_mind/universal_round_u4_manifest.json](/Users/jonasweiss/MathTeach/data/teacher_mind/universal_round_u4_manifest.json): Startmanifest fuer die erste support-spezifische Runde des Tutors
- [sql/001_foundation_schema.sql](/Users/jonasweiss/MathTeach/sql/001_foundation_schema.sql): Erstes Postgres-Schema fuer die Datenbasis
- [sql/002_math_corpus_collection.sql](/Users/jonasweiss/MathTeach/sql/002_math_corpus_collection.sql): Quellenkatalog, Collection-Queue und Ingestion-Tabellen
- [sql/003_math_history_program.sql](/Users/jonasweiss/MathTeach/sql/003_math_history_program.sql): Epochen, Werke und Story-Tabellen fuer Beweise und Gleichungen
- [sql/004_source_access_registry.sql](/Users/jonasweiss/MathTeach/sql/004_source_access_registry.sql): Zugriffsrouten und lokales Speicher-Audit fuer Quellen
- [sql/005_cross_epoch_network.sql](/Users/jonasweiss/MathTeach/sql/005_cross_epoch_network.sql): Generisches Schema fuer epochenuebergreifende Linien und Anker
- [src/mathteach/main.py](/Users/jonasweiss/MathTeach/src/mathteach/main.py): FastAPI-Startpunkt
- [src/mathteach/response_matrix.py](/Users/jonasweiss/MathTeach/src/mathteach/response_matrix.py): Eigenes Modellmodul fuer Support-Signale und Tutor-Response-Settings
- [src/mathteach/services/corpus.py](/Users/jonasweiss/MathTeach/src/mathteach/services/corpus.py): Blueprint-Service fuer die Mathe-Datenbank
- [src/mathteach/services/foundation.py](/Users/jonasweiss/MathTeach/src/mathteach/services/foundation.py): Datenfundament fuer Wissenskern und Lehrerfigur
- [src/mathteach/services/planner.py](/Users/jonasweiss/MathTeach/src/mathteach/services/planner.py): Planungslogik fuer Tutor-Sessions mit blockweiser Runtime-Adaption und sichtbaren Support-Moves je Block
- [src/mathteach/services/response_engine.py](/Users/jonasweiss/MathTeach/src/mathteach/services/response_engine.py): Regelbasierte Ableitung von Support-Signalen zu Tutor-Response-Settings fuer Einzel- und Mischprofile
- [src/mathteach/services/runtime_mode_adapter.py](/Users/jonasweiss/MathTeach/src/mathteach/services/runtime_mode_adapter.py): Erste H.1-Runtime-Komponente fuer blockweise Modusanpassung mit `SignalInterpreter`, Hysterese und Transition-Templates
- [src/mathteach/services/session_store.py](/Users/jonasweiss/MathTeach/src/mathteach/services/session_store.py): Erste file-backed Persistenz-Huelle fuer `session_id`-Resume und `mode_adaptation_checkpoint`
- [src/mathteach/services/session_manager.py](/Users/jonasweiss/MathTeach/src/mathteach/services/session_manager.py): Koordinationsschicht fuer `session_id`, Resume-Konflikte und schlankeren API-Glue-Code
- [src/mathteach/services/checkpoint_validation.py](/Users/jonasweiss/MathTeach/src/mathteach/services/checkpoint_validation.py): H.1-Validierungs- und Versionslogik fuer `mode_adaptation_checkpoint`
- [src/mathteach/services/checkpoint_migrator.py](/Users/jonasweiss/MathTeach/src/mathteach/services/checkpoint_migrator.py): Automatische Einzelschritt- und Mehrschritt-Migration fuer bekannte Legacy-Checkpoints bis `phase_h1_v1`
- [src/mathteach/services/session_quarantine.py](/Users/jonasweiss/MathTeach/src/mathteach/services/session_quarantine.py): Erste Quarantaene-Huelle fuer defekte Session-Dateien
- [src/mathteach/services/session_audit.py](/Users/jonasweiss/MathTeach/src/mathteach/services/session_audit.py): JSONL-Audit-Trail fuer Migrationen und Resume-Fehler

## Schnellstart

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn mathteach.main:app --reload
```

Danach:

- `GET /health`
- `GET /api/v1/stack`
- `GET /api/v1/foundation`
- `GET /api/v1/corpus/blueprint`
- `GET /api/v1/corpus/chronology`
- `GET /api/v1/corpus/source-access`
- `GET /api/v1/corpus/network`
- `POST /api/v1/tutoring/plan`
- `GET /api/v1/admin/quarantine/sessions`
- `GET /api/v1/admin/quarantine/{session_id}`
- `POST /api/v1/admin/quarantine/{session_id}/restore`
- `POST /api/v1/admin/quarantine/{session_id}/discard`

## Naechste Produktstufe

Die aktuelle Repo-Version ist bewusst die erste belastbare Basis:

- Produkt- und Systemrichtung sind festgelegt.
- Das Modell- und Datenkonzept ist dokumentiert.
- Das Datenfundament ist jetzt explizit zweigeteilt in fachlichen Wissenskern und paedagogische Lehrerfigur.
- Die mathematische Datensammlung hat jetzt ein erstes Manifest mit Prioritaeten, Quellenfamilien und Collection-Queue.
- Die erste historische Sammelschicht ordnet Mathematik nach Epochen, Werken, Beweisen und Gleichungsgeschichten.
- Die Chronologie reicht jetzt als erste belastbare Linie von der Antike bis in die Moderne.
- Das erste Quellenregister sagt jetzt auch, wo historische Werke heute gelesen werden koennen und wie Rohdateien lokal abgelegt werden sollen.
- Die epochenuebergreifende Vernetzung hat jetzt ein erstes Manifest mit Proof Lines, Equation Lines, Transmission Paths, Domain Lines und Application Bridges.
- Eine kleine API zeigt schon, wie Wissens- und Lehrlogik getrennt orchestriert werden.

Die support-sensitive Moduswahl im Planner ist jetzt als eigene Schicht eingefuehrt.

Die `planner-level live mode adaptation` ist jetzt im ersten H.1-MVP als
Block-Loop, Resume-Pfad und Mehrblock-Beobachtungsfenster real im Code
angekommen.

Die aktuellen Reviews bestaetigen dabei ausdruecklich:

- `mode_selector` als richtige neue Zwischenschicht
- `requested_mode` versus `selected_mode` als tragende Trennung
- `live mode adaptation` als naechste echte Architekturphase
- `block-level adaptation` als sichere erste H-Version
- `runtime_mode_adapter` als neue geplante H-Komponente
- Phase `H` ist jetzt auch operativ geschaerft mit Schwellen, Block-Takt,
  Entscheidungs-Matrix und Template-Logik fuer Uebergaenge
- `Phase H` ist jetzt auch auf API- und MVP-Ebene weiter geschaerft:
  mit `SignalInterpreter`, Planner-Flow und Startkalibrierung fuer `H.1`
- `Phase H.1` ist nicht mehr nur `implementation-ready`, sondern bereits
  als erste Runtime-Stufe umgesetzt
- die H.1-Codeartefakte tragen jetzt auch Resume-Pfade,
  Transition-Konsumierung und Mehrblock-Signalverdichtung
- `SessionStore` und `SessionManager` sind jetzt als erste Persistenz- und
  Koordinationsschicht operational
- eine erste Validierungs- und Migrationskante fuer Sessions ist jetzt
  ebenfalls operational, inklusive `400/410/422`-Semantik im API-Pfad
- ein erster echter `checkpoint_migrator` ist jetzt ebenfalls operational
  und hebt bekannte Alt-Checkpoints jetzt auch ueber mehrere bekannte
  Zwischenstufen automatisch auf den H.1-Stand
- defekte oder nicht migrierbare Sessions werden jetzt ausserdem
  quarantainiert und auditiert, statt im aktiven Resume-Pfad zu bleiben
- erste Admin-/Repair-Pfade fuer quarantainierte Sessions sind jetzt
  ebenfalls live, inklusive `list`, `inspect`, `restore` und `discard`
- derselbe `session_id`-Wert startet nach Quarantaene jetzt auch explizit
  wieder sauber neu, wenn kein aktiver Checkpoint mehr vorhanden ist
- die Support Response Matrix wirkt jetzt nicht mehr nur global ueber
  `response_settings`, sondern sichtbar ueber `support_moves` und
  `support_scaffolds` in jedem `planned_block`
- diese Blockausgabe reagiert jetzt auch auf Modus und Runtime-Evidenz,
  also z.B. anders bei Verwirrung, Textueberlastung, Stagnation oder
  sichtbarem Erfolg
- Resume-Previews koennen dabei jetzt auch ohne neue Runtime-Inputs an
  `last_observation_evidence` anknuepfen, statt mit leerer Evidenz neu
  anzusetzen
- der API-Output macht diese Resume-Semantik jetzt auch explizit ueber
  `resume_context` sichtbar, inklusive `resume_source`,
  `carried_observation_evidence` und konsumierter
  `pending_transition_message`
- partielle H.1-Checkpoints mit fehlenden Optionalfeldern bleiben dabei
  resume-faehig, weil fehlende Felder kontrolliert auf Defaults
  zurueckfallen
- die Signalpalette ist jetzt ausserdem um erste H.2c-Typen erweitert,
  darunter `rapid_success_three_blocks`, `vocabulary_request_again`,
  `error_recovery_with_hint` und `mixed_success_inconsistent`
- Mischprofile bekommen jetzt auf Blockebene ausserdem eine sichtbare
  `conflict_resolution_summary`, statt konkurrierende `support_moves`
  nur roh nebeneinander zu sehen
- diese Block-Zusammenfassung traegt jetzt auch `generated_moves` und
  `move_dependencies_applied`, sodass Triad-/Pair-Aufloesung nicht nur
  sortierte, sondern auch explizit neu kombinierte Moves sichtbar macht
- bekannte Mehrprofil-Konstellationen koennen dadurch jetzt Moves
  semantisch umformen, z.B. zu
  `reframe_concept_with_simple_language_and_quantity_support` oder
  `use_predictable_visual_reading_sequence`
- H.2f koppelt diese Mehrprofil-Regeln jetzt zusaetzlich an
  `lesson_mode`, sodass dieselbe Triad in
  `worked_example_tutoring`, `origin_story_explanation` und
  `guided_concept_explanation` unterschiedliche angepasste Moves
  liefern kann
- H.2g koppelt dieselben Regeln jetzt zusaetzlich an explizite
  `block_type`-Heuristiken und verdichtete
  `evidence_combination.patterns`, sodass z.B. ein
  `worked_example`-Block mit `rapid_consecutive_success` andere
  Support-Moves traegt als ein `error_recovery`-Block mit
  `stagnation_pattern`
- H.3 nutzt diese Blocksignale jetzt fuer echte Sequenzplanung:
  jeder `planned_block` traegt jetzt sichtbar den empfohlenen
  `next_block_type`, Alternativen und einen `sequence_intent`, und der
  finale Preview-Block uebernimmt die letzte Routing-Entscheidung
- H.4 bewertet jetzt zusaetzlich mehrere kurze Sequenzpfade und macht
  deren Scores sichtbar, sodass die gewaehlte Blockroute nicht nur
  lokal, sondern auch im nahen Verlauf begruendet werden kann
- H.5 bewertet diese Pfade jetzt zusaetzlich gegen Langfristlernziele
  und den bisherigen Sitzungsverlauf, sodass das System sichtbarer
  zwischen kurzfristig passenden und langfristig sinnvolleren Pfaden
  unterscheiden kann
- H.6 loggt diese Pfadentscheidungen jetzt zusaetzlich, verknuepft sie
  mit spaeteren Outcome-Beobachtungen und kann die sichtbare
  Preview-Empfehlung damit gegen erste empirische Rueckmeldungen
  nachjustieren
- H.7 macht diese Kalibrierung jetzt dauerhaft:
  Entscheidungslogs, Outcomes und Gewichts-Historie koennen ueber
  persistente Stores erhalten bleiben und ueber API-Endpunkte inspiziert
  werden
- H.8 nutzt diese persistenten Kalibrierungsdaten jetzt
  profilspezifisch: `TeachingPlan` und `enriched_paths` zeigen, welches
  Kalibrierungsprofil gerade aktiv war und mit welcher Konfidenz es
  gegen das globale Gewichtungsset gemischt wurde
- der naechste Engpass ist jetzt nicht mehr Phase-A-Dokumentation,
  sondern Meta-Kalibrierung ueber verwandte Profile hinweg,
  spaetere
  runtime-sensitive Response-Anpassung und danach punktuelle
  Rollen-/Monitoring-Haertung fuer Admin-Pfade

Die ersten direkten Arbeitsdokumente dafuer sind bereits:

- `ADHD-aware support`
- `dyscalculia-aware support`
- `dyslexia-aware support`
- `autism-spectrum-aware support`
- `language-sensitive support`
- `scarcity-aware support`
- der erste `Implementation Plan` fuer Code-Skeleton, Planner-Integration und spaetere Validierung
- das erste `Live Mode Adaptation Program` fuer Phase `H`
- die erste `Live Mode Adaptation Specification` fuer die operative H-Umsetzung

Im Code existiert dazu jetzt bereits ein erster `response_engine`, der
`support signal profile` und `response settings` in die Tutoring-Planung
einspeist. Dazu kommt jetzt auch ein eigenes Modellmodul `response_matrix.py`
sowie operative Codepfade fuer `dyslexia-aware support`,
`autism-spectrum-aware support`, `language-sensitive support`
und `scarcity-aware support`.

Neu dazu kommt jetzt der erste H.1-Runtime-Kern:

- `SignalInterpreter` fuer support-sensitive Blocksignale
- `runtime_mode_adapter` fuer blockweises `stay` oder `shift`
- erste Hysterese- und Transition-Logik
- initialer `mode_adaptation_state` direkt im `TeachingPlan`
- versionierter `mode_adaptation_checkpoint` als externe Resume- und Persistenzform
- `SessionStore` als erste file-backed Storage-Huelle fuer Checkpoints
- erster Planner-Block-Loop mit `planned_blocks` und `mode_adaptation_trace`
- erste Session-Fortsetzung ueber wiederverwendeten `mode_adaptation_state`
- erste Session-Fortsetzung ueber versionierten `mode_adaptation_checkpoint`
- erste Session-Fortsetzung ueber `session_id` und gespeicherten Checkpoint
- Persistenz offener `transition_message` ueber Resume-Pfade
- Konsumierung angezeigter `transition_message` ohne doppelte Wiederholung
- resume-faehige `last_observation_evidence` fuer echte Beobachtungsfenster
- expliziter `resume_context` im `TeachingPlan` fuer sichtbare
  Resume-Herkunft und Evidenz-Nutzung
- dokumentierte Resume-Semantik in
  [resume-semantics.md](/Users/jonasweiss/MathTeach/docs/resume-semantics.md)
- automatische Ableitung von Mehrblock-Signalen wie
  `transfer_success_two_blocks` und `no_progress_three_blocks`
- erste H.2c-Signale fuer stabile Erfolge, wiederholte Vokabularlast,
  Hint-Erholung und inkonsistente Erfolgswechsel
- blockweise Konfliktaufloesung fuer Paar- und erste Triad-Konstellationen
  mit sichtbarer `priority_ladder`
- automatische Ableitung von `visible_small_success` und
  `no_success_visible_two_blocks` fuer realistischere Erfolgs- und
  Friktionslinien

Darauf aufbauend existiert jetzt auch eine erste `conflict_resolver`-Schicht,
die gemischte Supportprofile explizit prueft und konfliktbehaftete Profilpaare
mit nachvollziehbaren Regeln aufloest.

Darauf aufbauend existieren jetzt auch erste `triad_groups` und
`priority_ladders`, die fuer mehrfache konkurrierende Supportlagen eine
explizite Reihenfolge sichtbar machen.

Die naechste Ausbauphase ist damit:

- `SessionManager` als Koordinationsschicht ueber `SessionStore` vorbereiten
- Storage-Semantik fuer unbekannte, alte oder spaetere Checkpoint-Versionen haerten
- Resume- und Serialisierungsgrenzen fuer den neuen Checkpoint weiter haerten
- spaeter weitere reale Signalszenarien verbreitern und kalibrieren
- `triad coverage erweitern`
- `broader mixed-profile prioritization`
- spaetere Pilotierung mit echten Mischprofil-Szenarien
