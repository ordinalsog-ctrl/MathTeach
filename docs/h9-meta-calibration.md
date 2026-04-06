# H.9 Meta-Calibration

## Ziel

H.9 erweitert die H.8-Profilschicht um einen ersten
Transfer-Mechanismus zwischen verwandten Profilen.

Die Leitidee:

- H.8 waehlt weiterhin ein exaktes Profil fuer den aktuellen Kontext
- H.7 bleibt der globale Sicherheitsanker
- H.9 fuegt dazwischen jetzt einen begrenzten Meta-Prior aus aehnlichen
  Profilen ein, wenn das exakte Profil noch zu wenig eigene Outcomes
  hat

## Was der erste H.9-Schritt jetzt tut

Die aktuelle Implementierung fuehrt drei neue Verhaltensweisen ein:

1. Profil-Aehnlichkeit

Die Engine bewertet, wie nah zwei Profile beieinanderliegen.
Aktuell beruecksichtigt sie:

- Support-Mix-Ueberlappung
- gleichen Sequenz-Intent
- gleiches dominantes Evidence-Muster
- gleichen Blocktyp

Support-Ueberlappung ist der staerkste Faktor. Profile ohne
Support-Ueberlappung werden nicht als Meta-Transfer-Quelle benutzt.

2. Transfer-aware Fallback

Wenn ein exaktes Profil schon existiert, aber noch duenn ist, wird
nicht nur gegen globale oder breitere Elterngewichte geblendet.
Zusatzlich kann jetzt ein Meta-Prior aus den aehnlichsten
Nachbarprofilen berechnet werden.

Dieser Transfer ist bewusst begrenzt:

- nur vertrauenswuerdige Nachbarprofile mit positiver Konfidenz
- nur die besten wenigen Kandidaten
- gedeckelte Transfer-Staerke

3. Transparenz

Die Runtime macht den neuen H.9-Effekt sichtbar:

- `EnrichedPathEvaluation.meta_transfer_strength`
- `EnrichedPathEvaluation.meta_transfer_source_profiles`
- `EnrichedPathEvaluation.meta_transfer_source_shares`
- `EnrichedPathEvaluation.meta_transfer_weight_delta`
- `EnrichedPathEvaluation.meta_transfer_was_effective`
- `CalibrationContext.meta_transfer_strength`
- `CalibrationContext.meta_transfer_source_profiles`
- `CalibrationContext.meta_transfer_source_shares`
- `CalibrationContext.meta_transfer_weight_delta`
- `CalibrationContext.meta_transfer_was_effective`

Damit ist jetzt zweierlei getrennt sichtbar:

- wie stark ein Meta-Prior ueberhaupt angeboten wurde
- ob dieser Prior die finalen Gewichte tatsaechlich veraendert hat

`meta_transfer_strength` behaelt dabei seine bisherige Semantik als
Blend-Staerke des Meta-Priors. Die neue Metrik
`meta_transfer_weight_delta` misst getrennt davon die tatsaechliche
Veraenderung der finalen Gewichte gegen dieselbe Profilkette ohne
Meta-Transfer.

## Persistente Meta-Historie

Der aktuelle H.9-Stand speichert jetzt nicht mehr nur die laufende
Transferentscheidung, sondern auch deren beobachtete Wirkung.

Pro Zielprofil werden jetzt gespeichert:

- welche Quellprofile bereits als Meta-Transfer genutzt wurden
- mit welchen Anteilen diese Quellprofile am Meta-Prior beteiligt waren
- wie oft dieser Transfer eingesetzt wurde
- welcher durchschnittliche Outcome-Score dabei beobachtet wurde
- wie stark und wie aehnlich der letzte Transfer war

Zusaetzlich wird eine kleine Ereignishistorie gefuehrt:

- welche Quellprofile bei einer konkreten Entscheidung aktiv waren
- mit welchen `source_shares` sie beteiligt waren
- welcher Outcome-Score spaeter beobachtet wurde
- wie hoch die damalige Transferstaerke war
- wie gross die tatsaechliche Gewichtsveraenderung durch den Transfer war

