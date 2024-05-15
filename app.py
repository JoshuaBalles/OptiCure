import os
import requests
import time
from flask import Flask, render_template, jsonify

app = Flask(__name__)

nodeMCU_ip = '192.168.100.82:80'
variables = ['temp_val', 'moist_val', 'n_val', 'p_val', 'k_val']

def fetch_sensor_values():
    values = {}  # Dictionary to store values
    for variable_name in variables:
        response = requests.get(f'http://{nodeMCU_ip}/{variable_name}')
        variable = float(response.text)
        values[variable_name] = variable
    return values

@app.route("/")
def home():
    return render_template("landing.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/parameters")
def parameters():
    return render_template("parameters.html", values=fetch_sensor_values())

@app.route("/history")
def history():
    return render_template("history.html")

@app.route("/get_sensor_values")
def get_sensor_values():
    return jsonify(fetch_sensor_values())

if __name__ == "__main__":
    app.run(debug=True)
