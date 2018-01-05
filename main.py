"""DOCSTRING"""
import os
import numpy as np
from sklearn import metrics

from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

import utils as u
from config import CONFIG as c


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


# u.group_train_files(c.TRAIN_FILES_DIR)

TRAIN_FILES = [f for f in os.listdir(c['TRAIN_FILES_DIR'])]
TRAIN_FILES_LEN = len(TRAIN_FILES)

X = u.get_signal_features(TRAIN_FILES, c['TRAIN_FILES_DIR'], False, 'features.csv')
Y = np.matrix([0]*c['TRAIN_FILES_LAST_GOOD'] + [1]*(TRAIN_FILES_LEN - c['TRAIN_FILES_LAST_GOOD']))

DATA = np.hstack((X, np.transpose(Y)))


X_train, X_test, y_train, y_test = train_test_split(DATA[:, :-1],
                                                    DATA[:, -1],
                                                    shuffle=True,
                                                    train_size=c['TRAIN_PERCENT'],
                                                    test_size=1-c['TRAIN_PERCENT'],
                                                    random_state=0)

for name, clf in CLASSIFIERS:
    clf.fit(X_train, y_train)
    score = clf.score(X_test, y_test)
    print("{}: {}%".format(name, round(score*100, 2)))
