#!/usr/bin/env python
# coding: utf-8

# # Homework1 Question 6

# In[ ]:


import os
import pandas as pd
import numpy as np
import nltk
from nltk.stem import PorterStemmer
import re
import time
from nltk.corpus import stopwords
import scipy.stats
from numpy import linalg as LA
import sklearn
from sklearn import model_selection
import matplotlib.pyplot as plt


# In[ ]:


path = '/Users/tt/Desktop/哥大/S2/Machine Learning/hw1/enron1'
word_dict = set()
label = {}
porter = PorterStemmer()

# Generate the label dictionary and word_dict list
# Note that for conveniency, I put all emails into one folder, named "data"
for filename in os.listdir(path+'/data')[:]:
    if filename[0].isdigit():
        with open(os.path.join(path+'/data',filename),'r') as f:
            data = f.read()
            label.update({int(filename[:4]):filename.split('.')[-2]})
            word_dict = word_dict.union(set([porter.stem(x) for x in re.split('; |, |/ | |\r|/. |:|\n |\!|\?|-', data)
                                             if ((x.isalpha())&(len(x)>1))]))
            f.close()
label_series = pd.Series(label)


# In[ ]:


# Split train and test set
X_train,X_test,y_train,y_test = sklearn.model_selection.train_test_split(label.keys(),label.values(),test_size = .3)


# In[ ]:


word_count = pd.DataFrame()

# Generate word_count for every single email. Takes 40mins on my mac.
for filename in os.listdir(path+'/data')[:]:
    if filename[0].isdigit():
        with open(os.path.join(path+'/data',filename),'r') as f:
            word_data = [porter.stem(x) for x in re.split('; |, |/ | |\r|/. |:|\n |\!|\?|-', f.read()) if ((x.isalpha())&(len(x)>1))]
            temp = {x:0 for x in word_dict}
            for i in set(word_data):
                if i in temp.keys():
                    temp[i] = word_data.count(i)
            word_count[int(filename[:4])]=(pd.Series(temp))
            if int(filename[:4])%100 == 0:
                print (filename[:4])
            f.close()


# In[ ]:


stop_words = set(stopwords.words('english')) 
drop_word_count = word_count.loc[[x for x in word_count.index if x not in stop_words]]

temp = drop_word_count.loc[:,X_train].sum(axis=1)
drop_word_count = drop_word_count.loc[temp>0]
drop_word_count = drop_word_count[(drop_word_count.sum(axis = 1)>100)&(drop_word_count.replace(0,np.nan).count(axis = 1)>=0)]
len(drop_word_count)


# In[ ]:


drop_word_count.sample(10)


# In[ ]:


# Naive Bayes

train_data = drop_word_count.loc[:,X_train]

ham = drop_word_count.loc[:, np.array(X_train)[np.array(y_train)=='ham']]
spam = drop_word_count.loc[:, np.array(X_train)[np.array(y_train) == 'spam']]

# P[Y='ham']
p_y1 = float(y_train.count('ham'))/len(y_train)

# P[Y='spam']
p_y2 = 1 - p_y1

correct = 0
wrong = 0

for j in X_test[:]:
    test_data = drop_word_count.loc[:,j]
    
    # P[Xi=xi|Y='ham']
    temp = (ham.T == test_data).sum(axis = 0)
    length = pd.Series([len(ham.columns)]*len(temp),index = temp.index)
    # pseudo count: if meet 0, add 1 to the certain element of test data and whole set.
    length[temp==0] += 1.
    temp[temp==0] += 1.
    p_x1 = np.log(temp.div(length)).cumsum()[-1]

    # P[Xi=xi|Y='spam']
    temp = (spam.T == test_data).sum(axis = 0)
    length = pd.Series([len(spam.columns)]*len(temp),index = temp.index)
    # pseudo count: if meet 0, add 1 to the certain element of test data and whole set.
    length[temp==0] += 1.
    temp[temp==0] += 1.
    p_x2 = np.log(temp.div(length)).cumsum()[-1]
    
    # Final probabilities for calculation
    p1 = p_x1+np.log(p_y1)
    p2 = p_x2+np.log(p_y2)

    if p1>= p2:
        predict_label = 'ham'
    else:
        predict_label = 'spam'

    if predict_label == label[j]:
        correct += 1
    else:
        wrong += 1

print (correct/float(correct+wrong))


# In[ ]:


def cosine_similarity(x,y):
    return np.dot(x,y)/np.sqrt(np.dot(x,x)*np.dot(y,y))


