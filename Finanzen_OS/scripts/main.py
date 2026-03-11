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
    print(f"Analysiere Datei: {os.path.basename(datapath)}...")
    bank_name, header_line = bank_identifier.identify(datapath, bank_rules)

    if not bank_name:
        print("--- FEHLER: Bank konnte nicht identifiziert werden ---")
        return

    print(f"-> Erkannt: {bank_name} (Header in Zeile {header_line})")

    # 4. Extrahieren
    df_raw = extractor.get_data(datapath, bank_name, header_line, bank_rules)
    if df_raw is None:
        print("FEHLER: Datenextraktion fehlgeschlagen.")
        return

    # 5. ID hinzufügen
    df_with_id = add_id.generate_unique_id(df_raw)

    # 6. Duplikate checken & Archiv pflegen
    # ACHTUNG: new_entries sind nur die, die noch NICHT im Archiv sind.
    new_entries = dupl_checker.filter_duplicates(df_with_id, bank_name, project_dir)

    # --- LOGIK FÜR AKTUALISIERUNG / REFRESH ---
    # Wir wollen den Categorizer IMMER laufen lassen, damit der Refresh-Button in Excel
    # auch bei bereits archivierten Daten funktioniert (z.B. nach Template-Änderung).

    print("Starte Kategorisierungsprozess...")

    # Pfade definieren
    input_csv = os.path.join(project_dir, "data", "input", "to_be_categorized.csv")
    template_json = os.path.join(project_dir, "data", "rules", "template.json")
    output_dir = os.path.join(project_dir, "data", "output")
    ready_csv = os.path.join(output_dir, "ready_for_excel.csv")
    archive_dir = os.path.join(project_dir, "data", "archiv", bank_name)
    archive_cat_csv = os.path.join(archive_dir, f"categorized_{bank_name}_data.csv")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # WICHTIG: Wir nehmen df_with_id (ALLE aktuellen Zeilen der CSV),
    # nicht nur new_entries, damit der Refresh alle Zeilen im Excel-Blatt aktualisiert.
    df_with_id.to_csv(input_csv, index=False, sep=";", encoding="utf-8")

    # Kategorisierung starten
    categorizer.run_categorization(input_csv, ready_csv, archive_cat_csv, template_json)

    # Aufräumen
    if os.path.exists(input_csv):
        os.remove(input_csv)

    print(f"--- ERFOLG ---")
    print(f"Verarbeitet: {len(df_with_id)} Zeilen")
    if not new_entries.empty:
        print(f"Davon neu hinzugefügt: {len(new_entries)} Zeilen")
    else:
        print("Keine neuen Zeilen zum Archiv hinzugefügt (Refresh-Modus).")
    print(f"Output bereit: {ready_csv}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("\n" + "=" * 30)
        print("KRITISCHER FEHLER IM SKRIPT:")
        print(e)
        import traceback

        traceback.print_exc()
        print("=" * 30)
        import time

        time.sleep(5)