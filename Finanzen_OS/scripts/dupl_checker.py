import pandas as pd
import os


def filter_duplicates(new_df, bank_name, project_dir):
    """
    Gleicht IDs mit dem Archiv ab.
    Verhindert, dass bereits verarbeitete Umsätze erneut importiert werden.
    """

    # Pfad zum Archiv-Ordner
    archive_dir = os.path.join(project_dir, "data", "archiv", bank_name)
    filename = f"raw_{bank_name}_data.csv"
    archive_path = os.path.join(archive_dir, filename)

    # Verzeichnis erstellen, falls nötig
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)

    if os.path.exists(archive_path):
        try:
            # Archiv laden (sig wichtig für Umlaute in Excel)
            archive_df = pd.read_csv(archive_path, sep=";", encoding="utf-8-sig")

            # IDs als String normalisieren, um Vergleichsfehler zu vermeiden
            archive_ids = archive_df['ID'].astype(str).unique()
            current_ids = new_df['ID'].astype(str)

            # Nur Zeilen behalten, deren ID NICHT im Archiv ist
            new_entries = new_df[~current_ids.isin(archive_ids)].copy()

            if not new_entries.empty:
                # Nur bei echten neuen Einträgen das Archiv erweitern
                updated_archive = pd.concat([archive_df, new_entries], ignore_index=True)
                updated_archive.to_csv(archive_path, index=False, sep=";", encoding="utf-8-sig")

        except Exception as e:
            print(f"HINWEIS: Archiv konnte nicht gelesen werden ({e}). Erstelle neues Archiv.")
            new_entries = new_df.copy()
            new_df.to_csv(archive_path, index=False, sep=";", encoding="utf-8-sig")
    else:
        # Falls kein Archiv da ist, ist alles neu
        new_entries = new_df.copy()
        new_df.to_csv(archive_path, index=False, sep=";", encoding="utf-8-sig")

    return new_entries