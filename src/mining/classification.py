import os
import sys
import pandas as pd
import numpy as np
import time

from sklearn.model_selection import train_test_split
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn import metrics


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
labels = np.array(mined_data_df[['resolved','unresolved','fatal']])




features = mined_data_df.drop(['fatal','unresolved','resolved'], axis=1)#drops fatal, unresolved and resolved column
feature_list = list(mined_data_df.columns)#list of columns in mined_data.csv
features = np.array(features)#contains data of each row in csv from features, therefore fatal column is dropped

train_features, test_features, train_labels, test_labels = train_test_split(
    features, labels, test_size=0.25, random_state=42)

def gen_random_forest():
    '''
    Source: https://towardsdatascience.com/random-forest-in-python-24d0893d51c0
    '''
    print ('\nRandom Forest Algorithm')
    start = time.perf_counter ()
    rf_clf = RandomForestClassifier(n_jobs=-1)
    rf_clf.fit (train_features, train_labels)
    rf_pred=rf_clf.predict(test_features)
    print(classification_report(test_labels, rf_pred ))
    end = time.perf_counter ()
    print ("Time: ", end-start)


def gen_decision_tree():
    print ('\nDecision Tree Algorithm')
    start = time.perf_counter ()
    dt_clf = DecisionTreeClassifier()
    dt_clf.fit (train_features, train_labels)
    dt_pred = dt_clf.predict (test_features)
    print(classification_report(test_labels, dt_pred))
    end = time.perf_counter ()
    print ("Time: ", end-start)


def gen_gradient_boost():
    print ('\nGradient Boost Algorithm')
    start = time.perf_counter ()
    gradient_booster = GradientBoostingClassifier ()
    # gradient_booster.fit (train_features, train_labels)
    # gradient_booster_pred = gradient_booster.predict (test_features)
    # print(classification_report(test_labels, gradient_booster_pred))
    end = time.perf_counter ()
    print ("Time: ", end-start)


def main():
    gen_random_forest()
    gen_decision_tree()
    gen_gradient_boost() #TODO: NOT WORKING


if __name__ == "__main__":
    main()
