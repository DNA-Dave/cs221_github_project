import collections
import math
import os
import json


def dotProduct(d1, d2):
    """
    @param dict d1: a feature vector represented by a mapping from a feature (string) to a weight (float).
    @param dict d2: same as d1
    @return float: the dot product between d1 and d2
    """
    if len(d1) < len(d2):
        return dotProduct(d2, d1)
    else:
        return sum(d1.get(f, 0) * v for f, v in d2.items())

def increment(d1, scale, d2):
    """
    Implements d1 += scale * d2 for sparse vectors.
    @param dict d1: the feature vector which is mutated.
    @param float scale
    @param dict d2: a feature vector.
    """
    for f, v in d2.items():
        d1[f] = d1.get(f, 0) + v * scale

def evaluatePredictor(examples, predictor):
    '''
    predictor: a function that takes an x and returns a predicted y.
    Given a list of examples (x, y), makes predictions based on |predict| and returns the fraction
    of misclassiied examples.
    '''
    error = 0
    fileToScore = []
    for i in range(len(examples)):
        name, x, y = examples[i]
        loss = math.fabs(predictor(x) - y)
        error = error*(i)/float(i+1) + loss/float(i+1)
    fileToScore.append((loss, name))
    fileToScore.sort(reverse=True)
    while True:
        numIters = 0  # input()
        if numIters == 0:
            break
        for i in range(numIters):
            print fileToScore[i][1], fileToScore[i][0]
    return error

def evaluatePredictorRSquared(examples, predictor):
    # u = (ytrue - ypred)**2 (pred)
    # v = (ytrue - ypredMean)**2(pred)
    
    yTrueMean = 0
    for i in range(len(examples)):
        name, x, y = examples[i]
        yTrueMean += y
    yTrueMean /= len(examples)

    u = 0
    v = 0
    for i in range(len(examples)):
        name, x, y = examples[i]
        yPred = predictor(x)
        u += (yPred - y)**2
        v += (y - yTrueMean)**2
    
    return 1 - u/v

def beginWeightEvaluation(trainExamples, testExamples):
    '''
    Given |trainExamples| and |testExamples| (each one is a list of (x,y)
    pairs where x is a list of features), and the number of iterations to
    train |numIters|, the step size |eta|, return the weight vector (sparse
    feature vector) learned.

    You should implement stochastic gradient descent.

    Note: only use the trainExamples for training!
    You should call evaluatePredictor() on both trainExamples and testExamples
    to see how you're doing as you learn after each iteration.
    '''

    weights = {} # feature => weight

    with open(str(os.getcwd()) + "//results_basic_classifier.json", 'r') as weight_file:
        weights = json.load(weight_file)

    print ("Train Error ")
    print (str(evaluatePredictor(trainExamples, lambda(x): dotProduct(x, weights))))
    print ("RSquared " + str(evaluatePredictorRSquared(trainExamples, lambda(x): dotProduct(x, weights))))
    print ("Test Error ")
    print (str(evaluatePredictor(testExamples, lambda(x): dotProduct(x, weights))))
    print ("RSquared " + str(evaluatePredictorRSquared(testExamples, lambda(x): dotProduct(x, weights))))

    return weights

def getDataFrom(featuresFile, truthFile):
    # you'll need to change this to let it read the CSV and get the features of each project in this function
    nameToTruth = {}
    with open(truthFile) as truth:
        header = truth.readline()
        for line in truth.readlines():
            repo, stars, forks, watches = line.split('\t')
            nameToTruth[repo] = 0.5 * \
                float(stars) + 0.15*float(watches) + 0.35*float(forks)
    nameToFeatures = {}
    with open(featuresFile) as features:
        header = features.readline()
        featuresList = header.split('\t')
        for line in features.readlines():
            parts = line.split('\t')
            name = parts[0]
            nameToFeatures[name] = {}
            for i in range(1, len(parts)-1):
                nameToFeatures[name][featuresList[i]] = float(parts[i])
    result = []
    for repo in nameToTruth:
        if repo in nameToFeatures:
            result.append((repo, nameToFeatures[repo], nameToTruth[repo]))
    return result

data = getDataFrom(
    "featurized-repos_v1DW.txt", "common_stuff/all_project_ground_truths.txt")
trainingData = data[:int(len(data)*3.0/4.0)]
print len(trainingData)
testData = data[len(trainingData):]
print len(testData)
beginWeightEvaluation(trainingData, testData)