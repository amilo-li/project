import json
from datetime import datetime


# Funktion zur Speicherung der Daten aus dem Formular im JSON-File
def speichern(antragsteller, projektleiter, businessunit, titel, prio, startdatum, meilenstein1, meilenstein2,
                        meilenstein3, meilenstein4, enddatum, erstesQuartal, zweitesQuartal, drittesQuartal, viertesQuartal, informatik, buchhaltung, marketing, entwicklung):
    datei = "ausgabe_dict.json"
    try:
        with open(datei) as open_file:
            datei_content = json.load(open_file)
    except FileNotFoundError:
        datei_content = {}

    sum_totalf = float(erstesQuartal) + float(zweitesQuartal) + float(drittesQuartal) + float(viertesQuartal)
    sum_totale = (float(informatik) * 55.50) + (float(buchhaltung) * 55.50) + (float(marketing) * 55.50) + (float(entwicklung) * 55.50)
    sum_totalI = sum_totalf + sum_totale

    datei_content[str(datetime.now())] = {'Antragsteller': antragsteller,
                                          'Projektleiter': projektleiter,
                                          'Businessunit': businessunit,
                                          'Titel': titel,
                                          'Priorität': prio,
                                          'Total Fremdleistungen': sum_totalf,
                                          'Total Eigenleistungen': sum_totale,
                                          'Total Investitionssumme': sum_totalI,
                                          'Startdatum': startdatum,
                                          'Meilenstein 1': meilenstein1,
                                          'Meilenstein 2': meilenstein2,
                                          'Meilenstein 3': meilenstein3,
                                          'Meilenstein 4': meilenstein4,
                                          'Enddatum': enddatum,
                                          '1.Quartal': erstesQuartal,
                                          '2.Quartal': zweitesQuartal,
                                          '3.Quartal': drittesQuartal,
                                          '4.Quartal': viertesQuartal,
                                          'Informatik Aufwand': informatik,
                                          'Buchhaltung Aufwand': buchhaltung,
                                          'Marketing Aufwand': marketing,
                                          'Entwicklung Aufwand': entwicklung,
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


