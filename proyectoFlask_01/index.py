import numpy as np
import tensorflow as tf
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Modelo TensorFlow: aprende la conversión Celsius -> Fahrenheit
celsius    = np.array([-40, -10,  0,  8, 15,  22,  38], dtype=float)
fahrenheit = np.array([-40,  14, 32, 46.4, 59, 71.6, 100.4], dtype=float)

modelo = tf.keras.Sequential([
    tf.keras.layers.Dense(units=1, input_shape=[1])
])
modelo.compile(optimizer=tf.keras.optimizers.Adam(0.5), loss='mean_squared_error')
modelo.fit(celsius, fahrenheit, epochs=500, verbose=0)


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


@app.route("/convertir", methods=["POST"])
def convertir():
    datos = request.get_json()
    celsius_val = float(datos.get("celsius", 0))
    resultado = modelo.predict(np.array([celsius_val]), verbose=0)[0][0]
    return jsonify({"celsius": celsius_val, "fahrenheit": round(float(resultado), 2)})


if __name__ == "__main__":
    app.run(debug=True)
