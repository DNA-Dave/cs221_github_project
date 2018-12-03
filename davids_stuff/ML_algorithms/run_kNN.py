import math
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
# difference of lasso and ridge regression is that some of the coefficients can be zero i.e. some of the features are
# completely neglected
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor
import itertools
from tqdm import tqdm

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


hello = (7, 11, 12, 16)


new_X_train = list()
new_X_test = list()
for element in X_train:
    new_features = list()
    for num in hello:
        new_features.append(element[num])
    new_X_train.append(new_features)
for element in X_test:
    new_features = list()
    for num in hello:
        new_features.append(element[num])
    new_X_test.append(new_features)
for i in range(1, 50):
    neigh = KNeighborsRegressor(n_neighbors=i)
    neigh.fit(new_X_train, y_train)
    print("kNN score on train with num neighbors = " + str(i) + "  :" + str(neigh.score(new_X_train, y_train)))
    print("kNN score on test with num neighbors = " + str(i) + "  :" + str(neigh.score(new_X_test, y_test)))
    print("\n\n")


'''
combination_set = set()
for i in range(0, 17):
    combination_set.add(i)


so_far_best = set([7, 11, 12, 16])


all_possible = list()
for i in range(5, 6):
    for comb in itertools.combinations(combination_set, i):
        if so_far_best.issubset(comb):
            all_possible.append(comb)

best_comb = None
best_score = None

for j in tqdm(range(len(all_possible))):
    all_comb = all_possible[j]
    sorted_list = sorted(list(all_comb))
    new_X_train = list()
    new_X_test = list()
    for element in X_train:
        new_features = list()
        for num in sorted_list:
            new_features.append(element[num])
        new_X_train.append(new_features)
    for element in X_test:
        new_features = list()
        for num in sorted_list:
            new_features.append(element[num])
        new_X_test.append(new_features)
    for i in range(1, 20):
        neigh = KNeighborsRegressor(n_neighbors=i)
        neigh.fit(new_X_train, y_train)
        #print("kNN score on train with num neighbors = " + str(i) + "  :" + str(neigh.score(new_X_train, y_train)))
        #print("kNN score on test with num neighbors = " + str(i) + "  :" + str(neigh.score(new_X_test, y_test)))
        score = neigh.score(new_X_test, y_test)
        if best_score is None or best_score < score:
            best_score = score
            best_comb = all_comb
print(best_score)
print(best_comb)
'''
