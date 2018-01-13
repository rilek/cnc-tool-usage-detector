"""CONFIGURATION CONSTS"""

import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis


FS = 25000
L = 16000
T = 1/FS
M = int(L/2)
F = [2*FS*(x)/L for x in list(range(0, M))]
CLASSIFIERS = [
    ["Nearest Neighbors", KNeighborsClassifier(3)],
    ["Linear SVM", SVC(kernel="linear", C=1)],
    ["RBF SVM", SVC(gamma=2, C=1)],
    ["Decision Tree", DecisionTreeClassifier()],
    ["Random Forest", RandomForestClassifier()],
    ["Neural Net", MLPClassifier(alpha=1)],
    ["AdaBoost", AdaBoostClassifier()],
    ["Naive Bayes", GaussianNB()],
    ["QDA", QuadraticDiscriminantAnalysis()]
]


CONFIG = {
    'VARS': ['AccXSignal', 'VelZSignal', 'AccXSignal1', 'MicSignal'],
    'TRAIN_FILES_DIR': 'train/',
    'TRAIN_FILES_LAST_GOOD': 552,
    'TRAIN_PERCENT': 0.9,
    'CLASSIFIERS': CLASSIFIERS,
    'Fs': FS,
    'T': T,
    'L': L,
    't': np.linspace(0.0, L*T, L),
    'm': M,
    'f': F,
    'thousandHertsIndex': F.index(next(i for i in F if i > 1000)),
    'EXISTS': True
}
