import pandas as pd
import json
import os
import csv


def run_categorization(input_path, output_path, archive_path, template_path):
    # 1. Daten laden
    # utf-8-sig beim Lesen hilft, falls die Datei von Excel/VBA erstellt wurde
    df = pd.read_csv(input_path, sep=";", encoding="utf-8-sig")

    # 2. Regeln laden
    if os.path.exists(template_path):
        with open(template_path, "r", encoding="utf-8") as f:
            # Sicherstellen, dass "rules" geladen wird, auch wenn JSON anders strukturiert ist
            data = json.load(f)
            rules = data.get("rules", []) if isinstance(data, dict) else data
    else:
        rules = []
        print(f"Warnung: Keine Template-Datei unter {template_path} gefunden.")

    # 3. Vorbereiten der Spalten & robuste Zahlenkonvertierung
    def clean_currency(value):
        if pd.isna(value) or value == "":
            return 0.0
        if isinstance(value, (int, float)):
            return float(value)
        val_str = str(value).strip()
        # Logik für deutsches Format: 1.116,28 -> 1116.28
        val_str = val_str.replace('.', '').replace(',', '.')
        return pd.to_numeric(val_str, errors='coerce')

    df['Betrag'] = df['Betrag'].apply(clean_currency)

    # Standardwerte setzen
    df['Type'] = ""
    df.loc[df['Betrag'] > 0, 'Type'] = "Einnahme"
    df.loc[df['Betrag'] < 0, 'Type'] = "Ausgabe"

    # Sicherstellen, dass alle Spalten existieren
    for col in ['Kategorie', 'Subkategorie', 'Schlagwort']:
        if col not in df.columns:
            df[col] = ""

    # 4. Schlagwort-Suche
    for rule in rules:
        keyword = rule.get('keyword', '')
        if not keyword: continue

        direction = rule.get('direction')

        # Suche in Details und Empfänger
        mask = (df['Details'].str.contains(keyword, case=False, na=False)) | \
               (df['Empfänger'].str.contains(keyword, case=False, na=False))

        # Richtungs-Filter
        if direction == "plus":
            mask = mask & (df['Betrag'] > 0)
        elif direction == "minus":
            mask = mask & (df['Betrag'] < 0)

        if mask.any():
            df.loc[mask, 'Type'] = rule.get('type', df.loc[mask, 'Type'])
            df.loc[mask, 'Kategorie'] = rule.get('category', '')
            df.loc[mask, 'Subkategorie'] = rule.get('subcategory', '')
            df.loc[mask, 'Schlagwort'] = keyword

    # 5. Spaltenreihenfolge fixieren
    cols = ['ID', 'Datum', 'Betrag', 'Empfänger', 'Type', 'Kategorie', 'Subkategorie', 'Schlagwort', 'Details']
    # Nur Spalten nehmen, die auch wirklich im DF sind
    df = df[[c for c in cols if c in df.columns]]

    # 6. SPEICHERN: Output-Datei (für Excel)
    # utf-8-sig ist ESSENZIELL für deutsche Umlaute in Excel
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False, sep=";", encoding="utf-8-sig", quoting=csv.QUOTE_ALL)

    # 7. SPEICHERN: Archivierung
    # Wir fügen nur neue IDs hinzu, um das Archiv sauber zu halten
    os.makedirs(os.path.dirname(archive_path), exist_ok=True)
    if os.path.exists(archive_path):
        old_archive = pd.read_csv(archive_path, sep=";", encoding="utf-8-sig")
        # Dubletten-Vermeidung im Archiv basierend auf ID
        combined = pd.concat([old_archive, df]).drop_duplicates(subset=['ID'], keep='last')
        combined.to_csv(archive_path, index=False, sep=";", encoding="utf-8-sig", quoting=csv.QUOTE_ALL)
    else:
        df.to_csv(archive_path, index=False, sep=";", encoding="utf-8-sig", quoting=csv.QUOTE_ALL)

    return df