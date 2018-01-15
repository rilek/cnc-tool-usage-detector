"""CONFIGURATION CONSTS"""

import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis


CLASSIFIERS = [
    ["Nearest Neighbors", KNeighborsClassifier()],
    ["Linear SVM", SVC(kernel="linear")],
    ["RBF SVM", SVC()],
    ["Decision Tree", DecisionTreeClassifier()],
    ["Random Forest", RandomForestClassifier()],
    ["Neural Net", MLPClassifier()],
    ["AdaBoost", AdaBoostClassifier()],
    ["Naive Bayes", GaussianNB()],
    ["QDA", QuadraticDiscriminantAnalysis()]
]

FS = 25000
L = 16000
T = 1/FS
M = int(L/2)
F = [2*FS*(x)/L for x in list(range(0, M))]

TEST_CSV = True
# VER = ""
# TRAIN_FILES_DIR = ('new_train/final_f/' + VER) if TEST_CSV is True else 'train/'
# LAST_GOOD = 1892 if TEST_CSV is True else 552
VER = "v2/"
TRAIN_FILES_DIR = ('new_train/final/' + VER) if TEST_CSV is True else 'train/'
LAST_GOOD = 686 if TEST_CSV is True else 552

CONFIG = {
    # 'VARS': ['AccXSignal', 'VelZSignal', 'AccXSignal1', 'MicSignal'],
    'VARS': ['AccXSignal', 'MicSignal'],
    'TMP_FILES_DIR': 'tmp_files/',
    'TRAIN_FILES_DIR': TRAIN_FILES_DIR,
    'NEW_TRAIN_FILES_DIR': 'new_train/',
    'TRAIN_FILES_LAST_GOOD': LAST_GOOD,
    'VER': VER,
    'TEST_CSV': TEST_CSV,
    'TRAIN_PERCENT': 0.9,
    'CLASSIFIERS': CLASSIFIERS,
    'EXISTS': False,
    'FEATURES_FILE': 'features2.csv',
    'Fs': FS,
    'T': T,
    'L': L,
    't': np.linspace(0.0, L*T, L),
    'm': M,
    'f': F,
    'HertzIndex': F.index(next(i for i in F if i > 500)),
    'HertzIndex_min': F.index(next(i for i in F if i > 0)),
}
