# -*-coding:utf-8-*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math


# Function of calculating the amount of stocks covered
def coverage_plot(coverage, n= 465):
    month_average_coverage = pd.rolling_mean(pd.Series(coverage), 52) # 12月移动均线
    time = range(0, n)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xticks([1, 52, 103, 154, 205, 255, 306, 359, 411, 461])
    ax.set_xticklabels(['2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017'])
    ax.plot(time, coverage, color='blue',label='Coverage of Portfolios')
    ax.plot(time, month_average_coverage,color='red',label='12-month moving average')
    ax.set_ylim(0, 2500)
    ax.set_title('Coverage of Portfolios')
    ax.set_ylabel('# of Stocks')
    ax.legend(loc='best')

# Function of calculating annual return
def annual_return(time,return_i):
    annual= 1
    for i in range(0,time):
        annual=annual*(1+return_i[i])
    annual=(annual ** (52.0/time)-1)*100
    return annual

# Function of barplot of annual return
def annual_return_plot(return_1,return_2,return_3,return_4,return_5,n= 465):
    return_i=[]
    for i in range(0,n):
        return_i.append(return_1[i]-return_5[i])
    annual=[annual_return(n,return_5),annual_return(n,return_4),
                   annual_return(n,return_3),annual_return(n,return_2),
                   annual_return(n,return_1),annual_return(n,return_i)]
    num_list=['quantile 1','quantile 2' ,'quantile 3' ,'quantile 4' ,'quantile 5','L/S' ]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.bar(num_list,annual)
    ax.set_title('Annualized Return(%)')
    ax.set_ylabel('Annualized Return(%)')
    ax.set_ylim(-20,40)
    ax.legend(loc='best')

# Function of calculating annual volatility
def annual_volatility(return_i):
    return np.std(return_i)/np.sqrt(9.0)*100

# Function of barplot of annual volatility
def annual_volatility_plot(return_1,return_2,return_3,return_4,return_5,n= 465):
    return_i = []
    for i in range(0, n):
        return_i.append(return_5[i] - return_1[i])
    annual=[annual_volatility(return_1),annual_volatility(return_2),
                      annual_volatility(return_3),annual_volatility(return_4),
                      annual_volatility(return_5),annual_volatility(return_i)]
    num_list = ['quantile 1','quantile 2' ,'quantile 3' ,'quantile 4' ,'quantile 5', 'L/S' ]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.bar(num_list, annual)
    ax.set_title('Annualized Volatility(%)')
    ax.set_ylabel('Annualized Volatility(%)')
    ax.legend(loc='best')

# Function of calculating turnover and plot
def factor_turnover_plot(factor_turnover, n=465):
    month_average = pd.rolling_mean(pd.Series(factor_turnover), 52) # 12月移动均线
    fig = plt.figure()
    ax = fig.add_subplot(111)
    time=range(0,n)
    ax.set_xticks([1, 52, 103, 154, 205, 255, 306, 359, 411, 461])
    ax.set_xticklabels(['2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017'])
    ax.plot(time,factor_turnover,color='b',label='Factor Turnover')
    ax.plot(time, month_average,color='r',label='12-month moving average')
    ax.set_title('Factor Turnover(%)')
    ax.set_ylabel('Turnover(%)')
    ax.set_ylim(0,90)
    ax.legend(loc='best')

# Calculating portfolio IR
def portfolio_ir(return_i):
    return  np.mean(return_i)/np.std(return_i)

# Drawing barplot of portfolio IR
def portfolio_ir_plot(return_1,return_2,return_3,return_4,return_5,n=465) :
    return_i = []
    for i in range(0, n):
        return_i.append(return_5[i] - return_1[i])
    ir=[portfolio_ir(return_1),portfolio_ir(return_2),
        portfolio_ir(return_3),portfolio_ir(return_4),portfolio_ir(return_5),portfolio_ir(return_i)]
    num_list = ['quantile 1', 'quantile 2', 'quantile 3', 'quantile 4', 'quantile 5', 'L/S']
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.bar(num_list, ir)
    ax.set_title('Portfolio IR')
    ax.set_ylabel('IR')
    ax.legend(loc='best')

# Function of printing table of return data
def return_table(return_1,return_2,return_3,return_4,return_5,factor,n=465):
    return_i = []
    for i in range(0, n):
        return_i.append(return_5[i] - return_1[i])
    df = pd.DataFrame([return_1, return_2, return_3, return_4, return_5, return_i],
                        index=['quantile 1', 'quantile 2', 'quantile 3', 'quantile 4', 'quantile 5', 'L/S'],
                        columns=factor.columns)
    df = df.T + 1
    df.to_csv('C:\Users\ASUS-PC\Desktop\Backtesttoy_by_Hengbo Liang\Result\Portfolio Returns.csv', sep=',',
                header=True, index=True)


# Function of calculating accumulated return in a certain time period
def c_return(time,return_1):
    c=1
    for i in range(0,time):
        c=c*(1+return_1[i])
    return c

