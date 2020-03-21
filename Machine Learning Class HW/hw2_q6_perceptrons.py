#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Group member: 
    
    Li, Xiyu: xl2940 
    Lu, Yunzhi: yl4352 
    Liang, Hengbo: hl3308 
    
"""

from scipy.io import loadmat
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import pandas as pd

path = '/Users/tt/Desktop/哥大/S2/Machine Learning/hw2/mnist_digits.mat'



data = loadmat(path)
y = np.asarray(data['Y'],dtype = 'float')
X = np.asarray(data['X'],dtype = 'float')

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)



#%%  V0


    
n = len(y_train)
T = int(3*n)

func = lambda x: 1. if x else -1.
        
result = np.full((len(y_test),10),np.nan)

for num in range(0,10):
    
    w = np.full((T+1,784),0.)
    
    for t in range(1, T+1):
        i = t % (n+1)
        xi = X_train[i-1,:]
        yi = func(y_train[i-1] == num)
        
        if yi*(np.dot(w[t-1,:],xi)) <= 0.:
            w[t,:] = w[t-1,:] + yi*xi
        else:
            w[t,:] = w[t-1,:]
   
    for j in range(len(X_test)):
        predict = np.dot(w[-1], X_test[j])
        result[j, num] = predict
        
accuracy = (result.argmax(axis = 1)==y_test.T)[0]
print ('Accuracy for V0:')
print (len(accuracy[accuracy==True])/float(len(accuracy)))






 #%%  V1
n = len(y_train)
T = int(3*n)
func = lambda x: 1. if x else -1.

result = np.full((len(y_test),10),np.nan)

for num in range(0,10):
    
    w = np.full((T+1,784),0.)
    y_temp = np.array([1. if x==num else -1. for x in y_train])
    
    for t in range(1, T+1):
        
        i = np.argmin(y_temp*((np.dot(w[t-1],X_train.T))))
        
        xi = X_train[i,:]
        yi = func(y_train[i] == num)
        
        if yi*(np.sum(np.dot(w[t-1,:],xi))) <= 0.:
            w[t,:] = w[t-1,:] + yi*xi
        else:
            w[t,:] = w[t-1,:]
            break
        
    print ('Digit '+ str(num)+' finished')
    
    for j in range(len(X_test)):
        predict = np.sum(np.dot(w[t], X_test[j]))
        result[j, num] = predict
        
accuracy = (result.argmax(axis = 1)==y_test.T)[0]
print ('Accuracy for V1:')
print (len(accuracy[accuracy==True])/float(len(accuracy)))


#%%   V2

n = len(y_train)
T = int(3*n)

result = np.full((len(y_test),10),np.nan)

for num in range(0,10):
    
    # Should be c1 = 0
    c = [0,0]
    k = 1
    w = np.full((T+1,784),0.)
    
    for t in range(1, T+1):
        i = t % (n+1)
        
        func = lambda x: 1. if x else -1.
        
        xi = X_train[i-1,:]
        yi = func(y_train[i-1] == num)
        
        if yi*(np.dot(w[k],xi)) <= 0.:
            w[k+1] = w[k] + yi*xi
            c.append(1)
            k = k + 1
        else:
            c[k] = c[k] + 1
   
    for j in range(len(X_test)):
        predict = 0
        for s in range(1,k+1):
            predict += c[s] * np.sign(np.dot(w[s], X_test[j]))
        result[j, num] = predict
    print ('Digit '+ str(num)+' finished')
accuracy = (result.argmax(axis = 1)==y_test.T)[0]
print ('Accuracy for V2:')
print len(accuracy[accuracy==True])/float(len(accuracy))


#%% Kernel
   
n = len(y_train)
T = 3
func = lambda x: 1. if x else -1.
result = np.full((len(y_test),10),np.nan)

for num in range(0,10):
    
    y_temp = np.array([1. if x==num else -1. for x in y_train])
    alpha = np.full(n,0.)
    
    for t in range(1, T+1):
        
        for i in range(0,n):
            xi = X_train[i]
            temp = (1+np.dot(X_train,xi))**d
            s = np.dot(alpha * y_temp, temp)
            if np.sign(s)!=y_temp[i]:
                alpha[i] += 1

    ptemp = np.array([(1+np.dot(X_train,xj))**d for xj in X_test]).reshape(-1,n)
    predict = np.dot(alpha * y_temp, ptemp.T)
    result[:, num] = predict
        
    print ('Digit '+ str(num)+' finished')
accuracy = (result.argmax(axis = 1)==y_test.T)[0]
print ('Accuracy for kernel percetron:')
print (len(accuracy[accuracy==True])/float(len(accuracy)))

