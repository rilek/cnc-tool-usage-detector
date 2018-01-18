"""Starts REST API with one endpoint to predict class.
Uses trained model from file."""

import os
import random
from shutil import copy2
import time as t
import utils.utils as u
from config.config import CONFIG as c


def init():
    machine_state = "running"
    from_dir = c['TRAIN_FILES_DIR']
    to_dir = c['TMP_FILES_DIR']
    file_list = os.listdir(from_dir)

    while machine_state == "running":
        copy2(from_dir + random.choice(file_list), to_dir)
        t.sleep(5)


init()
