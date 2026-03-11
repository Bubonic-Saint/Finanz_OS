import os
import json
import bank_identifier
import extractor
import add_id
import dupl_checker
import categorizer

# --- SETUP (Relative Pfade) ---
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)

# Zentrale Pfad-Definitionen
input_dir = os.path.join(project_dir, "data", "input")
output_dir = os.path.join(project_dir, "data", "output")
rules_dir = os.path.join(project_dir, "data", "rules")
archive_base = os.path.join(project_dir, "data", "archiv")

rules_path = os.path.join(rules_dir, "bank.json")
template_json = os.path.join(rules_dir, "template.json")
datapath = os.path.join(input_dir, "bank_upload.csv")
input_csv = os.path.join(input_dir, "to_be_categorized.csv")
ready_csv = os.path.join(output_dir, "ready_for_excel.csv")


def main():
    # 0. Fehlende Ordner automatisch erstellen (User-friendly für GitHub)
    for folder in [input_dir, output_dir, rules_dir, archive_base]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    print(f"DEBUG: Suche Bank-Datei unter: {datapath}")

    # 1. Check ob Input-Datei existiert
    if not os.path.exists(datapath):
        print(f"FEHLER: Keine Datei unter {datapath} gefunden.")
        return

    # 2. Bank-Konfiguration laden
    if not os.path.exists(rules_path):
        print(f"FEHLER: Konfigurationsdatei nicht gefunden unter {rules_path}")
        return

    with open(rules_path, "r", encoding="utf-8") as f:
        bank_rules = json.load(f)

    # 3. Identifizieren
    bank_name, header_line = bank_identifier.identify(datapath, bank_rules)
    if not bank_name:
        print("--- FEHLER: Bank konnte nicht identifiziert werden ---")
        return

    print(f"-> Erkannt: {bank_name}")

    # 4. Extrahieren
    df_raw = extractor.get_data(datapath, bank_name, header_line, bank_rules)
    if df_raw is None: return

    # 5. ID hinzufügen
    df_with_id = add_id.generate_unique_id(df_raw)

    # 6. Duplikate checken & Archiv pflegen
    new_entries = dupl_checker.filter_duplicates(df_with_id, bank_name, project_dir)

    # --- KATEGORISIERUNG ---
    print("Starte Kategorisierungsprozess...")

    archive_dir = os.path.join(archive_base, bank_name)
    if not os.path.exists(archive_dir): os.makedirs(archive_dir)
    archive_cat_csv = os.path.join(archive_dir, f"categorized_{bank_name}_data.csv")

    # Speichern mit utf-8-sig für Excel-Kompatibilität (Umlaute!)
    df_with_id.to_csv(input_csv, index=False, sep=";", encoding="utf-8-sig")

    # Kategorisierung starten
    categorizer.run_categorization(input_csv, ready_csv, archive_cat_csv, template_json)

    # Aufräumen
    if os.path.exists(input_csv):
        os.remove(input_csv)

    print(f"--- ERFOLG ---")
    print(f"Verarbeitet: {len(df_with_id)} Zeilen")
    print(f"Output bereit: {ready_csv}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nKRITISCHER FEHLER: {e}")
        import traceback

        traceback.print_exc()
        import time

        time.sleep(5)