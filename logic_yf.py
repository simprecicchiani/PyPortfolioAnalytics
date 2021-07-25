import pandas as pd
import datetime
import pyxirr
import yfinance as yf

class Account:

    def __init__(self, currency, timeline):
        self.currency = currency
        self.name = 'CASH.' + self.currency
        self.internal_transactions = pd.Series(0, index=timeline)
        self.external_transactions = pd.Series(0, index=timeline)
    
    def internal_flow(self, date, amount):
        self.internal_transactions.at[date] = self.internal_transactions.at[date] + amount

    def external_flow(self, date, amount):
        self.external_transactions.at[date] = self.external_transactions.at[date] + amount

    def process_data(self):
        self.holdings = self.internal_transactions.cumsum()
        self.invested_capital = self.external_transactions.cumsum()


class Ticker:
    
    def __init__(self, name, timeline):
        self.name = name
        self.transactions = pd.Series(0, index=timeline)
        day = datetime.timedelta(days=1)
        self.data = yf.Ticker(self.name).history(start=timeline[0] + day, end=timeline[-1] + day).reindex(index=timeline)
        self.prices = self.data['Close'].fillna(method='ffill')
        self.dividends = self.data['Dividends'].fillna(0)
        self.splits = self.data['Stock Splits'].fillna(1).replace(0, 1).iloc[::-1].cumprod().iloc[::-1]

    def update(self, date, amount):
        self.transactions.at[date] = self.transactions.at[date] + amount

    def process_data(self):
        self.holdings = (self.transactions * self.splits).cumsum()
        self.holdings_value_locale = self.holdings * self.prices
        self.holdings_value = self.holdings_value_locale.rename(self.name) # / fx_rate


class Portfolio:

    def __init__(self, filename, currency):
        self.data = pd.read_csv(filename, sep=',', index_col='Date', parse_dates=True).sort_index()
        self.timeline = pd.date_range(start=self.data.index[0].date(), end=datetime.date.today())
        self.currency = currency
        self.account = Account(self.currency, self.timeline)
        self.tickers = dict() # dictionary with Ticker object at key='TICKER NAME'

    def process_data(self):
        for date, transaction in self.data.iterrows():
            self.add_transaction(date, transaction)
        self.dividend()
        self.account.process_data()
        self.join_holdings()
        self.generate_stats()

    def add_transaction(self, date, transaction):
        getattr(self, transaction.Order)(date, transaction)
    
    def deposit(self, date, transaction):
        self.account.internal_flow(date, transaction.Quantity * transaction.Price - transaction.Fee)
        self.account.external_flow(date, transaction.Quantity * transaction.Price)

    def withdrawal(self, date, transaction):
        self.account.internal_flow(date, - transaction.Quantity * transaction.Price - transaction.Fee)
        self.account.external_flow(date, - transaction.Quantity * transaction.Price)
    
    def purchase(self, date, transaction):
        self.account.internal_flow(date,- transaction.Quantity * transaction.Price - transaction.Fee ) # / fx_rate
        tick = self.tickers.setdefault(transaction.Ticker, Ticker(transaction.Ticker, self.timeline))
        tick.update(date, transaction.Quantity)

    def sale(self, date, transaction):
        self.account.internal_flow(date, transaction.Quantity * transaction.Price - transaction.Fee) # / fx_rate
        tick = self.tickers.setdefault(transaction.Ticker, Ticker(transaction.Ticker, self.timeline))
        tick.update(date, - transaction.Quantity)

    '''Not sure if this approach is better than record dividends as transactions'''
    def dividend(self):
        for ticker in self.tickers.values():
            ticker.process_data()
            self.account.internal_transactions = self.account.internal_transactions + ticker.dividends * ticker.holdings # / fx_rate

    def join_holdings(self):
        self.holdings = pd.DataFrame(self.account.holdings, columns=[self.account.name])
        for ticker in self.tickers.values():
            self.holdings = self.holdings.join(ticker.holdings_value)

    def generate_stats(self):
        self.value = self.holdings.sum(axis=1)
        self.pl = self.value - self.account.invested_capital
        self.pctpl = self.pl / self.account.invested_capital
        self.cash_flows = - self.account.external_transactions
        self.cash_flows.iloc[-1] = self.cash_flows.iloc[-1] + self.value.iloc[-1]
        self.xirr = pyxirr.xirr(self.cash_flows.index, self.cash_flows.values)
        self.xirr_ann = (1+self.xirr)**(365/len(self.timeline))-1

    def run_benchmark(self, ticker):
        day = datetime.timedelta(days=1)
        benchmark = yf.download(tickers = ticker, start=self.timeline[0] + day, end=self.timeline[-1] + day)['Adj Close'].reindex(index=self.timeline, method='ffill').fillna(method='ffill')
        benchmark = benchmark/benchmark[0]-1
        self.benchmark = pd.concat({
            'Portfolio': self.pctpl,
            ticker: benchmark,
        }, axis=1)