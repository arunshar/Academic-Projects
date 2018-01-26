
"""
FOR STOCHASTIC GRADIENT DESCENT FOR SYNTHETIC DATASET, CHANGE THE VALUE OF FROM INVERSE MATRIX (inv1, inv2, inv3) TO IDENTITY MATRIX (Iden1)
"""

import csv
import numpy as np
dataset = csv.reader(open('Querylevelnorm_X.csv','rU'));
nominal = csv.reader(open('Querylevelnorm_t.csv','rU'));
#dataset = csv.reader(open('input.csv','rU'));
#nominal = csv.reader(open('output.csv','rU'));
x1 = list(dataset);
x2 = list(nominal);
print "LeToR DATASET"
M = 16;
lamda = 0
eeta = 0.00000001;
#print "REMARK : ONLY FOR SYNTHETIC DATASET"
#print "FOR STOCHASTIC GRADIENT DESCENT FOR SYNTHETIC DATASET, CHANGE THE VALUE OF FROM INVERSE MATRIX (inv1, inv2, inv3) TO IDENTITY MATRIX (Iden1)"
#print  "Just comment out in the SCG loop. Discard the closed form solution (CF) of synthetic dataset while calculating it's SGD. "
#print "FOR CLOSED FORM SOLUTION FOR SYNTHETIC DATASET RUN THE LOOP just take inv1, inv2 and inv3 and discard its SGD value while considering CF"
#print "lamda : ", lamda
#print "M : ", M

target_values = x2
length1 = int(0.8*len(x1))
length2 = int(0.9*len(x1))
training_set = x1[0:length1]

testing_set = x1[length2:len(x1)]
training_set = np.array(training_set, dtype = 'float_')


#covariance matrix inverse
x3 = [];
for i in range(0,len(training_set[0])):
    ele1= np.var(training_set[:,i]);
    if (ele1 == 0.0):
        x3.append(0.0001);
    else: x3.append(ele1);
#print(x3) 
daignal_cov_mat = np.diag(x3);
inv1 = np.linalg.inv(daignal_cov_mat);

Iden1 = np.eye(len(training_set[1,:]),len(training_set[1,:]))
Iden1 = Iden1 + Iden1*0;

batch_len = int(len(training_set)/M);
batch_len1 = int(len(training_set)/M);

#taking mean 
temp = 0;
x6 = [];
dummy = np.zeros(len(training_set[1]));
for t in range(0,M):
    batch_len = batch_len + temp;
    x6 = training_set[temp:batch_len]
    x3 = [];
    for column in range(0,len(x6[0])):
        for row in range(0,len(x6)):
            x = [];
            ele2 = x6[row][column];
            x.append(ele2);
        x5 = np.transpose(x)
        ele3 = np.mean(x5);
        x3.append(ele3);
    temp = batch_len1;
    stack_row = np.asarray(x3);
    if t == 0:        
        mean = np.vstack((dummy,stack_row))
    else: mean = np.vstack((mean,stack_row))

mean = np.delete(mean,0,axis=0);
#print(mean)

#taking phi3
dummy = np.zeros(M);
for row in range(0,len(training_set)):
    phi = [];
    for col in range(0,len(mean)):
        stack_row1 = training_set[row] - mean[col]
        stack_row1 = np.asarray(stack_row1);
        stack_row2 = np.transpose(stack_row1);
        phi1 = stack_row1.dot(inv1).dot(stack_row2);
        #phi1 = stack_row1.dot(Iden1).dot(stack_row2);
        phi1 = -phi1/2;
        phi1 = np.exp(phi1);
        phi.append(phi1)
    stack_row3 = np.asarray(phi);
    if row == 0:        
        phi3 = np.vstack((dummy,stack_row3))
    else: phi3 = np.vstack((phi3,stack_row3))

phi3 = np.delete(phi3,0,axis=0);

target_values1 = np.array(target_values, dtype = 'float_')
output_values = target_values1[0:length1]
val2 = np.asanyarray(output_values);


