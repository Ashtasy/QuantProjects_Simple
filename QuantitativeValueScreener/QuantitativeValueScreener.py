# value investing means investing in the cheapest relative stocks to common measures of business values(like earnings or assets)
# investing strategy that selects the 50 stocks with the best value metrics. From there we will calculate recommended trades for an equal-weight portfolio of these 50 stocks

import numpy as np
import pandas as pd
import xlsxwriter
import requests
from scipy import stats
import math

# (--IMPORTING OUR LISTS OF STOCKS--)

stocks = pd.read_csv('sp_500_stocks.csv')
from secrets_1 import FMP_API_TOKEN


# (--MAKING OUR FIRST API CALL--)

# find the pe ratie api call url and price
#symbol='AAPL'

#api_url = f'https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey={FMP_API_TOKEN}'
#batch_api_url =f'https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey={FMP_API_TOKEN}'
#data= requests.get(api_url).json()
#print(data)


# (--PARSING OUT API CALL--)

#price = data[0]['price']
#pe_ratio = data[0]['pe']
#print(price, pe_ratio)



# (--SPLITTING OUR STOCKS INTO GROUPS OF 100--)

def chunks(lst,n): # splits the tickers list into groups 
    """Yield successive n-sized chunks from lst."""
    for i in range(0,len(lst),n):
        yield lst[i:i+n]

symbol_strings=[]

symbol_groups = list(chunks(stocks['Ticker'],100)) # we are doing splitting of sets of 100

for i in range(0,len(symbol_groups)):
    symbol_strings.append(','.join(symbol_groups[i])) # take every group in symbol_strings and create a comma separated string


# (--CREATING A BLANK DataFrame and Adding our Data in it--)
    
my_columns = ['Ticker','Price','PE Ratio','Number Of Shares to Buy' ]

final_dataframe= pd.DataFrame(columns=my_columns)

for symbol_string in symbol_strings:  # separates the stocks from its comma separation
    batch_api_url=f'https://financialmodelingprep.com/api/v3/quote/{symbol_string}?apikey={FMP_API_TOKEN}' # for our batch api call it only takes in string value hence we had to convert the input to symbol_string
    data=requests.get(batch_api_url).json() 

    for symbol in symbol_string.split(','):
        final_dataframe= final_dataframe.append(
            pd.Series(
                [
                    symbol,
                    data['symbol']['price'],
                    data['symbol']['pe'],
                    'N/A'
                ], index=my_columns
            ), ignore_index=True
        )




# (--REMOVING GLAMOUR STOCKS--)
        
final_dataframe.sort_values('PE Ratio',inplace=True)  # sort accoring to PE ratio, Inplace=TRue ensures the dataframe is modified
final_dataframe = final_dataframe[final_dataframe['PE Ratio'] > 0]  # keeping the stocks with positive PE Ratios
final_dataframe = final_dataframe[:50] # keeps the top 50
final_dataframe.reset_index(inplace=True)  # resetd the index (numbering)
final_dataframe.drop('index',axis=1,inplace= True) # drop method acts on a horizontal so we neeed to say axis 1



# (--CALCULATING NUMBERS OF SHARES TO BUY--)

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