# Functiono of drawing curve of accumulated return
def q_return_plot(return_1,return_2,return_3,return_4,return_5,n= 465):
    q_return1 = []
    q_return2 = []
    q_return3 = []
    q_return4 = []
    q_return5 = []
    for time in range(0,n):
        q_return1.append(c_return(time, return_1))
        q_return2.append(c_return(time, return_2))
        q_return3.append(c_return(time, return_3))
        q_return4.append(c_return(time, return_4))
        q_return5.append(c_return(time, return_5))
    time=range(0,n)
    fig = plt.figure()
    ax=fig.add_subplot(111)
    ax.plot(time, q_return1,label='quantile 1')
    ax.plot(time, q_return2,label='quantile 2')
    ax.plot(time, q_return3,label='quantile 3')
    ax.plot(time, q_return4,label='quantile 4')
    ax.plot(time, q_return5,label='quantile 5')
    ax.set_title('Quantile Returns')
    ax.set_xticks([1,52,103,154,205,255,306,359,411,461])
    ax.set_xticklabels(['2008','2009','2010','2011','2012','2013','2014','2015','2016','2017'])
    ax.set_ylabel('Cumulative Return')
    ax.legend(loc='best')

# Calculating serial correlation
def serial_corr_plot(factor, n=465):
    corr = []
    factor_data=factor.dropna()
    for i in range(0,n-1):
        corr.append(factor_data.iloc[:,i].corr(factor_data.iloc[:,i+1]))
    month_average = pd.rolling_mean(pd.Series(corr), 52)  # 12月移动均线
    time = range(0, n-1)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xticks([1, 52, 103, 154, 205, 255, 306, 359, 411, 457])
    ax.set_xticklabels(['2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017'])
    ax.plot(time, corr,color='g',label='Serial Corr')
    ax.plot(time, month_average ,color='red',label='12-month moving average')
    ax.set_ylim(0, 1)
    ax.set_title('Serial Correlation')
    ax.set_ylabel('Serial Corr')
    ax.legend(loc='best')

# Calculating sortinal ratio
def sortinal_ratio(time,return_i):
    dr=0
    for i in range(1,time):
        dr+= (min(0,return_i[i]))**2
    dr=np.sqrt(dr/time)
    sr=(np.mean(return_i))/dr
    return sr

# Drawing barplot of sortinal ratio
def sortinal_ratio_plot(return_1,return_2,return_3,return_4,return_5,n= 465):
    return_i = []
    for i in range(0, n):
        return_i.append(return_5[i] - return_1[i])
    sr=[sortinal_ratio(n,return_1),sortinal_ratio(n,return_2),sortinal_ratio(n,return_3),
        sortinal_ratio(n,return_4),sortinal_ratio(n,return_5),sortinal_ratio(n,return_i)]
    num_list = ['quantile 1', 'quantile 2', 'quantile 3', 'quantile 4', 'quantile 5', 'L/S']
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.bar(num_list, sr)
    ax.set_title('Sortinal Ratio')
    ax.set_ylabel('Sortinal Ratio')
    ax.legend(loc='best')

# Drawing curve of IC
def ic_plot(ic,n= 465):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    month_average = pd.rolling_mean(pd.Series(ic), 52)  # 12月移动均线
    time=range(0,n)
    ax.set_xticks([1, 52, 103, 154, 205, 255, 306, 359, 411, 461])
    ax.set_xticklabels(['2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017'])
    ax.plot(time,ic,color='b',label='Spearman IC')
    ax.plot(time, month_average ,color='r',label='12-month moving average')
    ax.set_title('Spearman IC(%)')
    ax.set_ylabel('Spearman(%)')
    ax.set_ylim(-30,50)
    ax.legend(loc='best')

# Drawing time series spread
def time_series_plot(return_1,return_5,n= 465):
    time_series = []
    for time in range(0, n):
        time_series.append((return_1[time]-return_5[time])*100)
    month_average = pd.rolling_mean(pd.Series(time_series), 52)
    time=range(0,n)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xticks([1, 52, 103, 154, 205, 255, 306, 359, 411, 461])
    ax.set_xticklabels(['2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017'])
    ax.plot(time, time_series,color='b',label='Time Series Spread')
    ax.plot(time, month_average , color='red',label='12-month moving average')
    ax.set_title('Time Series Spread(%)')
    ax.set_ylabel('Spread(%)')
    ax.set_ylim(-5,15)
    ax.legend(loc='best')

# Calculating the return of Long/short in a certain time period
def wealth(time,return_1,return_5):
    r=1
    for i in range(0,time):
        r=r*(1+return_1[i]-return_5[i])
    return r

# Function of drawing wealth curve
def wealth_curve_plot(return_1,return_5,n= 465):
    wealth_curve=[]
    for time in range(0,n):
        wealth_curve.append(wealth(time,return_1,return_5))
    time=range(0,n)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    #ax.set_xticks([1, 52, 103, 154, 205, 255, 306, 359, 411, 461])
    #ax.set_xticklabels(['2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017'])
    ax.plot(time,wealth_curve,label='L/S Return')
    ax.set_title('Wealth Curve')
    ax.set_ylabel('L/S Return')
    ax.set_ylim(0,16)
    ax.legend(loc='best')

#-*-coding:utf-8-*-