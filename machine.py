"""Starts REST API with one endpoint to predict class.
Uses trained model from file."""

import time as t
import numpy as np
from bottle import run, request, get
import utils as u

machine_state = "running"

while machine_state == "running":
    with open("./tmp_files/file_" + str(round(t.time()*1000)) + ".mat", "w+") as f:
        f.write("DUPA")
    t.sleep(5)
# if __name__ == "__main__":
