import os


def identify(datapath, bank_rules):
    """
    Scannt die Datei nach spezifischen Headern aus der bank.json.
    Unterstützt verschiedene Encodings für maximale Kompatibilität.
    """
    encodings = ['utf-8', 'latin1', 'cp1252']

    for encoding in encodings:
        try:
            with open(datapath, 'r', encoding=encoding) as f:
                # Wir prüfen die ersten 50 Zeilen (reicht für jeden Bank-Header)
                lines = [f.readline() for _ in range(50)]

            for bank_name, rules in bank_rules.items():
                target_keyword = rules.get('first-column')
                if not target_keyword:
                    continue

                for i, line in enumerate(lines):
                    if not line: continue  # Ende der Datei erreicht

                    # Wir prüfen, ob das Schlagwort vorkommt.
                    # case=False ist oft sicherer, falls Banken Header ändern
                    if target_keyword.lower() in line.lower():
                        # DEBUG-Print nur für die Entwicklung, für GitHub sauber halten
                        # print(f"DEBUG: '{target_keyword}' in Zeile {i} gefunden ({encoding}).")
                        return bank_name, i

            # Wenn wir hier ankommen, hat dieses Encoding nichts gefunden,
            # wir probieren das nächste.

        except (UnicodeDecodeError, UnicodeError):
            continue  # Encoding passt nicht, nächster Versuch
        except Exception as e:
            print(f"Fehler beim Lesen der Datei: {e}")
            return None, None

    print("INFO: Bank konnte nicht identifiziert werden. Prüfen Sie die bank.json.")
    return None, None