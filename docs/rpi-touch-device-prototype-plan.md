# RPi Touch Device Prototype Plan

## Ziel

MathTeach soll nicht nur als abstrakte Tutor-Engine weiterwachsen,
sondern als erstes lokales Lerngeraet pruefbar werden:

- offline
- fokussiert
- persoenlich
- neurodiversitaetsbewusst
- ohne Cloud-Zwang

Dieses Dokument beschreibt den kleinsten realistischen
Geraete-Prototypen auf `Raspberry Pi 5` plus
`RPi Touch Display 2 (7")`.

## Warum dieser Schritt jetzt

Die Engine ist in H.9 bereits tief kalibriert und stark beobachtbar.

Das naechste Projektrisiko ist nicht mehr nur algorithmisch, sondern
produktseitig:

- keine echte Schuelerinteraktion
- keine reale Nutzungssituation
- keine pruefbare UI-Wirkung

Der Device-Prototyp schliesst genau diese Luecke.

## Produktposition fuer den Prototypen

Der erste Prototyp ist:

- kein Endkundenprodukt
- kein Massenmarkt-Geraet
- kein eigenes PCB-Projekt

Er ist ein `Proof of Use`:

- ein Schueler kann ihn einschalten
- er versteht ohne Setup, was er tun soll
- die Engine erklaert sichtbar anders fuer unterschiedliche
  Unterstuetzungsbedarfe
- das Geraet fuehlt sich eher wie ein persoenlicher Tutor als wie eine
  App an

## Zielgruppen fuer den ersten Feldtest

Der erste Prototyp soll mindestens fuer diese drei Typen anschlussfaehig
sein:

- Schueler mit fragiler Aufmerksamkeit / ADHS-naher Nutzung
- Schueler ohne starke Unterstuetzung zu Hause
- neugierige Selbstlerner, die mehr Tiefe wollen

Das Geraet wird nicht als Spezialgeraet fuer "Problemfaelle" gebaut.
Es wird als wuerdiges Lernwerkzeug fuer sehr unterschiedliche Lernlagen
gebaut.

## Hardware-Basis fuer Prototyp 1

Fest eingeplant:

- `Raspberry Pi 5`
- `RPi Touch Display 2 (7")`
- Netzbetrieb fuer die erste Version

Optional spaeter:

- Akku
- eigenes Gehaeuse
- robustere Einhausung fuer Transport

## Software-Schnitt fuer Prototyp 1

Der schnellste realistische Prototyp-Pfad ist:

- bestehende MathTeach-Engine bleibt Backend
- lokale Web-UI im Kiosk-Modus
- Chromium startet fullscreen
- kein sichtbarer Desktop
- keine sichtbare Browser-Chrome

Warum dieser Weg:

- minimale neue Infrastruktur
- schnelle UI-Iteration trotz noch geringer Frontend-Erfahrung
- bestehende FastAPI-/Engine-Struktur kann weiter genutzt werden
- spaetere Portierung in eine andere Shell bleibt moeglich

## Nicht-Ziele fuer Prototyp 1

Bewusst noch nicht enthalten:

- Akku-Optimierung
- eigenes Mainboard
- App Store / Distribution
- Voice-Layer
- Cloud-Synchronisation
- Eltern-Portal
- Multi-User-Schulverwaltung

## Erster didaktischer Scope

Der Prototyp braucht nicht sofort den ganzen Mathematikraum.

Er braucht einen einzigen ueberzeugenden Themenkorridor, der die volle
Pipeline zeigt.

Empfohlener Scope fuer Seed 1:

- ein klar abgegrenztes Thema
- vollstaendige Lernstrecke
- mindestens drei Darstellungsniveaus
- mindestens ein visuell starkes Kernthema

Beispielpfade:

- lineare Gleichungen
- Bruchverstehen
- fruehe Differentialrechnung

Die Themenwahl kann spaeter getrennt festgelegt werden; der Prototyp
selbst haengt nicht an genau einem dieser Themen.

## Kernanforderungen an das Geraet

Das Geraet muss:

- ohne Internet grundlegend funktionieren
- direkt in die Lernoberflaeche starten
- sich den letzten Stand merken
- Schueler nicht bewerten, sondern fuehren
- lernrelevante Profile intern nutzen, ohne sie nach aussen
  zu diagnostischen Labels zu machen

Das Geraet darf nicht:

- wie ein abgesperrtes Billig-Tablet wirken
- wie ein Browser mit Website wirken
- den Nutzer in Menues verlieren
- bei Fehlern Druck aufbauen

## Artefakte, die vor dem ersten Feldtest stehen muessen

### 1. Forschungsbasiertes UI-Lastenheft

Siehe:

- [rpi-touch-ui-lastenheft.md](/Users/jonasweiss/MathTeach/docs/rpi-touch-ui-lastenheft.md)

### 2. Einfache Kiosk-Startkette

Noetig:

- automatischer Start der lokalen UI
- Touch-Bedienung ohne Tastatur/Maus
- definierter Resume-Pfad

### 3. Erstes Schueler-Onboarding

Noetig:

- wenige, natuerliche Fragen
- lokale Profilinitialisierung
- keine klinische Sprache

### 4. Eine echte Lernansicht auf 800x480

Noetig:

- Illustration als didaktisches Kernelement
- klarer Textfluss
- grosse Touch-Flaechen
- drei Hauptaktionen oder weniger

### 5. Ein kompletter Seed-Korridor

Noetig:

- Inhalt
- Beispiele
- Reaktionslogik
- Resume-Semantik

## Konkreter 6-Wochen-Schnitt

### Woche 1

- Device-Pfad festziehen
- UI-Lastenheft finalisieren
- Kiosk-Architektur entscheiden

### Woche 2

- Startkette auf dem RPi bootfaehig machen
- lokales UI-Frame ohne echte Schoenheit, aber mit echtem
  Geraeteverhalten

### Woche 3

- Onboarding-Grundfluss bauen
- Profilantworten lokal in die bestehende Tutorlogik uebergeben

### Woche 4

- erste Lernansicht fuer 800x480
- Illustration als separates Asset sauber einbinden

### Woche 5

- ein kompletter Themenkorridor
- Resume- und Wiedereinstieg pruefen

### Woche 6

- erster echter Test mit einer realen Lernperson
- Beobachtung dokumentieren
- danach erst weitere Hardware- oder UI-Verfeinerung

## Technische Entscheidung fuer den ersten Prototypen

Empfohlen:

- `FastAPI + lokale Web-UI + Chromium Kiosk`

Noch nicht empfohlen:

- native Python-GUI als erster Schritt
- eigenes PCB
- ESP32-Edge-Port

Begruendung:

- schnellster Weg zu echter Nutzung
- geringstes Infrastruktur-Risiko
- erlaubt spaetere starke visuelle Iteration

## Erfolgskriterium

Der erste Prototyp ist erfolgreich, wenn:

- ein echter Schueler ohne Fremdhilfe starten kann
- die Session sichtbar ruhiger und persoenlicher wirkt als eine
  generische Lern-App
- die Engine bereits unterscheidbare Tutorreaktionen zeigt
- ein Testnutzer sinnvoll sagen kann, was geholfen oder gestoert hat

Nicht das Geraet selbst ist dann bewiesen.
Aber die Richtung ist bewiesen.
