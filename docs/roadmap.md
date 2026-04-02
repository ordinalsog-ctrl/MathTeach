# Roadmap

## Phase 0: Fundament

- Projektstruktur
- Modellentscheidung
- API-Skelett
- Datenmodell
- Trennung von Knowledge Core und Teacher Mind
- erstes SQL-Schema fuer beide Schichten

## Phase 1: MVP Tutor

- Lernprofil erfassen
- kleine kuratierte Mathematikbasis
- Hybrid Retrieval fuer wenige Themen
- tutorische Antwort mit Quellenfeldern
- Lehrerfigur nur als Vermittlungsschicht, nie als Faktenquelle
- Basis-Evals fuer Korrektheit und Verstaendlichkeit

## Phase 2: Mathematik-Korpus

- historische Standardwerke priorisieren
- Schul- bis Hochschulmathematik systematisch abdecken
- Ontologie fuer Konzepte, Gleichungen, Theoreme, Anwendungen
- Chunking- und Graph-Build-Pipeline

## Phase 3: Support Response Matrix

- kanonisches `support signal profile` definieren
- erste `response dimensions` festziehen
- Einzelprofile fuer ADHD, Dyskalkulie, Dyslexie, Autismusspektrum, ELL und Scarcity ausarbeiten
- kombinierte Profile spaeter aus stabilen Einzelprofilen ableiten
- `response_engine` als explizite Regelmaschine vorbereiten
- zuerst `ADHD-aware support` und `dyscalculia-aware support` voll operationalisieren
- danach Code-Skeleton fuer `response_matrix.py` und `response_engine.py`
- danach Planner-Integration und spaetere Pilot-Validierung

## Phase 4: Adaptive Lehre

- Misskonzept-Erkennung
- Frustrations- und Motivationssignale
- alternative Erklaerpfade
- visuelle und textuelle Lehrmodi
- Routing zwischen Beispielmodus und Ursprung-Erklaermodus
- support-sensitive Moduswahl unter Mixed Profiles und Priority-Ladders
- block-level live mode adaptation innerhalb einer Session
- Hysterese und ruhige Uebergaenge zwischen Modi
- spaeter history-aware mode adaptation

## Phase 5: Expertenmodus

- formalerer Stil
- Beweis-Skizzen und Varianten
- Literaturvergleich
- Forschungsnahe Hilfestellung mit Quellenketten

## Phase 6: Globalisierung

- mehrsprachige Erklaerungen
- regionale Curricula
- Barrierefreiheit
- sprach- und kulturadaptive Beispiele
