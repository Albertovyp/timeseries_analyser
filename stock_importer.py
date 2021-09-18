import yfinance as yf
import pandas as pd
from importer import clean_frame


tickerSymbol = 'TSLA'

tickerData = yf.Ticker(tickerSymbol)

tickerDF = tickerData.history(period='1d', start='2010-1-1', end='2021-6-7')

print('Do you want to update an existing file?. If you want to update introduce yes. \n')
update = input('Do you want to update?: ')

if update == 'yes':
    tickerDF.to_csv("file_path", mode='a')
    tickerDF = pd.read_csv("file_path", parse_dates=[0], index_col=['Date'])
    clean_frame(tickerDF)
    tickerDF.to_csv("file_path", mode='w')

else:
    tickerDF.to_csv("file path", mode='w')