# -*-coding:utf-8-*-
import pandas as pd
import matplotlib.pyplot as plt
import backtest as bt

print"data reading..."
# reading data
return_data = pd.read_csv("C:\\Users\\ASUS-PC\\Desktop\\A\\csv\\Forward5D.csv").loc['20150101':, :].fillna(0)
factor = pd.read_csv("E:\\NEWFACTOR.csv")

# divided the stock into 5 quantiles according to the factor values
return_1 = []  # The best 20%
return_2 = []
return_3 = []
return_4 = []
return_5 = []  # The worst0%

# some list for saving some data
factor_turnover = []
IC = []
coverage = []
month_average_coverage = []
corr = []
print "data processing..."
# Preprocessing data, not neccesary
#factor = factor.iloc[:, 1:]
#return_data = return_data.iloc[:, 1:]

# Divided the data into 5 groups and complete calculation in these loops.
for i in range(0, len(factor.index)):
    # sort values(small to big) this week
    factor_i = factor.iloc[i, :].dropna().sort_values()
    # sort values (small to big)  last week
    factor_1 = factor.iloc[:, i-1].dropna().sort_values()
    # stocks this week
    index = factor_i.index
    # stocks last week
    index1 = factor_1.index
    # Rank of factor values
    factor_rank = factor.iloc[:, i].dropna().rank(ascending=False)
    # Rank of return
    return_data_rank = return_data.iloc[:, i].dropna().rank(ascending=False)
    # Calculating IC every week
    IC.append(factor_rank.corr(return_data_rank)*100)
    # Calculating coverage every week
    coverage.append(len(factor_i))

    
    # The worst20%:
    s = 0
    for j in range(0, len(factor_i)/5):
        s = s+return_data.iloc[i,index[j]]
    return_5.append(s/(len(factor_i)/5))
    s = 0
    for j in range(len(factor_i)/5, len(factor_i)*2/5):
        s = s+return_data.iloc[index[j], i]
    return_4.append(s/(len(factor_i)/5))
    s = 0
    for j in range(len(factor_i)*2/5, len(factor_i)*3/5):
        s = s+return_data.iloc[index[j], i]
    return_3.append(s/(len(factor_i)/5))
    s = 0
    for j in range(len(factor_i)*3/5, len(factor_i)*4/5):
        s = s+return_data.iloc[index[j], i]
    return_2.append(s/(len(factor_i)/5))
    # The best 20%:
    s = 0
    for j in range(len(factor_i)*4/5, len(factor_i)):
        s = s+return_data.iloc[i,index[j]]
    return_1.append(s/(len(factor_i)/5))
    turnover = 0

    # Turnover every week:
    for j in index1[0:len(factor_i)/5]:
        if j not in index[0:len(factor_1)/5]:
            turnover += 1
    for j in index1[len(factor_i)*4/5:len(factor_i)]:
        if j not in index[len(factor_i)*4/5:len(factor_i)]:
            turnover += 1
    factor_turnover.append(5.0*100.0*turnover/len(factor_1))


# ---------------------------------------------------------------------------------
# Using the plot function:
print "graphs drawing..."
'''
# 1. Coverage
bt.coverage_plot(coverage)
# 2. Annualized Returns
bt.annual_return_plot(return_1, return_2, return_3, return_4, return_5)
# 3. Annualized Volatility
bt.annual_volatility_plot(return_5, return_4, return_3, return_2, return_1)
# 4. Factor Turnover
bt.factor_turnover_plot(factor_turnover)
# 5. Portfolio IR
bt.portfolio_ir_plot(return_5, return_4, return_3, return_2,  return_1)
# 6. Portfolio Returns (Please remember to change the saving path）
bt.return_table(return_5, return_4, return_3, return_2, return_1, factor)
# 7. Quantile Returns
bt.q_return_plot(return_1, return_2, return_3, return_4, return_5)
# 8. Serial Correlation
bt.serial_corr_plot(factor)
# 9. Sortinal Ratio
bt.sortinal_ratio_plot(return_5, return_4, return_3, return_2,  return_1)
# 10. Spearson Rank IC
bt.ic_plot(IC)
# 11. Time Series Spread
bt.time_series_plot(return_1, return_5)
'''
# 12. Wealth Curve
bt.wealth_curve_plot(return_1, return_5,len(factor_i))
# Show the graphs
plt.show()
