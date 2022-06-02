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


@app.route("/overview")
def overview():
    return render_template("overview.html")


# # Angaben im Formular erfassen
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


if __name__ == "__main__":
    app.run(debug=True, port=5000)
