"""DOCSTRING"""

import json
import requests
from appJar import gui
import features as f
from config import CONFIG as c

import datetime

API_URL = 'http://localhost:8080'
HEADERS = {"Content-Type": "application/json"}
APP = gui()

def send_request(features):
    """Takes array of signal features
    Sends POST request to API_URL with features
    Returns response (predicted class)"""

    body = json.dumps({'features': features})
    res = requests.post(API_URL, headers=HEADERS, data=body)
    return res.text

def press(button, config):
    """Takes button name
    Executes action assigned to button"""

    if button == "SEND":
        ts = datetime.datetime.now()

        file_path = APP.getEntry("f")
        features = f.extract_features(file_path, config)
        response = send_request(features)

        tf = datetime.datetime.now()
        print(tf-ts)

        if response == "1":
            APP.setLabelBg("result", "red")
            APP.setLabel("resultText", "Tępe")
        elif response == "0":
            APP.setLabelBg("result", "green")
            APP.setLabel("resultText", "Ostre")
        return True

def start_gui(config):
    """Starts GUI app"""

    # PYLINT does not recognize inner config variable
    # pylint: disable=E0602
    press_fn = (lambda config: lambda button: press(button, config))(config)

    APP.addLabel("result", " ", 0, 0, 1)
    APP.setLabelBg("result", "gray")
    APP.addLabel("resultText", "Waiting", 0, 1, 2)

    APP.addFileEntry("f", 1, 0, 3)
    APP.addButton("SEND",
                  press_fn,
                  2, 0, 3)

    APP.go()


if __name__ == "__main__":
    start_gui(c)
