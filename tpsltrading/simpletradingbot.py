# region imports
from AlgorithmImports import *
# endregion

class SquareBrownChicken(QCAlgorithm):

    def initialize(self):
        self.SetStartDate(2018,1,1)
        self.SetEndDate(2021,1,1)
        self.SetCash(100000)

        self.qqq = self.AddEquity("QQQ", Resolution.Hour).Symbol
        
        # helper variables
        self.entryTicket = None # tracks the order filled
        self.stopMarketTicket = None # tracks the order closed
        self.entryTime = datetime.min # tracks the time we filled
        self.stopMarketOrderFillTime = datetime.min  # tracks when we close the order
        self.highestPrice = 0 # tracks the highest price recorded by QQQ

    def OnData(self, data):
        # wait 30 days aftet last closed orders
        if (self.Time - self.stopMarketOrderFillTime).days < 30:
            return # we dont do anyth because it hasnt been 30 days

        price = self.Securities[self.qqq].Price # retrieve price from the securities dictionary

        # send in an entry limit order for the order size
        if not self.Portfolio.Invested and not self.Transactions.GetOpenOrders(self.qqq): # check if we have aldy invested, if there arent any orders the transacyions.getopenorders wil be an empty list and evaluate to false
            quantity = self.CalculateOrderQuantity(self.qqq,0.9) # calculate the order quantity, here we are allocating 90% of our portfolio so it will calculate the number of shares based on that
            self.entryTicket = self.LimitOrder(self.qqq, quantity, price, "Entry Order") # sending a limit order, and tagging as "Entry Order"
            self.entryTime = self.Time # saving the time we execute the trade
        
        # if not filled within one day, move limit price up
        if (self.Time - self.entryTime).days > 1 and self.entryTicket.Status != OrderStatus.Filled: # first part is to check more than 1 day, second part is to make sure order hasnt been filled
            self.entryTime = self.time
            updateFields = UpdatedOrderFields() # create an update order fields object
            updateFields.LimitPrice = price # update the limit price to the current price of qqq
            self.entryTicket.Update(updateFields) # update the limit order with the changes

        #  move up the trailing stop price if necessary
        if self.stopMarketTicket is not None and self.Portfolio.Invested: # ensure we still have an active order
            if price > self.highestPrice: # check qqq current price is higher than the prev recorded peak
                self.highestPrice = price 
                updateFields = UpdateOrderFields() # creating an updated object fields object so we can easily amend
                updateFields.StopPrice = price * 0.95 # set a new stop price which is 5% lower the new high price
                self.stopMarketTicket.Update(updateFields) # we add in the updates to the stop price to the market order


    def OnOrderEvent(self, orderEvent):
        if orderEvent.Status != OrderStatus.Filled: # check if the order is filled,
            return # we are only interested in cases thar the order is not filled, thats why we return here
        
        # send stop loss order only if our entry order is filled
        if self.entryTicket is not None and self.entryTicket.OrderId == orderEvent.OrderId: # check if order is filled and the order we are dealing with the correct one through Order ID
            self.stopMarketTicket = self.StopMarketOrder(self.qqq, -self.entryTicket.Quantity,0.95*self.entryTicket.AverageFillPrice) # sending in a close order by creating a SELL of the order we filled, setting the stop loss price at 5% below than our entry price
        
        # save fill time of stop loss order, so we can re enter after 30 days from the stop loss
        if self.stopMarketTicket is not None and self.stopMarketTicket.OrderId == orderEvent.OrderId: # checking again if the order we intaited earlier got filled and we are checking whether the order we are talking about is indeed the same order through Order Id
            self.stopMarketOrderFillTime = self.Time # saving the time the order gets closed for the loop
            self.highestPrice = 0 # set it as 0 as we do not know the future peaks of qqq