Diese Historie dient zwei Zwecken:

- Debugging und Admin-Inspektion
- leichte Rueckkopplung in die Priorisierung kuenftiger
  Transferkandidaten

Das System nutzt diese Historie schon jetzt vorsichtig als Bonus in der
Ranking-Logik fuer Meta-Transfer-Kandidaten. Erfolgreiche fruehere
Transferpfade koennen dadurch bei ansonsten aehnlicher Kontextnaehe
bevorzugt werden.

Wichtig fuer die neue Attribution:

- Phantom-Transfer wird nicht mehr historisiert. Wenn ein Meta-Prior
  zwar vorhanden ist, aber das exakte Profil die finalen Gewichte
  vollstaendig dominiert, bleibt `meta_transfer_strength` als
  Diagnosesignal sichtbar, aber `meta_transfer_was_effective` ist
  `False` und es wird keine Outcome-Gutschrift auf Transfer-Links
  gebucht.
- Mehrere Quellprofile erhalten Outcome- und
  Transfer-Staerke-Gutschrift jetzt proportional zu ihren
  `source_shares`, statt dass jeder Donor den vollen Outcome-Kredit
  bekommt.

## H.9.1 Monitoring und Admin-Inspektion

Die aktuelle H.9.1-Stufe macht die Meta-Transfer-Oekologie jetzt auch
ueber die API sichtbar.

Neue Admin-Endpunkte:

- `GET /api/v1/admin/calibration/transfer-network`
- `GET /api/v1/admin/calibration/weak-transfers`
- `GET /api/v1/admin/calibration/profile-density`
- `GET /api/v1/admin/calibration/profiles/{profile_id}/transfer-history`
- `GET /api/v1/admin/calibration/profiles/{profile_id}/transfer-candidates`

Diese Endpunkte bauen bewusst nur auf der gehaerteten Attribution auf:

- Transfer-Kanten werden aus effektiven Historieneintraegen aggregiert
- Phantom-Transfer taucht in der historischen Kantenbewertung nicht als
  wirksamer Link auf
- Multi-Source-Transfers werden ueber `source_shares` proportional
  aggregiert
- Donor-Ranking und `top_donors` werden ebenfalls aus effektiver
  `meta_transfer_history` statt aus rohen Alt-Linkaggregaten abgeleitet
- `GET /api/v1/admin/calibration/weak-transfers` filtert seine
  Schwellwerte jetzt gegen den vollstaendigen effektiven Edge-Satz statt
  nur gegen eine schon vorgefilterte Standardliste

Dadurch lassen sich jetzt drei Dinge inspizieren:

- Transfer-Netzwerke zwischen Profilen mit Nutzungszahl,
  durchschnittlichem Outcome und durchschnittlicher Gewichtsdelta
- schwache Transfer-Kanten mit hoher Blend-Staerke, aber geringer
  Outcome-Wirkung
- Profil-Dichte mit duennen oder isolierten Profilen und passenden
  Donor-Kandidaten

## H.9.2 Active Steering

H.9.2 greift jetzt nicht mehr nur beobachtend, sondern aktiv steuernd in
Meta-Transfer-Entscheidungen ein.

### Phase 1: Donor-Auswahl

Die erste Phase greift leicht steuernd in die Donor-Auswahl ein.

Wichtig: Diese Steuerung sitzt bewusst in der `CalibrationEngine`,
konkret in `_meta_transfer_candidates()`, nicht im Planner. Dadurch
bleibt die Meta-Transfer-Auswahl an genau einer Stelle im System
konsistent.

Phase 1 fuehrt zwei Signale ein:

- Weak-edge penalty:
  Donor-Ziel-Kanten, die im H.9.1-Monitoring als schwach erkannt
  wurden, erhalten einen Strafmultiplikator auf ihre aehnlichkeitsnahe
  Kandidatenbewertung.
