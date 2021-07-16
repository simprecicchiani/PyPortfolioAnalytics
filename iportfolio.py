import datetime
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

transactions = pd.read_csv('./test-portfolio.csv', sep=',', index_col='Date', parse_dates=True, ).sort_index()
tickers = transactions.Ticker.unique()
tickers.sort()

start_date = transactions.index[0]
end_date = '2020-01-29'  # datetime.date.today()

port_holdings = pd.DataFrame(columns=tickers, index=pd.date_range(start=start_date, end=end_date))
port_holdings = port_holdings.fillna(0)
market_data = yf.download(list(tickers), start=start_date + datetime.timedelta(days=1), end='2020-01-30')['Adj Close']
market_data = market_data.asfreq(freq='1D', method='ffill')
market_data.loc[:,'CASH$']=1

for date, transaction in transactions.iterrows():
    t = transaction['Ticker']
    p = transaction['Price']
    q = transaction['Quantity']
    f = transaction['Fee']
    o = transaction['Order']
    if t != 'CASH$':
        if o == 'purchase':
            o = 1
        else:
            o = -1
        port_holdings.loc[date, t] = o * q
        port_holdings.loc[date, 'CASH$'] = - o * p * q - f
    else:
        if o == 'withdrawal':
            o = -1
        else:
            o = 1
        port_holdings.loc[date, t] = + o * q * p - f

for date in port_holdings.index:
    try:
        yesterday = date + pd.Timedelta(-1, unit='D')
        port_holdings.loc[date] = port_holdings.loc[date] + port_holdings.loc[yesterday]
    except:
        pass

port_value = port_holdings*market_data

tot_value = port_value.sum(axis=1)

tot_value.plot()
plt.show()