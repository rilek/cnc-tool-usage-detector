"""Features extraction module"""

import os
import csv
import numpy as np
import scipy.io as sio
import scipy.stats as ss
from statsmodels import robust
import utils as u


def get_fft(arr, config):
    """Takes array of numbers.
    Returns One-Side FFT of it."""

    data_fft = np.fft.fft(arr)
    ds_spectrum = np.abs(data_fft/config['L'])
    ss_spectrum = 2*ds_spectrum[0:config['m']]

    return ss_spectrum[0:config['thousandHertsIndex']]

def extract_features(file_path, config):
    """Takes path to file with signals.
    Separate specifies signals.
    Computes Mean, Median, STD, Skew, Kurtosis and MAD for each one.
    Returns flat array of features"""
    file_data = sio.loadmat(file_path)
    signals = [np.transpose(file_data[signal])[0] for signal in config['VARS']]
    # ffts = [get_fft(signal, config) for signal in signals]
    # signals.extend(ffts)

    features_list = []
    for signal in signals:
        signal_abs = np.abs(signal)
        # print(rms(signal))
        features_list.extend([
            np.mean(signal_abs),
            np.median(signal_abs),
            np.std(signal),
            ss.skew(signal),
            ss.kurtosis(signal),
            # robust.mad(signal)
        ])
    return features_list

def get_signal_features(directory, config, exists=True, csvfilename='features.csv'):
    """Takes directory path, and two optional arguments.
    If exists if True, then features are taken from 'csvfilename' file
    Else features are computed from every *.mat file in directory
    Returns matrix of features"""

    if exists is False:
        print("Extracting features from files")
        result = [extract_features(directory + item, config)
                  for item in os.listdir(directory)]
        u.save_features_to_file(result)
        print("Extracting finished")
        return np.matrix(result)
    else:
        with open(csvfilename, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            result = [np.array([float(i) for i in row]) for row in reader]
            return np.matrix(result)
