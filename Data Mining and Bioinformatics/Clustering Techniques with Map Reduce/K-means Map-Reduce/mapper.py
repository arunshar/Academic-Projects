#!/usr/bin/env python

import sys
import numpy as np

f = open("centroids.txt", 'r')
lines = f.readlines()
f.close()
centroids = []

for centroid in lines:
	x = centroid.strip().split("\t")
	centroids.append(np.array(x, dtype=float))

for line in sys.stdin:
	line = line.strip()
	dataPoint = line.split("\t")
	dataPoint = np.array(dataPoint[2:], dtype=float)
	clusterID = min([(a[0],np.linalg.norm(dataPoint-a[1])) for a in enumerate(centroids)], key = lambda y:y[1])[0]
	dataPoint = "\t".join([str(a) for a in dataPoint])
	print '%s\t%s' % (clusterID, dataPoint)