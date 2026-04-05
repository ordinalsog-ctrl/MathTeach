# H.8 Profile-Aware Calibration

Stand: 2026-04-05

## Ziel

H.8 erweitert die persistente H.7-Kalibrierung um eine kontextsensitive
Profilschicht. Pfade werden jetzt nicht mehr nur gegen ein globales
Gewichtungsprofil nachjustiert, sondern koennen auf Support-Mix,
Sequenz-Intent, dominante Evidence und aktuellen Blocktyp reagieren.

## Neue Bausteine

- `CalibrationProfile`
  - haelt Stratifikationsdimensionen, Profilgewichte, Stichprobengroesse
    und eigene Gewichts-Historie
- erweiterte `DecisionRecord`
  - speichern jetzt auch `sequence_intent`,
    `calibration_profile_id` und die benutzten
    `calibration_stratification_dimensions`
- erweiterte `CalibrationContext` und `EnrichedPathEvaluation`
  - zeigen das verwendete Profil, dessen Konfidenz und den
    Blend-Anteil zum globalen Gewichtsset

## Engine-Verhalten

Die `CalibrationEngine` verwaltet jetzt neben dem globalen
Gewichtungsset mehrere Profil-Slices.

Sie erzeugt dafuer abgestufte Profilvarianten ueber:

- `support_profile`
- `sequence_intent`
- `evidence_pattern`
- `block_type`

Wenn fuer einen Kontext noch nicht genug Outcomes vorliegen, werden die
Profilscores kontrolliert in das globale H.7-Gewichtungsset
zurueckgemischt. Damit bleibt die Kalibrierung bei kleinen Samples
stabil, ohne profilspezifische Signale zu verlieren.

## Persistenz und API

`CalibrationStore` speichert jetzt auch `calibration_profiles`.

Neue Admin-Endpunkte:

- `GET /api/v1/admin/calibration/profiles`
- `GET /api/v1/admin/calibration/profiles/{profile_id}`

`POST /api/v1/tutoring/outcome` liefert jetzt zusaetzlich
`calibration_profile_updated`, damit sichtbar bleibt, welcher
Profil-Slice durch das Outcome fortgeschrieben wurde.

## Testanker

- [tests/test_h8_profile_calibration.py](/Users/jonasweiss/MathTeach/tests/test_h8_profile_calibration.py)
- [tests/test_calibration_store.py](/Users/jonasweiss/MathTeach/tests/test_calibration_store.py)
- [tests/test_planner_runtime_flow.py](/Users/jonasweiss/MathTeach/tests/test_planner_runtime_flow.py)
- [tests/test_api.py](/Users/jonasweiss/MathTeach/tests/test_api.py)

## Naechster Schritt

H.9 kann jetzt auf diesen Profil-Slices Meta-Kalibrierung aufsetzen:
also Transfer zwischen verwandten Profilen, robustere Hierarchien und
spaeter content- oder domaeenspezifische Gewichte.
