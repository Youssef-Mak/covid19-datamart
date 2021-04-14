import os
import sys
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier

'''
All the preprocessed data is nicely formatted in a csv file. It is located in data/preprocessed_data/mined_data.csv. 
So for all your stuff in part B you will just need to read in that csv and it's all ready to go. 

The label we will be predicting is resolved, unresolved, fatal. If you have any questions just hmu. 

All the data is normalized (as per the instructions) so that is why the age and date and stuff look fucked up. But it is correct dw. 

Additionally, the non-numerical data was encoded using one-hot encoding so that is why you will see columns like special_measure-lockdown, special_measure-stay-at-home, etc.
'''


curr_dir = os.path.abspath(os.path.dirname(sys.argv[0]) or '.')
mined_data_csv = os.path.join(
    curr_dir, './../../data/preprocessed_data/mined_data.csv')

mined_data_df = pd.read_csv(mined_data_csv)

# We want to predict fatal cases
labels = np.array(mined_data_df['fatal'])
features = mined_data_df.drop('fatal', axis=1)
feature_list = list(mined_data_df.columns)
features = np.array(features)

train_features, test_features, train_labels, test_labels = train_test_split(
    features, labels, test_size=0.25, random_state=42)


def gen_random_forest():
    '''
    Source: https://towardsdatascience.com/random-forest-in-python-24d0893d51c0
    '''
    rf_clf = RandomForestClassifier(n_jobs=-1)

    params_dist = {
        'n_estimators': np.arange(100, 1500, 100),
        'max_depth': [None, 2, 4, 7, 10, 20],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 3, 5, 10]
    }

    CV_rf_clf = RandomizedSearchCV(rf_clf, params_dist, cv= 5, n_iter=20, scoring='f1')
    CV_rf_clf.fit(train_features, train_labels)

    rf_pred = CV_rf_clf.best_estimator_.predict(test_features)
    print(classification_report(test_labels, rf_pred))


def gen_decision_tree():
    dt_clf = DecisionTreeClassifier()

    params_dist = {
        'max_depth': [None, 2, 4, 7, 10, 20],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 3, 5, 10]
    }

    CV_dt_clf = RandomizedSearchCV(dt_clf, params_dist, cv= 5)
    CV_dt_clf.fit(train_features, train_labels)

    dt_pred = CV_dt_clf.best_estimator_.predict(test_features)
    print(classification_report(test_labels, dt_pred))


def gen_ada_boost():
    ada_boost_clf = AdaBoostClassifier()

    params_dist = {
        'n_estimators': np.arange(50, 1500, 50),
        'learning_rate': [1e-4, 1e-3, 1e-2, 1e-1, 1, 10],
        'algorithm': ['SAMME', 'SAMME.R']
    }

    CV_ada_boost_clf = RandomizedSearchCV(ada_boost_clf, params_dist, cv= 5)
    CV_ada_boost_clf.fit(train_features, train_labels)

    ada_boost_pred = CV_ada_boost_clf.best_estimator_.predict(test_features)
    print(classification_report(test_labels, ada_boost_pred))


def main():
    gen_random_forest()
    gen_decision_tree()
    # gen_ada_boost() #TODO: NOT WORKING


if __name__ == "__main__":
    main()
