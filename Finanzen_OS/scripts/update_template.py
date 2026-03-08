import json
import sys
import os


def add_rule(keyword, t_type, cat, sub_cat):
    path = r"C:\Users\kevin\Git\Finanzen_OS\data\rules\template.json"

    # 1. Bestehende Regeln laden
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except:
            data = {"rules": []}
    else:
        data = {"rules": []}

    # 2. Neue Regel vorbereiten
    new_rule = {
        "keyword": keyword,
        "type": t_type,
        "category": cat,
        "subcategory": sub_cat
    }

    # 3. Dubletten entfernen (falls Keyword schon existiert)
    data["rules"] = [r for r in data["rules"] if r["keyword"].lower() != keyword.lower()]

    # 4. Neue Regel hinzufügen
    data["rules"].append(new_rule)

    # 5. Sauber speichern
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    # sys.argv[1-4] sind die Argumente von VBA
    if len(sys.argv) > 4:
        add_rule(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])