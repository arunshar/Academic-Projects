'''
	A main driver program that will call the mapper and reducer multiple 
	times until the centroids converge.
'''
import subprocess
from utils import *

if __name__ == "__main__":
	dataFile = 'data/iyer.txt'
	numCentroids = 10
	outputFolder = "data-output"
	maxIterations = 100
	initialGeneID = [357,509,435,66,163,197,53,392,329,190]

	hadoopPath = "/usr/local/hadoop/bin/"
	hdfsClearDataCommand = "{}hdfs dfs -rm -r ~/run-data".format(hadoopPath)
	hdfsMakeDirectoryCommand = "{}hdfs dfs -mkdir ~/run-data".format(hadoopPath)
	hdfsPutDataCommand = "{}hdfs dfs -put {} ~/run-data/".format(hadoopPath, dataFile)
	hdfsRemoveOutputCommand = "{}hdfs dfs -rm -r {}".format(hadoopPath, outputFolder)
	hadoopCommand = "{}hadoop jar hadoop-streaming-2.7.4.jar -files mapper.py,reducer.py,centroids.txt -mapper mapper.py -reducer reducer.py -input ~/run-data -output {}".format(hadoopPath, outputFolder)
	fetchCentroidsCommand = "{}hdfs dfs -cat {}/*".format(hadoopPath,outputFolder)
	#onlyMapperCommand = "cat {} | ./mapper.py".format(dataFile)

	converged = False
	iterations = 0
	tempStdOutput = None

	groundTruth,data = readDataFromFile(dataFile)
	currentCentroids = assignInitialCentroids(initialGeneID, data,'centroids.txt',numCentroids)
	
	subprocess.Popen(hdfsClearDataCommand, shell=True, stdout=subprocess.PIPE).stdout.read()	
	subprocess.Popen(hdfsMakeDirectoryCommand, shell=True, stdout=subprocess.PIPE).stdout.read()
	subprocess.Popen(hdfsPutDataCommand, shell=True, stdout=subprocess.PIPE).stdout.read()
	
	while not converged:
		subprocess.Popen(hdfsRemoveOutputCommand, shell=True, stdout=subprocess.PIPE).stdout.read()	
		subprocess.Popen(hadoopCommand, shell=True, stdout=subprocess.PIPE).stdout.read()	
		fetchedReducerOutput = subprocess.Popen(fetchCentroidsCommand, shell=True, stdout=subprocess.PIPE).stdout.read()	
		updatedCentroids = processCentroids(fetchedReducerOutput, 'centroids.txt')
		iterations+=1
		if checkConvergence(currentCentroids,updatedCentroids):
		 	converged = True		
		if iterations == maxIterations:
			converged = True
		currentCentroids = updatedCentroids

	print "Total Iterations: ", iterations
	
	resultClusters, finalClusters = assignCentroidToData(data, currentCentroids)

	print "Jaccard:",calculateJaccard(groundTruth, resultClusters)
	print "Rand:", calculateRand(groundTruth, resultClusters)
	
	print "Final Clusters (cluster, [GeneIDs]):"
	for cluster in finalClusters:
		stringOuptut = ",".join([str(i) for i in finalClusters[cluster]])
		print "{}:\t{}".format(cluster,stringOuptut)

	calculatePCA(data, resultClusters, currentCentroids, "K-Means Clustering Result")