- Proven-donor boost:
  Donoren mit starker Paar-Historie fuer genau dieses Zielprofil
  erhalten einen positiven Multiplikator und koennen dadurch generische
  Aehnlichkeit ueberholen.

Diese Steering-Signale werden jetzt sichtbar in:

- `EnrichedPathEvaluation.steering_weak_edge_penalty_applied`
- `EnrichedPathEvaluation.steering_proven_donor_boost_applied`
- `EnrichedPathEvaluation.meta_transfer_source_steering_factors`
- `DecisionRecord.steering_weak_edge_penalty_applied`
- `DecisionRecord.steering_proven_donor_boost_applied`
- `DecisionRecord.meta_transfer_source_steering_factors`
- `CalibrationContext.steering_weak_edge_penalty_applied`
- `CalibrationContext.steering_proven_donor_boost_applied`
- `CalibrationContext.meta_transfer_source_steering_factors`

Damit bleibt auditierbar:

- ob eine schwache Kante aktiv abgewertet wurde
- ob ein historisch bewaehrter Donor aktiv hochgestuft wurde
- welche Faktoren fuer jeden verwendeten Donor in die finale
  Kandidatenbewertung eingegangen sind

### Phase 2: Adaptive Blend-Caps

Phase 2 erweitert dieselbe Engine-Schicht jetzt um donor-spezifische
Steuerung der Transfer-Intensitaet.

Wichtig:

- die donor-spezifische Effectiveness-History wird aus effektiver
  `meta_transfer_history` rekonstruiert
- bei Multi-Source-Transfers werden Outcomes ueber `source_shares`
  proportional je Donor zugeschrieben
- `meta_transfer_strength` bleibt semantisch stabil das eine aggregierte
  Blend-Signal fuer den final verwendeten Transfer
- Adaptive Caps beeinflussen also nicht die Bedeutung dieses Feldes,
  sondern dessen Herleitung

Die aktuelle Phase-2-Logik verwendet folgende Buckets:

- `< 3` History-Samples:
  `0.30`, Grund `insufficient_history`
- geringe donor-spezifische Effectiveness `< 0.25`:
  `0.20`, Grund `weak_edge`
- niedrige donor-spezifische Effectiveness `< 0.50`:
  `0.30`, Grund `low_effectiveness`
- mittlere donor-spezifische Effectiveness `< 0.70`:
  `0.35`, Grund `moderate`
- starke donor-spezifische Effectiveness `>= 0.70`:
  `0.45`, Grund `strong_edge`

Diese Signale werden jetzt sichtbar in:

- `EnrichedPathEvaluation.meta_transfer_source_adaptive_caps`
- `DecisionRecord.meta_transfer_source_adaptive_caps`
- `CalibrationContext.meta_transfer_source_adaptive_caps`
- `CalibrationContext.adaptive_cap_distribution`

Wichtig zur Semantik von `CalibrationContext.adaptive_cap_distribution`:

- es ist ein Snapshot des aktuell ausgewaehlten Pfads
- es aggregiert nur die Donor-Caps, die in genau dieser einen
  Planentscheidung aktiv waren
- es ist keine verlaufsweite Statistik ueber alle frueheren Decisions,
  Sessions oder das gesamte Transfer-Netzwerk
- wer historische Verteilungen will, braucht dafuer einen separaten
  Monitoring- oder Admin-Endpunkt

Zusaetzlich enthaelt
`meta_transfer_source_steering_factors` jetzt auch adaptive Cap-Daten,
zum Beispiel:

- `adaptive_transfer_cap`
- `adaptive_transfer_cap_reason`
- `adaptive_transfer_effectiveness_observed`
- `adaptive_transfer_history_samples`
- `applied_source_contribution`

### Phase 3: Steering Observability

Die aktuelle Folgephase fuegt zwei read-only Admin-Endpunkte hinzu, die
H.9.2-Steering operativ sichtbar machen, ohne die Engine-Entscheidungen
selbst zu veraendern.

`GET /api/v1/admin/calibration/steering-log`

