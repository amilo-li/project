from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/")
def start():
    return render_template("index.html")


@app.route("/overview")
def overview():
    return render_template("overview.html")


@app.route("/formular")
def formular():
    return render_template("formular.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)