w3 = np.ones(M)
w3 = np.array(w3, dtype = 'float_')
w4 = np.matrix(w3);
w5 = np.ones(M)
w5 = np.array(w5, dtype = 'float_')
w5 = np.matrix(w5);
tp = np.matrix(w5);
deltaw = -w5*eeta
for i in range(0,len(training_set)):    
    prod = np.dot(w4,phi3.T)
    prod1 = np.transpose(prod);
    diff2 = (val2-prod1)
    diff2 = np.transpose(diff2);
    ed2 = -diff2.dot(phi3)
    ew2 = w4
    e2 = ed2 + lamda*ew2
    deltaw1 = np.multiply(deltaw,e2)
    w4 = w4 + deltaw1;

#print(w4)

prod = np.dot(w4,phi3.T)
prod1 = np.transpose(prod)
diff = (val2-prod1)
s1 = np.square(diff)
ed1 = sum(s1);
ed = ed1/2;

erms = np.sqrt(np.divide(2*ed,length1))
print "Training_Error SGD" , erms

phi3[:,0] = 1;
#print phi3
#print+(phi2)

Id = np.eye(M,M);
#inverse = np.linalg.pinv(phi3);
phi4 = (phi3.T).dot(phi3) + lamda*(Id.T);
inverse = (np.linalg.inv(phi4)).dot(phi3.T);
w = inverse.dot(val2)
#print(w)


tw = np.transpose(w);
tp = np.transpose(phi3);
prod = np.dot(tw,tp)
prod1 = np.transpose(prod)
diff = (val2-prod1)
#print(diff)
s1 = np.square(diff)
ed1 = sum(s1);
ed = ed1/2;
#print(ew)
wt = np.transpose(w);
ew1 = np.dot(wt,w)
ew = ew1/2;
#print(ew)
e = ed + np.multiply(lamda,ew);
#print e
erms = np.sqrt(np.divide(2*e,length1))
print "Training Error CF: ", erms

#------------------------------validation testing---------------------------------------
# We once again find out phi3 value, mean 

validation_set = x1[length1:length2]
validation_set = np.array(validation_set, dtype = 'float_')
#covariance matrix inverse
x4 = [];
for i in range(0,len(validation_set[0])):
    ele1= np.var(validation_set[:,i]);
    if (ele1 == 0.0):
        x4.append(0.0001);
    else: x4.append(ele1);
#print(x4) 
daignal_cov_mat1 = np.diag(x4);
inv2 = np.linalg.inv(daignal_cov_mat1);

batch_len2 = int(len(validation_set)/M);
batch_len3 = int(len(validation_set)/M);

temp1 = 0;
x7 = [];
dummy1 = np.zeros(len(validation_set[1]));
for t1 in range(0,M):
    batch_len2 = batch_len2 + temp1;
    x7 = validation_set[temp1:batch_len2]
    x3 = [];
    for column in range(0,len(x7[0])):
        for row in range(0,len(x7)):
            x = [];
            ele2 = x7[row][column];
            x.append(ele2);
        x5 = np.transpose(x)
        ele3 = np.mean(x5);
        x3.append(ele3);
    temp1 = batch_len3;
    stack_row4 = np.asarray(x3);
    if t1 == 0:        
        mean1 = np.vstack((dummy1,stack_row4))
    else: mean1 = np.vstack((mean1,stack_row4))

mean1 = np.delete(mean1,0,axis=0);
#print(mean1)

#taking phi4
dummy = np.zeros(M);
for row in range(0,len(validation_set)):
    phi = [];
    for col in range(0,len(mean1)):
        stack_row1 = validation_set[row] - mean1[col]
        stack_row1 = np.asarray(stack_row1);
        stack_row2 = np.transpose(stack_row1);        
        phi1 = stack_row1.dot(inv2).dot(stack_row2);
        #phi1 = stack_row1.dot(Iden1).dot(stack_row2);        
        phi1 = -phi1/2;
        phi1 = np.exp(phi1);
        phi.append(phi1)
    stack_row3 = np.asarray(phi);
    if row == 0:        
        phi4 = np.vstack((dummy,stack_row3))
    else: phi4 = np.vstack((phi4,stack_row3))
    
