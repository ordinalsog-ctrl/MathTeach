# H.7 Persistent Calibration

Stand: 2026-04-05

## Ziel

H.7 schliesst die wichtigste Luecke aus H.6: Kalibrierungsdaten bleiben
jetzt nicht mehr nur im laufenden Prozess, sondern koennen dateibasiert
ueber Prozessstarts und mehrere Sessions hinweg erhalten bleiben.

## Neue Bausteine

- `CalibrationStore`
  - laedt und speichert Kalibrierungsdaten atomar als JSON
  - liefert erste Persistenz-Statistiken wie
    `total_decisions`, `total_outcomes`,
    `recent_success_rate` und `weight_stability_index`

- `CalibrationData`
  - kapselt
    - `decision_records`
    - `outcome_metrics`
    - `calibration_weights`
    - `weights_history`

- `CalibrationWeightsSnapshot`
  - dokumentiert, wann und warum sich Gewichte sichtbar verschoben haben

## Engine-Verhalten

Die `CalibrationEngine` kann jetzt optional mit einem Store laufen.

Damit kommen drei neue Eigenschaften hinzu:

- geloggte Entscheidungen koennen direkt persistiert werden
- Outcome-Updates koennen spaeter von einer neuen Engine-Instanz weiter
  verarbeitet werden
- Kalibrierungsrunden hinterlassen eine nachvollziehbare
  Gewichtshistorie statt nur einen ueberschriebenen Endzustand

## Planner- und API-Integration

`build_teaching_plan(...)` kann jetzt mit einer persistenten
`CalibrationEngine` arbeiten. Wenn ein Store aktiv ist, wird die
sichtbare Pfadentscheidung danach sofort weggeschrieben.

Die API stellt dazu jetzt neue H.7-Endpunkte bereit:

- `POST /api/v1/tutoring/outcome`
- `GET /api/v1/admin/calibration/statistics`
- `GET /api/v1/admin/calibration/history`

`calibration_context` zeigt jetzt zusaetzlich:

- `persistent_store_path`
- `persisted_decision_count`
- `recent_success_rate`
- `weight_stability_index`

## Konfiguration

Die Persistenz ist in der aktuellen Codebasis ueber Settings steuerbar:

- `MATHTEACH_CALIBRATION_STORE_PATH`
- `MATHTEACH_CALIBRATION_AUTOSAVE_THRESHOLD`

Damit bleibt H.7 im bestehenden, env-basierten Projektstil und fuehrt
keine zweite Konfigurationswelt ein.

## Testanker

- [tests/test_calibration_store.py](/Users/jonasweiss/MathTeach/tests/test_calibration_store.py)
- [tests/test_h7_persistent_calibration.py](/Users/jonasweiss/MathTeach/tests/test_h7_persistent_calibration.py)
- [tests/test_api.py](/Users/jonasweiss/MathTeach/tests/test_api.py)

## Naechster Schritt

H.8 kann jetzt auf echter Persistenz aufbauen und die Kalibrierung
profilspezifisch machen, statt weiterhin nur ein globales Gewichtungsset
zu lernen.
