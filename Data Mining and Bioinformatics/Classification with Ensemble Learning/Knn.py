
# coding: utf-8

# In[402]:


import numpy as np
from numpy import linalg as LA
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import euclidean_distances
import random
from collections import defaultdict
from sklearn.decomposition import *
from numpy import linalg as LA
from collections import defaultdict
from collections import Counter
from sklearn.metrics import confusion_matrix

readTestFromFile=True
testFile = 'project3_dataset3_test.txt'

#list of files to read.  Eg: files = ['pca_a.txt','pca_b.txt']
#files = ['train3.txt']
files = ['project3_dataset3_trian.txt']

folds=10


k1=11
fixedK = True


testDataSize = 40

#data file path
filePath = '/Users/arun/Desktop/'





# In[403]:


def readRawFromFile(fileName):
        file = filePath+fileName
        fo = open(file)
        Xstring = fo.read()
        Xrows = Xstring.split('\n')
        return np.array([row.split('\t') for row in Xrows])


# In[404]:


def getTrainAndTestData(X):
        np.random.seed()
        testIdx = np.random.randint(0,X.shape[0],testDataSize)
        x = X[testIdx, :]
        mask = np.ones(X.shape[0],dtype=bool)
        mask[testIdx] = False
        x1 = X[mask, :]
        return x1,x,testIdx


# In[405]:


def getTrainAndTestDataForFold(X,f):
    init = f*testDataSize
    testIdx = np.arange(init, init+testDataSize,dtype=int)%X.shape[0]
    x = X[testIdx, :]
    mask = np.ones(X.shape[0],dtype=bool)
    mask[testIdx] = False
    x1 = X[mask, :]
    return x1,x,testIdx


# In[406]:

def normalize(data):
        l = data.shape[1]
        m = np.zeros(l)
        sd = np.zeros(l)
        for i in range(0,l):
                m[i] = np.mean(data[:,i])
                sd[i] = np.std(data[:,i])
                data[:,i]-=m[i]
                data[:,i]/=sd[i]
        return data,m,sd

def normalizeWithData(data,m,sd):
        l = data.shape[1]
        for i in range(0,l):
                data[:,i]-=m[i]
                data[:,i]/=sd[i]
        return data

def getDist(x1,x2):
    x1dup = x1[0].copy()
    contIdx = np.array([val.replace('.','',1).isdigit() for val in np.array(x1dup)])
    h1 = x1[:,False==contIdx]
    h2 = x2[:,False==contIdx]
    eTest = x1[:,True==contIdx].astype(np.float)
    eTrain = x2[:,True==contIdx].astype(np.float)
    e1,m,sd = normalize(eTrain)
    e2 = normalizeWithData(eTest,m,sd)
    d1 = hamming_distance(h1,h2)
    d2 = euclidean_distances(e2,e1)
    #print("x1.shape:[",x1.shape,"] x2.shape:[",x2.shape,"] h1.shape:[",h1.shape,"] h2.shape:[",h1.shape,"] d1.shape:",d1.shape," d2.shape:",d2.shape," eTest.shape:",eTest.shape," eTrain.shape:",eTrain.shape," e1.shape:",e1.shape," e2.shape:",e2.shape," d2.shape:",d2.shape)
    return d1+d2


# In[407]:


def hamming_distance(x1, x2):
    dist = np.zeros((len(x1),len(x2)))
    i=0
    for s1 in x1:
        j=0
        for s2 in x2:
            if len(s1) != len(s2):
                raise ValueError("Undefined for sequences of unequal length")
            dist[i][j] = sum(ch1 != ch2 for ch1, ch2 in zip(s1, s2))
            j+=1
        i+=1
    return dist


# In[408]:


def doKnn(test,train,label):
    if(not fixedK):
        k = int(train.shape[0]/len(np.unique(label)))
        if(k% 2 == 0):
            k+=1
    else:
        k = k1
    dist = getDist(test,train)
    nearestLab = np.argsort(dist,axis = 1)[:,:k]
    predLabel = np.zeros(nearestLab.shape[0])
    for i in range(0,nearestLab.shape[0]):
        predLabelCount = Counter(classLabel[nearestLab[i]])
        predLabel[i] = predLabelCount.most_common(1)[0][0]
    return predLabel,k


# In[409]:


def evaluate(actual,predicted):
        #CM=confusion_matrix(actual,predicted)
        #a=CM[0][0]
        #b=CM[0][1]
        #c=CM[1][0]
        #d=CM[1][1]
        a=0
        b=0
        c=0
        d=0
        for i in range(0,len(actual)):
                if(actual[i]==predicted[i] and actual[i]==1):
                        a+=1
                elif(actual[i]==predicted[i] and actual[i]==0):
                        d+=1
                elif(actual[i]!=predicted[i] and actual[i]==1):
                        b+=1
                elif(actual[i]!=predicted[i] and actual[i]==0):
                        c+=1
                
        #print("TP:",a," TN:",d," FN:",b," FP:",c)
        Accuracy = (a+d)/(a+b+c+d)
        Precision = (a)/(a+c)
        Recall = (a)/(a+b)
        FMeasure = (2*a)/((2*a)+b+c)
        #print("Accuracy",Accuracy)
        #print("Precision",Precision)
        #print("Recall",Recall)
        #print("FMeasure",FMeasure)
        return Accuracy,Precision, Recall, FMeasure


# In[411]:

if(not readTestFromFile):
        fileName = files[0]
        X = readRawFromFile(fileName)
        classCol = X.shape[1]-1
        testDataSize=X.shape[0]/folds
        np.random.seed(3)
        np.random.shuffle(X)
        A = np.zeros(folds)
        P = np.zeros(folds)
        R = np.zeros(folds)
        FM = np.zeros(folds)
        for f in range(0,folds):
            trainD, testD, testIdx = getTrainAndTestDataForFold(X,f)
            classLabel = np.array(trainD[:,classCol])
            xTrain = trainD[:,:classCol]
            xTest = testD[:,:classCol]
            predLabel,k = doKnn(xTest,xTrain,classLabel)
            groundTruths = np.array(testD[:,classCol]).astype(np.float)
            #print("Metrics for fold # ",f,":")
            A[f],P[f],R[f],FM[f] = evaluate(groundTruths,predLabel)
        print("Average Metrics after 10 fold evaluation with k = ",k,":")
        print("Accuracy",np.mean(A))
        print("Precision",np.mean(P))
        print("Recall",np.mean(R))
        print("FMeasure",np.mean(FM))

else:
        trainFile = files[0]
        trainX = readRawFromFile(trainFile)
        classCol = trainX.shape[1]-1
        xTrain = trainX[:,:classCol]
        classLabel = np.array(trainX[:,classCol])

        testX = readRawFromFile(testFile)
        xTest = testX[:,:classCol]
        predLabel,k = doKnn(xTest,xTrain,classLabel)
        groundTruths = np.array(testX[:,classCol]).astype(np.float)
        #print("Metrics for fold # ",f,":")
        A,P,R,FM = evaluate(groundTruths,predLabel)
        print("Accuracy",A)
        print("Precision",P)
        print("Recall",R)
        print("FMeasure",FM)
