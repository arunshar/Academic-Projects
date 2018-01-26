# coding: utf-8

# In[1]:

from random import seed
from random import *
import time
from math import *
from itertools import groupby
from collections import defaultdict


# In[2]:

def loadDataSet(fileName, delim='\t'):
    fr = open(fileName)
    stringArr = [line.strip().split(delim) for line in fr.readlines()]
    return stringArr


# In[3]:

def convert(sequence):
    for item in sequence:
        try:
            yield float(item)
        except ValueError as e:
            yield item


# In[4]:

def getValidationSplit(dataset):
    splits = list()
    datasetCopy = list(dataset)
    # shuffle(datasetCopy)
    chunkSize = len(datasetCopy) // kFolds
    leftOver = len(datasetCopy) % kFolds
    start = 0
    for i in range(kFolds):
        if i < leftOver:
            end = start + chunkSize + 1
        else:
            end = start + chunkSize
        splits.append(datasetCopy[start:end])
        start = end
    return splits


# In[5]:

def performanceMetrics(actual, predicted):
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    for i in range(len(actual)):

        if actual[i] == 1 and predicted[i] == 1:
            tp = tp + 1
        if actual[i] == 1 and predicted[i] == 0:
            fn = fn + 1
        if actual[i] == 0 and predicted[i] == 1:
            fp = fp + 1
        if actual[i] == 0 and predicted[i] == 0:
            tn = tn + 1
    precision = 0
    recall = 0
    F1 = 0
    accuracy = 0

    if tp + fp != 0:
        precision = tp / float(tp + fp)
    if tp + fn != 0:
        recall = tp / float(fn + tp)
    if tp + tn + fp + fn != 0:
        accuracy = (tp + tn) / float(tp + tn + fp + fn)
    if precision + recall != 0:
        F1 = (2 * precision * recall) / float(precision + recall)

    precision = precision * 100
    recall = recall * 100
    accuracy = accuracy * 100
    F1 = F1 * 100
    return {'precision': precision, 'recall': recall, 'accuracy': accuracy, 'F1': F1}


# In[6]:

def splitOnValue(index, value, dataset):
    left = []
    right = []
    _ = [left.append(row) if row[index] < value else right.append(row) for row in dataset]
    return left, right


# In[7]:

def getClasses(dataset):
    return [row[-1] for row in dataset]


# In[8]:

def calculateGINI(left, right, classes):
    n_instances = float(len(left) + len(right))
    gini = 0.0

    score = 0.0
    size = float(len(left))
    if size != 0:
        for class_val in classes:
            tempList = getClasses(left)
            p = tempList.count(class_val) / size
            score += p * p
        gini += (1.0 - score) * (size / n_instances)

    score = 0.0
    size = float(len(right))
    if size != 0:
        for class_val in classes:
            tempList = getClasses(right)
            p = tempList.count(class_val) / size
            score += p * p
        gini += (1.0 - score) * (size / n_instances)

    return gini


# In[9]:

def getSplit(dataset, isRandomForest):
    classes = list(set(getClasses(dataset)))
    indexesList = []

    if isRandomForest:
        indexesList = selectFeatures(len(dataset[0]) - 1)
    else:
        indexesList = [x for x in range(len(dataset[0]) - 1)]

    index, value, score, left, right = inf, inf, inf, None, None

    for i in indexesList:
        for row in dataset:
            l, r = splitOnValue(i, row[i], dataset)
            gini = calculateGINI(l, r, classes)
            if gini <= score:
                index, value, score, left, right = i, row[i], gini, l, r
    return {'index': index, 'value': value, 'leftHalf': left, 'rightHalf': right}


# In[10]:

def terminal(group):
    outcomes = getClasses(group)
    d = defaultdict(float)
    for i in outcomes:
        d[i] += 1
    result = max(d.items(), key=lambda x: x[1])
    return result[0]


# In[11]:

