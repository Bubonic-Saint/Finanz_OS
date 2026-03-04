import pandas as pd
import json

dateipfad = "data/ING_test.csv"
regel_datei = "data/bank.json"

with open(regel_datei, "r", encoding="utf-8") as f:
    regel_datei = json.load(f)




