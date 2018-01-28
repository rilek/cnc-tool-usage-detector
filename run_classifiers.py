"""A"""

import data_analysis.classifiers as classifiers
from config.config import CONFIG as c

classifiers.test_classifiers(c['CLASSIFIERS'], c)