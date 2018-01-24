"""A"""

import sys
import emulator.machine as machine


def init():
    """Init function"""

    experiment = 1
    if len(sys.argv) > 1:
        experiment = int(sys.argv[1])

    machine.init(experiment)


init()
