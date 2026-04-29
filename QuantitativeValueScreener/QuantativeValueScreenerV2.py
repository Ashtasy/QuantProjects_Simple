import numpy as np
import pandas as pd
import xlsxwriter
import requests
from scipy import stats
import math

# takes into account many more metrics
# Better and More Realistic Value Investing Strategy
from secrets_1 import FMP_API_TOKEN
symbol = 'AAPL'
batch_api_url= f'https://financialmodelingprep.com/api/v3/quote,key-metrics/{symbol}?apikey={FMP_API_TOKEN}'
data = requests.get(batch_api_url).json()
print(data)

# Price-to-earning ratio
pe_ratio = data[symbol]['quote']['pe']

# Price-to-Book ratio
pb_ratio = data['AAPL']['key-metrics']['pricetoBook']  # Not a Number data structure stored in the Numpy Library, like a placeholder

# Price-to-sales ratio
ps_ratio = data['AAPL']['key-metrics']['pricetoSales']

# Enterprise Value divided vy Earnings Before Interest, Taxes, Depreciation, and Amortization (EV/EBITDA)
enterprise_value = data['AAPL']['key-metrics']['enterpriseValue']
ebitda = data['AAPL']['key-metrics']['EBITDA']
ev_to_ebitda = enterprise_value/ebitda

# Enterprise Value divided by Gross Profit (EV/GP)
grossprofit = data['AAPL']['key-metrics']['grossProfit']
ev_to_grossprofit = enterprise_value/grossprofit



# (--DATAFRAME--)

rv_columns = ('Ticker',
              'Price', 
              'Number of Shares to Buy',
              'PE Ratio',
              'PE Percentile',
              'PB Ratio',
              'PB Percentile',
              'PS Ratio', 
              'PS Percentile',
              'EV/EBITDA',
              'EV/EBITDA Percentile',
              'EV/GP',
              'EV/GP Percentile',
              'RV Score')

rv_dataframe = pd.DataFrame(columns=rv_columns)  # rv means robust value

from QuantitativeValueScreener import symbol_string, symbol_strings

for symbol_string in symbol_strings:
    batch_api_url= f'https://financialmodelingprep.com/api/v3/quote,key-metrics/{symbol_string}?apikey={FMP_API_TOKEN}'
    data = requests.get(batch_api_url).json() 

    for symbol in symbol_string.split(','):
        enterprise_value = data['AAPL']['key-metrics']['enterpriseValue']
        ebitda = data['AAPL']['key-metrics']['EBITDA']
        grossprofit = data['AAPL']['key-metrics']['grossProfit']

        try:
            ev_to_ebitda = enterprise_value/ebitda  # tries to calculate the ev_to_ebitda but if the ebitda is None and you 
        except TypeError:                           # you get a type error then it will put np.NaN for those values
            ev_to_ebitda = np.NaN
        
        try:
            ev_to_grossprofit= enterprise_value/grossprofit  # tries to calculate the ev_to_ebitda but if the ebitda is None and you 
        except TypeError:                           # you get a type error then it will put np.NaN for those values
            ev_to_grossprofit = np.NaN

        rv_dataframe=rv_dataframe.append(
            pd.Series([

                symbol,
                data[symbol]['Price'], 
                'N/A',
                data[symbol]['quote']['pe'],
                'N/A',
                data[symbol]['key-metrics']['pricetoBook'],
                'N/A',
                data[symbol]['key-metrics']['pricetoSales'], 
                'N/A',
                ev_to_ebitda,
                'N/A',
                ev_to_grossprofit,
                'N/A',
                'N/A'

            ],index=rv_columns
            ), ignore_index=True 
            
        )



# (--DEALING WITH MISSING DATA IN OUR DATAFRAME--)
        
# when there is no EBITDA value in the api so now its NaN
        
rv_dataframe[rv_dataframe.isnull().any(axis=1)] # taking our dataframe and finding our axis=1 (rows) with missing data or null data

