"""Utility functions"""

import sys
import csv
from sklearn.externals import joblib
from colorama import init, Fore, Style

init()

def save_features_to_file(features, filename, for_excel=False):
    """Takes matrix of features extracted from training set.
    Saves it to 'features.csv' file"""

    with open(filename, "w+", newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')

        # Required for Excel to handle separator properly
        if for_excel is True:
            writer.writerow(['sep=,'])

        for fil in features:
            writer.writerow(fil)

def load_model(model_path='model.pkl'):
    """Takes optional model file path.
    Returns trained model loaded from file."""

    return joblib.load(sys.path[0] + "\\models\\" + model_path)

COLORS = {
    "black": Fore.BLACK,
    "red": Fore.RED,
    "green": Fore.GREEN,
    "yellow": Fore.YELLOW,
    "blue": Fore.BLUE,
    "magenta": Fore.CYAN,
    "white": Fore.WHITE,
    "bold": Style.BRIGHT
}

def pprint(text, color='', end='\n'):
    """Takes text string and color string.
    Prints to console with color."""
    colors = COLORS[color]
    print(colors + text + Style.RESET_ALL, end=end)

def print_model_score(name, score, n):
    """Takes name of model and its score.
    Prints prettified score."""

    print("{}. {}: {} {} {}% {}"
          .format(n,
                  name,
                  ''.join(["."]*(35-len(name)-10)),
                  Style.BRIGHT,
                  round(score*100, 2),
                  Style.RESET_ALL))


def print_cm(cm, labels, hide_zeroes=False, hide_diagonal=False, hide_threshold=None):
    """pretty print for confusion matrixes"""

    columnwidth = max([len(x) for x in labels] + [5])  # 5 is value length
    empty_cell = " " * columnwidth
    # Print header
    print("    " + empty_cell, end=" ")
    for label in labels:
        pprint("%{0}s".format(columnwidth) % label, 'bold', end=" ")
    print()
    # Print rows
    for i, label1 in enumerate(labels):
        pprint("    %{0}s".format(columnwidth) % label1, 'bold', end=" ")
        for j in range(len(labels)):
            cell = "%{0}.1f".format(columnwidth) % cm[i, j]
            if hide_zeroes:
                cell = cell if float(cm[i, j]) != 0 else empty_cell
            if hide_diagonal:
                cell = cell if i != j else empty_cell
            if hide_threshold:
                cell = cell if cm[i, j] > hide_threshold else empty_cell
            print(cell, end=" ")
        print()
