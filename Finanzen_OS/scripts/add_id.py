import hashlib
import pandas as pd


def generate_unique_id(df):
    """
    Erstellt eine eindeutige ID pro Transaktion.
    Robust gegenüber verschiedenen Datentypen und Formatierungen.
    """

    def create_hash(row):
        # 1. Betrag normieren (Egal ob String "1.200,50" oder Float 1200.5)
        betrag_raw = row['Betrag']
        try:
            if isinstance(betrag_raw, (int, float)):
                betrag_clean = "{:.2f}".format(float(betrag_raw))
            else:
                # Entferne Tausender-Punkte und ersetze Dezimal-Komma durch Punkt
                val_str = str(betrag_raw).strip().replace('.', '').replace(',', '.')
                betrag_clean = "{:.2f}".format(float(val_str))
        except (ValueError, TypeError):
            betrag_clean = "0.00"

        # 2. Datum und Details säubern
        datum_clean = str(row.get('Datum', '')).strip()
        details_clean = str(row.get('Details', '')).strip().lower()
        empfaenger_clean = str(row.get('Empfänger', '')).strip().lower()

        # 3. Payload kombinieren
        # Wir nehmen den Empfänger dazu, falls Details mal leer sind (z.B. bei Barabhebungen)
        payload = f"{datum_clean}|{betrag_clean}|{empfaenger_clean}|{details_clean}"

        return hashlib.md5(payload.encode('utf-8')).hexdigest()

    # Nur einfügen, wenn ID noch nicht existiert
    if 'ID' not in df.columns:
        # Wir nutzen apply, fangen aber Fehler ab, falls Spalten fehlen
        try:
            ids = df.apply(create_hash, axis=1)
            df.insert(0, 'ID', ids)
        except KeyError as e:
            print(f"FEHLER bei ID-Generierung: Spalte {e} fehlt im DataFrame!")
            df.insert(0, 'ID', 'ERROR_ID')

    return df