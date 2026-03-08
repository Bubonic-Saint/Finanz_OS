import hashlib


def generate_unique_id(df):
    """Fügt dem DataFrame eine 'ID' Spalte basierend auf Datum, Betrag und Details hinzu."""

    def create_hash(row):
        # Wir kombinieren die Felder zu einem String
        payload = (
                str(row['Datum']).strip() +
                "{:.2f}".format(float(row['Betrag'].replace('.', '').replace(',', '.'))) +
                str(row['Details']).strip().lower()
        )
        return hashlib.md5(payload.encode('utf-8')).hexdigest()

    # ID an der ersten Stelle (Index 0) einfügen
    if 'ID' not in df.columns:
        df.insert(0, 'ID', df.apply(create_hash, axis=1))

    return df