phi4 = np.delete(phi4,0,axis=0);

output_values1 = target_values1[length1:length2]
val2 = np.asanyarray(output_values1);

w3 = np.ones(M)
w3 = np.array(w3, dtype = 'float_')
w4 = np.matrix(w3);
w5 = np.ones(M)
w5 = np.array(w5, dtype = 'float_')
w5 = np.matrix(w5);
deltaw = -w5*0.000001
for i in range(0,len(validation_set)):    
    prod = np.dot(w4,phi4.T)
    prod1 = np.transpose(prod);
    diff2 = (val2-prod1)
    diff2 = np.transpose(diff2);
    ed2 = -diff2.dot(phi4)
    ew2 = w4
    e2 = ed2 + lamda*ew2
    deltaw1 = np.multiply(deltaw,e2)
    w4 = w4 + deltaw1;
    
prod = np.dot(w4,phi4.T)
prod1 = np.transpose(prod)
diff = (val2-prod1)
s1 = np.square(diff)
ed1 = sum(s1);
ed = ed1/2;

erms = np.sqrt(np.divide(2*ed,len(validation_set)))
print "Validation_Error SGD " , erms

phi4[:,0] = 1;
#print phi4

#inverse = np.linalg.pinv(phi3);
output_values1 = target_values1[length1:length2]
val3 = np.asanyarray(output_values1);
tp1 = np.transpose(phi4);
prod = np.dot(tw,tp1)
prod2 = np.transpose(prod)
diff2 = (val3-prod2)
s2 = np.square(diff2)
ed1 = sum(s2);
ed = ed1/2;
#print(ew)
wt = np.transpose(w);
ew1 = np.dot(wt,w)
ew = ew1/2;
#print(ew)
e = ed + np.multiply(lamda,ew);
#print e
erms = np.sqrt(np.divide(2*e,len(validation_set)))
print "Validation Error CF: ", erms

#------------------------------testing set---------------------------------------
# We once again find out phi3 value, mean and covaraince

testing_set = x1[length2:len(x1)]
testing_set = np.array(testing_set, dtype = 'float_')

x5 = [];
for i in range(0,len(testing_set[0])):
    ele1= np.var(testing_set[:,i]);
    if (ele1 == 0.0):
        x5.append(0.0001);
    else: x5.append(ele1);

daignal_cov_mat2 = np.diag(x5);
inv3 = np.linalg.inv(daignal_cov_mat2);

batch_len4 = int(len(testing_set)/M);
batch_len5 = int(len(testing_set)/M);

temp1 = 0;
x7 = [];
dummy2 = np.zeros(len(testing_set[1]));
for t1 in range(0,M):
    batch_len4 = batch_len4 + temp1;
    x7 = testing_set[temp1:batch_len4]
    x3 = [];
    for column in range(0,len(x7[0])):
        for row in range(0,len(x7)):
            x = [];
            ele2 = x7[row][column];
            x.append(ele2);
        x5 = np.transpose(x)
        ele3 = np.mean(x5);
        x3.append(ele3);
    temp1 = batch_len5;
    stack_row5 = np.asarray(x3);
    if t1 == 0:        
        mean2 = np.vstack((dummy2,stack_row5))
    else: mean2 = np.vstack((mean2,stack_row5))

mean2 = np.delete(mean2,0,axis=0);
#print(mean1)

#taking phi4
dummy = np.zeros(M);
for row in range(0,len(testing_set)):
    phi = [];
    for col in range(0,len(mean1)):
        stack_row1 = testing_set[row] - mean2[col]
        stack_row1 = np.asarray(stack_row1);
        stack_row2 = np.transpose(stack_row1);
        phi1 = stack_row1.dot(inv3).dot(stack_row2);
        #phi1 = stack_row1.dot(Iden1).dot(stack_row2);        
        phi1 = -phi1/2;
        phi1 = np.exp(phi1);
        phi.append(phi1)
    stack_row3 = np.asarray(phi);
    if row == 0:        
        phi5 = np.vstack((dummy,stack_row3))
    else: phi5 = np.vstack((phi5,stack_row3))
    
