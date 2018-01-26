import numpy as np
import xlrd
import scipy
#import matplotlib.pyplot as plt
from scipy.stats import norm
book = xlrd.open_workbook('university data.xlsx','r')
print "UBitName = arunshar"
print "personNumber = 50206920"

first_sheet = book.sheet_by_index(0)
col1 = first_sheet.col_values(2,1)
col1.remove(u'')
col2 = first_sheet.col_values(3,1)
col2.remove(u'')
col3 = first_sheet.col_values(4,1)
col3.remove(u'')
col4 = first_sheet.col_values(5,1)
col4.remove(u'')

mu1 = round(np.mean(col1),3)
print "mu1 = " , mu1
mu2 = round(np.mean(col2),3)
print "mu2 = " , mu2
mu3 = round(np.mean(col3),3)
print "mu3 = " , mu3
mu4 = round(np.mean(col4),3)
print "mu4 = " , mu4
var1 = round(np.var(col1),3)
print "var1 = " , var1
var2 = round(np.var(col2),3)
print "var2 = " , var2
var3 = round(np.var(col3),3)
print "var3 = " , var3
var4 = round(np.var(col4),3)
print "var4 = " , var4
sigma1 = round(np.std(col1),3)
print "sigma1 = " , sigma1
sigma2 = round(np.std(col2),3)
print "sigma2 = " , sigma2
sigma3 = round(np.std(col3),3)
print "sigma3 = " , sigma3
sigma4 = round(np.std(col4),3)
print "sigma4 = " , sigma4

myarray = np.asarray(col1)
myarray2 = np.asarray(col2)
myarray3 = np.asarray(col3)
myarray4 = np.asarray(col4)
tr1 = myarray.transpose()
tr2 = myarray2.transpose()
tr3 = myarray3.transpose()
tr4 = myarray4.transpose()


x1 = np.vstack((tr1,tr2,tr3,tr4))
X = np.cov(x1)
X2 = np.corrcoef(x1)

    
X3 = np.empty([4,4])
i = 0
while i < len(X2):
    j = 0
    while j < len(X2):
        X3[i,j] = round(X2[i,j],3)
        j = j + 1
    i = i + 1

X4 = np.empty([4,4])
i = 0
while i < len(X3):
    j = 0
    while j < len(X3):
        X4[i,j] = round(X[i,j],3)
        j = j + 1
    i = i + 1

print "covaraianceMat = \n" , X4
print "correlationMat = \n" , X3
pd1 = scipy.stats.norm.pdf(tr1,mu1,sigma1)
logpd1 = np.log(pd1)
l1 = sum(logpd1)
pd2 = scipy.stats.norm.pdf(tr2,mu2,sigma2)
logpd2 = np.log(pd2)
l2 = sum(logpd2)
pd3 = scipy.stats.norm.pdf(tr3,mu3,sigma3)
logpd3 = np.log(pd3)
l3 = sum(logpd3)
pd4 = scipy.stats.norm.pdf(tr4,mu4,sigma4)
logpd4 = np.log(pd4)
l4 = sum(logpd4)

f = l1 + l2 + l3 + l4

print "logLikelihood = \n" , round(f,3)

unitvector = []
i = 0
while i < 49:
    unitvector.append(1)
    i = i + 1

cs_score = col1
research_overhead = col2
admin_base_pay = col3
tuition = col4

parents = [research_overhead,admin_base_pay,tuition]
child = np.asarray(cs_score)
myarray5 = np.asarray(unitvector)
parents = np.vstack((myarray5,parents))
y = child

A = np.empty([len(parents),len(parents)])
for row in range(0,len(parents)):    
    for col in range(0,len(parents)):
        count1 = []
        for element in range(0,len(col1)):
            count1.append(np.multiply(parents[col][element],parents[row][element]))
        A[col][row] = sum(count1)       

yn = []
for r in range(0,len(parents)):
    count2 = 0
    for element in range(0,len(col1)):            
        count2 = count2 + np.multiply(y[element],parents[r][element])
    yn.append(count2)
yn = np.transpose(yn)
beta1 = np.linalg.solve(A,yn)

vari = 0
for element in range(0,len(col1)):
    sum1 = 0
    for r in range(0,len(parents)):          
        sum1 = sum1 + np.multiply(beta1[r],parents[r][element])
    vari = vari + np.square(sum1 - y[element])
variance = vari/len(y)
print variance

constant = (-0.5)*(np.log(2*np.pi*variance))

l = 0
for element in range(0,len(col1)):
    sum1 = 0
    for r in range(0,len(parents)):
        sum1 = sum1 + np.multiply(beta1[r],parents[r][element])
    l = l + (constant - (0.5)*(1/variance)*((sum1 - y[element])**2))  

matrix = np.matrix('0 0 0 0;1 0 0 0;1 0 0 0;1 0 0 0')
print 'BNgraph = ', matrix
print "BNlogLikelihood = ", round(l,3)

#plt.scatter(col1,col2)
#plt.scatter(col1,col3)
#plt.scatter(col1,col4)
#plt.scatter(col2,col3)
#plt.scatter(col2,col4)
#plt.scatter(col3,col4)
#plt.xlabel('CS Score')
#plt.xlabel('Research Overhead')
#plt.xlabel('Admin Base Pay')
#plt.ylabel('Research_Overhead')
#plt.ylabel('Admin Base Pay')
#plt.ylabel('Tuition')
#plt.show()
#fig = plt.figure()
#fig.savefig('2nd_fig.jpg')