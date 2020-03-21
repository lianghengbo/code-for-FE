# -*- coding: utf-8 -*-
"""
Created on Fri Sep  7 14:09:11 2018

@author: Hengbo LIANG
"""

import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import random
import warnings
warnings.filterwarnings("ignore")


class StockData(object):
    # 1.1 构造函数
    def __init__(self, path):
        self.path = path
        return

    # 1.2 读取数据，用series在类中存储
    def read(self, symbols):  # symbols是list的格式，每个元素是股票代码（前6位即可）的字符串
        temp = pd.Series()
        for i in symbols:
            # 检查该股票代码是否存在并进行数据的读取与预处理
            if (i + '.SZ.csv') in os.listdir(self.path):
                temp[i] = pd.read_csv(self.path + '//' + i + '.SZ.csv', encoding='utf8')
                temp[i] = temp[i].rename(index=str,
                                         columns={"S_INFO_WINDCODE": "symbol", "TRADE_DT": "date",
                                                  "S_DQ_AMOUNT": "turnover", "S_DQ_VOLUME": "volume"})
                temp[i] = temp[i].sort_values('date', ascending=True)
            elif (i + '.SH.csv') in os.listdir(self.path):
                temp[i] = pd.read_csv(self.path + '//' + i + '.SH.csv', encoding='utf8')
                temp[i] = temp[i].rename(index=str,
                                         columns={"S_INFO_WINDCODE": "symbol", "TRADE_DT": "date",
                                                  "S_DQ_AMOUNT": "turnover", "S_DQ_VOLUME": "volume"})
                temp[i] = temp[i].sort_values('date', ascending=True)
            else:
                # 若不存在该股票代码 则报错
                print ('Error! No symbol named ' + i + ' exists!')
        # 将数据存储在类中
        self.data = temp
        return

    # 1.3 获取某股票从start_date 到end_date之间的所有日频数据
    # 注意！ 这里的start date和end date 都包含在内
    def get_data_by_symbol(self, symbol, start_date, end_date):
        temp = self.data.loc[symbol].copy()
        temp = temp[['date', 'S_DQ_OPEN', 'S_DQ_HIGH', 'S_DQ_LOW', 'S_DQ_CLOSE', 'turnover', 'volume', 'S_DQ_AVGPRICE']]
        temp.columns = ['date', 'open', 'high', 'low', 'close', 'turnover', 'volume', 'vwap']
        temp = temp[(temp['date'] >= start_date) & (temp['date'] <= end_date)].set_index('date')
        return temp

    # 1.4 获取某一天中，对应股票的所有日频数据
    def get_data_by_date(self, adate, symbols):
        res = pd.DataFrame(columns=['open', 'high', 'low', 'close', 'turnover', 'volume', 'vwap'], index=symbols)
        for i in symbols:
            res.loc[i] = StockData.get_data_by_symbol(self, i, adate, adate).values
        return res

    # 1.5 获取symbols在某个field上所有的所有交易日的数据
    # field以字符串的形式输入，如‘open'
    def get_data_by_field(self, field, symbols):
        field = 'S_DQ_' + field.upper()
        res = pd.DataFrame(columns=symbols)
        for i in symbols:
            temp = self.data.loc[i].set_index('date').sort_index()[field].copy()
            res[i] = temp
        return res

    # --------------------------------------------------------------------------
    # 2.1 将date转化为datetime类型，结果会覆盖原有数据。

    def format_date(self, symbol):

        self.data.loc[symbol]['date'] = self.data.loc[symbol]['date'].apply(lambda x: pd.to_datetime(str(x)))

        return self.data.loc[symbol]

    # 2.2 画图函数
    def plot(self, symbol, field):
        if (field != 'turnover') and (field != 'volumn'):
            kind = 'line'
            field = 'S_DQ_' + field.upper()
        else:
            kind = 'bar'
        temp_data = StockData.format_date(self, symbol).set_index('date').sort_index()[field]
        temp_data.plot(kind)
        plt.title(symbol+'_'+field)
        plt.show()
        return

    # 2.3 利用复权因子，将数据进行前复权，结果会覆盖原有数据。
    def adjust_data(self, symbol):
        temp = self.data.loc[symbol].copy()
        temp1 = temp.drop(['S_DQ_CLOSE','S_DQ_OPEN','S_DQ_HIGH','S_DQ_LOW'], axis=1)
        self.data = self.data.drop(symbol)
        self.data.loc[symbol] = temp1.copy()
        self.data.loc[symbol]['S_DQ_CLOSE'] = temp['S_DQ_CLOSE'] * temp['S_DQ_ADJFACTOR'] / temp['S_DQ_ADJFACTOR'].iloc[-1]
        self.data.loc[symbol]['S_DQ_OPEN'] = temp['S_DQ_OPEN'] * temp['S_DQ_ADJFACTOR'] / temp['S_DQ_ADJFACTOR'].iloc[-1]
        self.data.loc[symbol]['S_DQ_HIGH'] = temp['S_DQ_HIGH'] * temp['S_DQ_ADJFACTOR'] / temp['S_DQ_ADJFACTOR'].iloc[-1]
        self.data.loc[symbol]['S_DQ_LOW'] = temp['S_DQ_LOW'] * temp['S_DQ_ADJFACTOR'] / temp['S_DQ_ADJFACTOR'].iloc[-1]
        return self.data.loc[symbol]

    # ---------------------------------------------------------------------------------------------
    # 3.1 滑动平均
    def moving_average(self, symbol, field, window):
        res = StockData.get_data_by_field(self, field, [symbol])
        res = pd.rolling_mean(res, window)
        res.plot(kind='line')
        plt.title(symbol + '_' + field + '_ma' + str(window))
        plt.show()
        return res

    # 3.2 指数滑动平均， 参数：span 即滑动周期
    def ema(self, symbol, field, span):
        res = StockData.get_data_by_field(self, field, [symbol])
        res = pd.ewma(res, span)
        res.plot(kind='line')
        plt.title(symbol + '_' + field + '_ema' + str(span))
        plt.show()
        return res

    # 3.3 ATR， 参数：window， 即滑动周期
    def atr(self, symbol, window):
        temp = self.data.loc[symbol].set_index('date').sort_index().copy()
        temp['tr1'] = np.abs(temp['S_DQ_HIGH'] - temp['S_DQ_LOW'])
        temp['tr2'] = np.abs(temp['S_DQ_HIGH'] - temp['S_DQ_PRECLOSE'])
        temp['tr3'] = np.abs(temp['S_DQ_PRECLOSE'] - temp['S_DQ_LOW'])
        temp['tr'] = np.max(temp[['tr1', 'tr2', 'tr3']], axis=1)
        res = pd.rolling_mean(temp['tr'], window)
        res.plot(kind='line')
        plt.title(symbol + '_atr_' + str(window))
        plt.show()
        temp = temp.drop(['tr1', 'tr2', 'tr3', 'tr'], axis=1)
        return res

    # 3.4 RSI， 参数：window, 即滑动周期
    def rsi(self, symbol, window):
        temp = self.data.loc[symbol].set_index('date').sort_index().copy()
        temp = temp['S_DQ_CLOSE'].diff()

        def rsi_cal(sr):
            s1 = sr[sr >= 0]
            s2 = sr[sr < 0]
            return s1.sum() / (s1.sum() - s2.sum()) * 100.

        return pd.rolling_apply(temp, window, rsi_cal)

    # 3.5 MACD, 参数：window：滚动周期 默认为9，fast:快指数移动平均线周期 默认为12， slow：慢指数移动平均线周期 默认为26
    def macd(self, symbol, window=9, fast=12, slow=26):
        res = StockData.get_data_by_field(self, 'close', [symbol]).iloc[-100:]
        res1 = pd.ewma(res, fast)
        res2 = pd.ewma(res, slow)
        dif = res1 - res2
        dea = pd.ewma(dif, window)
        macd = 2. * (dif - dea)
        # 画图展示macd
        plt.figure()
        # plt.plot(res1, color='red',label='fast')
        # plt.plot(res2, color='green',label='slow')
        plt.bar(np.array(res1.index), np.array(macd.iloc[:, 0].values))
        plt.title(symbol+'_macd'+str(fast) +  '_' + str(slow) + '_' + str(window))
        plt.legend()
        plt.show()
        return macd


