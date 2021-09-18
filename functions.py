import pandas as pd
from ta.momentum import RSIIndicator
from ta.volume import MFIIndicator


def getIndexes(frame, value):
    position_list = list()
    result = frame.isin([value])
    seriesObj = result.any()
    columnNames = list(seriesObj[seriesObj == True].index)
    for col in columnNames:
        rows = list(result[col][result[col] == True].index)
        for row in rows:
            position_list.append((row, col))
    return position_list


def pct_change(frame, interval):
    change = frame.Close.pct_change(freq=interval)
    frame['change'] = change
    return frame


def typical_price(frame):
    typ_price = (frame['High'] + frame['Low'] + frame['Close']) / 3
    frame['Typical'] = typ_price
    return frame


def highest_price(frame):
    highest_price = frame.High.max()
    return highest_price


def lowest_price(frame):
    lowest_price = frame.Low.min()
    return lowest_price


def average_price(frame):
    average_price = round(frame.Typical.mean(), 3)
    return average_price


def median_price(frame):
    median_price = round(frame.Typical.median(), 3)
    return median_price


def biggest_up_movements(frame, interval, number_of_movements):
    h = frame.change.resample(interval).last().nlargest(number_of_movements)
    return h


def biggest_drawdowns(frame, interval, number_of_movements):
    s = frame.change.resample(interval).last().nsmallest(number_of_movements)
    return s


def biggest_volume(frame, interval, data_points):
    v = frame.Volume.resample(interval).sum().nlargest(data_points)
    return v


def lowest_volume(frame, interval, data_points):
    v = frame.Volume.resample(interval).sum().nsmallest(data_points)
    return v


def volatility(frame):
    daily_volatility = frame.change.resample('D').last().std()
    annualized_volatility = daily_volatility * (365 ** (1 / 2))
    return [daily_volatility, annualized_volatility]


# subperiod is the window of volatility you want. -30, -15, +15...
def graph_volatility(frame, subperiod):
    copy = frame
    index = frame.index
    i = len(index)
    x = 0
    list = []
    while i > x:
        subframe = copy[:subperiod]
        window_volatility = subframe.change.std()
        window_volatility = window_volatility * (365 ** (1 / 2))
        list.append(window_volatility)
        copy = copy.iloc[1:]
        x = x + 1
    return list


def simple_moving_average(frame, window):
    frame['SMA' + str(window)] = df.iloc[:, 1].rolling(window=window).mean()
    return frame


def rsi_indicator(daily_frame):
    indicator_RSI = RSIIndicator(close=daily_frame['Close'])
    daily_frame['RSI'] = indicator_RSI.rsi()
    return daily_frame


def money_flow_index(daily_frame):
    indicator_MFI = MFIIndicator(high=daily_frame['High'], low=daily_frame['Low'], close=daily_frame['Close'],
                                 volume=daily_frame['Volume'])
    daily_frame['MFI'] = indicator_MFI.money_flow_index()
    return daily_frame


def simple_moving_average(daily_frame, window):
    daily_frame['SMA' + str(window)] = daily_frame['Typical'].rolling(window=window).mean()
    return daily_frame


def flhl_to_ohlc(frame):
    new_df = frame.rename(columns={'First':'Open', 'Last':'Close'})
    return new_df


def resample_df(frame, period):
    new_df = frame.resample(period).last()
    new_df['Open'] = frame['Open'].resample(period).first()
    new_df['High'] = frame['High'].resample(period).max()
    new_df['Low'] = frame['Low'].resample(period).min()
    new_df['Volume'] = frame['Volume'].resample(period).sum()
    return new_df


def correlation(frame, asset2_frame):
    frame = resample_df(frame, 'D')
    asset2_frame = resample_df(asset2_frame, 'D')
    typical_price(frame)
    typical_price(asset2_frame)
    asset1 = frame['Typical']
    asset2 = asset2_frame['Typical']
    corr = asset1.corr(asset2)
    return corr


#Gets a list of low prices and returns the lowest and the date
def get_low(frame, low_list):
    low = min(low_list)
    df = (frame.where(frame['Low'] == low))
    df1 = df.dropna()
    low_date = df1.index[0]
    return low, low_date


def peak_to_valley(frame):
    high_low = []
    highest = 0
    lowest = 10000
    low_list = []
    for index, row in frame.iterrows():
        if row['High'] > highest:
            if low_list:
                low = get_low(frame, low_list)[0]
                low_date = get_low(frame, low_list)[1]
                pct_change = (low - temp[0])/temp[0]
                temp.append(low)
                temp.append(low_date)
                temp.append(pct_change)
                tempt_tup = tuple(temp)
                high_low.append(tempt_tup)
                low_list = []
            temp = [row['High'], index]
            lowest = highest
            highest = row['High']
        else:
            if row['Low'] < lowest:
                lowest = row['Low']
                low_list.append(lowest)

    temp.append(get_low(frame, low_list)[0])
    temp.append(get_low(frame, low_list)[1])
    temp.append(0)
    tempt_tup = tuple(temp)
    high_low.append(tempt_tup)
    return high_low