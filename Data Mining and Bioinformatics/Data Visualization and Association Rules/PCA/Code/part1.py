import numpy as np
from numpy import linalg as LA
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.decomposition import *




###################
# Configurations: #
###################

#data file path
filePath = 'C:/Users/presh/Google Drive/MS/Sem 3/DM/Projects/Project 1/part1data/'

#list of files to read.  Eg: files = ['pca_a.txt','pca_b.txt']
#files = ['pca_a.txt','pca_b.txt','pca_c.txt','pca_demo.txt']
files = ['pca_c.txt']

#list of algos. Eg: files = ['pca','svd','tsne']
#algos = ['pca','svd','tsne']
algos = ['tsne']







##############
# Functions: #
##############

def getDataFromFile(fileName):
	file = filePath+fileName
	fo = open(file)
	Xstring = fo.read()
	Xrows = Xstring.split('\n')
	Xmat = []
	for row in Xrows:
		subX = []
		for x in row.split('\t'):
			subX.append(x)
		Xmat.append(subX)

	X = np.matrix(Xmat)
	return X

def doPCA(x):
        N = x.shape[0]
        meanx = np.mean(x,axis = 0)
        x1 = x - meanx
        x1t = np.transpose(x1)        

        #S = np.dot(x1t,x1)/N
        S = np.cov(x1t)
        
        evals, evect = LA.eig(S)
        
        idx = (-evals).argsort()[:d]
#        print(idx)
        sevals = evals[idx]
        sevect = evect[:,idx]
#        print(sevals)
#        print(sevect)
#        print(S)
#        print(np.transpose(sevect))
        ret = np.dot(x1,sevect)

        return ret

def doSVD(x):
        

        y = TruncatedSVD(n_components=d,random_state=0).fit_transform(x)
        #U,s,V = LA.svd(x1,full_matrices = False, compute_uv = True)
        #S = np.diag(s)
        #U = U[:,:d]
        #S = S[:d,:d]
        ##V = V[:d,:d]
        ##y = np.dot(U, np.dot(S, V))
        #y = np.dot(U,S)
        
        return y

        
def dotSNE(x):

        
        y = TSNE(n_components=d, perplexity=50, learning_rate=300, verbose = 2).fit_transform(x)
        return y
        

def getLabels(X,l):
	return np.unique(np.array(X[:,l]))

def plotGraph(y,X,labels,title,file):
        cmap = plt.get_cmap('Set1')
        for labl in labels:
                plt.scatter(y[np.where(X==labl)[0],0],y[np.where(X==labl)[0],1],color=cmap(np.where(labels==labl)[0]/float(labels.shape[0])),label = labl)
        plt.title(title + ' for ' + file)
        plt.legend(loc='upper left', numpoints=1, frameon=False, fontsize=10)
        plt.savefig(file+'_'+title+'.png')
        plt.show()

def reduceDimension(file,algo):
        X = getDataFromFile(file)
        labelColumn = X.shape[1]-1
        
        x = X[:,:labelColumn].astype(np.float)

        if(algo == 'pca'):
                y = doPCA(x)
        elif(algo == 'svd'):
                y = doSVD(x)
        elif(algo == 'tsne'):
                y = dotSNE(x)
        else:
                print("Invalid Algo")
                exit(0)
        
        labels = getLabels(X,labelColumn)
        
        plotGraph(y,X,labels,algo,file)
        



################
# Main Begins: #
################



#reduced diminsion count
d = 2

for algo in algos:
        for file in files:
                reduceDimension(file,algo)



