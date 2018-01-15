"""Features extraction module"""

import sys
import os
import csv
import numpy as np
import pandas as pd
import scipy.io as sio
import scipy.stats as ss
from statsmodels import robust
import utils as u
import matplotlib.pyplot as plt
import json
import collections
from config import CONFIG as c


def get_fft(arr, config):
    """Takes array of numbers.
    Returns One-Side FFT of it."""

    data_fft = np.fft.fft(arr)
    ds_spectrum = np.abs(data_fft/config['L'])
    ss_spectrum = 2*ds_spectrum[0:config['m']]

    return ss_spectrum[config['HertzIndex_min']:config['HertzIndex']]

def extract_features(file_path, config):
    """Takes path to file with signals.
    Separate specifies signals.
    Computes Mean, Median, STD, Skew, Kurtosis and MAD for each one.
    Returns flat array of features"""
    if config['TEST_CSV']:
        file_data = pd.read_csv(file_path, header=None)
        signals = [file_data[0].tolist(), file_data[1].tolist()]
    else:
        file_data = sio.loadmat(file_path)
        signals = [np.transpose(file_data[signal])[0] for signal in config['VARS']]


    ffts = [get_fft(signal, config) for signal in signals]
    # signals.extend(ffts)


    # print(file_path)

    # print(config['HertzIndex'])
    # xf = 2*np.linspace(0.0, 1.0/(2.0*config['T']), config['L']/2)
    # plt.plot(xf[61:68], ffts[1][61:68])
    # plt.show()
    # shown = True

    features_list = []
    for signal in signals:
        # print(rms(signal))
        features_list.extend([
            np.mean(signal),
            np.median(signal),
            np.std(signal),
            ss.skew(signal),
            ss.kurtosis(signal)
        ])


    features_list_fft = []
    for signal in ffts:
        # PEAK IDXS [61:68]
        peak = signal[61-config['HertzIndex_min']:68-config['HertzIndex_min']]

        features_list_fft.extend([
            np.mean(signal),
            # np.median(signal),
            np.std(signal),
            ss.skew(signal),
            np.sqrt(np.mean(signal**2)),
            ss.kurtosis(signal),
            np.var(signal),
            np.ptp(signal)
        ])

        features_list_fft.extend([
            np.mean(peak),
            np.median(peak),
            np.std(peak),
            ss.skew(peak),
            np.sqrt(np.mean(peak**2)),
            ss.kurtosis(peak),
            np.var(peak),
            np.ptp(peak)
        ])

    return features_list + features_list_fft


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

# if __name__ == "__main__":
#     if len(sys.argv) > 1:
#         args = sys.argv[1:]
#         _dir = args[0]
#         dt = {}
#         np.set_printoptions(threshold=sys.maxsize)
#         ft = extract_features(_dir, c)
#         pred_cls = "2"
#         if _dir.split("/")[-1].startswith("Tepe"):
#             pred_cls = "1"
#         elif _dir.split("/")[-1].startswith("Ostre"):
#             pred_cls = "0"

#         print('{"features":' + str(ft) + ', "class": '+ pred_cls  + '}')
#         sys.stdout.flush()
