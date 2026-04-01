# Wissenssystem

## Ziel

Das Wissenssystem soll Mathematik so speichern, dass der Agent nicht nur Antworten findet, sondern die fachliche Linie hinter einer Aussage erklaeren kann.

## Zentrale Objekttypen

### SourceDocument

- Titel
- Autorinnen und Autoren
- Jahr
- Sprache
- Quelle
- Dokumenttyp
- Vertrauensstufe
- Lizenz

### ConceptNode

- Name
- Alternative Bezeichnungen
- Kurzdefinition
- strenge Definition
- Voraussetzungen
- typische Intuition
- typische Fehlvorstellungen

### EquationNode

- Formel
- Name
- erster bekannter Ursprung
- spaetere Wiederentdeckungen
- uebliche Notation
- typische Einsatzgebiete

### TheoremNode

- Aussage
- Voraussetzungen
- Beweisidee
- kanonische Quellen
- verwandte Resultate

### PedagogyPattern

- Zielgruppe
- Erklearstil
- Visualisierungsform
- Fehlerdiagnostik
- Uebungsstrategie

## Retrieval-Strategie

MathTeach sollte Hybrid Retrieval nutzen:

- `keyword retrieval` fuer exakte Begriffe, Namen und Formeln
- `vector retrieval` fuer semantisch aehnliche Fragen
- `graph traversal` fuer Voraussetzungsketten, Beweislinien und historische Herleitungen

Beispiel:

Wenn jemand nach der quadratischen Formel fragt, soll das System nicht nur die Formel finden, sondern auch:

- lineare und quadratische Grundbegriffe als Voraussetzungen
- historische Herleitung
- geometrische Intuition
- moderne Standardanwendung
- altersgerechte Erklaerungsformen

## Ingestion-Pipeline

1. Dokument einlesen
2. Metadaten normalisieren
3. logische Segmente bilden
4. mathematische Entitaeten extrahieren
5. Quellen und Behauptungen verlinken
6. Embeddings erzeugen
7. Kanten im Wissensgraphen anlegen
8. Review und Freigabe

## Qualitaetsregeln

- Jede fachliche Kernaussage muss auf Dokumentsegmente zurueckfuehrbar sein.
- Historische Aussagen brauchen mindestens eine primaere oder gut belegte sekundaere Quelle.
- Didaktische Muster werden getrennt vom Fachwissen versioniert.
- Schlechte OCR oder unsichere Extraktion darf nicht stillschweigend produktiv werden.
