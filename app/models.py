from collections import defaultdict
from typing import Iterable, Literal, NamedTuple
from datetime import date, datetime
import pandas as pd
import numpy as np
import yfinance as yf
import requests
import streamlit as st

from helpers import TOBAY, DatePeriod, to_bday_fwd, bdatetime

ss = st.session_state


OrderType = Literal["purchase", "sale"]
CurrencyId = Literal["USD", "EUR"]


class PortfolioMetrics(NamedTuple):
    NAV: float
    investment: float
    profit_loss: float
    profit_loss_pct: float
    annualized_return_pct: float
    annualized_volatility_pct: float
    sharpe_ratio: float
    max_drawdown_pct: float
    max_drawdown_date: datetime


class Transaction(NamedTuple):
    date: date
    order: OrderType
    ticker: str
    shares: float
    price: float

    @property
    def bdate(self) -> bdatetime:
        return to_bday_fwd(self.date)

    @property
    def is_future(self) -> bool:
        return self.bdate > TOBAY()

    @property
    def direction(self) -> Literal[1, -1]:
        match self.order:
            case "purchase":
                return 1
            case "sale":
                return -1
        raise ValueError(f"{self.order} is not a known order")

    @property
    def cost(self) -> float:
        return self.direction * self.price * self.shares

    @property
    def quantity(self) -> float:
        return self.direction * self.shares


class Portfolio(NamedTuple):
    transactions: list[Transaction]

    @property
    def empty(self) -> bool:
        return not self.transactions

    @property
    def start_date(self) -> bdatetime:
        return min(
            transaction.bdate
            for transaction in self.transactions
            if not transaction.is_future
        )

    def process(self):

        date_period: DatePeriod = DatePeriod(self.start_date, TOBAY())

        investment_movements_dict: dict[bdatetime, float] = defaultdict(float)
        assets_movements_dict: dict[str, dict[datetime, float]] = defaultdict(
            lambda: defaultdict(float)
        )
        investment_movements_dict[date_period.start] = 0.0
        investment_movements_dict[date_period.end] = 0.0

        for transaction in self.transactions:
            if transaction.is_future:
                continue
            investment_movements_dict[transaction.bdate] += transaction.cost
            assets_movements_dict[transaction.ticker][
                transaction.bdate
            ] += transaction.quantity

        investment_movements_series = (
            pd.Series(investment_movements_dict, name="Investment")
            .asfreq("B")
            .fillna(0.0)
        )
        assets_movements_df = pd.DataFrame(
            assets_movements_dict, index=investment_movements_series.index
        ).fillna(0.0)

        investment_series = investment_movements_series.cumsum()

        assets_price_df, assets_dividend_df, assets_split_df = get_securities_data(
            tickers=assets_movements_dict.keys(),
            date_period=date_period,
        )

        assets_holding_df = (assets_movements_df * assets_split_df).cumsum()

        assets_values_df = assets_holding_df * assets_price_df
        nav_series = assets_values_df.sum(axis=1).rename("NAV")

        deposits = pd.Series(
            investment_movements_series.loc[investment_movements_series > 0],
            index=investment_movements_series.index,
            name="DEPOSIT",
        ).fillna(0.0)
        withdrawals = pd.Series(
            investment_movements_series.loc[investment_movements_series < 0],
            index=investment_movements_series.index,
            name="WITHDRAWAL",
        ).fillna(0.0)

        clean_returns = (
            (nav_series + withdrawals) / (nav_series.shift(1) + deposits) - 1
        ).replace([np.inf, -np.inf, np.nan, -1], 0.0)

        normalized_return_series = (clean_returns + 1).cumprod()

        return (
            investment_series.round(2),
            nav_series.round(2),
            normalized_return_series.round(2),
        )


def get_securities_data(
    tickers: Iterable[str],
    date_period: DatePeriod,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:

    securities_price_list = []
    securities_dividend_list = []
    securities_split_list = []

    for ticker in tickers:
        hist_df: pd.DataFrame = yf.Ticker(
            ticker=ticker, session=ss.get("session", requests.Session())
        ).history(interval="1d", start=date_period.start.strftime("%Y-%m-%d"))

        securities_price_list.append(hist_df["Close"].rename(ticker))
        if "Dividends" not in hist_df.columns:
            hist_df["Dividends"] = 0.0
        securities_dividend_list.append(hist_df["Dividends"].rename(ticker))
        if "Stock Splits" not in hist_df.columns:
            hist_df["Stock Splits"] = 0.0
        securities_split_list.append(hist_df["Stock Splits"].rename(ticker))

    date_index = pd.DatetimeIndex(
        pd.bdate_range(date_period.start, date_period.end), name="date"
    )

    return (
        pd.concat(securities_price_list, axis=1)
        .reindex(index=date_index)
        .fillna(method="ffill")
        .fillna(method="bfill")
        .fillna(1.0),  # for missing ticker
        pd.concat(securities_dividend_list, axis=1)
        .reindex(index=date_index)
        .fillna(0.0),
        pd.concat(securities_split_list, axis=1)
        .replace(0.0, 1.0)
        .iloc[::-1]
        .cumprod()
        .iloc[::-1]
        .reindex(index=date_index, method="nearest"),
    )
