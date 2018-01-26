
# coding: utf-8

# In[2]:

from numpy import *
import operator
import timeit
import sys
import itertools 
import colorsys
from matplotlib.pyplot import *
from collections import defaultdict
from optparse import OptionParser
from heapq import heappush, heappop


# In[3]:

class DisjointSet:
    _disjoint_set = list()

    def __init__(self, init_arr):
        self._disjoint_set = []
        if init_arr:
            for item in list(set(init_arr)):
                self._disjoint_set.append([item])

    def _find_index(self, elem):
        for item in self._disjoint_set:
            if elem in item:
                return self._disjoint_set.index(item)
        return None

    def find(self, elem):
        for item in self._disjoint_set:
            if elem in item:
                return self._disjoint_set[self._disjoint_set.index(item)]
        return None

    def union(self,elem1, elem2):
        index_elem1 = self._find_index(elem1)
        index_elem2 = self._find_index(elem2)
        if index_elem1 != index_elem2 and index_elem1 is not None and index_elem2 is not None:
            self._disjoint_set[index_elem2] = self._disjoint_set[index_elem2]+self._disjoint_set[index_elem1]
            del self._disjoint_set[index_elem1]
        return self._disjoint_set

    def get(self):
        return self._disjoint_set

    def getSize(self):
        return len(self._disjoint_set)


# In[4]:

def loadDataSet(fileName, delim='\t'):
    fr = open(fileName)
    stringArr = [line.strip().split(delim) for line in fr.readlines()]                
    allData = array(stringArr)
    data = allData[:,2:]
    label = allData[:,1]
    idx = allData[:,0]
    return data.astype(float),label.astype(int),idx


# In[5]:

def euclidean_distance(u, v):
    diff = u - v
    return sqrt(dot(diff, diff))


# In[6]:

def pca(dataMat, dimension):
    meanVals = mean(dataMat, axis=0)
    meanRemoved = dataMat - meanVals 
    covMat = cov(meanRemoved, rowvar=0)
    eigVals,eigVects = linalg.eig(mat(covMat))
    eigValInd = argsort(eigVals)
    eigValInd = eigValInd[:-(dimension+1):-1]
    redEigVects = eigVects[:,eigValInd]
    lowDDataMat = meanRemoved * redEigVects 
    return lowDDataMat


# In[7]:

def testPCA(data,Y,fileName):
    ySet = unique(Y)
    
    lowDDataMat = pca(data,2)
        
    label_map = dict(zip(ySet, ySet))
    
    rcParams["figure.figsize"] = [16,9]
    
    suptitle('Algorithm : PCA', fontsize=30)
    title('TestData :'+fileName , fontsize=20)
    
    i = 2;
    
    for l in ySet:
        tempArr = array([[lowDDataMat[i,0], lowDDataMat[i,1]]for i in range(len(Y)) if Y[i]==l])
        scatter(tempArr[:,0], tempArr[:,1],s=pi*i**2,label = label_map[l],cmap='Set1')
        i += 2 
    
    xlabel('PC 1')
    ylabel('PC 2')
    legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    savefig('HAC_'+fileName + '_PCA.png')
    show()


# In[8]:

def generateLabels(clusters,x):
    labels = zeros((x,), dtype=int)
    for i in range(len(clusters)):
        for j in range(len(clusters[i])):
            labels[clusters[i][j]] = i+1
    return labels


# In[9]:

def jaccardCoeff(actualLabels,Y):
    aMat = makeJaccardMatrix(actualLabels)
    bMat = makeJaccardMatrix(Y)
    m11 = 0
    m10 = 0
    l = len(Y)
    for i in range(l):
        for j in range(l):
            if aMat[i][j] == bMat[i][j] == 1:
                m11 += 1
            elif aMat[i][j] != bMat[i][j]:
                m10 += 1
    return m11/(m11+m10)


# In[14]:

def makeJaccardMatrix(Y):
    size = len(Y)
    aMat = zeros((size,size), dtype=int)
    for i in range(size):
        for j in range(size):
            if Y[i] == Y[j]:
                aMat[i][j] = 1
                aMat[j][i] = 1
    return aMat


# In[46]:

def printClusters(clusters):
    for i in range(len(clusters)):
        clusters[i].sort()
        if clusters[i][0] == -1:
            print('cluster ' +str(-1) + " -> ", clusters[i])
        else:
            print('cluster ' +str(i+1) + " -> ", clusters[i])


# In[47]:

def hacAlgorithm(data, clustersSize):
    x,y = shape(data)
    heap = []
    for i in range(x):
        for j in range(i+1,x):
            d = euclidean_distance(data[i],data[j])
            elems = [i,j]
            item = (d,elems)
            heappush(heap, item)
    test_set = DisjointSet([i for i in range(x)])
    while heap:
        elems = heappop(heap)[1]
        test_set.union(elems[0],elems[1])
        if clustersSize == test_set.getSize():
            break;
            
    return test_set.get()


# In[48]:

if __name__=='__main__':
    optparser = OptionParser()
    optparser.add_option('-f', '--inputFile',
                         dest='input',
                         help='filename containing data',
                         default=None)
    optparser.add_option('-s', '--clustersSize',
                         dest='clustersSize',
                         help='clusters count at which algorithm stops',
                         default=5,
                         type='float')
    
    (options, args) = optparser.parse_args()
    
    fileName = None
    if options.input is None:
        fileName = sys.stdin
    elif options.input is not None:
        fileName = options.input
    else:
        print ('Data File Missing\n')
        sys.exit('System will exit')
    
    clustersSize = options.clustersSize
    
    data, actualLabels, idx = loadDataSet(fileName)
    
    clusters = hacAlgorithm(data,clustersSize)
    
    Y = generateLabels(clusters,shape(data)[0])
    
    res = jaccardCoeff(actualLabels, Y)
    
    testPCA(data,Y,fileName)
    
    printClusters(clusters)
    
    print('The Jaccard Coefficient = %5.3f.' % res)

