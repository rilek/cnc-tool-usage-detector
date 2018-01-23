"""Features extraction module"""

import sys

import os
sys.path.insert(1, sys.path[0] + os.sep + ".." + os.sep)
import csv
import numpy as np
# from numpy import matrix, mean, median, std, absolute, fft
from pandas import read_csv
from scipy.io import loadmat
# import scipy.stats as ss
from scipy.stats import skew, kurtosis
from bottle import run, request, post, get
# from statsmodels import robust
import matplotlib.pyplot as plt
import json
# import collections
from data_analysis import utils as u
from config.config import CONFIG as c
# import time


FEATURES = {
    "mean": lambda x: np.mean(x),
    "median": lambda x: np.median(x),
    "std": lambda x: np.std(x),
    "var": lambda x: np.var(x),
    "ptp": lambda x: np.ptp(x),
    "skew": lambda x: skew(x),
    "kurtosis": lambda x: kurtosis(x),
    "min": lambda x: min(x),
    "max": lambda x: max(x),
    "rms": lambda x: np.sqrt(np.mean(x**2))
}

def get_features(signal, features):
    """A"""
    
    results = []
    for feature in features:
        results.append( FEATURES[feature](signal) )
    return results

F = c['f']

def get_Hz_index(hz):
    return F.index(next(i for i in F if i >= hz))

def get_Hz_range(signal, _range):
    _from = get_Hz_index(_range[0])
    _to = get_Hz_index(_range[1])

    return signal[_from:_to]

def get_fft(arr, config):
    """Takes array of numbers.
    Returns One-Side FFT of it from 0Hz to 1000Hz."""

    data_fft = np.fft.fft(arr)
    ds_spectrum = np.abs(data_fft/config['L'])
    ss_spectrum = 2*ds_spectrum[0:config['m']]

    return ss_spectrum[0:config['f'].index(next(i for i in config['f'] if i >= 1000))]

def extract_features(file_path, config):
    """Takes path to file with signals.
    Separate specifies signals.
    Computes Mean, Median, STD, Skew, Kurtosis for each one.
    Returns flat array of features"""

    features_list = []
    features_list_fft = []

    if config['TEST_CSV']:
        file_data = read_csv(file_path, header=None)
        signals = [file_data[0].tolist(), file_data[1].tolist()]
    else:
        file_data = loadmat(file_path)
        signals = [np.transpose(file_data[signal])[0] for signal in config['VARS']]


    ffts = [get_fft(signal, config) for signal in signals]

    # print(file_path)

    # print(config['HertzIndex'])
    # plt.plot(xf[61:68], ffts[1][61:68])
    # plt.show()    

    # xf = 2*np.linspace(0.0, 1.0/(2.0*config['T']), config['L']/2)
    # plt.plot(get_Hz_range(xf, [0, 1000]), ffts[1])
    # plt.show()


    # ACC signal features
    features_list.extend(
        get_features(signals[0],
                     ['mean', 'median', 'skew', 'std', 'kurtosis', 'ptp']))
    # ACC FFT
    features_list_fft.extend(
        get_features(get_Hz_range(ffts[0], [150, 250]),
                     ['mean', 'std', 'ptp', 'var', 'skew', 'kurtosis', 'max']))
    # ACC FFT PEAKS
    features_list_fft.extend(
        get_features(get_Hz_range(ffts[0], [190, 210]),
                     ['mean', 'median', 'skew', 'kurtosis', 'rms', 'max']))

    # Mic signal features
    features_list.extend(
        get_features(signals[1],
                     ['median', 'skew', 'std', 'kurtosis', 'ptp', 'min']))
    # Mic FFT
    features_list_fft.extend(
        get_features(get_Hz_range(ffts[1], [150, 250]),
                     ['mean', 'median', 'skew', 'kurtosis', 'rms', 'max']))
    # Mic FFT Peaks
    features_list_fft.extend(
        get_features(get_Hz_range(ffts[1], [190, 210]),
                     ['mean', 'median', 'skew', 'kurtosis', 'rms', 'max']))
    # features_list_fft.extend(
    #     get_features(get_Hz_range(ffts[1], [690, 710]),
    #                  ['max']))



    # return features_list 
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
        u.save_features_to_file(result, csvfilename)
        print("Extracting finished")
        return np.matrix(result)
    else:
        with open(csvfilename, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            result = [np.array([float(i) for i in row]) for row in reader]
            return np.matrix(result)



@post('/')
def index():
    file_name = str(request.body.getvalue(), 'utf-8')
    return json.dumps(extract_features(file_name, c))

def start_server():
    """Starts server"""

    run(host='localhost', port=8082)

if __name__ == "__main__":

    start_server()
    # if len(sys.argv) > 1:
    #     args = sys.argv[1:]
    #     _dir = args[0]
    #     dt = {}
    #     ft = extract_features(_dir, c)
    #     pred_cls = "2"
    #     if _dir.split("/")[-1].startswith("Tepe"):
    #         pred_cls = "1"
    #     elif _dir.split("/")[-1].startswith("Ostre"):
    #         pred_cls = "0"

    #     print('{"features":' + str(ft) + ', "class": '+ pred_cls  + '}')
    #     sys.stdout.flush()
