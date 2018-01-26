import numpy as np
from numpy import linalg as LA
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import euclidean_distances
import random
from collections import defaultdict
from sklearn.decomposition import *
from numpy import linalg as LA


###################
# Configurations: #
###################

getCentroidsFromFile =True
centroidFile = 'cho_centroid.txt'
initCentIdx = np.array([5,25,32,100,132])

useReducedK=False
kFixed=5

useReducedIter = False
iLimit = 10

#data file path
filePath = './'

#list of files to read.  Eg: files = ['pca_a.txt','pca_b.txt']
files = ['cho.txt']

#list of algos. Eg: files = ['pca','svd','tsne']
algo = "kmeans"


#get_ipython().magic('matplotlib inline')
def plotGraph(y,X,labels,title,file):
        cmap = plt.get_cmap('Set1')
        print(np.unique(labels))
        #for labl in labels:
            #plt.scatter([y[np.where(X==labl)[0],0]],[y[np.where(X==labl)[0],1]],color=cmap(np.where(labels==(int(labl) if title=="GT" else (int(labl)+1)))[0]/float(labels.shape[0])),label = labl)
                #plt.scatter([y[np.where(X[:,1]==labl)[0],0]],[y[np.where(X[:,1]==labl)[0],1]],color=cmap(np.where(labels==labl)[0]/float(labels.shape[0])),label = labl)
                #y1 = np.where(X[:,1]==labl)
                #plt.scatter(y[y1[0],0],y[y1[0],1],c=np.full((len(y1),1),labl),label = labl)                
        plt.title(title+'_MapReduce'+ ' for ' + file)
        plt.scatter(y[:,0],y[:,1],c=labels);
        #plt.legend(loc='upper left', numpoints=1, frameon=False, fontsize=10)
        plt.savefig(file+'_'+title+'.png')
        plt.show()



def doPCA(x):
        pca = PCA(n_components=2)
        return pca.fit_transform(x)


def getJaccard(p,c):
        l = p.shape[0]
        cIM =  np.zeros((l,l), dtype=bool)
        gIM =  np.zeros((l,l), dtype=bool)
        p = np.asarray(p, dtype = np.int) - 1
        for i in range(0,l):
                for j in range(0,l):
                        gIM[i,j] = p[i]==p[j]
                        cIM[i,j] = c[i]==c[j]
        
        M11 = np.sum(gIM&cIM)
        M101= np.sum(gIM^cIM)
        jaccard = (M11*100)/(M101+M11)
        print(jaccard)


def readRawFromFile(fileName):
        file = filePath+fileName
        fo = open(file)
        Xstring = fo.read()
        Xrows = Xstring.split('\n')
        return np.array([row.split('\t') for row in Xrows])


def readFromFile(fileName):
        Xmat = readRawFromFile(fileName)
        print(Xmat.shape)
        return Xmat[Xmat[:,1] != '-1']

def getInitCentroid():
        centMat = readRawFromFile(centroidFile)
        return centMat.astype(np.float)


def findCluster(fileName):
        X = readFromFile(fileName)
        geneIdCol = 0
        pCol = 1
        p = np.array(X[:,pCol])
        K = np.unique(p)
        k = kFixed if useReducedK else K.size
        
        x = X[:,pCol+1:].astype(np.float)
        d = x.shape[1]
        l = x.shape[0]
        #init new centroids
        #centroid = getInitCentroid() if getCentroidsFromFile else x[np.random.randint(0,l-1,k), :]
        centroid = x[initCentIdx-1] if getCentroidsFromFile else x[np.random.randint(0,l-1,k), :]
        print(centroid)
        prevCent = centroid.copy()
        it =0

        while(True):
                it += 1
                #get dist to new centroids
                dist = euclidean_distances(x,centroid)
                clusterIdx = np.argmin(dist,axis = 1)
                #assign to clusters
                for i in np.unique(clusterIdx):
                        centroid[i] = np.mean(x[clusterIdx==i], axis = 0)
                if (centroid==prevCent).all():
                        break
                if(useReducedIter and iLimit==it):
                        break
                prevCent = centroid.copy()

        print(centroid)
        c = clusterIdx
        for k in K:
                print(c)
        print("hola")
        print(c+1)
        print(it)
        getJaccard(p,c)
        y=doPCA(x)


        #plotGraph(y,X,p.asType(int),"GT",file)

        X[:,pCol]=c
        plotGraph(y,X,c,algo,file)



for file in files:
        findCluster(file)
