"""Utility functions"""

import math
import scipy.io as sio
import numpy as np
import config as c
import scipy.stats as ss
from sklearn.metrics import mean_squared_error
from statsmodels import robust
import matplotlib.pyplot as plt

def rms(arr):
    return float(np.sqrt(np.mean(np.square(arr))))

Fs = 25000
T = 1/Fs
L = 16000
t = np.linspace(0.0, L*T, L)
m = int(L/2)
f = [2*Fs*(x)/L for x in list(range(0, m))]
thousandHertsIndex = f.index(next(i for i in f if i > 1000))

def getFFT(arr):
    dataFFT = np.fft.fft(arr)
    P2 = np.abs(dataFFT/L)
    P1 = P2[0:m]
    P1 = 2*P1

    return P1[0:thousandHertsIndex]


def extract_features(file_data):
    """FN DOSCSTING"""
    signals = [np.transpose(file_data[signal])[0] for signal in c.VARS]
    ffts = [getFFT(signal) for signal in signals]
    signals.extend(ffts)

    features_list = []
    for signal in signals:
        # signal = np.abs(signal)
        # print(rms(signal))
        features_list.extend([
            np.mean(signal),
            np.median(signal),
            np.std(signal),
            ss.skew(signal),
            ss.kurtosis(signal),
            robust.mad(signal)
        ])
    return features_list

def load_train_files(file_names, dir=""):
    """FN DOCSTRING"""
    result = []
    for item in file_names:
        result.append(extract_features(sio.loadmat(dir + item)))
    return np.matrix(result)