# timeseries_analyser
Import cryptocurrency and stock historical price data from Btifinex and Yahoo Finance APIs, store it in a csv file and perform basic analysis over it. This project consists of three scripts: a cryptocurrency importer, a stock importer and a set of functions to perform various kinds of analysis.

## importer.py
This code comes from the Bitfinex API documentation (https://docs.bitfinex.com/docs) and from a blogpost from Carsten Klein, an engenieer from Bitfinex (https://medium.com/coinmonks/how-to-get-historical-crypto-currency-data-954062d40d2d). My adittions are a few lines of code to export the DataFrame to a new csv and to update an existing csv file. Make sure to follow the steps of the Bitfinex API docs to set up the connection to the API correctly.
 - Asks the user whether he wants to create a csv file or update an existing one. 
 - Connects to the Bitfinex API and gets the desiried data. The user can specify:
    - Cryptocurrency ticker.
    - Granularity of the data (minute, hour, day...). 
    - Timeframe.
 - Transforms the output of the query (a list of lists) containing the data into a pandas dataframe to facilitate the analysis.
 - Writes the pandas DataFrame into a csv file.

## stock_importer.py
Code from the Yahoo API documentation (https://python-yahoofinance.readthedocs.io/en/latest/api.html)

## functions.py
- Provides a function to change the name of the columns of cryptocurrency data to the standard OHLC format.
- Provides a set of functions that abstract the sintax of the pandas library and calculates various metrics. The functions can be used to calculate: percentage change between different data points, typical price, highest price, lowest price, average price, biggest up movements, biggest drawdowns, biggest volumes, lowest volumes, correlation, volatility and peak to valley drawdowns (largest cumulatives percentage declines in the timeseries).
- Provides functions to calculate technical indicators that might be useful to spot overbought and oversold situations. The indicators are: Simple Moving Averages, the Relative Strength Indicator and the Money Flow Index (The latter two functions are just abstractions of the ta library developed by bukosabino https://github.com/bukosabino/ta). 

