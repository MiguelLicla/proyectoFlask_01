import numpy as np
import tensorflow as tf
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Carga el modelo preentrenado TFLite
interp = tf.lite.Interpreter(model_path="model_c2f.tflite")
interp.allocate_tensors()
inp_det = interp.get_input_details()
out_det = interp.get_output_details()


def predecir(celsius):
    interp.set_tensor(inp_det[0]['index'], np.array([[celsius]], dtype=np.float32))
    interp.invoke()
    return float(interp.get_tensor(out_det[0]['index'])[0][0])


@app.route("/")
def inicio():
    return render_template("login.html", mensaje="")


@app.route("/login", methods=["POST"])
def login():
    usuario = request.form.get("usuario")
    clave = request.form.get("clave")

    if usuario == "admin" and clave == "1234":
        return f"<h1>Bienvenido, {usuario}</h1><p>Acceso correcto.</p>"
    else:
        return render_template("login.html", mensaje="Usuario o contraseña incorrectos")


@app.route("/convertir", methods=["GET"])
def convertir_page():
    return render_template("convertir.html")


@app.route("/convertir", methods=["POST"])
def convertir():
    datos = request.get_json()
    celsius_val = float(datos.get("celsius", 0))
    fahrenheit_val = predecir(celsius_val)
    return jsonify({"celsius": celsius_val, "fahrenheit": round(fahrenheit_val, 2)})


if __name__ == "__main__":
    app.run(debug=True)
