"""Starts REST API with one endpoint to predict class.
Uses trained model from file."""

import os
import random
from shutil import copy2, rmtree
import time as t
from utilities import utils as u
from config.config import CONFIG as c


def init():
    """A"""

    machine_state = "running"
    from_dir = c['TRAIN_FILES_DIR']
    to_dir = c['TMP_FILES_DIR']
    file_list = os.listdir(from_dir)

    while machine_state == "running":
        copy2(from_dir + random.choice(file_list), to_dir)
        tmp_files = os.listdir(to_dir)
        if len(os.listdir(to_dir)) >= 10:
            for f in tmp_files:
                os.remove(to_dir + f)
        t.sleep(1)


init()
