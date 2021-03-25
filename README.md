# iPortfolio

[![status](https://img.shields.io/badge/Status-I%20haven't%20even%20started-red)](/)

## The idea

Quickly visualize the performance of a portfolio of stocks, funds or whatever is quoted on financial markets (with accessible data e.g. Yahoo Finance).

## The UX

- **Input**: User's transactions of securities in form of a tabulated file (e.g. CSV);
- **Output**: A graph showing portfolio performance (P/L) against a given benchmark (e.g. SPY).

`[In]`
| date | symbol | position | unit_price | quantity | fee |
|------|--------|----------|------------|----------|-----|
| 2019-12-04 | AAPL | short | 112.07 | 200 | 20 |
| 2019-11-24 | MSFT | long | 213.37 | 250 | 25 |
| 2019-10-12 | AAPL | long | 124.00 | 350 | 35 |

`[Out]`
![](/resources/performance-sample.jpg)

## The UI

Interactive web page with [Streamlit](https://streamlit.io).

## Under the Hood

Python 3 with additional libraries (pandas, yfinance, numpy, datetime, pandas_market_calendars, etc.)

## Challenges

- [ ] Give the possibility to generate a transactions' data table
- [ ] Deal with inflows and outflows of liquidity
- [ ] Find a suitable name for this project

## Further development

- Portfolio stats (High-Low-Avg, Correlation, etc.)
- Additional graphical informations (SMAs, Forecasts, Montecarlo Analysis, etc.)
- Basic advices (Optimal Allocation)
- Risk exposure (VaR)
- Hedging strategies

## Inspired by

- [Matt Grierson's Modeling Your Stock Portfolio Performance with Python](https://towardsdatascience.com/modeling-your-stock-portfolio-performance-with-python-fbba4ef2ef11), [repo](https://github.com/mattygyo/stock_portfolio_analysis)
- [Kristina Chodorow's Blog](https://kchodorow.com/2020/08/06/show-me-the-money-tracking-returns/)
