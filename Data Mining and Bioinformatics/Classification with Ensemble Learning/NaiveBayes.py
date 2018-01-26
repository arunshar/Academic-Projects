import numpy as np
import math
from random import randrange
# from sklearn.metrics import confusion_matrix

fr = open("/Users/arun/Desktop/dataset_1.txt");
stringArr = [line.strip().split('\t') for line in fr.readlines()]
allData = np.array(stringArr)


def naivebayes(trainingdata,testingdata):

    def getindex(dataset):
        index = []
        for i in range(dataset.shape[1]):
            try:
                dataset[0,i].astype(np.float)
            except ValueError:
                index.append(i)
        return index

    def getcontsummary(trainingdata,index):
        if len(index) > 0:
            for i in range(len(index)):
                trainingdata = np.delete(trainingdata,index[i],axis=1)

        def mean(numbers):
            return sum(numbers) / float(len(numbers))

        def stdev(numbers):
            avg = mean(numbers)
            variance = sum([pow(x - avg, 2) for x in numbers]) / float(len(numbers) - 1)
            return math.sqrt(variance)

        def get_map(dataset):
            summaries = [(mean(attribute), stdev(attribute)) for attribute in zip(*dataset)]
            return summaries

        def hashmap(dataset):
            dict = {}
            for i in range(len(dataset)):
                vector = dataset[i]
                float_vector = vector[:-1].astype(np.float)
                if (vector[-1] not in dict):
                    dict[vector[-1]] = []
                dict[vector[-1]].append(float_vector)
            return dict

        def classvalue(dataset):
            summaries = {}
            map = hashmap(dataset)
            for classValue, instances in map.items():
                summaries[classValue] = get_map(instances)
            return summaries

        summary = classvalue(trainingdata)
        return summary

    def getcontprobability(testdata,summary,index):
        if len(index) > 0:
            for i in range(len(index)):
                testdata = np.delete(testdata,index[i],axis=1)

        testdata = testdata[:,:-1].astype(np.float)

        cont_matrix = []
        def classwiseprobability(input_vec, summary):
            prob = {}
            for classval, classSummary in summary.items():
                prob[classval] = 1
                for i in range(len(classSummary)):
                    mean, stdev = classSummary[i]
                    x = input_vec[i]
                    prob[classval] *= calculateProbability(x, mean, stdev)
            return prob

        def calculateProbability(x, mean, stdev):
            exponent = math.exp(-(math.pow(x - mean, 2) / (2 * math.pow(stdev, 2))))
            return (1 / (math.sqrt(2 * math.pi) * stdev)) * exponent

        for i in range(len(testdata)):
            getswifty = []
            input_vec = testdata[i]
            prob_map = classwiseprobability(input_vec,summary)
            getswifty.append(prob_map['0'])
            getswifty.append(prob_map['1'])
            cont_matrix.append(getswifty)

        return cont_matrix

    def getcatsummary(trainingdata,testdata,index):
        if len(index) > 0 :
            final_catmatrix = 1
            for j in range(len(index)):
                train_data = trainingdata[:,index[j]]
                label_train = trainingdata[:,-1]
                dict = {}
                for i in range(len(label_train)):
                    if label_train[i] not in dict:
                        dict[label_train[i]] = []
                    dict[label_train[i]].append(train_data[i])
                cat_matrix1,prior = getcatprobability(testdata,dict,index[j])
                final_catmatrix *= cat_matrix1
            final_catmatrix = np.multiply(final_catmatrix,prior)
            return final_catmatrix
        else: return 1

    def getcatprobability(testdata,summary,index):
        label = testdata[:,-1]
        testdata = testdata[:,index]
        cat_matrix = []
        def getclasswiseprobability(summary,input_vector,label):
            prob1 = {}
            for classval, data1 in summary.items():
                prob1[classval] = 1
                if classval not in prob1:
                    prob1[classval] = []
                prior = len(summary[classval])/len(label)
                posterior = data1.count(input_vector) / len(summary[classval])
                prob1[classval] *= posterior
            return prob1,prior

        for i in range(len(testdata)):
            getswifty = []
            input_vector = testdata[i]
            prob,prior = getclasswiseprobability(summary,input_vector,label)
            getswifty.append(prob['0'])
            getswifty.append(prob['1'])
            cat_matrix.append(getswifty)

        return cat_matrix,prior

    def getpredictedlabels(x):
        predicted_labels = []
        for i in range(len(x)):
            for j in range(len(x[i])):
                if x[i][j] == np.max(x[i]):
                    predicted_labels.append(j)

        return predicted_labels

    x = getindex(trainingdata)
    summary = getcontsummary(trainingdata, x)
    cont_matrix = getcontprobability(testdata, summary, x)
    get_cat_value = getcatsummary(trainingdata, testdata, x)
    predicted_matrix = cont_matrix * get_cat_value
    predicted_labels = getpredictedlabels(predicted_matrix)

    return predicted_labels

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

def convert_labels(actual_labels):
    actual_labels1 = []
    for i in range(len(actual_labels)):
        actual_labels1.append(int(actual_labels[i]))

    return actual_labels1

def demo(dataset,testdata):

    def getindex(dataset):
        index = []
        for i in range(dataset.shape[1]):
            try:
                dataset[0,i].astype(np.float)
            except ValueError:
                index.append(i)
        return index

    traindata = dataset
    index = getindex(dataset)

    labels = list(dataset[:,-1])

    prior_0 = labels.count("0")/len(labels)
    prior_1 = labels.count("1")/len(labels)


    denominator = 1
    for i in range(len(testdata)):
        val = list(dataset[:,i])
        num = val.count(testdata[i])
        den = num/len(dataset)
        denominator = denominator*den

    post_0 = 1
    post_1 = 1
    for i in range(len(index)):
        train_data = traindata[:,index[i]]
        label_train = traindata[:, -1]
        dict = {}
        for j in range(len(label_train)):
            if label_train[j] not in dict:
                dict[label_train[j]] = []
            dict[label_train[j]].append(train_data[j])
        posterior_0 = dict['0'].count(testdata[i])/len(dict['0'])
        posterior_1 = dict['1'].count(testdata[i]) / len(dict['1'])
        post_0 = post_0 * posterior_0
        post_1 = post_1 * posterior_1

    prob_list = []
    prob_0 = (post_0*prior_0)/denominator
    prob_1 = (post_1*prior_1)/denominator
    prob_list.append(prob_0)
    prob_list.append(prob_1)
    val = prob_list.index(max(prob_list))

    print("probability for class 0 : ", prob_0)
    print("probability for class 1 : ", prob_1)
    print("The input will get classified to class : ", val)

    return prob_0,prob_1,val


kfold = 9
start = 0

sets = len(allData) // kfold
rest = len(allData) % kfold

accuracy = []
precision = []
recall = []
fmeasure = []

for i in range(0,kfold):

    testdata = allData
    trainingdata = allData
    test_labels = testdata[:,-1]

    end = start + sets

    if i == kfold-1:
        end = end + rest

    testdata = testdata[start:end]
    test_labels = test_labels[start:end]
    trainingdata = np.delete(trainingdata, np.s_[start:end], axis=0)

    predicted_labels = naivebayes(trainingdata, testdata)
    actual = convert_labels(test_labels)
    eval_dict = performanceMetrics(actual, predicted_labels)

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

# testdata = ['sunny', 'cool', 'high', 'weak']
# demo(allData,testdata)