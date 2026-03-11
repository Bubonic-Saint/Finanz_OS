import json
import sys
import os


def update_templates(raw_data):
    # --- RELATIVE PFADE ---
    # scripts/update_template.py -> eins hoch -> data/rules/template.json
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    path = os.path.join(project_dir, "data", "rules", "template.json")

    # Ordner erstellen, falls er fehlt
    os.makedirs(os.path.dirname(path), exist_ok=True)

    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Falls die JSON keine "rules"-Liste hat (z.B. leerer Dict)
                if not isinstance(data, dict) or "rules" not in data:
                    data = {"rules": []}
        except (json.JSONDecodeError, ValueError):
            data = {"rules": []}
    else:
        data = {"rules": []}

    # Trenne die verschiedenen Regeln (vom Excel-String)
    entries = raw_data.split("###")
    count_new = 0

    for entry in entries:
        fields = entry.split("|")
        if len(fields) < 5: continue

        keyword, t_type, cat, sub_cat, direction = fields

        new_rule = {
            "keyword": keyword.strip(),
            "type": t_type.strip(),
            "category": cat.strip(),
            "subcategory": sub_cat.strip(),
            "direction": direction.strip()
        }

        # Dubletten-Check: Keyword UND Richtung müssen identisch sein zum Ersetzen
        # Wir filtern die alte Regel raus, bevor wir die neue hinzufügen
        data["rules"] = [r for r in data["rules"] if not (
                r.get("keyword", "").lower() == keyword.lower().strip() and
                r.get("direction") == direction.strip()
        )]

        data["rules"].append(new_rule)
        count_new += 1

    # Speichern mit Einrückung für Lesbarkeit
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"Erfolgreich {count_new} Regeln in {path} aktualisiert.")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        update_templates(sys.argv[1])
    else:
        print("Keine Daten zum Updaten übergeben.")