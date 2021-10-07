import pandas as pd
from numpy import genfromtxt
import base64
import datetime

class Orders:
    
    ACCOUNT = ['deposit', 'withdrawal']
    SECURITY = ['purchase', 'sale']

class Tickers:

    US = genfromtxt('assets/us_tickers.csv', dtype=str, delimiter=',')
    CURRENCIES = genfromtxt('assets/currencies.csv', dtype=str, delimiter=',')

class Table:

    def new(self):

        COLS = ['Date','Ticker', 'Order', 'Price', 'Quantity', 'Fee']
        self.data = pd.DataFrame(columns=COLS)

    def __init__(self):
        self.new()

    @staticmethod
    def validate(date, ticker, order, price, quantity, fee):

        ticker = ticker.upper()
        ACCOUNT_TRANSACTION = (True if ticker == 'CASH.USD' else False)
        ORDERS = (Orders.ACCOUNT if ACCOUNT_TRANSACTION else Orders.SECURITY)

        if not isinstance(date, datetime.date):
            try: 
                date = datetime.datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                return print(f'{date} does not match format %Y-%m-%d (1970-01-01)'), None

        if not isinstance(ticker, str):
            # raise TypeError('Ticker is mandatory and should be a string.')
            return print('Ticker is mandatory and should be a string.'), None
        elif not ACCOUNT_TRANSACTION and not (ticker in Tickers.US):
            # raise Exception(f'{ticker} is not available.')
            return print(f'{ticker} is not available.'), None

        if not isinstance(order, str):
            # raise TypeError('Order is mandatory and should be a string.')
            return print('Order is mandatory and should be a string.'), None
        elif not (order in ORDERS):
            # raise Exception(f'{order} is not a valid order. Valid orders are {ORDERS}')
            return print(f'{order} is not a valid order. Valid orders are {ORDERS}'), None

        if not isinstance(price, (int, float)):
            # raise TypeError('Price is mandatory and should be a number.')
            return print('Price is mandatory and should be a number.'), None

        if not isinstance(quantity, (int, float)):
            # raise TypeError('Quantity is mandatory and should be a number.')
            return print('Quantity is mandatory and should be a number.'), None

        if not isinstance(fee, (int, float)):
            # raise TypeError('Fee should be a number.')
            return print('Fee should be a number.'), None

        TRANSACTION = {
            'Date' : date,
            'Ticker' : ticker,
            'Order' : order,
            'Price' : price,
            'Quantity' : quantity,
            'Fee' : fee
        }

        return True, TRANSACTION

    def add(self, date, ticker, order, price, quantity, fee):

        check, TRANSACTION = self.validate(date, ticker, order, price, quantity, fee)

        if check:
            self.data = self.data.append(TRANSACTION, ignore_index=True)
        else:
            check

    def add_from_csv(self, csv):

        csv = pd.read_csv(csv)

        for i, row in csv.iterrows():
            self.add(row.Date, row.Ticker, row.Order, row.Price, row.Quantity, row.Fee)

    def delete(self, index):
        self.data = self.data.drop([index]).reset_index(drop=True)

    def download(self):
        b64 = base64.b64encode(self.data.to_csv(index=False).encode()).decode()
        return f'<a href="data:file/txt;base64,{b64}" download="Portfolio.csv">Download as CSV</a>'
