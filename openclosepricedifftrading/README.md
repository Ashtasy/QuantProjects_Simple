# QuantConnectProject4

Not for real market applications, this is used as a learning model. Factors such as survivorship bias are not considered here

Intraday trading bot coded and backtested on the QuantConnect Platform.

Backtesting Results:

- Initial Equity ~ $100,000.00 
- Trade Period ~ 01/01/2022 - 01/01/2024 
- Final Equity ~ $97,781.72
- Fees ~ -$161.57
- Holdings ~ $0.00
- Net Profit ~ $-2,218.28
- PSR ~ 3.317%
- Return ~ -2.22 %

Rough year for Algorithm Trading Bots, the fluctuations in these 2 years and intraday strategies should be solidified with strict parameters.



How it works:

1. We are trading SPY with 100,000 with an intraday strategy
2. Using Rolling Window instead of the simpler group calls to only call necessary information
3. Firstly the algorithm is only called during US market trading hours and trades throughout those hours
4. The algorithm then compares today's open price to the close price the day before
5. If today's open price is 1% higher than yesterday's close price, it takes a Sell Order of 1
6. If today's open price is 1% lower than yesterday's close price, it takes a Buy Order of 1
7. All open trades are closed at the end of the trading hours of that day

A QuantConnect Account will help! But if you have your backtesting methods, go ahead.

This code and strategy was adapted from TradeOptionsWithMe on YouTube and could not have been executed well without the QuantConnect Platform
The QuantConnect platform is the best one I have come across that has a multitude of libraries and seamlessly backtesting capabilities
