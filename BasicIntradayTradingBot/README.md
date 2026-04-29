# QuantConnectProject1

Not for real market applications, this is used as a learning model. Factors such as survivorship bias are not considered here

Intraday trading bot coded and backtested on the QuantConnect Platform.

Backtesting Results:

- Initial Equity ~ $100,000.00
- Trade Period ~ 01/01/2022 - 01/01/2024
- Final Equity ~ $102,483.25
- Fees ~ --$1.05
- Holdings ~ $99,815.10
- Net Profit ~ $2,722.65
- PSR ~ 7.068%
- Return ~ -2.48 %


How it works:

1. We are trading SPY with 100,000
2. We only buy 1 order if it has been just or more than 30 days since our last closed order
3. Take Profit is set at 1% above the entry price and Stop Loss is set at 1% below the entry price
4. There is also a Log function that tracks every position taken

This code and strategy were adapted from TradeOptionsWithMe on YouTube and could not have been executed well without the QuantConnect Platform The QuantConnect platform is the best one I have come across that has a multitude of libraries and seamlessly backtesting capabilities
