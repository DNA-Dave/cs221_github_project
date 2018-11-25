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


def learnPredictor(trainExamples, testExamples, numIters, eta):
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
    weights = collections.defaultdict(float)  # feature => weight
    for i in range(numIters):
        print(i)
        for trainingData in trainExamples:
            #trainingData = trainExamples[i % len (trainExamples)]
            phiX = trainingData[1]
            score = dotProduct(phiX, weights)
            #print score
            y = trainingData[2]
            #print y
            if score < y:
                lossGrad = 1
            else:
                lossGrad = -1
            # lossGrad = -2*(score - y)#squared loss...
            #print lossGrad
            increment(weights, eta*lossGrad/(i+1), phiX)
            # raw_input()
        print weights
    print "Train Error " + \
        str(evaluatePredictor(trainExamples, lambda(x): dotProduct(x, weights)))
    print "Test Error " + \
        str(evaluatePredictor(testExamples, lambda(x): dotProduct(x, weights)))
    print weights
    # END_YOUR_CODE

    with open(str(os.getcwd()) + "//results.json", 'w+') as output_file:
        json.dump(weights, output_file, ensure_ascii=False)
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
    "tempdss2.txt", "common_stuff/all_project_ground_truths.txt")
trainingData = data[:int(len(data)*3.0/4.0)]
print len(trainingData)
testData = data[len(trainingData):]
print len(testData)
learnPredictor(trainingData, testData, 200, 0.0001)
