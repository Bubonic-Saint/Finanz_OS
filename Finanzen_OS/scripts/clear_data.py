import os
import shutil

# --- SETUP ---
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
data_dir = os.path.join(project_dir, "data")


def clear_folders():
    # Welche Ordner sollen geleert werden?
    # Wir leeren 'archiv' (komplett mit Unterordnern) und 'output'
    folders_to_clear = [
        os.path.join(data_dir, "archiv"),
        os.path.join(data_dir, "output"),
        os.path.join(data_dir, "input")
    ]

    # Einzelne Dateien im data-Hauptverzeichnis, die weg sollen
    files_to_delete = [
        os.path.join(data_dir, "to_be_categorized.csv"),
        os.path.join(data_dir, "ING_test.csv")
    ]

    print("Starte Bereinigung...")

    # 1. Ordner leeren
    for folder in folders_to_clear:
        if os.path.exists(folder):
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)  # Löscht Datei
                        print(f"Gelöscht: {file_path}")
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)  # Löscht Unterordner (z.B. /ING/)
                        print(f"Ordner entfernt: {file_path}")
                except Exception as e:
                    print(f"Fehler beim Löschen von {file_path}: {e}")
        else:
            print(f"Ordner nicht gefunden: {folder}")

    # 2. Einzelne Dateien löschen
    for file in files_to_delete:
        if os.path.exists(file):
            os.remove(file)
            print(f"Datei gelöscht: {file}")

    print("--- Bereinigung abgeschlossen ---")


if __name__ == "__main__":
    confirm = input("Möchtest du wirklich das Archiv und alle Outputs löschen? (y/n): ")
    if confirm.lower() == 'y':
        clear_folders()
    else:
        print("Abgebrochen.")