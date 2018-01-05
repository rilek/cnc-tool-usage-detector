"""Utility functions"""

import os
import csv
import numpy as np
import scipy.io as sio
import scipy.stats as ss
from statsmodels import robust

from config import CONFIG as c

def rms(arr):
    return float(np.sqrt(np.mean([x*x for x in arr])))


def getFFT(arr):
    dataFFT = np.fft.fft(arr)
    P2 = np.abs(dataFFT/c['L'])
    P1 = P2[0:c['m']]
    P1 = 2*P1

    return P1[0:c['thousandHertsIndex']]


def extract_features(file_data):
    """FN DOSCSTING"""
    signals = [np.transpose(file_data[signal])[0] for signal in c['VARS']]
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

def get_signal_features(file_names, dir="", exists=False, csvfilename=''):
    """FN DOCSTRING"""

    if exists is False:
        result = [extract_features(sio.loadmat(dir + item))
                  for item in file_names]
        save_features_to_file(result)
        return np.matrix(result)
    else:
        with open(csvfilename, 'r', newline='') as csvfile:
            return np.matrix(csvfile)


def save_features_to_file(features):
    """FN DOCSTRING"""

    with open("features.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['sep=,'])
        for f in features:
            writer.writerow(f)
