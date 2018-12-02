import math
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
# difference of lasso and ridge regression is that some of the coefficients can be zero i.e. some of the features are
# completely neglected
from sklearn.linear_model import Lasso, Ridge, LinearRegression, LassoCV
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import PolynomialFeatures

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


#alphas = np.logspace(-3, -0.5, 100)
#plt.figure(figsize=(5, 3))

'''
for Model in [Lasso, Ridge]:
    scores = [cross_val_score(Model(alpha), X_train, y_train, cv=3).mean()
            for alpha in alphas]
    max_score = max(scores)
    for alpha in alphas:
        if cross_val_score(Model(alpha), X_train, y_train, cv=3).mean() == max_score:
            print(str(Model) + ": " + str(alpha))
            break
    plt.plot(alphas, scores, label=Model.__name__)
'''

lasso = Lasso(alpha=0.29)
lasso.fit(X_train, y_train)
print("Lasso train score :" + str(lasso.score(X_train, y_train)))
print("Lasso test score: " + str(lasso.score(X_test, y_test)))
print(lasso.coef_)

ridge = Ridge()
ridge.fit(X_train, y_train)
print("Ridge train score :" + str(ridge.score(X_train, y_train)))
print("Ridge test score: " + str(ridge.score(X_test, y_test)))
print(ridge.coef_)

linear = LinearRegression()
linear.fit(X_train, y_train)
print("Linear train score :" + str(linear.score(X_train, y_train)))
print("Linear test score: " + str(linear.score(X_test, y_test)))
print(linear.coef_)


poly = PolynomialFeatures(degree=4)
X_ = poly.fit_transform(X_train)
predict_ = poly.fit_transform(X_test)

linear = LinearRegression()
linear.fit(X_, y_train)
print("Linear train score with poly degree 2:" + str(linear.score(X_, y_train)))
print("Linear test score with poly degree 2: " + str(linear.score(predict_, y_test)))

#plt.legend(loc='lower left')
#plt.xlabel('alpha')
#plt.ylabel('cross validation score')
#plt.tight_layout()
#plt.show()