for column in ['PE Ratio','PB Ratio','PS Ratio','EV/EBITDA','EV/GP','RV Score']:
     rv_dataframe[column].fillna(rv_dataframe[column].mean(), inplace=True) # filling the missing values with an average value



# (--CALCULATING VALUE PERCENTILES--)

from scipy.stats import percentileofscore as score     
metrics = {
        'PE Ratio':'PE Percentile',
        'PB Ratio':'PB Percentile',
        'PS Ratio':'PS Percentile',
        'EV/EBITDA':'EV/EBITDA Percentile',
        'EV/GP':'EV/GP Percentile'
}  # made it into a dictionary


for metric in metrics.keys():  # loops over every metric in our dictionary
    for row in rv_dataframe.index:  # loops over every row in our pandas dataframe 
        rv_dataframe.loc[row,metrics[metric]] = score(rv_dataframe[metric], rv_dataframe.loc[row, metric])/100 # calculated the percentile and assign it accordingly




# (--CALCULATING RV SCORE--)
        
from statistics import mean

for row in rv_dataframe.index:
    value_percentiles = []
    for metric in metrics.keys():
        value_percentiles.append(rv_dataframe.loc[row, metrics[metric]])
    rv_dataframe.loc[row, 'RV Score'] = mean(value_percentiles)


# (-- SELECTING THE 50 BEST VALUE STOCKS--)
    
rv_dataframe.sort_values('RV Score', ascending=True, inplace=True)
rv_dataframe = rv_dataframe[:50]
rv_dataframe.reset_index(drop=True,inplace=True) # drop=True, avoid duplicating the index, numbering



# (--CALCULATING THE NUMBER OF SHARES TO BUY--)

def portfolio_input():
    global portfolio_size
    portfolio_size = input('Enter the size of your portfolio: ')

    try:
        float(portfolio_size)
    except ValueError:
        print('That is not a number! \nPLease try again: ')
        portfolio_size = input('Enter the size of your portfolio: ')

portfolio_input()


position_size =float(portfolio_size)/len(rv_dataframe.index)

for row in rv_dataframe.index:
    rv_dataframe.loc[row, 'Number of Shares to Buy']= math.floor(position_size/rv_dataframe.loc[row,'Price'])


# (--FORMATTING OUR EXCEL OUTPUT--)
    
writer = pd.ExcelWriter('Value_Strategy.xlsx', engine='xlsxwriter')
rv_dataframe.to_excel(writer, sheet_name='Value Strategy',index=False)


# (--CREATING THE FORMATS FOR OUR EXCEL--)


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

integar_format= writer.book.add_format(
    {
        'num_format' :'0',
        'font_color':font_color,
        'bg_color':background_color,
        'border':1
    }
)

float_format= writer.book.add_format(
    {
        'num_format':'0',
        'font_color':font_color,
        'bg_color':background_color,
        'border':1
    }
)


percent_format= writer.book.add_format(
    {
        'num_format':'0.0%',
        'font_color':font_color,
        'bg_color':background_color,
        'border':1
    }
)


column_formats = {
    'A':['Ticker',string_format],
    'B':['Price',dollar_format],
    'C':['Number of Shares to Buy',integar_format],
    'D':['PE Ratio',float_format],
    'E':['PE Percentile',percent_format],
    'F':['PB Ratio',float_format],
    'G':['PB Percentile',percent_format],
    'H':['PS Ratio',float_format],
    'I':['PS Percentile',percent_format],
    'J':['EV/EBITDA',float_format],
    'K':['EV/EBITDA Percentile',percent_format],
    'L':['EV/GP',float_format],
    'M':['EV/GP Percentile',percent_format],
    'N':['RV Score',percent_format]
}


for column in column_formats.keys(): #loops through all the column letters in their keys
    writer.sheets['Value Strategy'].set_column[f'{column}:{column}',25,column_formats[column]]
    writer.sheets['Value Strategy'].write(f'{column}1',column_formats[column][0], column_formats[column][1])
    
writer.save()  
                                    