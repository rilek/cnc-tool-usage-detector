"""Utility functions"""

import csv
from sklearn.externals import joblib

def save_features_to_file(features, for_excel=False):
    """Takes matrix of features extracted from training set.
    Saves it to 'features.csv' file"""

    with open("features.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')

        # Required for Excel to handle separator properly
        if for_excel is True:
            writer.writerow(['sep=,'])

        for fil in features:
            writer.writerow(fil)

def load_model(model_path='model.pkl'):
    """Takes optional model file path.
    Returns trained model loaded from file."""

    return joblib.load(model_path)

def print_model_score(name, score):
    """Takes name of model and its score.
    Prints prettified score."""

    print("{}: {} {}%".format(name, ''.join(["."]*(35-len(name)-10)), round(score*100, 2)))
