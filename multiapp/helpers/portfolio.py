import datetime
import pandas as pd
from numpy import log
from pyxirr import xirr
from .account import Account
from .security import Security
from .alphavantage import av


class Portfolio:
    
    def __init__(self, data):
        self.data = data.sort_index()
        self.timeline = pd.date_range(start=self.data.index[0], end=datetime.date.today())
        self.account = Account(self.timeline)
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
        self.daily_gross_ret = self.value/self.value.shift(periods=1)
        self.daily_ret = self.daily_gross_ret - 1
        self.daily_log_ret = log(self.daily_gross_ret)
        self.semistd = self.daily_ret[self.daily_ret < self.daily_ret.mean()].std()
        self.pl = self.value - self.account.invested_capital
        self.pctpl = self.pl / self.account.invested_capital
        self.cash_flows = - self.account.external_transactions
        self.cash_flows.iloc[-1] = self.cash_flows.iloc[-1] + self.value.iloc[-1]
        self.xirr = xirr(self.cash_flows.index, self.cash_flows.values)
        self.cagr = (self.value[-1]/self.value[0])**(365/self.timeline.shape[0])-1 # meaningless with withdrawals    
    
    def benchmark(self, ticker):
        bench = Security(ticker, self.timeline).data['5. adjusted close']
        return pd.concat({
            'Portfolio': self.pctpl,
            ticker: (bench/bench[0]-1),
        }, axis=1)
