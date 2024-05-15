# sample_fetch_server.py

import random
from flask import Flask

app = Flask(__name__)

# Simulated values
temp_val = 25.0
moist_val = 50.0
n_val = 10.0
p_val = 5.0
k_val = 8.0

# Route to fetch each variable
@app.route('/temp_val')
def get_temp_val():
    global temp_val
    # Simulate temperature fluctuation
    temp_val += random.uniform(-0.5, 0.5)
    return str(temp_val)

@app.route('/moist_val')
def get_moist_val():
    global moist_val
    # Simulate moisture fluctuation
    moist_val += random.uniform(-2, 2)
    moist_val = max(0, min(100, moist_val))  # Clamp within 0-100 range
    return str(moist_val)

@app.route('/n_val')
def get_n_val():
    global n_val
    # Simulate nitrogen fluctuation
    n_val += random.uniform(-1, 1)
    n_val = max(0, n_val)  # Ensure non-negative value
    return str(n_val)

@app.route('/p_val')
def get_p_val():
    global p_val
    # Simulate phosphorous fluctuation
    p_val += random.uniform(-0.5, 0.5)
    p_val = max(0, p_val)  # Ensure non-negative value
    return str(p_val)

@app.route('/k_val')
def get_k_val():
    global k_val
    # Simulate potassium fluctuation
    k_val += random.uniform(-0.3, 0.3)
    k_val = max(0, k_val)  # Ensure non-negative value
    return str(k_val)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