- liefert eine per-Decision-Auditsicht auf angewendete Steering-Signale
- zeigt weak-edge penalty, proven-donor boost, adaptive Caps,
  `meta_transfer_source_shares`, `meta_transfer_strength`,
  `meta_transfer_weight_delta` und beobachteten Outcome-Score
- arbeitet historisch auf `DecisionRecord`, nicht auf
  `CalibrationContext`

`GET /api/v1/admin/calibration/adaptive-caps-trends`

- aggregiert adaptive Caps historisch ueber Decisions hinweg
- gruppiert nach `reason`, `profile` oder `effectiveness_bucket`
- trennt damit bewusst echte Verlaufssicht von
  `CalibrationContext.adaptive_cap_distribution`, das nur ein Snapshot
  des aktuell ausgewaehlten Pfads bleibt

Diese Phase ist die Grundlage fuer spaetere, aggressivere
Steering-Folgeschritte, weil jetzt erstmals direkt sichtbar ist, welche
Steering-Signale im Zeitverlauf tatsaechlich auftreten.

### Phase 4: Active Edge-Seeking

Phase 4 nutzt diese Sichtbarkeit jetzt, um fuer sparse oder isolierte
Zielprofile sehr vorsichtige Explorationssignale direkt in der Engine zu
aktivieren.

Wichtig:

- die Logik sitzt weiterhin in `_meta_transfer_candidates()` und nicht
  im Planner
- Edge-Seeking wird nur fuer sparse Zielprofile aktiviert
- proven donors oder bereits moderat/stark belegte Kanten schalten diese
  Exploration aus
- die Exploration ersetzt bestehende Steering-Signale nicht, sondern
  ergaenzt sie kontrolliert

Aktuelle Phase-4-Signale:

- `probe_insufficient_history_for_sparse_target`
  hebt datenarme, aber plausibel aehnliche Kanten vorsichtig an
- `recover_weak_edge_for_sparse_target`
  gibt bereits schwach bewerteten Kanten in echten Isolationslagen einen
  begrenzten Teil ihrer Chance zurueck

Diese Signale werden jetzt sichtbar in:

- `EnrichedPathEvaluation.steering_edge_seeking_applied`
- `DecisionRecord.steering_edge_seeking_applied`
- `CalibrationContext.steering_edge_seeking_applied`
- `meta_transfer_source_steering_factors[*].edge_seeking_applied`
- `meta_transfer_source_steering_factors[*].edge_seeking_multiplier`
- `meta_transfer_source_steering_factors[*].edge_seeking_reason`

Und sie erscheinen ebenfalls im Steering-Log:

- `GET /api/v1/admin/calibration/steering-log`
  kann jetzt auch edge-seeking-getriebene Decisions sichtbar machen
  und entsprechend filtern

### Phase 5: Edge Policy Layer

Phase 5 zieht ueber die vorhandenen Steering-Signale jetzt eine
explizite Policy-Schicht pro Donor-Ziel-Kante.

Wichtig:

- es gibt weiterhin keine zweite Edge-History; die Policy basiert auf
  `_edge_effectiveness_history()`,
  `_transfer_effectiveness_for_pair()` und effektiver
  `meta_transfer_history`
- die Policy ersetzt Weak-edge penalty, proven-donor boost, adaptive
  Caps oder Edge-Seeking nicht, sondern orchestriert sie als klar
  benannte Kantenpolitik
- dadurch wird sichtbarer, ob eine Kante aktuell eher vertrauenswuerdig,
  vorsichtig, probeartig oder bewusst geschuetzt behandelt wird

Aktuelle Policy-Typen:

- `trusted_edge`
  fuer historisch bewaehrte, hinreichend belegte Kanten
- `guarded_edge`
  fuer klar schwache oder aktiv abgewertete Kanten
- `explore_edge`
  fuer sparse Targets mit datenarmen, aber plausiblen Probe-Kanten
- `recovery_edge`
  fuer sparse Targets, bei denen eine schwache Kante kontrolliert erneut
  getestet wird