def nodeSplit(node, depth, isRandomForest):
    left, right = node['leftHalf'], node['rightHalf']

    del (node['leftHalf'])
    del (node['rightHalf'])

    if not left or not right:
        node['left'] = node['right'] = terminal(left + right)
        return

    if depth >= maxDepth:
        node['left'], node['right'] = terminal(left), terminal(right)
        return

    if len(left) <= minSize:
        node['left'] = terminal(left)
    else:
        node['left'] = getSplit(left, isRandomForest)
        nodeSplit(node['left'], depth + 1, isRandomForest)

    if len(right) <= minSize:
        node['right'] = terminal(right)
    else:
        node['right'] = getSplit(right, isRandomForest)
        nodeSplit(node['right'], depth + 1, isRandomForest)


# In[12]:

def buildTree(train, isRandomForest):
    root = getSplit(train, isRandomForest)
    nodeSplit(root, 1, isRandomForest)
    return root


# In[13]:

def predict(node, row):
    if row[node['index']] < node['value']:
        if isinstance(node['left'], dict):
            return predict(node['left'], row)
        else:
            return node['left']
    else:
        if isinstance(node['right'], dict):
            return predict(node['right'], row)
        else:
            return node['right']


# In[14]:

def makeDecisionTree(train, test):
    tree = buildTree(train, False)
    predictions = list()
    for row in test:
        prediction = predict(tree, row)
        predictions.append(prediction)
    return (predictions), tree


# In[15]:

def selectFeatures(currDataLength):
    indexesList = [x for x in range(currDataLength)]
    shuffle(indexesList)
    return indexesList[:featuresCount]


# In[16]:

def makeSubSample(dataset):
    sample = list()
    size = len(dataset)
    sampleCount = round(size * samplingRatio)
    indexes = [randint(0, size - 1) for x in range(sampleCount)]
    for i in indexes:
        sample.append(dataset[i])
    return sample


# In[17]:

def baggingPrediction(trees, row):
    predictions = [predict(tree, row) for tree in trees]
    return max(set(predictions), key=predictions.count)


# In[18]:

def makeRandomForest(train, test, treesCount):
    trees = list()
    for i in range(treesCount):
        sample = makeSubSample(train)
        tree = buildTree(sample, True)
        trees.append(tree)
    predictions = [baggingPrediction(trees, row) for row in test]
    return (predictions)


# In[24]:

seed(11)
filename = '/Users/arun/Desktop/dataset_1.txt'
datasetAll = loadDataSet(filename)
data = [list(convert(sublist)) for sublist in datasetAll]
kFolds = 10
maxDepth = 3
minSize = 1
featuresCount = int(sqrt(len(data[0]) - 1))
samplingRatio = 1.0

def decisionTrees():
    start_time = time.time()

    splits = getValidationSplit(data)
    scores = []
    for split in splits:
        trainSet = list(splits)
        trainSet.remove(split)
        trainSet = sum(trainSet, [])
        testSet = []
        actual = []
        for row in split:
            rowCopy = list(row)
            testSet.append(rowCopy)
            rowCopy[-1] = None
            actual.append(row[-1])
        predicted,tree = makeDecisionTree(trainSet, testSet)
        print(tree)
        accuracy = performanceMetrics(actual, predicted)
        print(accuracy)
        scores.append(accuracy)

    precision = 0
    recall = 0
    accuracy = 0
    F1 = 0

    for i in range(len(scores)):
        precision += scores[i]['precision']
        recall += scores[i]['recall']
        accuracy += scores[i]['accuracy']
        F1 += scores[i]['F1']

    print('Mean Precision: %.3f%%' % (precision/float(len(scores))))
    print('Mean Recall: %.3f%%' % (recall/float(len(scores))))
    print('Mean Accuracy: %.3f%%' % (accuracy/float(len(scores))))
    print('Mean F1: %.3f%%' % (F1/float(len(scores))))
    print("--- %s seconds ---" % (time.time() - start_time))

decisionTrees()