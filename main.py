"""DOCSTRING"""

import gui
import server
from config import CONFIG as c


if __name__ == "__main__":
    gui.start_gui(c)
    server.start_server()
