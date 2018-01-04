"""DOCSTRING"""
import os
import math
import random
import csv
import graphviz
from sklearn import tree
import numpy as np
import utils as u
import config as c
from sklearn.model_selection import train_test_split
from sklearn import metrics
import scipy.stats as ss
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_moons, make_circles, make_classification
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import LocalOutlierFactor
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

h = .02  # step size in the mesh

classifiers = [
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


TRAIN_FILES = [f for f in os.listdir(c.TRAIN_FILES_DIR)]
TRAIN_FILES_LEN = len(TRAIN_FILES)

X = u.load_train_files(TRAIN_FILES, dir=c.TRAIN_FILES_DIR)
Y = np.matrix([0]*c.TRAIN_FILES_LAST_GOOD + [1]*(TRAIN_FILES_LEN - c.TRAIN_FILES_LAST_GOOD))

DATA = np.hstack((X, np.transpose(Y)))

TRAIN_SIZE = 0.9

X_train, X_test, y_train, y_test = train_test_split(DATA[:, :-1], DATA[:, -1], shuffle=True, train_size=TRAIN_SIZE, test_size=1-TRAIN_SIZE, random_state=0)

for name, clf in classifiers:
    clf.fit(X_train, y_train)
    score = clf.score(X_test, y_test)
    print("{}: {}%".format(name, round(score*100, 2)))

# sclf = SVC
# for i in np.arange(0.5,3,0.5):
#     clf = sclf(kernel="poly", C=i)
#     clf.fit(X_train, y_train)
#     score = clf.score(X_test, y_test)
#     print("{}: {}%".format("SVC", round(score*100, 2)))


# CLF = tree.DecisionTreeClassifier()
# CLF = CLF.fit(X_train, y_train)

# y_pred_class = CLF.predict(X_test)

# print( metrics.accuracy_score(y_test, y_pred_class) )

# CLF = tree.DecisionTreeClassifier()
# CLF = CLF.fit(TRAIN_DATA_X, TRAIN_DATA_Y)

# dot_data = tree.export_graphviz(CLF2, out_file=None)
# graph = graphviz.Source(dot_data)
# graph.render("iris")

# precision = 0
# guessed = 0

# TEST_DATA_LEN = len(TEST_DATA)
# for row in TEST_DATA:
#     x = row[:, :-1]
#     y = row[:, -1].tolist()[0][0]
#     score = CLF2.predict(x)[0]
#     if score == y:
#         guessed = guessed + 1 
#     print('predicted: ', score, " . Was: ", y, ". Precision: ", round(guessed/TEST_DATA_LEN * 100), "%")

# random_row = random.choice(list(TEST_DATA))
# random_x = random_row[:,:-1].tolist()
# random_y = random_row[:,-1].tolist()[0][0]
# print('predicted: ', CLF2.predict(random_x), " . Was: ", random_y)


# with open('data.csv', 'w', newline='') as csvfile:
#     writer = csv.writer(csvfile, delimiter=',')
#     writer.writerow(['X'+str(i+1) for i in range(DATA.shape[1]-1)] + ['Y'])
#     for row in DATA:
#         writer.writerow(row.tolist()[0])


# with open('train_data.csv', 'w', newline='') as csvfile:
#     writer = csv.writer(csvfile, delimiter=',')
#     writer.writerow(['X'+str(i+1) for i in range(TRAIN_DATA.shape[1]-1)] + ['Y'])
#     for row in TRAIN_DATA:
#         writer.writerow(row.tolist()[0])

# with open('test_data.csv', 'w', newline='') as csvfile:
#     writer = csv.writer(csvfile, delimiter=',')
#     writer.writerow(['X'+str(i+1) for i in range(TEST_DATA.shape[1]-1)] + ['Y'])
#     for row in TEST_DATA:
#         writer.writerow(row.tolist()[0])
