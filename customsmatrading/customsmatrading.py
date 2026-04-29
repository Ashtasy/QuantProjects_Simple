# region imports
from AlgorithmImports import *
from collections import deque # deque double-sided queue that helps you amend and remove elements from both sides of the collection  
# endregion

class CrawlingRedOrangePony(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2020, 1, 1)
        self.set_end_date(2021,1,1)
        self.set_cash(100000)
        self.spy = self.add_equity("SPY", Resolution.Daily).Symbol

        # self.sma = self.SMA(self.spy,30,Resolution.Daily) # indicator, in the brackets security for this indictor, 30 days for the length of data into SMA 
        # closing_prices = self.History(self.spy,30,Resolution.Daily)["close"] # returns a pandas dataframe of closes,highs, lows of SPY for the past 30 days. we need closing prices so we index that out 
        #for time, price in closing_prices.loc[self.spy].items():
        #    self.sma.Update(time,price)  # updating the sma with data, this makes the sma ready without us having to check 
          

        self.sma = CustomSimpleMovingAverage("CustomSMA", 30) # create an instance for our custom indicator
        self.RegisterIndicator(self.spy,self.sma,Resolution.Daily) # register this instance of our indicator to our algorithm
    
    
    def on_data(self, data: Slice):
        if not self.sma.IsReady:  # check if sma is ready, they are churning data to create sma so takes time
            return                # only do this if you didnt do the "Closing Price" code and the iterations above
        
        # the method below is inefficient as we are api calling data every day for 365
        # use rolling window method or min and max indicator for a more efficient alternative
        hist = self.History(self.spy,timedelta(365),Resolution.Daily)  # gets a pandas dataframe of open,close,high and low prices of SPY, use timedelta(365) instead of 365 to not use bar count. Bar count accounts for trading days but we want the whole 365 days in a year
        low = min(hist["low"])    # minimum price in the low column
        high = max(hist["high"])  # max price in the high column

        price = self.Securities[self.spy].Price
        
        # engaging in a buy order
        if price * 1.05 >= high and self.sma.Current.Value < price : # checking if the current price is 5% below the 52-week high and if the current price is above the SMA signalling uptrend
            if not self.Portfolio[self.spy].IsLong:  # check if we havent Buy/Long yet
                self.SetHoldings(self.spy,1)  # enter a buy order of 1

        # engaging in a sell order    
        elif price * 0.95 <= low and self.sma.Current.Value > price: # checking if the current price is 5% above the 52-week low and if the current price is below the SMA signalling downtrend
            if not self.Portfolio[self.spy].IsShort: # ensure we havent sell/short yet
                self.SetHoldings(self.spy,-1)  # enter a sell order of 1
        
        else:
            self.Liquidate()  # close all the orders if none of our conditions meet

        self.Plot("Benchmark","52w-High",high) # arguments in the bracket (name of the chart the plot to be on, name of the actual plot, actual data)
        self.Plot("Benchmark","52w-Low",low)
        self.Plot("Benchmark","SMA",self.sma.Current.Value)

class CustomSimpleMovingAverage(PythonIndicator): # our own indicator
    def __init__(self, name, period): # just like def intialize 
        # helper variables below
        self.Name = name
        self.Time = datetime.min
        self.Value = 0. # actual value of our indicator, 0 for now
        self.queue = deque(maxlen=period) # a deque to help append, this queue will save up to 30 elements

    def Update(self,input):
        self.queue.appendleft(input.Close) 
        self.Time = input.EndTime
        count = len(self.queue)
        self.Value = sum(self.queue) / count
        return(count == self.queue.maxlen)
