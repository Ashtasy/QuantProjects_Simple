import numpy as np       # numerical computing library, fast, its a C/C++ module
import pandas as pd      # panel data, very easy to work with tabular data, pandas dataframe popular
import requests          # popular python library, gold standard for HTTPS requests, internet request send to api tp get back some data
import xlsxwriter         # form excel sheet from Python
import math              # just a mathematical library


# (--IMPORTING OUR LIST OF STOCKS--)

# we are using a static list of SP500

stocks = pd.read_csv('sp_500_stocks.csv')    # reads the file and converts into a pandas dataframe


# (--ACQUIRING AN API TOKEN--)

# using FMP API Token
# using sandbox mode, you get random data, free version for playing around, like to test before using the real API (not using sandbox now)
# API Tokens are sensitive information and must be stored in a secrets.py file so it doesnt'ty get pushed to your local Git repository
# To download secrets.py file go to : http://nickmccullum.com/algorithmic-trading-python/secrets.py
from secrets_1 import FMP_API_TOKEN

# (--MAKING OUR FIRST API CALL--)

# to call need market cap and price of the stock

symbol= 'AAPL'

# api url for the function Quote, {symbol} is a f string, placeholder for the stock we acting on

#api_url=f"https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey={FMP_API_TOKEN}"
#data = requests.get(api_url).json()


# (--PARSING OUR API GET--)
# retrieving price and mkt cap from the list 
#price= data[0]['price']
#marketcap=data[0]['marketCap']


#(--ADDING OUR STOCKS DATA TO A PANDAS DATAFRAME--)

#my_columns = ['Ticker', 'Stock Price', 'Market Capitalisation', 'Number of Shares to Buy']
#final_dataframe = pd.DataFrame(columns = my_columns)
#final_dataframe=final_dataframe.append(
    #pd.Series(
#        [
#            symbol,
#            'price',
#            'marketcap',
#            'N/A'
#        ],
    #index=my_columns),
    #ignore_index=True
#)


#my_columns = ['Ticker', 'Stock Price', 'Market Capitalisation', 'Number of Shares to Buy']
#data = [[symbol, 'price', 'marketcap', 'N/A']]
#final_dataframe = pd.DataFrame(data, columns=my_columns)

#print(final_dataframe)


# (--LOOKING THROUGH THE TICKERS IN OUR LIST OF STOCKS--)
#for stock in stocks['Ticker']:
    #print(stock)
    #api_url=f"https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey={FMP_API_TOKEN}"
    #data = requests.get(api_url).json()  HTTPS request
# the above method is slow, because is a single API request through HTTPS which is slow


# (--USING BATCH API CALLS TO IMPROVE PERFORMANCE--)

def chunks(lst,n): # splits the tickers list into groups 
    """Yield successive n-sized chunks from lst."""
    for i in range(0,len(lst),n):
        yield lst[i:i+n]
symbol_strings=[]
symbol_groups = list(chunks(stocks['Ticker'],100)) # we are doing splitting of sets of 100
for i in range(0,len(symbol_groups)):
    symbol_strings.append(','.join(symbol_groups[i]))
#    print(symbol_strings[i])
#for symbol_string in symbol_strings[:1]:
#    batch_api_url=f'https://financialmodelingprep.com/api/v4/batch-pre-post-market/{symbol_string}?apikey={FMP_API_TOKEN}'
#    data = requests.get(batch_api_url).json()
#    for symbol in symbol_string.split(','):
#        final_dataframe = final_dataframe.append(
#            pd.Series( # there is an issue here
#                [
#                    symbol,
#                    data[symbol]['quote'['price']]
#                ]
#            )
#        )



# (--CALCULATING THE NUMBER OF SHARES TO BUY--)
#portfolio_size=input('Enter the value of your portfolio: ')
#try:
#    val = float(portfolio_size)
#except ValueError:
#    print("That's not a number, please try again:")
#    portfolio_size=input('Enter the value of your portfolio: ')
#    val = float(portfolio_size)   

# The above code is asking for the user's portfolio size and ensuring the user types in an integer and not a string

#position_size = val/len(final_dataframe.index)
#for i in range(0.len(final_dataframe.index)):
#    final_datafraem.loc[i,'Number of Share to Buy'] = math.floor(position_size)/final_dataframe.loc[i, 'Stock price']

# the code above calculates the number of shares to buy for each stock and rounds down to make it a whole number
    




# (--INTIALIZING OUR XLXSXWRITER OBJECT--)

writer = pd.ExcelWriter('recommended trades.xlsx', engine = 'xlsxwriter')
#final_dataframe.toexcel(writer,'Recommended Trades', index=False)


# (--CREATING THE FORMATS IN OUR XLSX FILE)

background_color='#0a0a23'
font_color='#ffffff'

string_format= writer.book.add_format(
    {
        'font_color':font_color,
        'bg_color':background_color,
        'border':1
    }
)

dollar_format= writer.book.add_format(
    {
        'num_format':'0',
        'font_color':font_color,
        'bg_color':background_color,
        'border':1
    }
)

#integar_format= writer.book.add_format(
#    {
#        'int_format'0',
#        'font_color':font_color,
#        'bg_color':background_color,
#        'border':1
#    }
#)



writer.sheets['Recommeded Trades'].set_column('A1:Ticker',18,string_format)
writer.sheets['Recommeded Trades'].set_column('B1:Stock Price',18,string_format)
writer.sheets['Recommeded Trades'].set_column('C1:Market Capitalisation',18,string_format)
writer.sheets['Recommeded Trades'].set_column('D1:Number of Shares to Buy',18,string_format)
writer.save()

# making the above code easier

#column_formats = {
#    'A':['Ticker',string_format],
#    'B':['Stocker Price',dollar_format],
#    'C':['Market Capitalisation',dollar_format],
#    'D':['Number of Shares to Buy',integar_format]
#}
#for column in column_formats.keys():
#    writer.sheets['Recommended Trades'].set_column(f'{column}:{column}',18,column_formats[column][1])
#    writer.sheets['Recommeded Trades'].write(f'{column}1', column_formats[column][0],column_formats[column][1])
#
#writer.save()




