# iPortfolio

[![status](https://img.shields.io/badge/Status-Alpha-yellow)](/)

The app, despite its early stage, is working properly. You may encounter, however, issues where datasets are incomplete or wrong (from both yfinance and alpha vantage).

Testing with Anaconda:
```
$ git clone https://github.com/simprecicchiani/iPortfolio.git
$ cd iPortfolio
$ conda env create -f environment.yml
$ conda activate iportfolio
```

Test it with either `logic-yf.ipynb` (uses yahoo finance, slower) or `logic-av.ipynb` (requires [free Alpha Vantage API key](https://www.alphavantage.co/support/#api-key)). Run the web app with
```
$ streamlit run app.py
```

## The idea

Building a proper portfolio tracker. Featuring historical allocation, cash flows, real returns and more.

## The UX

`[In]` Transactions
| Date       | Ticker   | Order      | Price  | Quantity | Fee |
|------------|----------|------------|--------|----------|-----|
| 2019-10-01 | CASH.USD | deposit    | 1      | 100000   | 0   |
| 2019-10-12 | AAPL     | purchase   | 234.52 | 88       | 35  |
| 2019-11-24 | MSFT     | purchase   | 148.3  | 250      | 25  |
| 2019-12-04 | AAPL     | sale       | 267.76 | 50       | 20  |
| 2020-01-06 | FB       | purchase   | 208    | 100      | 10  |
| 2020-01-25 | CASH.USD | withdrawal | 1      | 30000    | 0   |

`[Out]` Portfolio stats
![](/samples/performance-sample.png)

## The UI

[Streamlit](https://streamlit.io) web app

## Built with

Python 3 and additional packages (leveraging pandas date index feature)

## To Do

- [x] Migration to Alpha Vantage
- [ ] Handle currencies (done in yf)
- [ ] Data validation, hedge cases
- [x] Leverage Python OOP
- [ ] UI

## Further development

- Portfolio Technicals
- Lots of charts
- Indicators (Sharpe Ratio, Beta, VaR, etc)
- Sector Exposure (stocks only)