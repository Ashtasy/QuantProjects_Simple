# selects the 50 stocks with the highest price momentum, then create a equal weight 50 stock portfolio

import numpy as np
import pandas as pd
import requests
from scipy import stats
import math
import xlsxwriter


# (--IMPORTING OUR LIST OF STOCKS--)

stocks = pd.read_csv('sp_500_stocks.csv')


# (--MAKING OUR FIRST API CALL--)
from secrets_1 import FMP_API_TOKEN
symbol='NVDA'
api_url = f'https://financialmodelingprep.com/api/v3/stock-price-change/{symbol}?apikey={FMP_API_TOKEN}'
performance= requests.get(api_url).json()


# (--PARSING OUR API CALL--)
# find out the 1Y returns
yearreturn= performance[0]['1Y']

# (--SPLITTING OUR STOCKS INTO GROUPS OF 100--)

def chunks(lst,n): # splits the tickers list into groups 
    """Yield successive n-sized chunks from lst."""
    for i in range(0,len(lst),n):
        yield lst[i:i+n]

symbol_strings=[]

symbol_groups = list(chunks(stocks['Ticker'],100)) # we are doing splitting of sets of 100

for i in range(0,len(symbol_groups)):
    symbol_strings.append(','.join(symbol_groups[i]))


# (--CREATE A DATAFRAME AND ADD OUR DATA--)
    
my_columns = ['Ticker','Price','One-Year Price Retinr','Number Of Shares to Buy' ]

final_dataframe=pd.DataFrame(columns=my_columns)
for symbol_string in symbol_strings:
    batch_api_call_url=''
    batchperformance= requests.get(batch_api_call_url).json()
    for symbol in symbol_string.split(','):
        final_dataframe = final_dataframe.append(
            pd.Series(
                [
                    symbol,
                    batchperformance[symbol]['price'],
                    batchperformance[symbol]['stats']['1 Year percentage change'],
                    'N/A'
                ],
                index=my_columns
            ),ignore_index=True
        )



# (--REMOVING LOW-MOMENTUM STOCKS--)
        
final_dataframe.sort_values('One-Year Price Retinr', ascending=False, inplace=True)
final_dataframe= final_dataframe[:50]
final_dataframe.reset_index(inplace=True)


# (--CALCULATING NUMBER OF SHARES TO BUY--)

def portfolio_input():
    global portfolio_size
    portfolio_size = input('Enter the size of your portfolio: ')

    try:
        float(portfolio_size)
    except ValueError:
        print('That is not a number! \nPLease try again: ')
        portfolio_size = input('Enter the size of your portfolio: ')

portfolio_input()
print(portfolio_size)

position_size =float(portfolio_size)/len(final_dataframe.index)
print(position_size)
for i in range(0/len(final_dataframe)):
    final_dataframe.loc[i, 'Number of Shares to Buy']= math.floor(position_size/final_dataframe.loc[i,'Price'])








