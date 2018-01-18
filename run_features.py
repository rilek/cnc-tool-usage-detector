"""A"""

import time
start_time = time.time()

import sys
from os import sep
from data_analysis.features import extract_features as extract_features
from config.config import CONFIG as c 


if __name__ == "__main__":

    if len(sys.argv) > 1:
        args = sys.argv[1:]
        _dir = args[0]
        dt = {}

        ft = extract_features(_dir, c)
        print("--- %s seconds ---" % (time.time() - start_time))
        pred_cls = "2"
        if _dir.split(sep)[-1].startswith("Tepe"):
            pred_cls = "1"
        elif _dir.split(sep)[-1].startswith("Ostre"):
            pred_cls = "0"

        # print('{"features":' + str(ft) + ', "class": '+ pred_cls  + '}')
        sys.stdout.flush()
        

