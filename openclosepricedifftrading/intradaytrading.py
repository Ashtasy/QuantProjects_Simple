# region imports
from AlgorithmImports import *
# endregion

class PensiveFluorescentOrangeAnt(QCAlgorithm):

    def initialize(self):
        self.SetStartDate(2018, 1, 1)
        self.SetEndDate(2021,1,1)
        self.set_cash(100000)
        self.symbol = self.AddEquity("SPY", Resolution.Minute).symbol
        self.rollingWindow = RollingWindow[TradeBar](2) # rolling window to compare the last close price to the currrent price
        # RollingWindow calls the function, uses TradeBar to get the date, dont need a long rolling window so 2 elements in our Array
        self.consolidate(self.symbol, Resolution.Daily, self.CustomBarHandler) # consolidates the minutely bars to daily bars, third arguement takes an consolidation event handler that we have to create
        
        # Trade Exit Logice
        self.Schedule.On(self.DateRules.EveryDay(self.symbol),   # ensure it is called everyday that SPY trades
                        self.TimeRules.BeforeMarketClose(self.symbol,15),  # ensure it is called 15 mins before the market closes, this accounts for days market close early like christmas days
                        self.ExitPositions)  # this is an event, a function that this will run based on the above parameters
    
    def on_data(self, data: Slice):
        if not self.rollingWindow.IsReady: # check if our rolling window is ready, its ready only after is filled up with data
            return
        
        if not (self.Time.hour == 9 and self.Time.minute == 31): # we want our market to trade right when the market opens and not any other time, 9.30 mkt open, but we can only access the 9.30 bar at 9.31
            return

        if data[self.symbol].Open >= 1.01 * self.rollingWindow[0].Close:  # check if the open price today is 1% more than the close price of the day before
            self.SetHoldings(self.symbol, -1) # if above condition is true we take a short sell
        elif data[self.symbol].Open <= 0.99 * self.rollingWindow[0].Close:  # check if the open price today is 1% less than the close price of the day before
            self.SetHoldings(self.symbol,1) # if above condition is true we take a long buy
        else:
            return
    def CustomBarHandler(self,bar):  # this is called when a new daily bar is consolidated out of the minutely bars
        self.rollingWindow.Add(bar) # rolling window access the prev day's closing price, we are stroing and adding daily tradebar objects. The bar parameter is to conolidate the daily bar which we want to add to the rolling window

    def ExitPositions(self):
        self.liquidate(self.symbol) # closes any SPY trades along with the conditions that we specified above
