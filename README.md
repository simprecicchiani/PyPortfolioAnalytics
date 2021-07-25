# iPortfolio

[![status](https://img.shields.io/badge/Status-Alpha-yellow)](/)

## The idea

Building a proper portfolio tracker. Featuring historical allocation, cash flows, **real** returns and more.

## The UX

- **Input**: Transactions
- **Output**: Portfolio stats

`[In]`
| Date       | Ticker   | Order      | Price  | Quantity | Fee |
|------------|----------|------------|--------|----------|-----|
| 2019-10-01 | CASH.USD | deposit    | 1      | 100000   | 0   |
| 2019-10-12 | AAPL     | purchase   | 234.52 | 88       | 35  |
| 2019-11-24 | MSFT     | purchase   | 148.3  | 250      | 25  |
| 2019-12-04 | AAPL     | sale       | 267.76 | 50       | 20  |
| 2020-01-06 | FB       | purchase   | 208    | 100      | 10  |
| 2020-01-25 | CASH.USD | withdrawal | 1      | 30000    | 0   |

`[Out]`
![](/samples/performance-sample.png)

## The UI

Interactive web page with [Streamlit](https://streamlit.io)

## Under the Hood

Python 3 with additional packages (leveraging pandas date index feature)

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