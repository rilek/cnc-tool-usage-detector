"""CONFIGURATION CONSTS"""

import numpy as np

Fs = 25000
L = 16000
T = 1/Fs
m = int(L/2)
f = [2*Fs*(x)/L for x in list(range(0, m))]

CONFIG = {
    'VARS': ['AccXSignal', 'VelZSignal', 'AccXSignal1', 'MicSignal'],
    'TRAIN_FILES_DIR': 'train/',
    'TRAIN_FILES_LAST_GOOD': 552,
    'TRAIN_PERCENT': 0.9,
    'Fs': Fs,
    'T': T,
    'L': L,
    't': np.linspace(0.0, L*T, L),
    'm': m,
    'f': f,
    'thousandHertsIndex': f.index(next(i for i in f if i > 1000))
}