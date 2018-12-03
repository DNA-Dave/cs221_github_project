
import math
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
# difference of lasso and ridge regression is that some of the coefficients can be zero i.e. some of the features are
# completely neglected
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler

def load_data():
    feature_vectors = list()
    ground_truth_values = list()
    name_to_ground_truths = dict()
    name_ordering = list()
    with open("/Users/davidwu/Desktop/cs221/cs221_github_project/davids_stuff/training_data/featurized-repos_v1DW.txt") as opened:
        counter = 0
        for line in opened:
            if counter == 0:
                counter += 1
                continue
            tokens = line.rstrip().split("\t")
            name = tokens[0]
            features = [float(element) for element in tokens[1:]]
            name_ordering.append(name)
            feature_vectors.append(features)
    with open("/Users/davidwu/Desktop/cs221/cs221_github_project/davids_stuff/training_data/all_ground_truths_DWv1.txt") as opened:
        for line in opened:
            tokens = line.rstrip().split("\t")
            name = tokens[0].replace("/", "_")
            vals = tokens[1:]
            stars = vals[0]
            forks = vals[1]
            watches = vals[2]
            score = 0.5*float(stars) + 0.35*float(forks) + 0.15*float(watches)
            name_to_ground_truths[name] = score
    for element in name_ordering:
        ground_truth_values.append(name_to_ground_truths[element])
    return np.array(feature_vectors), np.array(ground_truth_values)

X, Y = load_data()
X_train,X_test,y_train,y_test=train_test_split(X,Y, test_size=0.5, random_state=31)
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)


clf = GradientBoostingRegressor(loss="ls", learning_rate=0.11, n_estimators=100, random_state=1234)
clf.fit(X_train, y_train)
#clf = GradientBoostingRegressor(learning_rate=1, max_depth=8.75, max_features=3, min_samples_leaf=0.1, min_samples_split=0.775, n_estimators=200, random_state=1234)
#clf.fit(X_train, y_train)
print("Gradient Boosting Regressor score on training set: " + str(clf.score(X_train, y_train)))
print("Gradient Boosting Regressor score on testing set: " + str(clf.score(X_test, y_test)))

print(clf.feature_importances_)
'''
from sklearn.model_selection import GridSearchCV

learning_rates = [1, 0.1, 0.01]
n_estimators = [1, 2, 32, 100, 200]
max_depths = np.linspace(1, 32, 5, endpoint=True)
min_samples_splits = np.linspace(0.1, 1.0, 5, endpoint=True)
min_samples_leafs = np.linspace(0.1, 0.5, 3, endpoint=True)
max_features = list(range(1,X_train.shape[1]))

params = {
          "learning_rate": learning_rates,
          'n_estimators': n_estimators,
          'min_samples_leaf': min_samples_leafs,
          'min_samples_split':min_samples_splits,
          'random_state':[1234],
          'max_depth':max_depths,
           "max_features":max_features
         }

clf_grid = GridSearchCV(clf, param_grid=params, cv=10, n_jobs=-1, verbose=1)
clf_grid = clf_grid.fit(X_train, y_train)
print("Best Hyper Parameters:", clf_grid.best_params_)
'''