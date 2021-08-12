import pandas as pd
from .alphavantage import ts


class Security:

    def __init__(self, name, timeline, api_key):
        self.name = name
        self.transactions = pd.Series(0, name=self.name, index=timeline)
        try:
            self.data = pd.read_csv('./data/'+self.name+'.csv', sep=',', index_col='date', parse_dates=True)
        except FileNotFoundError:
            self.data = ts(api_key).get_daily_adjusted(self.name, outputsize='full')[0].iloc[::-1]
            self.data.to_csv(r'./data/'+self.name+'.csv')
        self.data = self.data.reindex(index=timeline, method='nearest').fillna(method='ffill').loc[timeline[0]:timeline[-1]]
        self.prices = self.data['4. close']
        self.dividends = self.data['7. dividend amount']
        self.splits = self.data['8. split coefficient'].cumprod()
        # self.overview = fd.get_company_overview(symbol='MSFT')[0]
        # self.currency = self.overview['Currency']
        # self.sector = self.overview['Sector']

    def update(self, date, amount):
        self.transactions.at[date] = self.transactions.at[date] + amount

    def run(self):
        self.holdings = self.transactions.cumsum() * self.splits
        self.holdings_value_locale = self.holdings * self.prices
        self.holdings_value = self.holdings_value_locale.rename(self.name) # / fx_rate
