import cv2
import numpy as np
import scipy
from scipy import signal
from matplotlib import pyplot as plt
import numpy.matlib

I = cv2.imread('MixedVegetables.jpg',0);
I1 = np.array(I);

[row, col] = np.shape(I1);
row1 = row*2;
col1 = col*2
expand = np.matlib.zeros((row1,col1));

k = 0;
count = 1;
for i in range(0,row):
    count = count + 1;
    l = 0;
    for j in range(0,col):
        expand[k,l] = I1[i,j]
        l = l + 2
    k = k + 2;

cv2.imwrite('expanded.png',expand)

for i in range(0,row1-2,2):
    for j in range(0,col1-2,2):
            expand[i,j+1]=abs(np.subtract(expand[i,j],expand[i,j+2]));
            expand[i+1,j]=abs(np.subtract(expand[i,j],expand[i+2,j]));
            
thresh = 20
for i in range(0,row1-2,2):
    for j in range(0,col1-2,2):
        if expand[i,j+1] > thresh:
            expand[i,j+1] = 255
        if expand[i+1,j] > thresh:
            expand[i+1,j] = 255

cv2.imwrite('crack_edge.png',expand)


#med = scipy.signal.medfilt(expand,3)

#expand1 = np.matlib.zeros((row1,col1));
thresh = 110
for i in range(0,row1-1):
    for j in range(0,col1-1):
        if expand[i,j]-expand[i,j+1] > thresh:
            expand[i,j] = 255

for i in range(0,row1-1):
    for j in range(0,col1-1):
        if expand[i,j]-expand[i+1,j] > thresh:
            expand[i,j] = 255

cv2.imwrite('new_crack_edge.png',expand)

