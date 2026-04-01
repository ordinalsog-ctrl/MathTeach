# Source Access Program

## Ziel

Wir brauchen fuer die erste historische Mathematik-Sammlung nicht nur Themen und Werke, sondern auch einen operativen Zugriffsplan:

- Welche Quelle ist gemeint?
- Wo kann sie heute gelesen werden?
- Duerfen wir sie lokal speichern?
- Wo legen wir Rohdatei, OCR, Metadaten und Ableitungen ab?

## Zugriffslogik

Jede Quelle wird mit mindestens einer `access_route` versehen.

Moegliche Zugriffsarten:

- `open_html`
- `open_pdf`
- `open_scan`
- `borrowable_scan`
- `institutional`
- `purchase_or_library`
- `open_snippet`

## Speicherlogik

Wir trennen vier Ebenen:

1. `library/raw/`
2. `library/normalized/`
3. `data/math_core/`
4. Git-tracked Metadaten und Manifeste

### 1. library/raw/

Hier liegen Originaldateien:

- PDFs
- Bildscans
- DjVu
- heruntergeladene HTML-Snapshots

Diese Dateien werden nicht in Git versioniert.

Pfadidee:

- `library/raw/public_domain/<source-slug>/`
- `library/raw/restricted/<source-slug>/`

### 2. library/normalized/

Hier liegen abgeleitete Arbeitsformate:

- OCR-Text
- bereinigte Textfassungen
- segmentierte JSONL-Dateien
- Formeltafeln

Auch diese Dateien werden standardmaessig nicht in Git versioniert.

### 3. data/math_core/

Hier liegen kleine, versionierbare Steuerdateien:

- Sammelmanifeste
- Quellenregister
- Queue-Definitionen
- Seeder-Dateien

### 4. Git-tracked Metadaten

In Git gehoeren:

- bibliographische Metadaten
- Rechte- und Zugriffshinweise
- Checksummen
- Ingestion-Protokolle
- Extraktionsstatistiken

Nicht in Git gehoeren grosse Roh-PDFs, OCR-Massenartefakte und ungeklaerte lizenzpflichtige Dateien.

## Arbeitsregel fuer historische Mathematik

Bei jedem Werk speichern wir getrennt:

- `what exists`: Werk oder Artefakt
- `how to read now`: heutiger Zugriffsweg
- `how to store`: lokaler Ablagepfad
- `what rights apply`: Rechte- und Risikohinweis

## Audit-Regel

Jede Erweiterung der Quellenliste endet mit einem Folgeaudit.

Die feste Projektregel dazu steht in [docs/curation-loop.md](/Users/jonasweiss/MathTeach/docs/curation-loop.md).

## Erste Prioritaet

Zuerst bauen wir ein belastbares Register fuer:

- Antike
- Medieval Transmission and Synthesis
- Early Modern Analysis and Chance

mit direktem Fokus auf:

- Zahlensysteme und Arithmetik
- Satz des Pythagoras und Beweiskultur
- Euklid
- Archimedes
- Brahmagupta
- al-Khwarizmi
- Fibonacci
- Newton
- Leibniz
- Pascal und Fermat

## Repo-Artefakte

- [data/math_core/source_access_manifest.json](/Users/jonasweiss/MathTeach/data/math_core/source_access_manifest.json)
- [sql/004_source_access_registry.sql](/Users/jonasweiss/MathTeach/sql/004_source_access_registry.sql)
- [library/README.md](/Users/jonasweiss/MathTeach/library/README.md)
