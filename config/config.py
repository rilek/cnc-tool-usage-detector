"""CONFIGURATION CONSTS"""

import sys, os, inspect
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB

ROOT_FOLDER = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + os.sep + '..' + os.sep
CLASSIFIERS = [
    ["Nearest Neighbors", KNeighborsClassifier()],
    ["Linear SVM", SVC(kernel="linear")],
    ["Decision Tree", DecisionTreeClassifier()],
    ["Random Forest", RandomForestClassifier()],
    ["Neural Net", MLPClassifier()],
    ["AdaBoost", AdaBoostClassifier()],
    ["Naive Bayes", GaussianNB()],
]


FS = 25000
L = 16000
T = 1/FS
M = int(L/2)
F = [2*FS*(x)/L for x in list(range(0, M))]

TEST_CSV = True
VER = "v1"
LAST_NEW_GOOD = 928 if VER == "v1" else 686
TRAIN_FILES_DIR_CSV = 'train_data/new_train/final/'+VER+'/'
TRAIN_FILES_DIR_MAT = 'train_data/train/'
TRAIN_FILES_DIR = TRAIN_FILES_DIR_CSV if TEST_CSV is True else TRAIN_FILES_DIR_MAT
LAST_GOOD = LAST_NEW_GOOD if TEST_CSV is True else 552
MODEL_FILE_SUFIX = "mat" if not TEST_CSV else "csv"

CONFIG = {
    'VARS': ['AccXSignal', 'MicSignal'],
    'TMP_FILES_DIR': 'tmp_files/',
    'TRAIN_FILES_DIR': TRAIN_FILES_DIR,
    'TRAIN_FILES_DIR_CSV': TRAIN_FILES_DIR_CSV,
    'TRAIN_FILES_DIR_MAT': TRAIN_FILES_DIR_MAT,
    'NEW_TRAIN_FILES_DIR': 'train_data/new_train/',
    'TRAIN_FILES_LAST_GOOD': LAST_GOOD,
    'VER': VER + '/',
    'TEST_CSV': TEST_CSV,
    'TRAIN_PERCENT': 0.9,
    'CLASSIFIERS': CLASSIFIERS,
    'FEATURES_EXISTS': False,
    'FEATURES_FILE': ROOT_FOLDER + 'data_analysis' + os.sep + 'csv' + os.sep + 'features.csv',
    'MODEL_FILE': ROOT_FOLDER + 'models' + os.sep + 'model_' + MODEL_FILE_SUFIX + '.pkl',
    'MODEL_MAT_FILE': ROOT_FOLDER + 'models' + os.sep + 'model_mat.pkl',
    'MODEL_CSV_FILE': ROOT_FOLDER + 'models' + os.sep + 'model_csv.pkl',
    'Fs': FS,
    'T': T,
    'L': L,
    't': np.linspace(0.0, L*T, L),
    'm': M,
    'f': F
}