phi5 = np.delete(phi5,0,axis=0);

output_values2 = target_values1[length2:len(x2)]
val2 = np.asanyarray(output_values2);

w3 = np.ones(M)
w3 = np.array(w3, dtype = 'float_')
w4 = np.matrix(w3);
w5 = np.ones(M)
w5 = np.array(w5, dtype = 'float_')
w5 = np.matrix(w5);
deltaw = -w5*0.000001
for i in range(0,len(testing_set)):    
    prod = np.dot(w4,phi5.T)
    prod1 = np.transpose(prod);
    diff2 = (val2-prod1)
    diff2 = np.transpose(diff2);
    ed2 = -diff2.dot(phi5)
    ew2 = w4
    e2 = ed2 + lamda*ew2
    deltaw1 = np.multiply(deltaw,e2)
    w4 = w4 + deltaw1;
    
prod = np.dot(w4,phi5.T)
prod1 = np.transpose(prod)
diff = (val2-prod1)
s1 = np.square(diff)
ed1 = sum(s1);
ed = ed1/2;

wt = np.transpose(w4);
ew1 = np.dot(wt,w4)
ew = ew1/2;
#print(ew)
e = ed + np.multiply(lamda,ew);

erms = np.sqrt(np.divide(2*ed,len(testing_set)))
print "Testing_Error SGD" , erms


phi5[:,0] = 1;

#inverse = np.linalg.pinv(phi3);
output_values2 = target_values1[length2:len(x1)]
val4 = np.asanyarray(output_values2);
tp1 = np.transpose(phi5);
prod = np.dot(tw,tp1)
prod2 = np.transpose(prod)
diff3 = (val4-prod2)
s2 = np.square(diff3)
ed1 = sum(s2);
ed = ed1/2;
#print(ew)
wt = np.transpose(w);
ew1 = np.dot(wt,w)
ew = ew1/2;
#print(ew)
e = ed + np.multiply(lamda,ew);
#print e
erms = np.sqrt(np.divide(2*e,len(testing_set)))
print "Testing Error CFS: ", erms

dataset = csv.reader(open('input.csv','rU'));
nominal = csv.reader(open('output.csv','rU'));

x1 = list(dataset);
x2 = list(nominal);

print "Synthetic DATASET"
M = 10;
lamda = 0
eeta = 0.00000001;
print "REMARK : ONLY FOR SYNTHETIC DATASET"
print "FOR STOCHASTIC GRADIENT DESCENT FOR SYNTHETIC DATASET, CHANGE THE VALUE OF FROM INVERSE MATRIX (inv1, inv2, inv3) TO IDENTITY MATRIX (Iden1)"
print  "Just comment out in the SCG loop. Discard the closed form solution (CF) of synthetic dataset while calculating it's SGD. "
print "FOR CLOSED FORM SOLUTION FOR SYNTHETIC DATASET RUN THE LOOP just take inv1, inv2 and inv3 and discard its SGD value while considering CF"
print "lamda : ", lamda
print "M : ", M

target_values = x2
length1 = int(0.8*len(x1))
length2 = int(0.9*len(x1))
training_set = x1[0:length1]

testing_set = x1[length2:len(x1)]
training_set = np.array(training_set, dtype = 'float_')


#covariance matrix inverse
x3 = [];
for i in range(0,len(training_set[0])):
    ele1= np.var(training_set[:,i]);
    if (ele1 == 0.0):
        x3.append(0.0001);
    else: x3.append(ele1);
#print(x3) 
daignal_cov_mat = np.diag(x3);
inv1 = np.linalg.inv(daignal_cov_mat);

Iden1 = np.eye(len(training_set[1,:]),len(training_set[1,:]))
Iden1 = Iden1 + Iden1*0;

batch_len = int(len(training_set)/M);
batch_len1 = int(len(training_set)/M);

