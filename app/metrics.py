import pandas as pd
import numpy as np
from models import PortfolioMetrics


def to_drawdown(assets_prices: pd.DataFrame | pd.Series) -> pd.DataFrame | pd.Series:
    dd = assets_prices / np.maximum.accumulate(assets_prices) - 1.0
    return dd.replace([np.inf, -np.inf, -0], 0)


def to_pct(n: float) -> float:
    return round(n * 100, 2)


def get_portfolio_metrics(
    nav_series: pd.Series, investment_series: pd.Series, gross_return_series: pd.Series
) -> PortfolioMetrics:

    daily_return_series = gross_return_series.pct_change()
    drawdown = to_drawdown(gross_return_series)

    last_nav = nav_series.iat[-1]
    last_investment = investment_series.iat[-1]
    net_pl = last_nav - last_investment
    pl = net_pl / last_investment if last_investment != 0 else 0
    ann_ret = ((1 + daily_return_series.mean()) ** 261) - 1
    ann_vol = daily_return_series.std() * (261**0.5)
    sharpe_ratio = (ann_ret - 0.0) / ann_vol if ann_vol != 0 else 0.0
    max_dd = drawdown.min()
    max_dd_date = drawdown.idxmin()

    return PortfolioMetrics(
        NAV=last_nav,
        investment=last_investment,
        profit_loss=net_pl,
        profit_loss_pct=to_pct(pl),
        annualized_return_pct=to_pct(ann_ret),
        annualized_volatility_pct=to_pct(ann_vol),
        sharpe_ratio=round(sharpe_ratio, 2),
        max_drawdown_pct=to_pct(max_dd),
        max_drawdown_date=max_dd_date.to_pydatetime(),
    )
