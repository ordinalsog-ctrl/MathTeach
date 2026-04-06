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

## Aktuelle Grenzen

Das ist bewusst nur der Start von H.9.

Noch nicht enthalten:

- echtes hierarchisches Bayes-Modell
- lernende Merge/Split-Strategien fuer Profile
- separate Meta-Gewichte pro Dimension
- adaptive Transfer-Raten ueber Zeit
- eigener Admin- oder Steering-Log-Endpunkt fuer Phase-2-Signale

## Naechster logischer Ausbau

Die naechste H.9-Stufe sollte drei Dinge ergaenzen:

- bessere Nachbarschaftslogik fuer Mischprofile und Teilmengen
- staerkere Auswertung der Meta-Historie, welche Transferquellen fuer
  welches Profil langfristig wirklich hilfreich sind
- explizite Inspection- und Trend-Endpunkte fuer Steering-Signale und
  adaptive Cap-Verteilungen
