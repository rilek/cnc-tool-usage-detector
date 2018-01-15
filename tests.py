# import math
# import scipy.io as sio
# import numpy as np
# import config as c
# import scipy.stats as ss
# from statsmodels import robust
# import os
# import math
# import random
# import csv
# import graphviz
# from sklearn import tree
# import numpy as np
# import utils as u
# import config as c
# from sklearn.model_selection import train_test_split
# from sklearn import metrics
# import scipy.stats as ss
# import scipy.signal as ssi
# import matplotlib.pyplot as plt
# import statsmodels.api as sm
# import pandas as pd

# from scipy.fftpack import fft

# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import StandardScaler
# from sklearn.datasets import make_moons, make_circles, make_classification
# from sklearn.neural_network import MLPClassifier
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.neighbors import LocalOutlierFactor
# from sklearn.svm import SVC
# from sklearn.gaussian_process import GaussianProcessClassifier
# from sklearn.gaussian_process.kernels import RBF
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
# from sklearn.naive_bayes import GaussianNB
# from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
# import scipy.fftpack

# TRAIN_FILES = [f for f in os.listdir(c['TRAIN_FILES_DIR'])]

# single_file = sio.loadmat( c['TRAIN_FILES_DIR'] + 'Ostre1_165.mat')

# Acc = single_file['AccXSignal']
# AccFFT = np.fft.fft(np.transpose(Acc)[0])

# P2 = np.abs(AccFFT/L)
# m = int(L/2)
# P1 = P2[0:m]
# P1 = 2*P1
# f = [Fs*(x)/L for x in list(range(0, m))]

# print(f.index(next(i for i in f if i > 1000))-1)
# u.extract_features(single_file)

# # print(P1.shape)

# plt.plot(f, P1)
# axes = plt.gca()
# axes.set_xlim([0, 1000])
# plt.show()

# x = np.linspace(0.0, N*T, N)
# # y = np.sin(50.0 * 2.0*np.pi*x) + 0.5*np.sin(80.0 * 2.0*np.pi*x)
# yf = rfft(y_axis)
# xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
# print(xf)
# import matplotlib.pyplot as plt
# plt.plot(x_axis, 2.0/N * np.abs(ifft(yf)))
# plt.grid()
# plt.show()

# y = pd.Series(y_axis, index = x_axis)
