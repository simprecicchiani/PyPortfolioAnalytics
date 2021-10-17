import pandas as pd
import pandas_datareader as pdr


class Security:

    def __init__(self, name, timeline):
        self.name = name
        self.transactions = pd.Series(0, name=self.name, index=timeline)
        self.timeline = timeline
        self.get_data()

    def get_data(self):
        df = pdr.yahoo.daily.YahooDailyReader(
        symbols=self.name,
        start=self.timeline[0],
        end=None,
        retry_count=3,
        pause=0.1,
        session=None,
        adjust_price=False,
        ret_index=False,
        chunksize=25,
        interval='d',
        get_actions=True,
        adjust_dividends=False).read()
        split_adj_prices = df['Close'].reindex(index=self.timeline, method='nearest')
        if 'Dividends' in df.columns:
            self.dividends = df['Dividends'].reindex(index=self.timeline, fill_value=0).fillna(0)
        else:
            self.dividends = pd.Series(0, index=self.timeline)
        if 'Splits' in df.columns:
            split_coeff = df['Splits'].reindex(index=self.timeline, fill_value=1).fillna(1)
        else:
            split_coeff = pd.Series(1, index=self.timeline)

        self.prices = split_adj_prices / split_coeff.loc[::-1].cumprod()[::-1].shift(periods=-1, fill_value=1)
        self.splits = 1/split_coeff.cumprod()

    def update(self, date, amount):
        self.transactions.at[date] = self.transactions.at[date] + amount

    def run(self):
        self.holdings = self.transactions.cumsum() * self.splits
        self.holdings_value_locale = self.holdings * self.prices
        self.holdings_value = self.holdings_value_locale # / fx_rate
        self.holdings_dividend_locale = self.holdings * self.dividends
        self.holdings_dividend = self.holdings_dividend_locale # / fx_rate