import os
import requests
import time
from flask import Flask, render_template, jsonify, request, redirect, url_for
import pandas as pd
from joblib import load

app = Flask(__name__)

nodeMCU_ip = "192.168.100.82:80" # change accordingly
variables = ["temp_val", "moist_val", "n_val", "p_val", "k_val"]
last_values = {}

# Load the model and scaler
model = load("svm_model.joblib")
scaler = load("scaler.joblib")


def fetch_sensor_values():
    global last_values
    values = {}  # Dictionary to store values
    for variable_name in variables:
        try:
            response = requests.get(f"http://{nodeMCU_ip}/{variable_name}")
            response.raise_for_status()  # Raise an exception for HTTP errors
            variable = float(response.text)
            values[variable_name] = variable
        except (requests.exceptions.RequestException, ValueError) as e:
            print(f"Error fetching {variable_name}: {e}")
            values[variable_name] = last_values.get(variable_name, None)
    last_values = values
    return values


def classify_values(values):
    # Convert the values dictionary to a DataFrame
    input_values = pd.DataFrame([values])

    # Scale the features using the loaded scaler
    input_values_scaled = scaler.transform(input_values)

    # Make a prediction using the loaded model
    predicted_cured = model.predict(input_values_scaled)

    # Return the classification result
    return "Yes" if predicted_cured[0] else "No"


@app.route("/")
def home():
    return render_template("landing.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/parameters", methods=["GET", "POST"])
def parameters():
    if request.method == "POST":
        seconds = int(request.form["seconds"])
        time.sleep(seconds)
        fetch_sensor_values()
        return redirect(url_for("history"))
    return render_template("parameters.html", values=fetch_sensor_values())


@app.route("/history")
def history():
    values = fetch_sensor_values()
    cured_status = classify_values(values)
    return render_template("history.html", values=values, cured_status=cured_status)


@app.route("/get_sensor_values")
def get_sensor_values():
    return jsonify(fetch_sensor_values())


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