- `cautious_edge`
  fuer Kanten mit niedriger, aber nicht ganz schwacher beobachteter
  Effectiveness
- `neutral_edge`
  wenn keine zusaetzliche Policy ueber die vorhandenen Basissignale
  hinaus notwendig ist

Diese Policy-Schicht wird jetzt sichtbar in:

- `EnrichedPathEvaluation.steering_edge_policy_applied`
- `EnrichedPathEvaluation.edge_policy_distribution`
- `DecisionRecord.steering_edge_policy_applied`
- `CalibrationContext.steering_edge_policy_applied`
- `CalibrationContext.edge_policy_distribution`
- `meta_transfer_source_steering_factors[*].edge_transfer_policy`
- `meta_transfer_source_steering_factors[*].edge_transfer_policy_reason`
- `meta_transfer_source_steering_factors[*].edge_transfer_policy_multiplier`
- `meta_transfer_source_steering_factors[*].policy_adjusted_candidate_strength`

Und im Steering-Log:

- `GET /api/v1/admin/calibration/steering-log`
  kann jetzt auch nach `include_edge_policy=true` filtern und zeigt pro
  Decision einen `edge_policy_distribution`-Snapshot

### Phase 6: Policy Trends and Profile Families

Phase 6 erweitert die Read-only-Sicht jetzt um historische Policy-Trends
zwischen Profilfamilien.

Wichtig:

- die Profilfamilie wird aktuell bewusst einfach ueber
  `support_profile` abgeleitet
- es wird weiterhin kein zweites Historienmodell eingefuehrt; die
  Trends werden aus `DecisionRecord` und
  `meta_transfer_source_steering_factors` rekonstruiert
- diese Phase fuehrt noch keine live wirksame Familienregel in der
  Engine ein; sie schafft zuerst die Sichtbarkeit, auf der spaetere
  Regeln sicher aufgebaut werden koennen

Neue historische Sicht:

`GET /api/v1/admin/calibration/edge-policy-trends`

- aggregiert Edge-Policies historisch nach:
  `policy`, `source_family`, `target_family` oder `family_pair`
- zeigt pro Aggregat:
  Anzahl, Sample-Groesse, durchschnittlichen Policy-Multiplikator,
  durchschnittliche beobachtete Pair-Effectiveness, Policy-Verteilung
  und Trend-Richtung

Erweiterter Steering-Log:

- `SteeringLogEntry.transfer_target_profile_family`
- `SteeringLogEntry.transfer_source_profile_families`

Damit lassen sich jetzt Fragen beantworten wie:

- welche Policy-Typen dominieren fuer `adhd_aware_support -> adhd_aware_support`
- ob `language_sensitive_support -> adhd_aware_support` eher
  `explore_edge` oder `guarded_edge` produziert
- ob sich der durchschnittliche Policy-Multiplikator bestimmter
  Familienpaare im Zeitverlauf stabilisiert

### Phase 7: Live Family Transfer Policies

Phase 7 nutzt die in Phase 6 sichtbaren Profilfamilien jetzt auch live
in der Engine. Die Family-Logik bleibt absichtlich eine leichte
Orchestrierungsschicht ueber bestehender Edge-History, Edge-Policy und
Adaptive-Cap-Logik.

Wichtig:

- es wird weiterhin kein zweites Family-Store-Modell eingefuehrt
- historische Family-Signale werden aus `DecisionRecord`,
  `meta_transfer_source_steering_factors` und beobachteten Outcomes
  rekonstruiert
- die live wirksame Family-Policy arbeitet damit auf derselben
  Single-Source-of-Truth wie die bisherigen H.9.2-Phasen

Neue live wirksame Family-Policies:

- `trusted_family_pair`
  fuer historisch starke Family-Pairs mit genuegend Samples
- `same_family_preference`
  fuer nicht-schwache Donor-Ziel-Paare innerhalb derselben
  Support-Familie
- `guarded_family_pair`
  fuer historisch schwache Family-Pairs
- `cross_family_probe_guard`
  fuer sparse Cross-family-Probes unter Edge-Seeking
