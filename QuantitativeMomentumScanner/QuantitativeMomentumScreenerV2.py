import numpy as np
import pandas as pd
import requests
from scipy import stats
import math
import xlsxwriter
from QuantitativeMomentumScreener import *

# Building a better and more realistic momentum strategy
# High quality momentum stocks are more preferred, steady and slow growth




hqm_columns = [
    'Ticker',
    'Price',
    'Number of Shares to Buy',
    'One-Year Price Return',
    'One-Year Return Percentile',
    'Six-Month Price Return',
    'Six-Month Return Percentile',
    'Three-Month Price Return',
    'Three-Month Return Percentile',
    'One-Month Price Return',
    'One-Month Return Percentile',
    'HQM Score'
]



# (--CREATE A DATAFRAME AND ADD OUR DATA--)

hqm_dataframe=pd.DataFrame(columns=hqm_columns)
for symbol_string in symbol_strings:
    batch_api_call_url2=''
    batchperformance= requests.get(batch_api_call_url2).json()
    for symbol in symbol_string.split(','):
        hqm_dataframe = hqm_dataframe.append(
            pd.Series(
                [
                    symbol,
                    batchperformance[symbol]['price'],
                    'N/A',
                    batchperformance[symbol]['stats']['1 Year percentage change'],
                    'N/A',
                    batchperformance[symbol]['stats']['6 Mth percentage change'],
                    'N/A',
                    batchperformance[symbol]['stats']['3 Mth percentage change'],
                    'N/A',
                    batchperformance[symbol]['stats']['1 Mth percentage change'],
                    'N/A',
                    'N/A'
                ],
                index=hqm_columns
            ),ignore_index=True
        )

print(hqm_dataframe)



# (--CALCULATING MOMENTUM PERCENTILES--)

time_periods = [
    'One-Year',
    'Six-Month',
    'Threee-Month',
    'One-Month'
]

for row in hqm_dataframe.index:
    for time_period in time_periods:
        change_col=f'{time_period} Price Return'
        percentile_col=f'{time_period} Return Percentile'
        hqm_dataframe.loc[row,percentile_col]= stats.percentileofscore(hqm_dataframe[change_col],hqm_dataframe.loc[row,change_col])/100



# (--CALCULATING HQM SCORES--)
# HQM scores will be the arithmic mean of the 4 momentum percentile scores that we calculates in the last section

from statistics import mean

for row in hqm_dataframe.index:  # looped over each row
    momentum_percentiles =[]     # for each row we created a momentum_percntiles
    for time_period in time_periods:  # loopped through the time periods list
        momentum_percentiles.append(hqm_dataframe.loc[row,f'{time_period} Return Percentile'])  # to the momentum_persentile lists we appended the percentile score for the stock
    hqm_dataframe.loc[row, 'HQM Score']= mean(momentum_percentiles)  # we used the loc method to assign all the average pf the percentiles to the HQM scores
 
    
# (--SELECTING THE 50 BEST MOMENTUM STOCKS--)
    
hqm_dataframe.sort_values('HQM Score', ascending=False, inplace=True) # inplace=True makes sure the sort actually modifies our dataframe
hqm_dataframe=hqm_dataframe[:50] # filters the top 50
hqm_dataframe.reset_index(drop=True,inplace=True )  # reassign the index number (the numbers on the left most side), drop=true removes the old index(numbering)



# (--CALCULATING THE NUMBER OF SHARES TO BUY--)

portfolio_input()

position_size= float(position_size)/len(hqm_dataframe.index)

for i in hqm_dataframe.index:
    hqm_dataframe.loc[i,'Number of Shares to Buy']=math.floor(position_size/hqm_dataframe.loc[i,'Price'])


# (--FORMAT OUR CODE TO OUR XLSX FILE--)
    
writer = pd.ExcelWriter('Momentum_strategy.xlsx', engine='xlsxwriter')  # intialise a writer object ('Name of the file you want to create', the engine)
hqm_dataframe.to_excel(writer, sheet_name='Momentum Strategy', index=False)



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

integar_format= writer.book.add_format(
    {
        'num_format' :'0',
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
    'D':['One-Year Price Return',percent_format],
    'E':['One-Year Return Percentile',percent_format],
    'F':['Six-Month Price Return',percent_format],
    'G':['Six-Month Return Percentile',percent_format],
    'H':['Three-Month Price Return',percent_format],
    'I':['Three-Month Return Percentile',percent_format],
    'J':['One-Month Price Return',percent_format],
    'K':['One-Month Return Percentile',percent_format],
    'L':['HQM score',percent_format]
}

for column in column_formats.keys():
    writer.sheets['Momentum Strategy'].set_column(f'{column}:{column}',25,column_formats[column][1])
    writer.sheets['Momentum Strategy'].write(f'{column}1',column_formats[column][0],column_formats[column][1])
#   wirter. what you want to format,set.column(column we want to apply the format to, column width, which column we are going to apply that)
    
writer.save()