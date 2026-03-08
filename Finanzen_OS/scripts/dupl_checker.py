import pandas as pd
import os


def filter_duplicates(new_df, bank_name, project_dir):
    """Gleicht IDs mit dem Archiv im Ordner data/archiv/BANKNAME/ ab."""

    # Pfad zum Archiv-Ordner
    archive_dir = os.path.join(project_dir, "data", "archiv", bank_name)

    # NEU: Dynamischer Dateiname (z.B. raw_ING_data.csv)
    filename = f"raw_{bank_name}_data.csv"
    archive_path = os.path.join(archive_dir, filename)

    # Erstellt 'data/archiv/BANKNAME/', falls noch nicht vorhanden
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)

    if os.path.exists(archive_path):
        # Vorhandene Daten laden
        archive_df = pd.read_csv(archive_path, sep=";", encoding="utf-8")

        # Nur Zeilen behalten, deren ID NICHT im Archiv ist
        new_entries = new_df[~new_df['ID'].isin(archive_df['ID'])].copy()

        # Das Archiv erweitern
        updated_archive = pd.concat([archive_df, new_entries], ignore_index=True)
    else:
        # Falls kein Archiv da ist, ist alles neu
        new_entries = new_df.copy()
        updated_archive = new_df

    # Das aktualisierte Archiv speichern
    updated_archive.to_csv(archive_path, index=False, sep=";", encoding="utf-8")

    return new_entries