#taking mean 
temp = 0;
x6 = [];
dummy = np.zeros(len(training_set[1]));
for t in range(0,M):
    batch_len = batch_len + temp;
    x6 = training_set[temp:batch_len]
    x3 = [];
    for column in range(0,len(x6[0])):
        for row in range(0,len(x6)):
            x = [];
            ele2 = x6[row][column];
            x.append(ele2);
        x5 = np.transpose(x)
        ele3 = np.mean(x5);
        x3.append(ele3);
    temp = batch_len1;
    stack_row = np.asarray(x3);
    if t == 0:        
        mean = np.vstack((dummy,stack_row))
    else: mean = np.vstack((mean,stack_row))

mean = np.delete(mean,0,axis=0);
#print(mean)

#taking phi3
dummy = np.zeros(M);
for row in range(0,len(training_set)):
    phi = [];
    for col in range(0,len(mean)):
        stack_row1 = training_set[row] - mean[col]
        stack_row1 = np.asarray(stack_row1);
        stack_row2 = np.transpose(stack_row1);
        phi1 = stack_row1.dot(inv1).dot(stack_row2);
        #phi1 = stack_row1.dot(Iden1).dot(stack_row2);
        phi1 = -phi1/2;
        phi1 = np.exp(phi1);
        phi.append(phi1)
    stack_row3 = np.asarray(phi);
    if row == 0:        
        phi3 = np.vstack((dummy,stack_row3))
    else: phi3 = np.vstack((phi3,stack_row3))

phi3 = np.delete(phi3,0,axis=0);

target_values1 = np.array(target_values, dtype = 'float_')
output_values = target_values1[0:length1]
val2 = np.asanyarray(output_values);


w3 = np.ones(M)
w3 = np.array(w3, dtype = 'float_')
w4 = np.matrix(w3);
w5 = np.ones(M)
w5 = np.array(w5, dtype = 'float_')
w5 = np.matrix(w5);
tp = np.matrix(w5);
deltaw = -w5*eeta
for i in range(0,len(training_set)):    
    prod = np.dot(w4,phi3.T)
    prod1 = np.transpose(prod);
    diff2 = (val2-prod1)
    diff2 = np.transpose(diff2);
    ed2 = -diff2.dot(phi3)
    ew2 = w4
    e2 = ed2 + lamda*ew2
    deltaw1 = np.multiply(deltaw,e2)
    w4 = w4 + deltaw1;

#print(w4)

prod = np.dot(w4,phi3.T)
prod1 = np.transpose(prod)
diff = (val2-prod1)
s1 = np.square(diff)
ed1 = sum(s1);
ed = ed1/2;

erms = np.sqrt(np.divide(2*ed,length1))
print "Training_Error SGD" , erms

phi3[:,0] = 1;
#print phi3
#print+(phi2)

Id = np.eye(M,M);
#inverse = np.linalg.pinv(phi3);
phi4 = (phi3.T).dot(phi3) + lamda*(Id.T);
inverse = (np.linalg.inv(phi4)).dot(phi3.T);
w = inverse.dot(val2)
#print(w)


tw = np.transpose(w);
tp = np.transpose(phi3);
prod = np.dot(tw,tp)
prod1 = np.transpose(prod)
diff = (val2-prod1)
#print(diff)
s1 = np.square(diff)
ed1 = sum(s1);
ed = ed1/2;
#print(ew)
wt = np.transpose(w);
ew1 = np.dot(wt,w)
ew = ew1/2;
#print(ew)
e = ed + np.multiply(lamda,ew);
#print e
erms = np.sqrt(np.divide(2*e,length1))
print "Training Error CF: ", erms

#------------------------------validation testing---------------------------------------
# We once again find out phi3 value, mean 

validation_set = x1[length1:length2]
validation_set = np.array(validation_set, dtype = 'float_')
#covariance matrix inverse
x4 = [];
for i in range(0,len(validation_set[0])):
    ele1= np.var(validation_set[:,i]);
    if (ele1 == 0.0):
        x4.append(0.0001);
    else: x4.append(ele1);
