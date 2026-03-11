import json
import sys
import os


def update_templates(raw_data):
    path = r"C:\Users\kevin\Git\Finanzen_OS\data\rules\template.json"

    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {"rules": []}

    # Trenne die verschiedenen Regeln
    entries = raw_data.split("###")

    for entry in entries:
        fields = entry.split("|")
        if len(fields) < 5: continue

        keyword, t_type, cat, sub_cat, direction = fields

        new_rule = {
            "keyword": keyword,
            "type": t_type,
            "category": cat,
            "subcategory": sub_cat,
            "direction": direction
        }

        # Dubletten-Check: Keyword UND Richtung müssen identisch sein zum Ersetzen
        data["rules"] = [r for r in data["rules"] if not (
                r["keyword"].lower() == keyword.lower() and
                r.get("direction") == direction
        )]
        data["rules"].append(new_rule)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        update_templates(sys.argv[1])