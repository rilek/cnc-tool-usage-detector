"""Starts REST API with one endpoint to predict class.
Uses trained model from file."""

import numpy as np
from bottle import run, request, post
import utils as u
import features
from config import CONFIG as c
import json
import io

CLF = u.load_model()


@post('/')
def index():
    """Takes dictionary with one kv pair - {'features': array_of_features}.
    Returns predicted class."""

    # fil = request.json
    # # ftrs = features.extract_features(fil, c)

    # print("ASD")
    # print(fil)
    # return "1";

    features = np.array(dict(request.json)['features']).T
    return str(int(CLF.predict([features])[0]))

def start_server():
    """Starts server"""

    run(host='localhost', port=8080)


if __name__ == "__main__":
    start_server()