- `neutral_family_policy`
  wenn keine zusaetzliche Family-Regel greift

Diese Signale erscheinen jetzt pro Source in
`meta_transfer_source_steering_factors[*]`:

- `family_transfer_policy`
- `family_transfer_policy_reason`
- `family_transfer_policy_multiplier`
- `source_family`
- `target_family`
- `family_pair_effectiveness`
- `family_pair_samples`
- `family_policy_adjusted_candidate_strength`

Und sie laufen weiter bis in Runtime und Admin-Sicht:

- `EnrichedPathEvaluation.steering_family_policy_applied`
- `CalibrationContext.steering_family_policy_applied`
- `CalibrationContext.family_policy_distribution`
- `DecisionRecord.steering_family_policy_applied`
- `SteeringLogEntry.family_policy_applied`
- `SteeringLogEntry.family_policy_sources`
- `SteeringLogEntry.family_policy_factor`
- `SteeringLogEntry.family_policy_distribution`

Der Steering-Log kann jetzt auch nach Family-Policies gefiltert werden:

- `GET /api/v1/admin/calibration/steering-log?include_family_policy=true`

### Phase 8: Persistent Family Snapshots

Phase 8 haertet die Family-Sicht historisch. Bis einschliesslich Phase 7
konnten Family-Labels bei alten Decisions implizit mitwandern, wenn ein
Profil spaeter anders klassifiziert wurde. Jetzt werden diese Labels
zusaetzlich im `DecisionRecord` gesnapshottet.

Neue persistierte Snapshot-Felder:

- `DecisionRecord.transfer_target_profile_family_snapshot`
- `DecisionRecord.transfer_source_profile_families_snapshot`

Wie sie verwendet werden:

- beim Loggen einer neuen Decision schreibt der Planner die aktuell
  sichtbaren Target-/Source-Familien als Snapshot in den Record
- `SteeringLogQuery` bevorzugt fuer `transfer_target_profile_family`
  und `transfer_source_profile_families` jetzt diese Snapshot-Werte
- `EdgePolicyTrendQuery` bevorzugt fuer `source_family`,
  `target_family` und `family_pair` ebenfalls die Snapshot-Werte
- nur wenn ein aelterer Record diese Felder noch nicht hat, faellt das
  System auf die bisherige Computed-on-Read-Rekonstruktion aus
  `DecisionRecord`, Steering-Faktoren und Profilen zurueck

Damit wird die Family-Semantik zweistufig:

- neue Decisions: historisch stabil ueber persistente Snapshots
- alte Decisions: weiter lesbar durch Fallback, aber semantisch weniger
  stabil

Das verbessert vor allem:

- historische Family-Trends
- spaetere Evaluation von Family-Policies
- Vergleichbarkeit ueber spaetere Profil-Reklassifizierungen hinweg

## Aktuelle Grenzen

Das ist bewusst nur der Start von H.9.

Noch nicht enthalten:

- echtes hierarchisches Bayes-Modell
- lernende Merge/Split-Strategien fuer Profile
- separate Meta-Gewichte pro Dimension
- adaptive Transfer-Raten ueber Zeit
- automatische Folgeaktionen auf Basis dieser Steering-Sicht
- Alt-Daten ohne Family-Snapshot bleiben auf Computed-on-Read-Fallback
  angewiesen, bis eine spaetere Migration sie optional nachzieht

## Naechster logischer Ausbau

Die naechste H.9-Stufe sollte drei Dinge ergaenzen:

- bessere Nachbarschaftslogik fuer Mischprofile und Teilmengen
- staerkere Auswertung der Meta-Historie, welche Policy-Typen fuer
  welche Profilfamilien langfristig wirklich hilfreich sind
- optionale Backfill-/Migrationsstrategie fuer aeltere Decisions ohne
  Family-Snapshot
- feinere Probe-Policies und Informationsgewinn-Heuristiken auf Basis
  des jetzt vorhandenen Edge-Seeking-, Policy- und Steering-Logs
