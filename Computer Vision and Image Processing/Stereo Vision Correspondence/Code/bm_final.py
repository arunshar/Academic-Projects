import numpy as np 
import scipy as sp
import matplotlib.pyplot as plt
from scipy import signal
from scipy import ndimage
import time

def blockmatching(size, searchrange):

  start = time.clock()

  leftim = sp.ndimage.imread('view3.png',flatten=True )
  rightim = sp.ndimage.imread('view1.png',flatten=True )

  # leftim = np.array([[0,0,0,0,0],[1,1,1,0,0],[1,1,1,0,0],[1,1,1,0,0],[0,0,0,0,0]])#<----------------------
  # rightim = np.array([[0,0,0,0,0],[0,0,1,1,1],[0,0,1,1,1],[0,0,1,1,1],[0,0,0,0,0]])#<----------------------

  disp_map = np.zeros((rightim.shape[0],rightim.shape[1]))
  # map = np.zeros()  
  for i in range(rightim.shape[0]):
    for j in range(rightim.shape[1]):
      # print i,j#<----------------------
      template = rightim[i-size/2:i+size/2+1,j-size/2:j+size/2+1]
      # print template#<----------------
      min = 99999999
      for p in range(searchrange):
        match = leftim[i-size/2:i+size/2+1,j-size/2-p:j+size/2-p+1] #modify only column range.
        # print match#<----------------------

        if template.shape == match.shape:
          diff = template - match
          abs_diff = np.absolute(diff)
          temp = np.sum(abs_diff**2)
          if temp<min:
            min = temp 
            minx = i - p
        else:
          break
        
        # print minx#<----------------------
      # time.sleep(5)#<----------------------
    
      distance = np.abs(i - minx)
      disp_map[i][j] = distance
  
  print "time taken in seconds:{}".format( time.clock() - start)

  return disp_map
  # print disp_map#<------------------------------
  
# def main():

disp1 = sp.ndimage.imread('/media/23e97447-9196-4c8e-be28-b24a49d2548e/home/jayaraj/Study/CS_CVIP/project/Data/disp1.png',flatten=True )
print "block matching with block size 3"
disp_map_size3= blockmatching(3,50)
# mse_size3 = (np.sqrt(np.sum(np.asarray(abs(disp_map_size3 - disp1))**2)))/(disp1.shape[0]*disp1.shape[1])
mse_size3 =  np.mean(np.abs(disp_map_size3[:,50:-50] - disp1[:,50:-50])**2)#<--- calculating mse excluding okklusion 
print "block matching with block size 5"
disp_map_size5= blockmatching(5,50)
# mse_size5 = np.sqrt(np.sum(np.asarray(abs(disp_map_size5 - disp1))**2))/(disp1.shape[0]*disp1.shape[1])
mse_size5 = np.mean(np.abs(disp_map_size5[:,50:-50] - disp1[:,50:-50])**2)
print "block matching with block size 9"
disp_map_size9= blockmatching(9,50)
# mse_size9 = np.sqrt(np.sum(np.asarray(abs(disp_map_size9 - disp1))**2))/(disp1.shape[0]*disp1.shape[1])
mse_size9 = np.mean(np.abs(disp_map_size9[:,50:-50] - disp1[:,50:-50])**2)
# blockmatching(3,50)

#*********no need**********************
#normalising (
# minn = np.amin(disp_map)
# maxx = np.amax(disp_map)
# norm_disp_map = np.zeros((disp_map.shape[0],disp_map.shape[1]))
# for i in range(disp_map.shape[0]):
#   for j in range(disp_map.shape[1]):
#     norm_disp_map[i][j] = disp_map[i][j]*255/maxx
#*******************************

# plt.imshow(norm_disp_map,cmap='Greys_r')
plt.subplot(311)
title_size3 = 'Disparity Map for size 3, mse = '+str(mse_size3)
plt.title(title_size3)
plt.imshow(disp_map_size3,cmap='Greys_r')

plt.subplot(312)
title_size5 = 'Disparity Map for size 5, mse = '+str(mse_size5)
plt.title(title_size5)
plt.imshow(disp_map_size5,cmap='Greys_r')

plt.subplot(313)
title_size9 = 'Disparity Map for size 9, mse = '+str(mse_size9)
plt.title(title_size9)
plt.imshow(disp_map_size9,cmap='Greys_r')

plt.show()

