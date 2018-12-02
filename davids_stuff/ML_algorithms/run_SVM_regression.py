import math
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report

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

c_vals = [1, 10]
for i in range(50, 1000, 500):
    c_vals.append(i)
gammas = [0.5, 0.1, 0.01, 0.001, 0.0001, 0.00001]
parameters = [{"C": c_vals, "kernel": ["linear"]},
    {"C": c_vals, "kernel": ["rbf"], "gamma":gammas}]
svr = GridSearchCV(SVR(), parameters, cv = 10, n_jobs=-1, verbose=10)
svr.fit(X_train, y_train)

grid_search = svr.fit(X_train, y_train)
best_accuracy = grid_search.best_score_
best_parameters = grid_search.best_params_
print(best_accuracy)
print(best_parameters)

#clf = SVR()
#clf.fit(X_train, y_train)
#print("SVR Regression train score: " + str(clf.score(X_train, y_train)))
#print("SVR Regression test score: " + str(clf.score(X_test, y_test)))