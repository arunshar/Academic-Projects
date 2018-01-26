from __future__ import division
import cPickle
import gzip
import numpy as np
import glob
import cv2
filename = 'mnist.pkl.gz'
f = gzip.open(filename, 'rb')
training_data, validation_data, test_data = cPickle.load(f)
f.close()

#training data
train = np.asmatrix(training_data[0]) 
target1 = np.asmatrix(training_data[1])
en1 = np.asmatrix(np.zeros((10,len(train))))
en1 = np.transpose(en1);
for i in range(0,len(train)):
    en1[i,target1[0,i]] = 1 

#testing data
test = np.asmatrix(test_data[0]) 
target2 = np.asmatrix(test_data[1]) 
en2 = np.asmatrix(np.zeros((10,len(test))))
en2 = np.transpose(en2);
for i in range(0,len(test)):
    en2[i,target2[0,i]] = 1

#validation data
val = np.asmatrix(validation_data[0]) 
target3 = np.asmatrix(validation_data[1]) 
en3 = np.asmatrix(np.zeros((10,len(val))))
en3 = np.transpose(en3);
for i in range(0,len(val)):
    en3[i,target3[0,i]] = 1

w = np.asmatrix(np.zeros((784,10))) 

y = np.asmatrix(np.zeros((len(train),10)))
y1 = np.asmatrix(np.zeros((len(val),10)))
y2 = np.asmatrix(np.zeros((len(test),10)))

deltaE = np.asmatrix(np.zeros((784,10)))
b = np.ones(10);
A = np.zeros(10);

for passes in range(0,1):    
    for i in range(0,len(train)):
        for j in range(0,10):
            A[j] = np.dot((w.T[j,:]),(train.T[:,i])) + b[j]
        for j in range(0,10):
            y[i,j] = np.exp(A[j])/np.sum(np.exp(A));        
        deltaE = (train[i,:].T*(y[i,:]-en1[i,:]))
        w = w - 0.01*deltaE
        
#training set
predict_lab = np.zeros(len(train))
predict_lab = np.zeros(len(train))
for i in range(0,len(y)):
    for j in range(0,10):
        if y[i,j] == np.max(y[i]):
            predict_lab[i] = j
count = np.count_nonzero(predict_lab-target1)
accuracy = (1 - count/len(train))*100
print "accuracy for MNIST training :", accuracy

#validation set
for i in range(0,len(val)):
    for j in range(0,10):
        A[j] = np.dot((w.T[j,:]),(val.T[:,i])) + b[j]
    for j in range(0,10):
        y1[i,j] = np.exp(A[j])/np.sum(np.exp(A));

predict_lab = np.zeros(len(val))
for i in range(0,len(y1)):
    for j in range(0,10):
        if y1[i,j] == np.max(y1[i]):
            predict_lab[i] = j
count = np.count_nonzero(predict_lab-target3)
accuracy = (1 - count/len(val))*100
print "accuracy for MNIST validation :", accuracy

#test set
for i in range(0,len(test)):
    for j in range(0,10):
        A[j] = np.dot((w.T[j,:]),(test.T[:,i])) + b[j]
    for j in range(0,10):
        y2[i,j] = np.exp(A[j])/np.sum(np.exp(A));
    
predict_lab = np.zeros(len(test))

for i in range(0,len(test)):
    for j in range(0,10):
        if y2[i,j] == np.max(y2[i]):
            predict_lab[i] = j
count = np.count_nonzero(predict_lab-target2)
accuracy = (1-count/len(test))*100
print "accuracy for MNIST testing :", accuracy

#USPS dataset
count = 1
samples = []
labels = []
for i in range(0,10):    
    directory = './Numerals/' +str(i)+ '/*.png'
    for filename in glob.glob(directory):
        image = cv2.imread(filename,0)
        resized_image = cv2.resize(image, (28, 28))
        vector = np.transpose(resized_image.flatten())
        vector = np.array(vector, dtype=float)
        vector1 = abs(np.divide(vector,255) - np.ones((np.shape(vector))))
            #count += 1
            #print count
        samples.append(vector1)
        labels.append(i)
        
y3 = np.asmatrix(np.zeros((len(samples),10)))
samples = np.asmatrix(samples)

for i in range(0,len(samples)):
    for j in range(0,10):
        A[j] = np.dot((w.T[j,:]),(samples.T[:,i])) + b[j]
    for j in range(0,10):
        y3[i,j] = np.exp(A[j])/np.sum(np.exp(A));

predict_lab = np.zeros(len(samples))

for i in range(0,len(samples)):
    for j in range(0,10):
        if y3[i,j] == np.max(y3[i]):
            predict_lab[i] = j
count = np.count_nonzero(predict_lab-labels)
accuracy = (1-count/len(predict_lab))*100
print "USPS accuracy: ", accuracy