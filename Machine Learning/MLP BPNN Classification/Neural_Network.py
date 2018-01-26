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

print "Neural Network"
def TrainNeural(passes,hidden,output):
    w1 = np.random.randn(len(training_data[0][1]),hidden)
    b1 = np.zeros(hidden)
    w2 = np.random.randn(hidden,output)
    b2 = np.zeros(output)
    for epochs in range(0,passes):
        for i in range(0,len(training_data[0])):
            z1 = np.dot(train[i],w1) + b1
            a1 = np.tanh(z1)
            z2 = np.dot(a1,w2) + b2
            y = np.exp(z2)/np.sum(np.exp(z2));
            dk = (y - en1[i])
            dj = np.multiply((1 -np.power(a1,2)),(dk*w2.T))
            delta_w1 = np.dot(train[i].T,dj)
            delta_w2 = np.dot(a1.T,dk)
            w1 = w1 - 0.01*(delta_w1)
            w2 = w2 - 0.01*(delta_w2)    
        
    z1 = train*w1
    a1 = np.tanh(z1)
    z2 = a1*w2   
    predict_lab = np.zeros(len(training_data[0]))
    for i in range(0,len(training_data[0])):
        for j in range(0,10):
            if z2[i,j] == np.max(z2[i]):
                predict_lab[i] = j
    count = np.count_nonzero(predict_lab-target1)
    accuracy = (1 - count/len(train))*100
    print "MNIST trainig accuracy :", accuracy
    
    z1 = val*w1
    a1 = np.tanh(z1)
    z2 = a1*w2   
    predict_lab = np.zeros(len(validation_data[0]))
    for i in range(0,len(val)):
        for j in range(0,10):
            if z2[i,j] == np.max(z2[i]):
                predict_lab[i] = j
    count = np.count_nonzero(predict_lab-target3)
    accuracy = (1 - count/len(val))*100
    print "MNIST validation accuracy :", accuracy

        
    z1 = test*w1
    a1 = np.tanh(z1)
    z2 = a1*w2   
    predict_lab = np.zeros(len(test_data[0]))
    for i in range(0,len(test_data[0])):
        for j in range(0,10):
            if z2[i,j] == np.max(z2[i]):
                predict_lab[i] = j
    count = np.count_nonzero(predict_lab-target2)
    accuracy = (1 - count/len(test))*100
    print "MNIST testing accuracy :", accuracy

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
            samples.append(vector1)
            labels.append(i)

    z1 = samples*w1
    a1 = np.tanh(z1)
    z2 = a1*w2
    z2 = np.asmatrix(z2)   
    predict_lab = np.zeros(len(labels))
    for i in range(0,len(vector1)):
        for j in range(0,10):
            if z2[i,j] == np.max(z2[i]):
                predict_lab[i] = j
    count = np.count_nonzero(predict_lab-labels)
    accuracy = (1 - count/len(samples))*100
    print "USPS accuracy :", accuracy

    print len(vector1)
TrainNeural(5,150,10)
