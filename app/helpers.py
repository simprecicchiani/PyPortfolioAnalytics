from typing import NamedTuple, NewType
import pandas as pd
from datetime import date, datetime


bdatetime = NewType("bdatetime", datetime)


class DatePeriod(NamedTuple):
    start: bdatetime
    end: bdatetime


def TOBAY() -> bdatetime:
    return to_bday_bwd(date.today())


def to_bday_fwd(date: date | datetime) -> bdatetime:
    date = datetime(date.year, date.month, date.day)
    return pd.tseries.offsets.BDay().rollforward(date)  # type: ignore


def to_bday_bwd(date: date | datetime) -> bdatetime:
    date = datetime(date.year, date.month, date.day)
    return pd.tseries.offsets.BDay().rollback(date)  # type: ignore
