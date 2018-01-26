from random import seed
from random import *
import time
from math import *
from itertools import groupby
from collections import defaultdict
import numpy as np
import random


def adaboost(testdata,traindata,iter,maxDepth,minSize):

    def splitOnValue(index, value, dataset):
        left = []
        right = []
        _ = [left.append(row) if row[index] < value else right.append(row) for row in dataset]
        return left, right

    def getClasses(dataset):
        return [row[-1] for row in dataset]

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

    def getSplit(dataset, isRandomForest):
        classes = list(set(getClasses(dataset)))
        indexesList = []

        indexesList = [x for x in range(len(dataset[0]) - 1)]

        index, value, score, left, right = inf, inf, inf, None, None

        for i in indexesList:
            for row in dataset:
                l, r = splitOnValue(i, row[i], dataset)
                gini = calculateGINI(l, r, classes)
                if gini < score:
                    index, value, score, left, right = i, row[i], gini, l, r
        return {'index': index, 'value': value, 'leftHalf': left, 'rightHalf': right}


    def terminal(group):
        outcomes = getClasses(group)
        d = defaultdict(float)
        for i in outcomes:
            d[i] += 1
        result = max(d.items(), key=lambda x: x[1])
        return result[0]


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


    def buildTree(train, isRandomForest):
        root = getSplit(train, isRandomForest)
        nodeSplit(root, 1, isRandomForest)
        return root

    def predict(node, row):
        if row[node['index']] < node['value']:
            if isinstance(node['left'], dict):
                return predict(node['left'], row)
            else:
                return node['left']
        else:
            # print(dict)
            if isinstance(node['right'], dict):
                return predict(node['right'], row)
            else:
                return node['right']

    def makeDecisionTree(train, test):
        tree = buildTree(train, False)
        predictions = list()
        for row in test:
            prediction = predict(tree, row)
            predictions.append(prediction)
        return predictions,tree


    def getNone(testdata):
        for i in range(len(testdata)):
            data[i][-1] = None
        return data

    def getLabels(data):
        labels = []
        for i in range(len(data)):
            labels.append(data[i][-1])
        return labels

    def getmisses(predicted,trainlabels):

        miss = []
        miss2 = []
        for i in range(len(predicted)):
            if predicted[i] != trainlabels[i]:
                miss.append(1)
                miss2.append(1)
            else:
                miss.append(0)
                miss2.append(-1)
        return miss,miss2

    def getindices(data):
        indices_list = []
        for i in range(len(data)):
            indices_list.append(i)
        return indices_list

    def getrandindex(indices,w):
        rand_indices = []
        for i in range(len(indices)):
            rand_ind = random.choices(indices,w)
            rand_indices.append(rand_ind[0])
        return rand_indices

    def getrandRows(data,rand_indices):
        rows = []
        for ind in rand_indices:
            rows.append(data[ind])
        return rows


    w = np.ones(len(traindata))/len(traindata)

    trainlabels = getLabels(traindata)
    train_indices = getindices(traindata)

    trees = []
    alpha = []

    j = 0

    while j < iter:
        if j > 0 :
            rand_indices = getrandindex(train_indices,w)
            traindata = getrandRows(traindata,rand_indices)

        predicted,tree = makeDecisionTree(traindata, traindata)

        miss,miss2 = getmisses(predicted,trainlabels)

        err_m = np.dot(w,miss)/sum(w)

        alpha_m = 0.5*np.log(float(1-err_m)/float(err_m))
        alpha.append(alpha_m)

        w = np.multiply(w,np.exp([float(x) * alpha_m for x in miss2]))
        trees.append(tree)

        j = j + 1


    predicted_label = []
    for row in testdata:
        zero_alpha = []
        one_alpha = []
        for i in range(len(trees)):
            prediction = predict(trees[i], row)
            if prediction == 0.0:
                zero_alpha.append(alpha[i])
            else:
                one_alpha.append(alpha[i])
        if sum(zero_alpha) > sum(one_alpha):
            predicted_label.append(0.0)
        else:predicted_label.append(1.0)

    # print(predicted_label)
    test_label = getLabels(testdata)

    return predicted_label,test_label


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

def loadDataSet(fileName, delim='\t'):
    fr = open(fileName)
    stringArr = [line.strip().split(delim) for line in fr.readlines()]
    return stringArr

def convert(sequence):
    for item in sequence:
        try:
            yield float(item)
        except ValueError as e:
            yield item



filename = '/Users/arun/Desktop/dataset_2.txt'
kFolds = 10
maxDepth = 1
minSize = 1

datasetAll = loadDataSet(filename)
data = [list(convert(sublist)) for sublist in datasetAll]

kfold = 10
start = 0

sets = len(data) // kfold
rest = len(data) % kfold

accuracy = []
precision = []
recall = []
fmeasure = []

for i in range(0,kFolds):

    testdata = data
    traindata = data


    end = start + sets

    if i == kFolds-1:
        end = end + rest

    testdata = testdata[start:end]

    trainingdata = np.delete(traindata, np.s_[start:end], axis=0)

    predicted_label,test_labels = adaboost(testdata, traindata, 5, maxDepth, minSize)

    eval_dict = performanceMetrics(test_labels, predicted_label)

    print(eval_dict)

    recall.append(eval_dict['recall'])
    precision.append(eval_dict['precision'])
    fmeasure.append(eval_dict['F1'])
    accuracy.append(eval_dict['accuracy'])

    start = end

mean_accuracy = np.mean(accuracy)
mean_precision = np.mean(precision)
mean_recall = np.mean(recall)
mean_fmeasure = np.mean(fmeasure)

print("Mean accuracy is : ",mean_accuracy)
print("Mean precision is : ",mean_precision)
print("Mean recall is : ",mean_recall)
print("Mean fmeasure is : ",mean_fmeasure)

# for i in range(0,kfold):
#
#     testdata = data
#     trainingdata = data
#     test_labels = testdata[:,-1]
#
#     end = start + sets
#
#     if i == kfold-1:
#         end = end + rest
#
#     testdata = testdata[start:end]
#     test_labels = test_labels[start:end]
#     trainingdata = np.delete(trainingdata, np.s_[start:end], axis=0)
#
#     # predicted_labels = naivebayes(trainingdata, testdata)
#     # actual = convert_labels(test_labels)
#     # eval_dict = performanceMetrics(actual, predicted_labels)
#
#     recall.append(eval_dict['recall'])
#     precision.append(eval_dict['precision'])
#     fmeasure.append(eval_dict['F1'])
#     accuracy.append(eval_dict['accuracy'])
#
#     start = end
#
# mean_accuracy = np.mean(accuracy)
# mean_precision = np.mean(precision)
# mean_recall = np.mean(recall)
# mean_fmeasure = np.mean(fmeasure)
#
# print("Mean accuracy is : ",mean_accuracy)
# print("Mean precision is : ",mean_precision)
# print("Mean recall is : ",mean_recall)
# print("Mean fmeasure is : ",mean_fmeasure)

