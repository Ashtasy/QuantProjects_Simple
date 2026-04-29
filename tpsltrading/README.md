# QuantConnectProject2

Not for real market applications, this is used as a learning model. Factors such as survivorship bias are not considered here

simple trading bot coded and backtested on the QuantConnect Platform.

Backtesting Results:

- Initial Equity ~ $100,000.00 
- Trade Period ~ 01/01/2022 - 01/01/2024 
- Final Equity ~ $132,646.90
- Fees ~ $35.66
- Holdings ~ $120,648.74
- Net Profit ~ $16,045.14
- PSR ~ 42.499%
- Return ~ 32.65 %


How it works:

1. In this case the algorithm trades 90% of its wallet (100,000) into the chosen equity QQQ
2. Once the order is filled, it adds a Stop Loss 5% below the entry price and a Take Profit 5% above the entry price
3. If the active trade is not closed within 24 hours of entry, the Stop Loss and Take Profit are modified to 5% below and 5% above the price at the current time.
4. Order is closed once the Take Profit or Stop Loss is hit.
5. Please refer to my comments in the code for a line-by-line understanding

A QuantConnect Account will help! But if you have your backtesting methods, go ahead.

This code and strategy was adapted from TradeOptionsWithMe on YouTube and could not have been executed well without the QuantConnect Platform
The QuantConnect platform is the best one I have come across that has a multitude of libraries and seamlessly backtesting capabilities
