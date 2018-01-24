"""Starts REST API with one endpoint to predict class.
Uses trained model from file."""

import sys
from os import sep
sys.path.insert(1, sys.path[0] + sep + ".." + sep)

from sklearn.externals import joblib
import ast
import numpy as np
import json
from bottle import run, request, post
from data_analysis import utils as u
from config.config import CONFIG as c

CLF_MAT = joblib.load(c['MODEL_MAT_FILE'])
CLF_CSV = joblib.load(c['MODEL_CSV_FILE'])

@post('/')
def index():
    """Takes dictionary with one kv pair - {'features': array_of_features}.
    Returns predicted class."""

    print("EXPERIMENT" + str(request.json["experiment"]))
    feats = np.asarray(request.json["features"]).reshape(1, -1)
    pred = ""
    experiment = request.json["experiment"] or 1
    if experiment == 1:
        pred = CLF_MAT.predict(feats)[0]
    elif experiment == 2:
        pred = CLF_CSV.predict(feats)[0]


    if isinstance(pred, str):
        print(pred)
    return str(int(pred))

def start_server():
    """Starts server"""

    run(host='localhost', port=8080)


if __name__ == "__main__":
    start_server()
