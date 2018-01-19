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
CLF = joblib.load(sys.path[0] + sep + ".." + sep + "models" + sep + "model.pkl")


@post('/')
def index():
    """Takes dictionary with one kv pair - {'features': array_of_features}.
    Returns predicted class."""

    feats = np.asarray(request.json["features"]).reshape(1, -1)
    return str(int(CLF.predict(feats)[0]))

def start_server():
    """Starts server"""

    run(host='localhost', port=8080)


if __name__ == "__main__":
    start_server()
