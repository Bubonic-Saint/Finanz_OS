import pandas as pd
import os


def get_data(datapath, bank_name, header_row, bank_rules):
    """
    Extrahiert Daten basierend auf bank.json Regeln.
    Behandelt fehlende Spalten und Encoding-Probleme elegant.
    """
    rules = bank_rules.get(bank_name)
    if not rules:
        print(f"FEHLER: Keine Regeln für {bank_name} in bank.json gefunden.")
        return None

    try:
        # Einlesen der Datei
        # Wir nutzen low_memory=False, um Warnungen bei gemischten Datentypen zu vermeiden
        df = pd.read_csv(
            datapath,
            sep=rules['sep'],
            encoding=rules['encoding'],
            skiprows=header_row,
            on_bad_lines='warn',  # Überspringt kaputte Zeilen statt abzustürzen
            low_memory=False
        )

        # Mapping der Spalten
        mapping = rules['mapping']

        # Sicherheits-Check: Existieren alle im Mapping definierten Spalten in der CSV?
        available_cols = [col for col in mapping.keys() if col in df.columns]
        missing_cols = [col for col in mapping.keys() if col not in df.columns]

        if missing_cols:
            print(f"WARNUNG: Folgende Spalten fehlen in der Datei: {missing_cols}")

        # Nur verfügbare Spalten extrahieren und umbenennen
        df = df[available_cols].rename(columns=mapping)

        # Datums-Bereinigung (Optional aber empfohlen für GitHub-User)
        # Verhindert, dass Excel das Datum später falsch interpretiert
        if 'Datum' in df.columns:
            df['Datum'] = pd.to_datetime(df['Datum'], dayfirst=True, errors='coerce').dt.strftime('%d.%m.%Y')

        # Falls Spalten fehlen (z.B. Empfänger), leer anlegen damit der Rest nicht crashed
        required_cols = ['Datum', 'Betrag', 'Empfänger', 'Details']
        for col in required_cols:
            if col not in df.columns:
                df[col] = ""

        return df

    except Exception as e:
        print(f"KRITISCHER FEHLER beim Extrahieren ({bank_name}): {e}")
        return None