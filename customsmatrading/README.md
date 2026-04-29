# QuantConnectProject3

Not for real market applications, this is used as a learning model. Factors such as survivorship bias are not considered here

simple trading bot coded and backtested on the QuantConnect Platform.

Backtesting Results:

- Initial Equity ~ $100,000.00 
- Trade Period ~ 01/01/2022 - 01/01/2024 
- Final Equity ~ $91,993.64
- Fees ~ -$50.90
- Holdings ~ $91,450.70
- Net Profit ~ $-15,297.16
- PSR ~ 1.296%
- Return ~ -8.01 %

As you have noticed this strategy did not do as well, this is mainly because 2022 and 2023 were years with major fluctuations and this bot does not have a concrete Stop Loss and Take Profit parameters set.


How it works:

1. We will be using a custom SMA (Simple Moving Average) indicator and 52-Week High and Low for our trading strategy
2. We will define an uptrend when the current price is above the SMA and is close to the 52-Week high, 5% below the 52-Week High
3. Downtrend is when the current price is below the SMA and it is close to the 52-Week Low, 5% above the 52-Week Low
4. Once our Algorithms see that it is an uptrend it will take a Buy position and vice versa for a downtrend
5. It will then close open positions if none of the conditions are met or if the price hits the 52-Week High and 52-Week Low 

A QuantConnect Account will help! But if you have your backtesting methods, go ahead.

This code and strategy was adapted from TradeOptionsWithMe on YouTube and could not have been executed well without the QuantConnect Platform
The QuantConnect platform is the best one I have come across that has a multitude of libraries and seamlessly backtesting capabilities
