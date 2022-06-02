import json
from datetime import datetime


# Funktion zur Speicherung der Daten aus dem Formular im JSON-File
def speichern(antragsteller, projektleiter, titel, datum):
    datei = "ausgabe_dict.json"
    try:
        with open(datei) as open_file:
            datei_content = json.load(open_file)
    except FileNotFoundError:
        datei_content = {}

    datei_content[str(datetime.now())] = {'Antragsteller': antragsteller,
                                         'Projektleiter': projektleiter,
                                         'Titel': titel,
                                         'Datum': datum,
                                        }

    with open(datei, "w") as open_file:
        json.dump(datei_content, open_file, indent=4)


# Daten im JSON File laden
def antrag_laden():
    datei_name = "ausgabe_dict.json"

    try:
        with open(datei_name) as open_file:
            datei_content = json.load(open_file)
    except FileNotFoundError:
        datei_content = {}

    return datei_content