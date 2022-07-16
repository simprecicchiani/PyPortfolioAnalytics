# Python Portfolio Analytics

[![status](https://img.shields.io/badge/Status-Running-green)](https://share.streamlit.io/simprecicchiani/pyportfolioanalytics/app/main.py)

A simple portfolio tracker app developed in Python.

### Develop

Local development (python>=3.10):
```console
$ git clone https://github.com/simprecicchiani/PyPortfolioAnalytics.git
$ cd PyPortfolioAnalytics
$ pip install -r requirements.txt
$ streamlit run app/main.py
```

### Input example

| date       | ticker   | order      | price  | shares   |
|------------|----------|------------|--------|----------|
| 2019-10-11 | AAPL     | purchase   | 234.52 | 88       |
| 2019-11-25 | MSFT     | purchase   | 148.3  | 250      |
| 2019-12-04 | AAPL     | sale       | 262.08 | 50       |
| 2020-01-06 | FB       | purchase   | 208    | 100      |