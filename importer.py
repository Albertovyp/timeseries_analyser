import datetime
import bitfinex
import time
import pandas as pd


start_date = ''
end_date = ''

def fetch_data(start, stop, symbol, interval, tick_limit, step):
    # Create api instance
    api_v2 = bitfinex.bitfinex_v2.api_v2()
    data = []
    start = start -step
    while start < stop:
        start = start + step
        end = start + step
        res = api_v2.candles(symbol=symbol, interval=interval,
                             limit=tick_limit, start=start, end=end)
        data.extend(res)
        time.sleep(2)
    return data


def clean_frame(frame):
    frame.drop_duplicates(inplace=True)
    frame.sort_index(inplace=True)
    counter = 0
    #Fill the prev_index variable
    for index, row in frame.iterrows():
        prev_index = index[:1]
        counter = counter + 1
        if counter > 1:
            break
    for index, row in frame.iterrows():
        if prev_index == index[:1]:
            prev_index = index[:1]
        else:
            frame.drop(row, axis=1)
            frame.drop(frame.tail(1).index, inplace=True)
    return frame


print('Do you want to update an existing file?. If you want to update introduce yes. \n')
update = input('Do you want to update?: ')

# Set step size
time_step = 60000000

# Define query parameters
pair = 'iotusd'  # Currency pair of interest
bin_size = '1h'  # This will return minute, hour or day data
limit = 1000  # We want the maximum of 1000 data points
# Define the start date
t_start = datetime.datetime(2021, 5, 25, 0, 0)
t_start = time.mktime(t_start.timetuple()) * 1000
# Define the end date
t_stop = datetime.datetime(2021, 6, 18, 0, 0)
t_stop = time.mktime(t_stop.timetuple()) * 1000
result = fetch_data(start=t_start, stop=t_stop, symbol=pair, interval=bin_size, tick_limit=limit, step=time_step)

# Converts the timestamp into readable datetime info

# Creates a pandas dataframe to store the results from the query

df = pd.DataFrame(result, columns=['Time', 'First', 'Last', 'High', 'Low', 'Volume'])
df['Time'] = pd.to_datetime(df['Time'], unit='ms')
df.set_index('Time', inplace=True)
# Imports the data into a csv file
if update == 'yes':
    df.to_csv("/Users/alberto_vega_peralta/PycharmProjects/CryptTrading/Data/IOTA-hour.csv", mode='a')
    df = pd.read_csv("/Users/alberto_vega_peralta/PycharmProjects/CryptTrading/Data/IOTA-hour.csv",
                     parse_dates=[0], index_col=['Time'])
    clean_frame(df)
    df.to_csv("/Users/alberto_vega_peralta/PycharmProjects/CryptTrading/Data/IOTA-hour.csv", mode='w')

else:
    df.to_csv("/Users/alberto_vega_peralta/PycharmProjects/CryptTrading/Data/IOTA-hour1.csv", mode='w')


print('Process finished successfully')