# iPortfolio

[![status](https://img.shields.io/badge/Status-Alpha-yellow)](/)

## The idea

Building a proper portfolio tracker. Featuring historical allocation, cash flows, **real** returns and more.

## The UX

- **Input**: User's transactions of securities in form of a tabulated file (e.g. CSV);
- **Output**: A graph showing portfolio performance (P/L) against a given benchmark (e.g. SPY).

`[In]`
| date       | symbol | position | unit_price | quantity | fee |
|------------|--------|----------|------------|----------|-----|
| 2019-12-04 | AAPL   | short    | 112.07     | 200      | 20  |
| 2019-11-24 | MSFT   | long     | 213.37     | 250      | 25  |
| 2019-10-12 | AAPL   | long     | 124.00     | 350      | 35  |

`[Out]`
![](/samples/performance-sample.png)

## The UI

Interactive web page with [Streamlit](https://streamlit.io).

## Under the Hood

Python 3 with additional packages (mainly pandas).

## To Do

- [x] Migration to Alpha Vantage
- [ ] Handle currencies
- [ ] Data validation, hedge cases
- [x] Leverage Python OOP
- [ ] UI

## Further development

- Portfolio Technicals
- Lots of charts
- Indicators (Sharpe Ratio, Beta, VaR, etc)
- Sector Exposure (stock only)