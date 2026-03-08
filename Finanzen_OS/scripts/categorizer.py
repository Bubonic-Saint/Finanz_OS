import pandas as pd
import json
import os
import csv

def run_categorization(input_path, output_path, archive_path, template_path):
    # 1. Daten laden
    df = pd.read_csv(input_path, sep=";", encoding="utf-8")

    # 2. Regeln laden
    if os.path.exists(template_path):
        with open(template_path, "r", encoding="utf-8") as f:
            rules = json.load(f).get("rules", [])
    else:
        rules = []
        print(f"Warnung: Keine Template-Datei unter {template_path} gefunden.")

    # 3. Vorbereiten der Spalten & robuste Zahlenkonvertierung
    def clean_currency(value):
        if pd.isna(value):
            return 0.0
        val_str = str(value).strip()
        # Entferne Tausenderpunkte (1.116,28 -> 1116,28)
        val_str = val_str.replace('.', '')
        # Ersetze Komma durch Punkt für Python-Float (1116,28 -> 1116.28)
        val_str = val_str.replace(',', '.')
        return pd.to_numeric(val_str, errors='coerce')

    df['Betrag'] = df['Betrag'].apply(clean_currency)

    # Standardwerte setzen
    df['Type'] = ""
    df.loc[df['Betrag'] > 0, 'Type'] = "Einnahme"
    df['Kategorie'] = ""
    df['Subkategorie'] = ""
    df['Schlagwort'] = ""

    # 4. Schlagwort-Suche (Details UND Empfänger prüfen)
    for rule in rules:
        keyword = rule['keyword']
        mask = (df['Details'].str.contains(keyword, case=False, na=False)) | \
               (df['Empfänger'].str.contains(keyword, case=False, na=False))

        if mask.any():
            df.loc[mask, 'Type'] = rule['type']
            df.loc[mask, 'Kategorie'] = rule['category']
            df.loc[mask, 'Subkategorie'] = rule['subcategory']
            df.loc[mask, 'Schlagwort'] = keyword

    # 5. Spaltenreihenfolge für den Export fixieren
    cols = ['ID', 'Datum', 'Betrag', 'Empfänger', 'Type', 'Kategorie', 'Subkategorie', 'Schlagwort', 'Details']
    df = df[cols]

    # 6. SPEICHERN: Output-Datei (für Excel)
    # csv.QUOTE_ALL stellt sicher, dass Semikolons im Text die Spalten nicht zerschießen
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False, sep=";", encoding="utf-8", quoting=csv.QUOTE_ALL)

    # 7. SPEICHERN: Kategorisiertes Archiv
    os.makedirs(os.path.dirname(archive_path), exist_ok=True)
    if os.path.exists(archive_path):
        # Wichtig: Das Archiv muss mit dem gleichen Quoting gelesen werden
        old_archive = pd.read_csv(archive_path, sep=";", encoding="utf-8")
        updated_archive = pd.concat([old_archive, df], ignore_index=True)
        updated_archive.to_csv(archive_path, index=False, sep=";", encoding="utf-8", quoting=csv.QUOTE_ALL)
    else:
        df.to_csv(archive_path, index=False, sep=";", encoding="utf-8", quoting=csv.QUOTE_ALL)

    return df