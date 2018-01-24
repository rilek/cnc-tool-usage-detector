"""Features extraction module"""

import sys
import os
import csv
import json
import numpy as np
from pandas import read_csv
from scipy.io import loadmat
from scipy.stats import skew, kurtosis
from bottle import run, request, post
sys.path.insert(1, sys.path[0] + os.sep + ".." + os.sep)
from data_analysis import utils as u
from config.config import CONFIG as c


F = c['f']
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


def get_Hz_index(hz):
    """Get index of specific HZ in FFT signal"""
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

def get_single_signal_features(signal, features):
    """Get signals features"""

    results = []
    for feature in features:
        results.append(FEATURES[feature](signal))
    return results

def get_features(signals, ffts, c, experiment=None):
    """Get features"""

    features_list = []
    if experiment == 1:
        features_list = get_old_data_features(signals, ffts)
    elif experiment == 2:
        features_list = get_v1_data_features(signals, ffts)
    elif c['TEST_CSV'] is False:
        features_list = get_old_data_features(signals, ffts)
    elif c['VER'] == 'v1/':
        features_list = get_v1_data_features(signals, ffts)
    elif c['VER'] == 'v2/':
        features_list = get_v2_data_features(signals, ffts)

    return features_list

def extract_features(file_path, config, experiment=None):
    """Takes path to file with signals.
    Separate specifies signals.
    Computes Mean, Median, STD, Skew, Kurtosis for each one.
    Returns flat array of features"""

    file_extension = file_path.split(".")[-1]
    experiment = 1 if file_extension == "mat" else 2

    if file_extension == "csv":
        file_data = read_csv(file_path, header=None)
        signals = [file_data[0].tolist(), file_data[1].tolist()]
    elif file_extension == "mat":
        file_data = loadmat(file_path)
        signals = [np.transpose(file_data[signal])[0] for signal in config['VARS']]

    ffts = [get_fft(signal, config) for signal in signals]

    return get_features(signals, ffts, config, experiment)

def get_signal_features(directory, config, exists=False, csvfilename='features.csv'):
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

def get_old_data_features(signals, ffts):
    results = []

    # ACC signal features
    results.extend(
        get_single_signal_features(signals[0],
                                   ['median', 'skew', 'std', 'kurtosis']))
    # ACC FFT
    results.extend(
        get_single_signal_features(ffts[0],
                                   ['median', 'std', 'skew', 'kurtosis']))
    # ACC FFT pt2
    results.extend(
        get_single_signal_features(get_Hz_range(ffts[0], [42, 62]),
                                   ['mean', 'median', 'std', 'skew']))

    # Mic signal features
    results.extend(
        get_single_signal_features(signals[1],
                                   ['median', 'skew', 'std', 'kurtosis']))
    # Mic FFT
    results.extend(
        get_single_signal_features(ffts[1],
                                   ['median', 'std', 'skew', 'kurtosis']))
    # # Mic FFT Peaks
    results.extend(
        get_single_signal_features(get_Hz_range(ffts[1], [42, 62]),
                                   ['mean', 'median', 'std', 'skew']))
    return results

def get_v1_data_features(signals, ffts):
    results = []

    # ACC signal features
    results.extend(
        get_single_signal_features(signals[0],
                                   ['median', 'skew', 'std', 'kurtosis']))
    # ACC FFT
    results.extend(
        get_single_signal_features(ffts[0],
                                   ['mean', 'median', 'std', 'skew', 'kurtosis']))
    # ACC FFT PEAKS
    results.extend(
        get_single_signal_features(get_Hz_range(ffts[0], [42, 62]),
                                   ['mean', 'median', 'std', 'skew', 'rms']))

    # Mic signal features
    results.extend(
        get_single_signal_features(signals[1],
                                   ['median', 'skew', 'std', 'kurtosis']))
    # Mic FFT
    results.extend(
        get_single_signal_features(ffts[1],
                                   ['mean', 'median', 'std', 'skew', 'kurtosis']))
    # # Mic FFT Peaks
    results.extend(
        get_single_signal_features(get_Hz_range(ffts[1], [42, 62]),
                                   ['mean', 'median', 'std', 'skew', 'rms']))
    return results

def get_v2_data_features(signals, ffts):
    results = []

    # ACC signal features
    results.extend(
        get_single_signal_features(signals[0],
                                   ['mean', 'median', 'skew', 'std', 'kurtosis', 'ptp']))
    # ACC FFT
    results.extend(
        get_single_signal_features(get_Hz_range(ffts[0], [150, 250]),
                                   ['mean', 'std', 'ptp', 'var', 'skew', 'kurtosis', 'max']))
    # ACC FFT PEAKS
    results.extend(
        get_single_signal_features(get_Hz_range(ffts[0], [190, 210]),
                                   ['mean', 'median', 'skew', 'kurtosis', 'rms', 'max']))

    # Mic signal features
    results.extend(
        get_single_signal_features(signals[1],
                                   ['median', 'skew', 'std', 'kurtosis', 'ptp', 'min']))
    # Mic FFT
    results.extend(
        get_single_signal_features(get_Hz_range(ffts[1], [150, 250]),
                                   ['mean', 'median', 'skew', 'kurtosis', 'rms', 'max']))
    # Mic FFT Peaks
    results.extend(
        get_single_signal_features(get_Hz_range(ffts[1], [190, 210]),
                                   ['mean', 'median', 'skew', 'kurtosis', 'rms', 'max']))
    return results


@post('/')
def index():
    file_name = str(request.body.getvalue(), 'utf-8')
    return json.dumps(extract_features(file_name, c))

def start_server():
    """Starts server"""

    run(host='localhost', port=8082)

if __name__ == "__main__":
    start_server()
