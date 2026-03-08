import os

def identify(datapath, bank_rules):
    try:
        # Wir lesen die Datei Zeile für Zeile als reinen Text
        with open(datapath, 'r', encoding='latin1') as f:
            lines = f.readlines()[:50]  # Wir prüfen nur die ersten 50 Zeilen

        for bank_name, rules in bank_rules.items():
            target_keyword = rules['first-column']

            for i, line in enumerate(lines):
                # Wir prüfen, ob das Schlagwort in der Zeile vorkommt
                # .strip() entfernt Leerzeichen, damit der Vergleich sauber ist
                if target_keyword in line:
                    print(f"DEBUG: '{target_keyword}' in Zeile {i} gefunden.")
                    return bank_name, i

        print("DEBUG: Kein Schlagwort aus der bank.json in der Datei gefunden.")
        return None, None
    except Exception as e:
        print(f"Fehler bei Identifizierung: {e}")
        return None, None