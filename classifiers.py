"""Classifiers testing module"""

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib
import features
import utils as u
from config import CONFIG as c


def test_classifiers(classifiers, config, model_filename='model.pkl'):
    """Take array of classifiers to test and configuration dictionary
    Tests each classifier, its score is printed.
    Best one is printed with score ans saved to 'model_filename' file """

    x_data = features.get_signal_features(config['TRAIN_FILES_DIR'], config, True, 'features.csv')
    y_data = np.matrix([0]*config['TRAIN_FILES_LAST_GOOD'] + \
                       [1]*(x_data.shape[0] - config['TRAIN_FILES_LAST_GOOD']))

    data = np.hstack((x_data, np.transpose(y_data)))

    x_train, x_test, y_train, y_test = \
        train_test_split(data[:, :-1],
                         data[:, -1],
                         shuffle=True,
                         train_size=config['TRAIN_PERCENT'],
                         test_size=1-config['TRAIN_PERCENT'],
                         random_state=0)

    models = []
    for name, clf in classifiers:
        clf.fit(x_train, np.array(y_train).ravel())
        score = clf.score(x_test, y_test)
        models.append([score, clf, name])

    models.sort(key=lambda x: -x[0])

    print("Models score sorted decs:")
    for score, clf, name in models:
        u.print_model_score(name, score)

    best_model = models[0]

    print("\nChosen model: {}, with score: {}%"
          .format(best_model[2], round(best_model[0]*100, 2)))

    joblib.dump(best_model[1], model_filename)


if __name__ == '__main__':
    test_classifiers(c['CLASSIFIERS'], c)
