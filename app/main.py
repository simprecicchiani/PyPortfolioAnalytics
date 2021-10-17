import streamlit as st
from helpers.portfolio import Portfolio

def dashboard():
    col1, col2, col3, col4 = st.columns(4)

    col1.metric('Portfolio Value',f"${round(st.portfolio.value[-1],2)}", f"${round(st.portfolio.pl[-1],2)}")

    col2.metric("Daily Change",f"${round(st.portfolio.daily_change[-1],2)}", f"{round(st.portfolio.daily_ret[-1]*100,2)}%")

    col3.metric("Annual Volatility _expected return", f"{round(st.portfolio.std*100, 2)}%", f"{round(st.portfolio.exp_ret,2)*100}%")

    col4.metric("Sharpe _sortino Raio", f"{round(st.portfolio.sharpe, 2)}", f"{round(st.portfolio.sortino, 2)}")

    col11, col12 = st.columns(2)

    with col11:
        st.subheader('Portfolio Value')
        st.line_chart(st.portfolio.value)
        st.subheader('Portfolio vs SPY (% return)')
        st.line_chart(st.portfolio.benchmark('SPY')*100)

    with col12:
        st.subheader('Portfolio Holdings')
        st.line_chart(st.portfolio.holdings)
        st.subheader('Portfolio Cash Flows')
        st.bar_chart(st.portfolio.cash_flows)

st.set_page_config(layout="wide")
st.title('Python Portfolio Analytics Dashboard 💰')

with st.expander('Instructions'):
    '''
    ### Input file example

    | Date       | Ticker   | Order      | Price  | Quantity | Fee |
    |------------|----------|------------|--------|----------|-----|
    | 2019-10-01 | CASH.USD | deposit    | 1      | 100000   | 0   |
    | 2019-10-11 | AAPL     | purchase   | 234.52 | 88       | 35  |
    | 2019-11-25 | MSFT     | purchase   | 148.3  | 250      | 25  |
    | 2019-12-04 | AAPL     | sale       | 262.08 | 50       | 20  |
    | 2020-01-06 | FB       | purchase   | 208    | 100      | 10  |
    | 2020-01-25 | CASH.USD | withdrawal | 1      | 30000    | 0   |
    
    [Download example](https://github.com/simprecicchiani/PyPortfolioAnalytics/raw/master/assets/portfolios/generic.csv)
    
    ### Input file rules:

    - File format is `.csv`
    - Firs row contains these columns `Date`, `Ticker`, `Order`, `Price`, `Quantity`, `Fee`
    - Date format is `%Y-%m-%d`
    - Type of order are `deposit`, `withdrawal`, `purchase`, `sale`
    - Only supports [Yahoo Finance](https://finance.yahoo.com/) tickers

    ### Caveats

    - Works with single currency account only
    - Requires a deposit to calculate return on investment
    - Only accepts transactions within business days
    '''
uploaded_file = st.file_uploader('Upload your transactions', type='csv')

if uploaded_file is not None:
    st.portfolio = Portfolio(uploaded_file)
    st.portfolio.run()
    dashboard()
