import numpy as np 
import scipy as sp
import matplotlib.pyplot as plt
import time
from scipy import ndimage
#import time
print "executing... takes about 5 mins.."
start_time = time.time()
leftim = sp.ndimage.imread('view3.png',flatten=True);
rightim = sp.ndimage.imread('view1.png',flatten=True);

plt.imshow(leftim,cmap='Greys_r')
plt.imshow(rightim,cmap='Greys_r')

o = 20
disp = np.zeros((leftim.shape[0],leftim.shape[1]))

for row in range(leftim.shape[0]):
    cost = np.zeros((leftim.shape[1],leftim.shape[1]))
    M = np.zeros((leftim.shape[1],leftim.shape[1])) #<-----------------
    for i in range(1,leftim.shape[0]):
        cost[i][0] = i*o
    for i in range(1,leftim.shape[0]):
        cost[0][i] = i*o
    for i in range(1,leftim.shape[1]):
        for j in range(1,rightim.shape[1]):
            temp = abs(leftim[row,i]-rightim[row,j])
            min1 = cost[i-1][j-1] + temp
            min2 = cost[i-1][j] + o
            min3 = cost[i][j-1] + o
            cmin = min(min1,min2,min3)
            cost[i][j] = cmin
            if (cmin == min1):
                M[i][j] = 1
            elif (cmin == min2):
                M[i][j] = 2;
            elif (cmin == min3):
                M[i][j] = 3;
                
    i = leftim.shape[1]-1
    j = leftim.shape[1]-1

    while (i != 0) & (j != 0):
        if M[i][j] == 1:
            disp[row][j] = abs(j-i)
            i -= 1
            j -= 1
        if M[i][j] == 2:
            i -= 1
        if M[i][j] == 3:
            j -= 1

plt.imshow(disp,cmap = 'Greys_r')
disp_ground = sp.ndimage.imread('/media/23e97447-9196-4c8e-be28-b24a49d2548e/home/jayaraj/Study/CS_CVIP/project/Data/disp5.png',flatten=True )

# result = np.mean(np.square(disp_ground-disp))
result = np.mean(np.square(disp_ground[:,50:]-disp[:,50:]))

# print("--- %s time taken in seconds ---" % (time.time() - start_time))
title = "Disparity map for occlusion"+ str(o) +" mse:"+str(result)
plt.title(title)
plt.show()


# minn = np.amin(disp)
# maxx = np.amax(disp)
# norm_disp_map = np.zeros((disp.shape[0],disp.shape[1]))
# for i in range(disp.shape[0]):
#   for j in range(disp.shape[1]):
#     norm_disp_map[i][j] = disp[i][j]*255/maxx