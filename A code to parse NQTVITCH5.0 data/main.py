from parse import *
import json

path = "/Users/tt/Desktop"
# This is the path where the gzip file exists. Output will also be in this path.
only_trading_hours = True
# It is a bool value, deciding the time that we use to calculate vwap.
# If true, we only calculate during trading hours(09:30-16:00).
# If false, we calculate for all the system hours(04:00-20:00).
frequency = 'H'
# This decides the interval time we need for our vwap.
# If it is "H", then we will calculate the vwap hourly.
# You can decide the frequency, such as using "30T" for half-hourly, or "T" for every minute.

parse = Parse(path, only_trading_hours, frequency)
result = parse.start_parse()
# After running the class, it will have 2 results.
# One is vwap we calculate, and the other is the trade info as a dictionary.

vwap = result[0]
vwap.to_csv(os.path.join(path, "vwap.csv"), encoding='utf8')
# Writing vwap into file.

trade_info = result[1]
jsObj = json.dumps(trade_info)
f = open(os.path.join("trade_info.txt"), "w")
f.write(jsObj)
f.close()
# Writing trade_info into file.
