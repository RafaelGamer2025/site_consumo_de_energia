from flask import Flask, render_template
from flask import jsonify
from flask import request

from funcoes import monitor_pc
from funcoes import calcular_energia
from funcoes import gerar_ideias

app = Flask(__name__)

@app.route("/")
def home():

    return render_template("index.html")

@app.route("/monitor")
def monitor():

    dados = monitor_pc()

    return jsonify(dados)

@app.route("/calcular", methods=["POST"])
def calcular():

    dados = request.json

    resultado = calcular_energia(dados)

    ideias = gerar_ideias(resultado)

    resultado["ideias"] = ideias

    return jsonify(resultado)

if __name__ == "__main__":
    app.run(debug=True)