#print(x4) 
daignal_cov_mat1 = np.diag(x4);
inv2 = np.linalg.inv(daignal_cov_mat1);

batch_len2 = int(len(validation_set)/M);
batch_len3 = int(len(validation_set)/M);

temp1 = 0;
x7 = [];
dummy1 = np.zeros(len(validation_set[1]));
for t1 in range(0,M):
    batch_len2 = batch_len2 + temp1;
    x7 = validation_set[temp1:batch_len2]
    x3 = [];
    for column in range(0,len(x7[0])):
        for row in range(0,len(x7)):
            x = [];
            ele2 = x7[row][column];
            x.append(ele2);
        x5 = np.transpose(x)
        ele3 = np.mean(x5);
        x3.append(ele3);
    temp1 = batch_len3;
    stack_row4 = np.asarray(x3);
    if t1 == 0:        
        mean1 = np.vstack((dummy1,stack_row4))
    else: mean1 = np.vstack((mean1,stack_row4))

mean1 = np.delete(mean1,0,axis=0);
#print(mean1)

#taking phi4
dummy = np.zeros(M);
for row in range(0,len(validation_set)):
    phi = [];
    for col in range(0,len(mean1)):
        stack_row1 = validation_set[row] - mean1[col]
        stack_row1 = np.asarray(stack_row1);
        stack_row2 = np.transpose(stack_row1);        
        phi1 = stack_row1.dot(inv2).dot(stack_row2);
        #phi1 = stack_row1.dot(Iden1).dot(stack_row2);        
        phi1 = -phi1/2;
        phi1 = np.exp(phi1);
        phi.append(phi1)
    stack_row3 = np.asarray(phi);
    if row == 0:        
        phi4 = np.vstack((dummy,stack_row3))
    else: phi4 = np.vstack((phi4,stack_row3))
    
phi4 = np.delete(phi4,0,axis=0);

output_values1 = target_values1[length1:length2]
val2 = np.asanyarray(output_values1);

w3 = np.ones(M)
w3 = np.array(w3, dtype = 'float_')
w4 = np.matrix(w3);
w5 = np.ones(M)
w5 = np.array(w5, dtype = 'float_')
w5 = np.matrix(w5);
deltaw = -w5*0.000001
for i in range(0,len(validation_set)):    
    prod = np.dot(w4,phi4.T)
    prod1 = np.transpose(prod);
    diff2 = (val2-prod1)
    diff2 = np.transpose(diff2);
    ed2 = -diff2.dot(phi4)
    ew2 = w4
    e2 = ed2 + lamda*ew2
    deltaw1 = np.multiply(deltaw,e2)
    w4 = w4 + deltaw1;
    
prod = np.dot(w4,phi4.T)
prod1 = np.transpose(prod)
diff = (val2-prod1)
s1 = np.square(diff)
ed1 = sum(s1);
ed = ed1/2;

erms = np.sqrt(np.divide(2*ed,len(validation_set)))
print "Validation_Error SGD " , erms

phi4[:,0] = 1;
#print phi4

#inverse = np.linalg.pinv(phi3);
output_values1 = target_values1[length1:length2]
val3 = np.asanyarray(output_values1);
tp1 = np.transpose(phi4);
prod = np.dot(tw,tp1)
prod2 = np.transpose(prod)
diff2 = (val3-prod2)
s2 = np.square(diff2)
ed1 = sum(s2);
ed = ed1/2;
#print(ew)
wt = np.transpose(w);
ew1 = np.dot(wt,w)
ew = ew1/2;
#print(ew)
e = ed + np.multiply(lamda,ew);
#print e
erms = np.sqrt(np.divide(2*e,len(validation_set)))
print "Validation Error CF: ", erms

#------------------------------testing set---------------------------------------
# We once again find out phi3 value, mean and covaraince

testing_set = x1[length2:len(x1)]
testing_set = np.array(testing_set, dtype = 'float_')

