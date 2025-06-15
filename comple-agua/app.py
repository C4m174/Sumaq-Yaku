from flask import Flask, render_template, request, jsonify
from distribucion_agua import ejecutar_algoritmos

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("interfaz.html")

@app.route("/procesar", methods=["POST"])
def procesar():
    datos = request.get_json()
    region = datos.get("region")

    try:
        resultado = ejecutar_algoritmos(region)
        return jsonify({
            "rutas_optimas": resultado["rutas_optimas"],
            "flujos_maximos": resultado["flujos_maximos"]
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True)

