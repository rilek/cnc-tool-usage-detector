"""Classifiers testing module"""

import numpy as np
import sklearn.metrics as metrics
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib
from colorama import init, Fore, Back, Style
import features
import utils as u
from config import CONFIG as c

init()

def test_classifiers(classifiers, config, model_filename='model.pkl'):
    """Take array of classifiers to test and configuration dictionary
    Tests each classifier, its score is printed.
    Best one is printed with score ans saved to 'model_filename' file """

    train_files_dir = config['CSV_TRAIN_FILES_DIR'] if config['TEST_CSV'] else config['TRAIN_FILES_DIR']
    x_data = features.get_signal_features(train_files_dir, config, config['EXISTS'], 'features2.csv')
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

    u.pprint("\nAlgorithms metrics:", 'green', end='')

    models = []
    for n, (name, clf) in enumerate(classifiers):
        n = n+1
        clf.fit(x_train, np.array(y_train).ravel())
        y_pred = [[clf.predict(x)[0]] for x in x_test]
        score = metrics.accuracy_score(y_test, y_pred)
        fpr, tpr, _ = metrics.roc_curve(y_test, y_pred)
        auc = metrics.auc(fpr, tpr)
        cm = metrics.confusion_matrix(y_test, y_pred)
        [[tp, fp], [fn, tn]] = cm



        u.pprint("\n{}.{}:".format(n, name), 'yellow')
        print("Score: {}%".format(round(score*100, 2)))
        print("False Alarm Rate: {}%".format(round(fp/(tn+fp)*100, 2)))
        print("AUC: {}".format(round(auc, 2)))
        print("Report: ")
        print(metrics.classification_report(y_test, np.matrix(y_pred),
                                            target_names=['Tępe', 'Ostre']))
        print("Confusion matrix:")
        u.print_cm(cm, ["Tępe", "Ostre"])

        models.append([clf, name, score, n])

    models.sort(key=lambda x: -x[2])

    u.pprint("\nModels score, sorted decs:", 'green')
    for clf, name, score, n in models:
        u.print_model_score(name, score, n)

    [bm_model, bm_name, bm_score, bm_n] = models[0]

    u.pprint("\nChosen model: {}.{}, with score: {}%".format(bm_n, bm_name, round(bm_score*100, 2)),
             'red')

    joblib.dump(bm_model, model_filename)


if __name__ == '__main__':
    test_classifiers(c['CLASSIFIERS'], c)
