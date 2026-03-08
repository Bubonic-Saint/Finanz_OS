import pandas as pd


def get_data(datapath, bank_name, header_row, bank_rules):
    # Wir holen uns die spezifischen Regeln für diese Bank
    rules = bank_rules[bank_name]

    # Jetzt lesen wir mit dem richtigen Trenner und Encoding
    df = pd.read_csv(
        datapath,
        sep=rules['sep'],
        encoding=rules['encoding'],  # Hier lag der Fehler!
        skiprows=header_row
    )

    # Mapping der Spalten (wie wir es vorher definiert hatten)
    mapping = rules['mapping']
    df = df[list(mapping.keys())].rename(columns=mapping)

    return df