x5 = [];
for i in range(0,len(testing_set[0])):
    ele1= np.var(testing_set[:,i]);
    if (ele1 == 0.0):
        x5.append(0.0001);
    else: x5.append(ele1);

daignal_cov_mat2 = np.diag(x5);
inv3 = np.linalg.inv(daignal_cov_mat2);

batch_len4 = int(len(testing_set)/M);
batch_len5 = int(len(testing_set)/M);

temp1 = 0;
x7 = [];
dummy2 = np.zeros(len(testing_set[1]));
for t1 in range(0,M):
    batch_len4 = batch_len4 + temp1;
    x7 = testing_set[temp1:batch_len4]
    x3 = [];
    for column in range(0,len(x7[0])):
        for row in range(0,len(x7)):
            x = [];
            ele2 = x7[row][column];
            x.append(ele2);
        x5 = np.transpose(x)
        ele3 = np.mean(x5);
        x3.append(ele3);
    temp1 = batch_len5;
    stack_row5 = np.asarray(x3);
    if t1 == 0:        
        mean2 = np.vstack((dummy2,stack_row5))
    else: mean2 = np.vstack((mean2,stack_row5))

mean2 = np.delete(mean2,0,axis=0);
#print(mean1)

#taking phi4
dummy = np.zeros(M);
for row in range(0,len(testing_set)):
    phi = [];
    for col in range(0,len(mean1)):
        stack_row1 = testing_set[row] - mean2[col]
        stack_row1 = np.asarray(stack_row1);
        stack_row2 = np.transpose(stack_row1);
        phi1 = stack_row1.dot(inv3).dot(stack_row2);
        #phi1 = stack_row1.dot(Iden1).dot(stack_row2);        
        phi1 = -phi1/2;
        phi1 = np.exp(phi1);
        phi.append(phi1)
    stack_row3 = np.asarray(phi);
    if row == 0:        
        phi5 = np.vstack((dummy,stack_row3))
    else: phi5 = np.vstack((phi5,stack_row3))
    
phi5 = np.delete(phi5,0,axis=0);

output_values2 = target_values1[length2:len(x2)]
val2 = np.asanyarray(output_values2);

w3 = np.ones(M)
w3 = np.array(w3, dtype = 'float_')
w4 = np.matrix(w3);
w5 = np.ones(M)
w5 = np.array(w5, dtype = 'float_')
w5 = np.matrix(w5);
deltaw = -w5*0.000001
for i in range(0,len(testing_set)):    
    prod = np.dot(w4,phi5.T)
    prod1 = np.transpose(prod);
    diff2 = (val2-prod1)
    diff2 = np.transpose(diff2);
    ed2 = -diff2.dot(phi5)
    ew2 = w4
    e2 = ed2 + lamda*ew2
    deltaw1 = np.multiply(deltaw,e2)
    w4 = w4 + deltaw1;
    
prod = np.dot(w4,phi5.T)
prod1 = np.transpose(prod)
diff = (val2-prod1)
s1 = np.square(diff)
ed1 = sum(s1);
ed = ed1/2;

wt = np.transpose(w4);
ew1 = np.dot(wt,w4)
ew = ew1/2;
#print(ew)
e = ed + np.multiply(lamda,ew);

erms = np.sqrt(np.divide(2*ed,len(testing_set)))
print "Testing_Error SGD" , erms


phi5[:,0] = 1;

#inverse = np.linalg.pinv(phi3);
output_values2 = target_values1[length2:len(x1)]
val4 = np.asanyarray(output_values2);
tp1 = np.transpose(phi5);
prod = np.dot(tw,tp1)
prod2 = np.transpose(prod)
diff3 = (val4-prod2)
s2 = np.square(diff3)
ed1 = sum(s2);
ed = ed1/2;
#print(ew)
wt = np.transpose(w);
ew1 = np.dot(wt,w)
ew = ew1/2;
#print(ew)
e = ed + np.multiply(lamda,ew);
#print e
erms = np.sqrt(np.divide(2*e,len(testing_set)))
print "Testing Error CFS: ", erms
