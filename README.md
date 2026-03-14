# Finanz-OS: Automatisierter Bank-Tracker 🚀

Ein intelligentes System zur Kategorisierung und Nachverfolgung von Bankumsätzen. 
Kombiniert die Power von **Python (Backend)** mit der Benutzerfreundlichkeit von **Excel (Frontend)**.

## 🛠 Features
Smarte Kategorisierung: Python-Skripte durchsuchen Verwendungszweck und Empfänger nach Schlagworten.

Hybrides System: Datenverarbeitung in Python (Pandas), Budget-Planung und Visualisierung in Excel.

Echtzeit-Feedback: Excel-Zellen färben sich automatisch (Gelb/Grün), basierend auf dem Kategorisierungsstatus.

Workflow-Sperre: Das VBA-Makro verhindert den Transfer in das Haupt-Tracking, solange Umsätze nicht eindeutig zugewiesen sind.

Regel-Lernsystem: Erstelle neue Schlagwort-Regeln direkt in Excel, die sofort in die Python-Logik (template.json) übernommen werden.

Deduplizierung: Ein lokales Archiv stellt sicher, dass keine Transaktion doppelt importiert wird.

## 📂 Projektstruktur
```text
Finanzen_OS/
├── Finanzen_Template.xlsm    # Excel-Hauptdatei mit Dashboard & Makros
├── scripts/                  # Die Python-Logik (Backend)
│   ├── main.py               # Zentrales Steuerungs-Skript
│   ├── bank_identifier.py    # Erkennt das Bank-Format
│   ├── extractor.py          # Liest Rohdaten basierend auf bank.json aus
│   ├── add_id.py             # Generiert ID für jede Transaktion
│   ├── dupl_checker.py       # Filtert bereits importierte Umsätze
│   ├── categorizer.py        # Schlagwortsuche & Kategorisierung
│   ├── update_template.py    # Speichert neue Regeln aus Excel in die JSON
│   ├── clear_data.py         # Hilfsskript zum Bereinigen von Verzeichnissen
│   └── emergency_reset.py    # Beendet hängende Prozesse & gibt Dateien frei
├── data/                     # Datenhaltung (lokal)
│   ├── input/                # Ablageort für Bank-CSVs
│   ├── output/               # Schnittstelle (Ready-to-Excel)
│   ├── rules/                # Konfiguration (bank.json & template.json)
│   └── archiv/               # Getrenntes Archiv pro Bank-Typ
├── requirements.txt          # Python-Abhängigkeiten (Pandas, psutil)
└── INSTALL_MY_FINANCES.bat   # Installations File

```
## JSON-Konfiguration
**bank.json**: Definiert die Struktur der Bank-CSV (Spaltennamen, Trennzeichen, etc.) für die Extraktion.
Bisherige unterstützte Banken:
- ING
- Sparkasse
``` json
    "ING": {
        "first-column": "Buchung;",
        "sep": ";",
        "encoding": "latin1",
        "mapping": {
            "Buchung": "Datum",
            "Betrag": "Betrag",
            "Auftraggeber/Empfänger": "Empfänger",
            "Verwendungszweck": "Details"
        }
```
**template.json**: Speichert die Schlagwort-Regeln, die in Excel erstellt und von Python für die Kategorisierung genutzt werden.
``` json
{
  "rules": [
    {
      "keyword": "Supermarkt",
      "type
      "category": "Lebensmittel"
    },
    {
      "keyword": "Tankstelle",
      "category": "Transport"
    }
  ]
```
## 🛠 Installation

### 1. Repository klonen
```bash
git clone https://github.com/Bubonic-Saint/Finanz_OS.git
```

### 2. Vorraussetzungen installieren
Öffne deinen Finanzen_OS Folder und doppelkliche die Datei:
"INSTALL_MY_FINANCES.bat"

Folgendes wird basieren:

-Python-Check: Das Skript prüft, ob Python auf deinem Rechner installiert ist.
Falls nicht: Lädt es den offiziellen Python-Installer herunter und startet ihn für dich.

-Umgebung (VENV): Es erstellt einen isolierten Ordner (.venv) innerhalb des Projektverzeichnisses. Das sorgt dafür, dass die Finanz-       Software keine anderen Programme auf deinem PC stört.

-Abhängigkeiten: Alle benötigten Rechen-Module (wie Pandas für die Datenverarbeitung) werden automatisch in diese Umgebung geladen.

-Infrastruktur: Fehlende Ordner für deine Bankdaten (input, output, archiv) werden angelegt, damit das Programm sofort startklar ist.

-Desktop-Verknüpfung: Es wird automatisch ein Icon namens "Finanz-OS" auf deinem Desktop erstellt. Über dieses Icon kannst du ab sofort direkt deine Excel-Verwaltung starten, ohne jemals wieder in den Projektordner gehen zu müssen.


### 3. Excel-Datei vorbereiten
- Öffne `Finanzen_Template.xlsm` in Excel.
- Aktiviere Makros, wenn du dazu aufgefordert wirst.

## 🚀 Nutzung

<img width="1683" height="894" alt="image" src="https://github.com/user-attachments/assets/3e642365-78d3-4347-bddf-fe611b18a33c" />


## 💳 Credits & Inspiration
Dieses Projekt basiert auf der Grundidee und dem Excel-Template von **The Office Lab**. 
Das ursprüngliche Konzept wurden in diesem Video vorgestellt:
- 📺 [
How to create Ultimate Personal Budget in Excel](https://youtu.be/eKyAOjH3Crk?list=PL0tDTM2-szCFA1b_mNM5rOzTQK82WKBvM)

Vielen Dank für die großartige Vorlage!
