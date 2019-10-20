import pandas as pd
from time import *
from datetime import datetime
import struct
import gzip
import os

class Parse(object):

    def __init__(self, path, only_trading_hours=True, frequency='H'):
        self.f = gzip.open(os.path.join(path, "01302019.NASDAQ_ITCH50.gz"), "rb")
        self.order_list = {}
        # A dictionary of different orders. Keys: order reference number; Values: stock symbol and price.
        self.trade_info = {}
        # A dictionary of trade information.
        # Keys: match number; Values: stock symbol, trade price, trade shares, trade time and trade types.
        self.only_trading_hours = only_trading_hours
        # It is a bool value, deciding the time that we use to calculate vwap.
        # If true, we only calculate during trading hours(09:30-16:00).
        # If false, we calculate for all the system hours(04:00-20:00).
        self.frequency = frequency
        # This decides the interval time we need for our vwap.
        # If it is "H", then we will calculate the vwap hourly.
        # You can decide the frequency, such as using "30T" for half-hourly, or "T" for every minute.

    def Add_Order(self, message):
        '''
        A function to add orders into the order list and to store the information of stock symbol and price.
        :param message:
        :return: None
        '''
        indicator = message[19]
        if indicator == 'B':
            order_reference_number = struct.unpack("!Q", message[11:19])[0]
            # shares = struct.unpack("!I", message[20:24])[0]
            stock_symbol = message[24:32].strip()
            price = struct.unpack("!I", message[32:36])[0] / 10000.
            self.order_list[order_reference_number] = [stock_symbol, price] #, shares]
        return

    def Cancel_Order(self, message):
        '''
        A function to cancel order, modifying the shares of an order.
        :param message:
        :return: None
        '''
        order_reference_number = struct.unpack("!Q", message[11:19])[0]
        try:
            cancel_shares = struct.unpack("!I", message[19:23])[0]
            self.order_list[order_reference_number][2] -= cancel_shares
        except KeyError:
            return
        return

    def Delete_Order(self, message):
        '''
        A function to delete an order from the order list.
        :param message:
        :return: None
        '''
        order_reference_number = struct.unpack("!Q", message[11:19])[0]
        try:
            self.order_list.pop(order_reference_number)
        except KeyError:
            return
        return

    def Replace_Order(self, message):
        '''
        A function to replace an original order with a new one, with a new order reference number added into the list.
        :param message:
        :return: None
        '''
        original_order_reference_number = struct.unpack("!Q", message[11:19])[0]
        new_order_reference_number = struct.unpack("!Q", message[19:27])[0]
        try:
            stock_symbol = self.order_list[original_order_reference_number][0]
            # new_shares = struct.unpack("!I", message[27:31])[0]
            new_price = struct.unpack("!I", message[31:35])[0] / 10000.
            self.order_list.pop(original_order_reference_number)
            self.order_list[new_order_reference_number] = [stock_symbol, new_price] #, new_shares]
        except KeyError:
            return
        return

    def Execute_Order(self, message):
        '''
        A function to store order execution information as trade information.
        :param message:
        :return: None
        '''
        order_reference_number = struct.unpack("!Q", message[11:19])[0]
        try:
            stock_symbol = self.order_list[order_reference_number][0]
            price = self.order_list[order_reference_number][1]
            executed_share = struct.unpack("!I", message[19:23])[0]
            timestamp = self.time_format(struct.unpack("!IH", message[5:11]))
            # print timestamp
            match_number = struct.unpack("!Q", message[23:31])[0]
            self.trade_info[match_number] = [stock_symbol, price, executed_share, timestamp, 'E']
        except KeyError:
            return
        return

    def Exectute_Order_With_Price(self, message):
        '''
        A function to store order execution information with new price as trade information.
        :param message:
        :return: None
        '''
        order_reference_number = struct.unpack("!Q", message[11:19])[0]
        try:
            stock_symbol = self.order_list[order_reference_number][0]
            execution_price = struct.unpack("!I", message[32:36])[0] / 10000.
            timestamp = self.time_format(struct.unpack("!IH", message[5:11]))
            executed_share = struct.unpack("!I", message[19:23])[0]
            match_number = struct.unpack("!Q", message[23:31])[0]
            self.trade_info[match_number] = [stock_symbol, execution_price, executed_share, timestamp, 'C']
        except KeyError:
            return
        return

    def Non_Cross_Trade(self, message):
        '''
        A function to store non-cross trade as trade information.
        :param message:
        :return: None
        '''
        indicator = message[19]
        if indicator == 'B':
            stock_symbol = message[24:32].strip()
            price = struct.unpack("!I", message[32:36])[0] / 10000.
            shares = struct.unpack("!I", message[20:24])[0]
            timestamp = self.time_format(struct.unpack("!IH", message[5:11]))
            match_number = struct.unpack("!Q", message[36:44])[0]
            self.trade_info[match_number] = [stock_symbol, price, shares, timestamp, "P"]

        return


    def Cross_Trade(self, message):
        '''
        A function to store cross trade as trade information.
        :param message:
        :return: None
        '''
        timestamp = self.time_format(struct.unpack("!IH", message[5:11]))
        shares = struct.unpack("!Q", message[11:19])[0]
        if not shares:
            return
        stock_symbol = message[19:27].strip()
        cross_price = struct.unpack("!I", message[27:31])[0] / 10000.
        match_number = struct.unpack("!Q", message[31:39])[0]
        self.trade_info[match_number] = [stock_symbol, cross_price, shares, timestamp, "Q"]
        return


    def Broken_Trade(self, message):
        '''
        A function to take care of broken trade information, by deleting it from the trade-info dictionary.
        :param message:
        :return: None
        '''
        match_number = struct.unpack("!Q", message[11:19])[0]
        try:
            self.trade_info.pop(match_number)
        except KeyError:
            return
        return


    def time_format(self, time):
        '''
        This is a function to transform the timestamp information obtained from the data into SECONDS since mid-night.
        :param time:
        :return: seconds
        '''
        seconds = (time[1] + (time[0] << 16)) / 1000000000.0
        # dt = datetime.utcfromtimestamp(seconds)
        # return dt.strftime('%H:%M:%S')
        return seconds


    def Message_Type(self, message):
        '''
        This is the function to deal with different types of message, and lead to different functions above.
        :param message:
        :return: None
        '''
        message_type = message[0]
        if (message_type == "A") | (message_type == "F"):
            self.Add_Order(message)
        elif message_type == "E":
            self.Execute_Order(message)
        elif message_type == "C":
            self.Exectute_Order_With_Price(message)
        # elif message_type == "X":
        #    self.Cancel_Order(message)
        elif message_type == "D":
            self.Delete_Order(message)
        elif message_type == "U":
            self.Replace_Order(message)
        elif message_type == "P":
            self.Non_Cross_Trade(message)
        elif message_type == "Q":
            self.Cross_Trade(message)
        elif message_type == 'B':
            self.Broken_Trade(message)

        return


    def start_parse(self):

        start = time()

        while True:
            try:
                message_length = struct.unpack("!H", self.f.read(2))[0]
            except:
                break
            message = self.f.read(message_length)
            if not message:
                break
            self.Message_Type(message)  # Process the message.

            # If it comes to certain beginning/end time, the texts will show and the time will be stored.
            if message[0] == "S":
                if message[11] == "S":
                    system_start_time = self.time_format(struct.unpack("!IH", message[5:11]))
                    print "System starts!"
                    print system_start_time
                    print "Used time:"
                    print time() - start
                    print "************"
                elif message[11] == "Q":
                    market_start_time = self.time_format(struct.unpack("!IH", message[5:11]))
                    print "Market begins!"
                    print market_start_time
                    print "Used time:"
                    print time() - start
                    print "************"
                elif message[11] == "M":
                    market_end_time = self.time_format(struct.unpack("!IH", message[5:11]))
                    print "Market ends!"
                    print market_end_time
                    print "Used time:"
                    print time() - start
                    print "************"
                    print
                elif message[11] == "E":
                    system_end_time = self.time_format(struct.unpack("!IH", message[5:11]))
                    print "System ends!"
                    print system_end_time
                    print "Used time:"
                    print time() - start
                    print "************"


        # Transform the trade information dictionary to a DataFrame. Rename the columns.
        print 'Writing to file...'
        all_hours_trade = pd.DataFrame(self.trade_info).T
        all_hours_trade.columns = ['Symbol', 'Price', 'Shares', 'Time', 'Type']

        # Select the trade info from 09:30 to 16:30. Transform the time to string, which is easy to read.
        if self.only_trading_hours:
            trading_hours_trade = all_hours_trade[(all_hours_trade.Time >= market_start_time) & (all_hours_trade.Time <= market_end_time)]
        else:
            trading_hours_trade = all_hours_trade
        trading_hours_trade.Time = trading_hours_trade.Time.apply(lambda x: datetime.utcfromtimestamp(x).strftime('%H:%M:%S'))

        # Calculate price * shares, and groupby the dataframe by symbol and time, then sum up.
        trading_hours_trade['Price*Shares'] = trading_hours_trade.Price.multiply(trading_hours_trade.Shares)
        temp_data = trading_hours_trade.drop(['Price', 'Type'], axis = 1)
        temp_data = temp_data.groupby(['Symbol', 'Time']).sum()

        # Calculate the vwap for every hour. We have 6 hours during 09:30-15:30, and a final half-hour from 15:30-16:00.
        temp_data_1 = temp_data.Shares.unstack().T
        temp_data_1.index = pd.to_timedelta(temp_data_1.index)
        temp_data_2 = temp_data['Price*Shares'].unstack().T
        temp_data_2.index = pd.to_timedelta(temp_data_2.index)
        vwap = (temp_data_2.resample(self.frequency).sum())/(temp_data_1.resample('H').sum())
        self.f.close()
        return vwap, self.trade_info

