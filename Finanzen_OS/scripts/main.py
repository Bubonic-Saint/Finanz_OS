import os
import json
import bank_identifier
import extractor
import add_id
import dupl_checker
import categorizer

# --- SETUP ---
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
input_dir = os.path.join(project_dir, "data", "input")

rules_path = os.path.join(project_dir, "data", "rules", "bank.json")
datapath = os.path.join(input_dir, "bank_upload.csv")


def main():
    print(f"DEBUG: Aktuelles Verzeichnis: {os.getcwd()}")
    print(f"DEBUG: Projekt-Pfad: {project_dir}")
    print(f"DEBUG: Suche Rules unter: {rules_path}")
    print(f"DEBUG: Suche Bank-Datei unter: {datapath}")
    # 1. Regeln laden
    if not os.path.exists(rules_path):
        print(f"Fehler: Konfigurationsdatei nicht gefunden unter {rules_path}")
        return

    with open(rules_path, "r", encoding="utf-8") as f:
        bank_rules = json.load(f)

    # 2. Identifizieren
    print(f"Analysiere Datei: {os.path.basename(datapath)}...")
    bank_name, header_line = bank_identifier.identify(datapath, bank_rules)

    if bank_name:
        print(f"-> Erkannt: {bank_name} (Header in Zeile {header_line})")

        # 3. Extrahieren
        df_raw = extractor.get_data(datapath, bank_name, header_line, bank_rules)

        if df_raw is not None:
            # 4. ID hinzufügen
            df_with_id = add_id.generate_unique_id(df_raw)

            # 5. Duplikate checken & Archiv pflegen
            new_entries = dupl_checker.filter_duplicates(df_with_id, bank_name, project_dir)

            if not new_entries.empty:
                # --- VERARBEITUNG NEUER EINTRÄGE ---
                input_csv = os.path.join(project_dir, "data", "input", "to_be_categorized.csv")
                template_json = os.path.join(project_dir, "data", "rules", "template.json")
                output_dir = os.path.join(project_dir, "data", "output")
                ready_csv = os.path.join(output_dir, "ready_for_excel.csv")

                archive_dir = os.path.join(project_dir, "data", "archiv", bank_name)
                archive_cat_csv = os.path.join(archive_dir, f"categorized_{bank_name}_data.csv")

                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                # Zwischendatei für Categorizer erstellen
                new_entries.to_csv(input_csv, index=False, sep=";", encoding="utf-8")

                # Kategorisierung starten
                categorizer.run_categorization(input_csv, ready_csv, archive_cat_csv, template_json)
                print(f"Kategorisierung abgeschlossen für {bank_name}.")

                # Aufräumen & Abschlussbericht
                if os.path.exists(input_csv):
                    os.remove(input_csv)

                print(f"--- ERFOLG ---")
                print(f"Gesamt in Datei: {len(df_with_id)} Zeilen")
                print(f"Neue Einträge:   {len(new_entries)} Zeilen verarbeitet und archiviert.")
                print(f"Output bereit:   {ready_csv}")

            else:
                print("--- INFO ---")
                print(f"Keine neuen Umsätze für {bank_name} gefunden. Das Archiv ist aktuell.")
    else:
        print("--- FEHLER ---")
        print("Bank konnte nicht identifiziert werden.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("\n" + "=" * 30)
        print("KRITISCHER FEHLER IM SKRIPT:")
        print(e)
        import traceback

        traceback.print_exc()  # Zeigt dir genau, in welcher Zeile es knallt
        print("=" * 30)

    # Das hier hält das Fenster offen, egal ob Erfolg oder Fehler
    input("\nDrücke ENTER, um dieses Fenster zu schließen...")