# In[ ]:


# K-NN methods
k = 3
norm_degree = 2
type = 'norm'  # or 'cosine'

train_data = drop_word_count.loc[:,X_train]
correct = 0
wrong = 0
for j in X_test[:]:
    test_data = drop_word_count.loc[:,j].values
    
    if type == 'norm':
        l = [LA.norm(x-test_data,norm_degree) for x in train_data.values.T]
        index = np.argsort(l)[:k]
    elif type == 'cosine':
        l = [cosine_similarity(x, test_data) for x in train_data.values.T]
        index = np.argsort(l)[-k:]
    
    predict_label = [label[x] for x in train_data.columns[index]]

    # Find the mode of the neighbors
    if scipy.stats.mode(predict_label)[0][0] == label[j]:
        correct += 1
    else:
        wrong += 1

print (str(correct/float(correct+wrong))+'for '+str(k)+'-NN')


# In[ ]:


# Decision Tree

class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def classification_error(x):
    length = len(x)
    verify_data = label_series.loc[x.index]
    ham_length = len(verify_data[verify_data=='ham'])
    p_ham = float(ham_length)/length
    p_spam = 1-p_ham

    return 1-np.maximum(p_ham,p_spam)


def entropy(x):
    length = len(x)
    verify_data = label_series.loc[x.index]
    ham_length = len(verify_data[verify_data=='ham'])
    p_ham = float(ham_length)/length
    p_spam = 1-p_ham

    if p_ham*p_spam == 0:
        return 0.
    return p_ham*np.log(1./p_ham)+p_spam*np.log(1./p_spam)


def gini(x):
    length = len(x)
    verify_data = label_series.loc[x.index]
    ham_length = len(verify_data[verify_data=='ham'])
    p_ham = float(ham_length)/length
    p_spam = 1-p_ham

    return 1-p_ham**2-p_spam**2


def find_branch(temp, min_sample_leaf, func):
    max = -np.inf
    feature = -1
    threshold = 0
    func_all = func(temp)
    
    for j in temp.columns:
        for t in range(temp[j].min(),temp[j].max()+1,3):
            left = temp[temp[j]<=t]
            right = temp[temp[j]>t]
            if len(left)*len(right)==0:
                continue
            if np.minimum(len(left),len(right))<min_sample_leaf:
                continue
            pl = len(left)/float(len(temp))
            pr = 1 - pl
            if (func_all-pl*func(left)-pr*func(right))>max:
                threshold = t
                feature = j
                max = (func(temp)-pl*func(left)-pr*func(right))

    if feature == -1:
        verify_data = label_series.loc[temp.index]
        return pd.DataFrame(), pd.DataFrame(), None, scipy.stats.mode(verify_data.values)[0][0]
    return temp[temp[feature]<=threshold],temp[temp[feature]>threshold],feature,threshold


# Using binomial tree to construct decision tree and its rules.
def construct_decision_tree(x, min_sample_leaf, func):
    root = TreeNode(x)
    dt_left, dt_right, feature, threshold = find_branch(x,min_sample_leaf, func)

    rules =  TreeNode((feature,threshold))

    if (len(dt_left)==0)&(len(dt_right)==0):
        return root, rules
    if len(dt_left):
        root.left, rules.left = construct_decision_tree(dt_left, min_sample_leaf, func)
    if len(dt_right):
        root.right, rules.right = construct_decision_tree(dt_right, min_sample_leaf, func)
    return root, rules


def test_decision_tree(test_data,rules):

    if not rules.val[0]:
        return rules.val[1]
    else:
        if test_data.loc[rules.val[0]]<= rules.val[1]:
            return test_decision_tree(test_data,rules.left)
        else:
            return test_decision_tree(test_data,rules.right)


# In[ ]:


# Decision tree running:

train_data = drop_word_count.loc[:,X_train]
temp = train_data.T
func = gini
min_sample_leaf = 10


[tree,rules] = construct_decision_tree(temp, min_sample_leaf, func)

correct = 0
wrong = 0

# Predict label for test data
for n in X_test:
    if test_decision_tree(drop_word_count.loc[:,n],rules)==label[n]:
        correct += 1
    else:
        wrong += 1
        
print (float(correct)/(correct+wrong))


# In[ ]:


# Print a series of rules
temp_rules= rules
while temp_rules!=None:
    print (temp_rules.val)
    temp_rules = temp_rules.left

