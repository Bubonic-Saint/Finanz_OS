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
└── requirements.txt          # Python-Abhängigkeiten (Pandas, psutil)
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
git clone [https://github.com/DEIN_USERNAME/Finanz_OS.git](https://github.com/DEIN_USERNAME/Finanz_OS.git)
cd Finanz_OS# Finanz_OS
```

### 2. Python-Umgebung einrichten
```bash
# 1. Virtuelle Umgebung erstellen
python -m venv .venv

# 2. Umgebung aktivieren
# In der Git Bash oder auf Linux/Mac:
source .venv/Scripts/activate
# In der Windows Eingabeaufforderung (CMD):
.venv\Scripts\activate.bat

# 3. Abhängigkeiten installieren
pip install -r requirements.txt
```

### 3. Excel-Datei vorbereiten
- Öffne `Finanzen_Template.xlsm` in Excel.
- Aktiviere Makros, wenn du dazu aufgefordert wirst.

## 🚀 Nutzung
