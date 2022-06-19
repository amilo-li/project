from flask import Flask
from flask import render_template
from flask import request
import daten
import plotly.express as px
from plotly.offline import plot
import pandas as pd

app = Flask(__name__)

"""
Ich erkläre hiermit, dass dieses Projekt selbstständig entwickelt wurde und keine anderen als die angegebenen Quellen benutzt wurden.
"""


# Home / Startseite
@app.route('/', methods=['GET', 'POST'])
def start():
    return render_template('index.html', user="Samira")  # hier wird der Begrüssungsname mitgegeben (Samira)


# User Input Form Felder
# Input Felder werden definiert und Funktion "speichern" aus daten.py wird aufgerufen
@app.route("/formular", methods=["POST", "GET"])
def formular():
    # Ausführen, wenn Button senden (post)
    if request.method == "POST":
        # Felder des Formulares definieren
        antragsteller = request.form["antragsteller"]
        projektleiter = request.form["projektleiter"]
        businessunit = request.form["businessunit"]
        titel = request.form["titel"]
        prio = request.form["prio"]
        startdatum = request.form["startdatum"]
        meilenstein1 = request.form["meilenstein1"]
        meilenstein2 = request.form["meilenstein2"]
        meilenstein3 = request.form["meilenstein3"]
        meilenstein4 = request.form["meilenstein4"]
        enddatum = request.form["enddatum"]
        erstesQuartal = request.form["erstesQuartal"]
        zweitesQuartal = request.form["zweitesQuartal"]
        drittesQuartal = request.form["drittesQuartal"]
        viertesQuartal = request.form["viertesQuartal"]
        informatik = request.form["informatik"]
        buchhaltung = request.form["buchhaltung"]
        marketing = request.form["marketing"]
        entwicklung = request.form["entwicklung"]

        # Input der Felder speichern
        # "speichern" Funktion in daten.py
        daten.speichern(antragsteller, projektleiter, businessunit, titel, prio, startdatum, meilenstein1, meilenstein2,
                        meilenstein3, meilenstein4, enddatum, erstesQuartal, zweitesQuartal, drittesQuartal,
                        viertesQuartal, informatik, buchhaltung, marketing, entwicklung)

        # Success Meldung, wenn daten gespeichert sind
        antrag_gespeichert = "Dein Investitionsantrag wurde gespeichert. Falls gewünscht kann ein weiterer " \
                             "Antrag erfassen werden. "

        return render_template("formular.html", antrag=antrag_gespeichert)

    return render_template("formular.html")


# Übersicht der Investitionsprojekte
# Daten werden mittels der Funktion antrag_laden in daten.py vom JSON File geladen
@app.route("/overview", methods=["GET", "POST"])
def overview():
    importeddata = daten.antrag_laden()  # Funktion antrag_laden in daten.py aufrufen
    filter_list = []
    filter_value = ""
    filter_key = ""
    filtered = False

    # Wenn auf den Button-Filter geklickt wird
    if request.method == 'POST':
        filtered = True
        businessunit = request.form['businessunit']

        if businessunit != "":
            filter_value = businessunit
            filter_key = "Businessunit"

        # Füge jeden Eintrag, bei dem der Key Businessunit und der entsprechende Wert vom Dropdown Feld übereinstimmt
        # der Liste hinzu.
        for key, value in importeddata.items():
            if value[filter_key] == filter_value:
                filter_list.append(value)

    return render_template('overview.html', data=importeddata, allitems=filter_list, Filter=filtered)


# Auswertung der Daten
@app.route("/analysis", methods=['GET', 'POST'])
def analysis():
    importdata = daten.antrag_laden()  # Funktion antrag_laden in daten.py aufrufen

    # Erste Auswertung Balkendiagramm Investitionssumme / Geschäftsfeld
    dictdiagram = {}

    # Für jeden key und value der importierten Daten
    # Dictionary erstellen mit key = Wert Businessunit und value = Wert Investitionssumme
    for key, values in importdata.items():
        businessunit = values["Businessunit"]
        dictdiagram[businessunit] = values["Total Investitionssumme"]

    x = list(dictdiagram.keys())  # businessunit
    y = list(dictdiagram.values())  # total investitionssumme

    # Erstellung des Balkendiagramms und Bennenung der Achsen
    fig = px.bar(x=x, y=y, labels={"x": "Geschäftsfeld",
                                   "y": "Investitionssumme"},
                 title="Übersicht der Investitionssummen pro Geschäftsfeld")
    # output_type = div, da mit fig.show() die html Seite nicht mehr ersichtlich wäre
    bar = plot(fig, output_type="div")
    # Quelle: https://plotly.com/python/figure-labels/

    # Zweite Auswertung Gant-Chart Projekt Start- / Enddatum
    dictgant = {}
    # Für jeden key und value der importierten Daten
    # Dictionary erstellen mit key = Wert Titel und values Wert Startdatum, Wert Enddatum
    for key, values in importdata.items():
        titel = values["Titel"]
        startdatum = values["Startdatum"]
        enddatum = values["Enddatum"]
        build_dict = {titel: {"Startdatum": startdatum, "Enddatum": enddatum}}
        dictgant.update(build_dict)

    df = pd.DataFrame(dictgant)
    # Erstellung des Gantt-Charts und Bennenung der Achsen
    fig = px.timeline(df, x_start=startdatum, x_end=enddatum, y=titel)
    # Sortierung der Achse y Titel
    fig.update_yaxes(autorange="reversed")
    # output_type = div, da mit fig.show() die html Seite nicht mehr ersichtlich wäre
    gant = plot(fig, output_type="div")
    # Quelle: https://plotly.com/python/gantt/

    return render_template('analysis.html', viz_bar=bar, data=dictdiagram, viz_gantt=gantt)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
