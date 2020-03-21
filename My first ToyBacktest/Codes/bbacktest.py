#-*-coding:utf-8-*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import backtest as bt

def wealth(time,return_1,return_5):
    r=1
    for i in range(0,time):
        r=r*(1+return_1[i]-return_5[i])
    return r

# drawing wealth curve
def wealth_curve_plot(return_1,return_5,n= 465):
    wealth_curve=[]
    for time in range(0,n):
        wealth_curve.append(wealth(time,return_1,return_5))
    time=range(0,n)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    #ax.set_xticks([1, 240, 485,720,960,1200,1440])
    #ax.set_xticklabels(['2011','2012','2013','2014','2015', '2016' ,'2017'])
    ax.plot(time,wealth_curve,label='L/S Return')
    ax.set_title('Wealth Curve')
    ax.set_ylabel('L/S Return')
    #ax.set_ylim(0,16)
    ax.legend(loc='best')


print "data loading..."
return_data = pd.read_csv("C:\\Users\\ASUS-PC\\Desktop\\A\\csv\\Forward5D.csv",index_col=0).loc['20150104':, :].fillna(0)
factor = pd.read_csv("E:\\ANSWER.csv",index_col=0).loc['20150104':, :]
print "data processing..."
#print return_data.head(),factor.head()
return_data.columns=factor.columns
r1=[]
r5=[]
#print return_data
for i in range(0,len(factor.index)):
    return1 = []
    return5 = []
    f1 = factor.iloc[i][factor.iloc[i,:] == 'long']
    f2 = factor.iloc[i][factor.iloc[i, :] == 'short']
    #print f1.index
    return1.append(return_data.iloc[i,:].loc[f1.index])
    return5.append(return_data.iloc[i,:].loc[f2.index])
    #print return1
    #return1.append(return_data.iloc[i][factor.iloc[i,:]==-1])
    #return5.append(return_data.iloc[i][factor.iloc[i, :] == 1])
    #for j in range(0,len(factor.columns)):
        #if factor.iloc[i][j]==-1:
            #return1.append(return_data.iloc[i][j])
        #elif factor.iloc[i][j]==1:
            #return5.append(return_data.iloc[i][j])
    if len(return1)>0 or len(return5)>0:
        r1.append(np.mean(return1))
        r5.append(np.mean(return5))
    else :
        r1.append(0)
        r5.append(0)
    print i
print r1
print r5
print len(r1)-len(r5)
wealth_curve_plot(r1, r5,len(factor.index))
# 显示出图片
plt.show()