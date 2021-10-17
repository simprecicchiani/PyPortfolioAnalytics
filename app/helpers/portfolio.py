import pandas as pd
import numpy as np
import datetime
from .account import Account
from .security import Security


class Portfolio:
    
    def __init__(self, filename, currency='USD'):
        self.data = pd.read_csv(filename, sep=',', index_col='Date', parse_dates=True).sort_index()
        self.timeline = pd.date_range(start=self.data.index[0], end=datetime.date.today(), freq='B')
        self.currency = currency
        self.account = Account(self.currency, self.timeline)
        self.securities = dict() # dictionary with Security object at key='TICKER NAME'
        self._processed = False

    def run(self):
        if not self._processed:
            for date, transaction in self.data.iterrows():
                self.add_transaction(date, transaction)
            self.join_holdings()
            self.generate_stats()
        self._processed = True

    def add_transaction(self, date, transaction):
        # pick correct function without ifs
        getattr(self, transaction.Order)(date, transaction)
    
    def deposit(self, date, transaction):
        self.account.internal_flow(date, transaction.Quantity * transaction.Price - transaction.Fee)
        self.account.external_flow(date, transaction.Quantity * transaction.Price)

    def withdrawal(self, date, transaction):
        self.account.internal_flow(date, - transaction.Quantity * transaction.Price - transaction.Fee)
        self.account.external_flow(date, - transaction.Quantity * transaction.Price)
    
    def purchase(self, date, transaction):
        self.account.internal_flow(date,- transaction.Quantity * transaction.Price - transaction.Fee ) # / fx_rate
        tick = self.securities.setdefault(transaction.Ticker, Security(transaction.Ticker, self.timeline))
        tick.update(date, transaction.Quantity)

    def sale(self, date, transaction):
        self.account.internal_flow(date, transaction.Quantity * transaction.Price - transaction.Fee) # / fx_rate
        tick = self.securities.setdefault(transaction.Ticker, Security(transaction.Ticker, self.timeline))
        tick.update(date, - transaction.Quantity)

    def join_holdings(self):
        self.holdings = pd.DataFrame(index=self.timeline)
        for security in self.securities.values():
            security.run()
            self.account.internal_transactions = self.account.internal_transactions + security.holdings_dividend
            self.holdings = self.holdings.join(security.holdings_value.rename(security.name))
        self.account.run()
        self.holdings = self.holdings.join(self.account.holdings.rename(self.account.name))

    def generate_stats(self):
        self.value = self.holdings.sum(axis=1)
        self.daily_change = (self.value-self.account.external_transactions) - self.value.shift()
        self.daily_gross_ret = (self.value-self.account.external_transactions)/self.value.shift()
        self.daily_ret = self.daily_gross_ret - 1
        self.daily_log_ret = np.log(self.daily_gross_ret)
        self.std = self.daily_log_ret.std() * np.sqrt(252)
        self.exp_ret = self.daily_log_ret.mean() * 252
        self.sharpe = self.exp_ret/self.std
        self.semistd = self.daily_log_ret[self.daily_log_ret < self.daily_log_ret.mean()].std() * np.sqrt(252)
        self.sortino = self.exp_ret/self.semistd
        self.daily_var_5 = np.sort(self.daily_log_ret)[int(0.05*self.daily_log_ret.size)]*self.value[-1]
        self.daily_var_1 = np.sort(self.daily_log_ret)[int(0.01*self.daily_log_ret.size)]*self.value[-1]
        self.pl = self.value - self.account.invested_capital
        self.pctpl = self.pl / self.account.invested_capital
        self.cash_flows = - self.account.external_transactions
        self.cash_flows.iloc[-1] = self.cash_flows.iloc[-1] + self.value.iloc[-1]
    
    def benchmark(self, ticker):
        bench = Security(ticker, self.timeline).prices
        return pd.concat({
            'Portfolio': self.pctpl,
            ticker: (bench/bench[0]-1),
        }, axis=1)
