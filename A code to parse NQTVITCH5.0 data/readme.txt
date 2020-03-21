Hi, this is the instructions of the parsing program written by Hengbo Liang, as a test by  Trexquant.

1. For the code:

You can find my codes in the “codes” folder, there are two python files in it:

“parse.py” is the definition of the class. I encapsulated all my functions into a class.
“main.py” is the main function, and you can change input in this file.

There are actually three inputs for my class:

path: the directory where the gzip file exists, and also the output files.

only_trading_hours: a bool value, deciding the time that we use for vwap.
If it is true, we only calculate during trading hours(09:30-16:00); if false, we calculate for all system hours(04:00-20:00)

frequency: a string. It decides the time interval we need for vwap. Normally we use “H” as we will calculate the vwap hourly. You can also change the frequency, such as “30T” for every half-hour, or “T” for every minute. This value has the same format as pandas.DataFrame.resample() function.

2. For the results:

vwap.csv:

After running the main.py, the vwap will be saved as a csv file (actually a DataFrame). The columns are different stock symbols, and the index are time intervals. Remember: “09:30:00” means the time interval during 09:30:00-10:30:00 and so on. But the last one “15:30:00” only means the time interval during 15:30:00-16:00:00.

trade_info.txt:

After running the main.py, the trade_info will also be saved as a txt file. It is actually a dictionary. The keys are the match numbers of each trade, and the values are a list of stock symbol, price, share, and type of this trade. (Trade types include executed order without price message “E”, executed order with price message “C”, non-cross trade “P”, and cross trades “Q”.) You can always read it again and transform it to DataFrame for further processing.

3.
The code is designed for gzip file as an input. It will take about 80 min to run this code. However, if using a unzipped file as an input, it will take only 50 min to run this code. Only stuff you need to do is to change the loading-file code in “parse.py”.


That’s all. You can always contact me for the further communication for the codes. Thank you!


Sincerely, 
Hengbo Liang

Complete time: 
9/20/2019 - 9/24/2019



