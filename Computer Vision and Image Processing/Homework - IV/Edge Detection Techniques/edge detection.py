import cv2
import numpy as np
import scipy
from scipy import signal
from matplotlib import pyplot as plt
X = cv2.imread('UBCampus.jpg',0);

X1 = np.array(X)
m3 = np.asmatrix([[0, 0, -1, -1, -1, 0, 0],[0, -2, -3, -3, -3, -2, 0],[-1, -3, 5, 5, 5, -3, -1],[-1, -3, 5, 16, 5, -3, -1],[-1, -3, 5, 5, 5, -3, -1],[0, -2, -3, -3, -3, -2, 0],[0, 0, -1, -1, -1, 0, 0]]);

x1 = signal.convolve2d(X1,m3,boundary='symm',mode='same');
cv2.imwrite('image.png',x1)
[row, col] = np.shape(x1)

cv2.imwrite('DoG.png',x1)
zero_cross = np.zeros(np.shape(x1))

for i in range(0,row-1):
    for j in range(0,col-1):
        if x1[i][j]*x1[i][j+1] < 0:
            zero_cross[i][j] = 255
        if x1[i][j]*x1[i+1][j] < 0:
            zero_cross[i][j] = 255
            
cv2.imwrite('zerocrossing_DoG.png',zero_cross)

dx = cv2.Sobel(X1,cv2.CV_64F,1,0,ksize = 3);
dy = cv2.Sobel(X1,cv2.CV_64F,0,1,ksize = 3);
sobel_image = np.hypot(dx,dy);

[row1, col1] = np.shape(sobel_image);
for i in range(0,row1-1):
    for j in range(0,col1-1):
        if sobel_image[i][j] < 105:
            sobel_image[i][j] = 0

cv2.imwrite('sobel_DoG.png',sobel_image)

final_image = np.logical_and(zero_cross,sobel_image);

plt.imshow(final_image,cmap='gray',interpolation='bicubic')
plt.show()


#m3 = np.asmatrix([[0, 0, -1, -1, -1, 0, 0],[0, -2, -3, -3, -3, -2, 0],[-1, -3, 5, 5, 5, -3, -1],[-1, -3, 5, 16, 5, -3, -1],[-1, -3, 5, 5, 5, -3, -1],[0, -2, -3, -3, -3, -2, 0],[0, 0, -1, -1, -1, 0, 0]]);
#m3 = np.asmatrix([[0, 0, -1, -1, -1, 0, 0],[0, -2, -3, -3, -3, -2, 0],[-1, -3, 5, 5, 5, -3, -1],[-1, -3, 5, 16, 5, -3, -1],[-1, -3, 5, 5, 5, -3, -1],[0, -2, -3, -3, -3, -2, 0],[0, 0, -1, -1, -1, 0, 0]]);
m3 = [[0, 0, 1, 0, 0],[0, 1, 2, 1, 0],[1, 2, -16, 2, 1],[0, 1, 2, 1, 0],[0, 0, 1, 0, 0]];
x1 = signal.convolve2d(X1,m3,boundary='symm',mode='same');
cv2.imwrite('image.png',x1)
[row, col] = np.shape(x1)

cv2.imwrite('LoG.png',x1)
zero_cross = np.zeros(np.shape(x1))

for i in range(0,row-1):
    for j in range(0,col-1):
        if x1[i][j]*x1[i][j+1] < 0:
            zero_cross[i][j] = 255
        if x1[i][j]*x1[i+1][j] < 0:
            zero_cross[i][j] = 255
            
cv2.imwrite('zerocrossing_LoG.png',zero_cross)

#dx = cv2.Sobel(X1,cv2.CV_64F,1,0,ksize = 3);
#dy = cv2.Sobel(X1,cv2.CV_64F,0,1,ksize = 3);
#sobel_image = np.hypot(dx,dy);

[row1, col1] = np.shape(sobel_image);
for i in range(0,row1-1):
    for j in range(0,col1-1):
        if sobel_image[i][j] < 120:
            sobel_image[i][j] = 0

cv2.imwrite('sobel_LoG.png',sobel_image)
final_image = np.logical_and(zero_cross,sobel_image);

plt.imshow(final_image,cmap='gray',interpolation='bicubic')
plt.show()
