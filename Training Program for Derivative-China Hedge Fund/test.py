# -*- coding: utf-8 -*-
"""
Created on Sat Sep  8 16:14:17 2018

@author: ASUS-PC
"""

# -*- coding: utf-8 -*-
from functions import *
# 选择数据所在路径
path = "C://Users//ASUS-PC//Desktop//training//data"


# 1.1
data = StockData(path)
# 1.2
data.read(['000001', '000002', '000027'])
# 1.3
print (data.get_data_by_symbol('000001',19950104,19950628))
# 1.4
print (data.get_data_by_date(19950104,['000001','000002']))
# 1.5
print (data.get_data_by_field('open',['000001','000002','000027']))


# 2.1
data.format_date('000001')
# 2.2
data.plot('000001','open')  # 画图时若要画turnover或volume，请选择合适的时间跨度，因为过长的时间跨度会导致画图很慢
# 2.3
print (data.adjust_data('000002')['S_DQ_CLOSE'])


# 3.1
data.moving_average('000001', 'open', 60)
# 3.2
data.ema('000001','open',20)
# 3.3
data.atr('000001',20)
# 3.4
print (data.rsi('000001',20))
# 3.5
data.macd('000001', 9, 12, 26) # 同样，画MACD柱状图时，请选择合适的时间跨度，因为过长的时间跨度会导致画图很慢