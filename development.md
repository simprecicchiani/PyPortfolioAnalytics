### reference data sample

Let's call every row: *transaction*

| date       | symbol | position | unit_price | quantity | fee |
|------------|--------|----------|------------|----------|-----|
| 2019-12-04 | AAPL   | short    | 112.07     | 200      | 20  |
| 2019-11-24 | MSFT   | long     | 213.37     | 250      | 25  |
| 2019-10-12 | AAPL   | long     | 124.00     | 350      | 35  |

### conceptual steps

1. create a "timeline" starting from first transaction until today (likely the index of a pandas dataframe)
1. add a column for every security (symbol) bought or sold
1. assign and update the quantity of each security at a given time *t*:

    | date       | AAPL_units | MSFT_units |
    |------------|------------|------------|
    | today      | 150        | 250        |
    | ...        | 150        | 250        |
    | 2019-12-04 | 150        | 250        |
    | ...        | 350        | 250        |
    | 2019-11-24 | 350        | 250        |
    | ...        | 350        |            |
    | 2019-10-12 | 350        |            |

1. portfolio_cost in *t* will be: summation of transaction_unit * transaction_price + fee

    | date       | portfolio_cost |
    |------------|----------------|
    | today      | 74408.5        |
    | ...        | 74408.5        |
    | 2019-12-04 | 74408.5        |
    | ...        | 96802.5        |
    | 2019-11-24 | 96802.5        |
    | ...        | 43435          |
    | 2019-10-12 | 43435          |

1. download securities adj-close with yfinance

    | date     | aapl_adj | msft_adj |
    |----------|----------|----------|
    | 25/03/20 | 120.59   | 232.34   |
    | ...      | ...      | ...      |
    | 04/12/19 | 122.07   | 213.87   |
    | ...      | ...      | ...      |
    | 24/11/19 | 115      | 213.37   |
    | ...      | ...      | ...      |
    | 12/10/19 | 124      | 220.31   |

1. portfolio_value in *t* will be: summation of security_units * security_price_t

    | date     | portfolio_value |
    |----------|-----------------|
    | 25/03/20 | 76173.5         |
    | ...      | ...             |
    | 04/12/19 | 71778           |
    | ...      | ...             |
    | 24/11/19 | 93592.5         |
    | ...      | ...             |
    | 12/10/19 | 43400           |

1. portfolio_pl (P\L) in *t* will be: portfolio_value - portfolio_cost

    | date     | portfolio_pl |
    |----------|--------------|
    | 25/03/20 | 1765         |
    | ...      | ...          |
    | 04/12/19 | -2630.5      |
    | ...      | ...          |
    | 24/11/19 | -3210        |
    | ...      | ...          |
    | 12/10/19 | -35          |

1. portfolio_return in *t* will be: log(portfolio_value_t/portfolio_value_t-1)
1. TBC...

### notes 

- implement columns header and sub-headers
- fill empty cells with interpolation
- deal with *short* notation (opposite sign for quantity)