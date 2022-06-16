from flask import Flask
from flask import render_template
from flask import request
import daten

app = Flask(__name__)


# Home / Startseite
@app.route('/', methods=['GET', 'POST'])
def start():
    # wird der Button "Senden" gedrückt, erscheint die Formularseite, sonst normal die Startseite
    if request.method == 'POST':
        return render_template('formular.html')
    return render_template('index.html', user="Samira")  # hier wird der Begrüssungsname mitgegeben (Samira)


# Angaben im Formular erfassen
@app.route("/formular", methods=["POST", "GET"])
def formular():
    # Ausführen, wenn auf den Button senden geklickt wird
    if request.method == "POST":
        # Felder des Formulares definieren
        antragsteller = request.form["antragsteller"]
        projektleiter = request.form["projektleiter"]
        titel = request.form["titel"]
        datum = request.form["datum"]
        # Daten der Felder speichern
        daten.speichern(antragsteller, projektleiter, titel, datum)

        antrag_gespeichert = "Dein Investitionsantrag wurde gespeichert. Falls gewünscht kannst ein weiterer " \
                             "Antrag erfassen werden. "

        return render_template("formular.html", antrag=antrag_gespeichert)

    # Die leeren Felder aus formular.html werden dargestellt. Mittels Speichern Button (POST) werden die Daten mit
    # der Funktion daten.speichern (definiert in der Datei daten.py) im JSON File gespeichert
    return render_template("formular.html")


# Übersicht der Investitionsprojekte -> Daten werden aus daten.py geladen
@app.route("/overview", methods=["GET", "POST"])
def overview():
    eingabe = daten.antrag_laden()
    filter_list = []
    filter_value = ""
    filter_key = ""
    filtered = False

    # if-Bedingung, falls gefiltert werden möchte
    if request.method == 'POST':
        filtered = True
        Projektantrag = request.form['Projektantrag']

        for key, antrag in eingabe.items():  # in dieser for-Schleife wird gefiltert und die leere Liste gefüllt
            if antrag[filter_key] == filter_value:
                filter_list.append(antrag)


    # hier werden die Informationen mitgegeben, die im template "uebersicht" aufgerufen werden können
    return render_template('overview.html', data=eingabe, allitems=filter_list, Filter=filtered)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
