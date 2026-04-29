# region imports
from AlgorithmImports import *
# endregion

class DeterminedTanBaboon(QCAlgorithm):

    def initialize(self):
        self.SetStartDate(2020,1,1) # set start date for backtesting
        self.SetEndDate(2021,1,1)          
        self.set_cash(100000) # set cash balance for backtesting, normally taken from broker platform
        
        spy = self.AddEquity("SPY",Resolution.Daily) # add the equity you are trading, this takes another arguement Resolution so for now we use daily
        # self.AddForex to trade forex, self.AddFuture to trade future

        spy.SetDataNormalizationMode(DataNormalizationMode.RAW) # not needed at the default mode is Adjusted which is alright but for this we change to Raw (options trading require RAW)

        self.spy = spy.Symbol # symbole hold more info than tickers that can remove unwanted ambiguity, price, striker price and etc
        
        self.SetBenchmark("SPY") # benchmark, automatically sets up a chart to analyse the perofrmance of our strat
        self.SetBrokerageModel(BrokerageName.InteractiveBrokersBrokerage, AccountType.Margin) # normally defaulted but you can specify so your algorithms best accounts to your brokerage fees and account type
        
        # helper variables,
        self.entryPrice = 0  # this tracks our entry price of the SPY
        self.period = timedelta(30) # set your tmeframe of 31 days
        self.nextEntryTime = self.Time # when we shoulde re-enter a trade, we set it as self.Time which is current time because we want invest now
    
    
    def on_data(self, data): # called when an end time of a bar reached or a ticker event occurs
        
        if not self.spy in data:
            return   # to check if the requested data exists

        # price = data.Bars[self.spy].Close # getting the closed price from the day before using Bars
        price = data[self.spy].Close  # another way to get the above
        # price = self.Securities[self.spy].Close # another way tp get the above by using the Securities

        if not self.Portfolio.Invested: # to check if our bot is already invested, will return a boolean, the portfolio property can help you check other stuff too, look it up
            if self.nextEntryTime <= self.Time:  # we are buying spy after a month
                self.SetHoldings(self.spy, 1) # manually dictating order size
                #self.MarketOrder(self.spy, int(self.Portfolio.Cash / price)) # the division calculates the order size
                self.Log("BUY SPY @" + str(price)) # logs/tracks what your bot is doing
                self.entryPrice = price # saving the price that we bought at so we can define the exit procedure of our trade

            elif self.entryPrice * 1.1 < price or self.entryPrice * 0.9 > price:
                self.Liquidate() #closes our positions
                self.Log("SELL SPY @" + str(price))
                self.nextEntryTime = self.Time + self.Period # tells the bot to on back after 30 days