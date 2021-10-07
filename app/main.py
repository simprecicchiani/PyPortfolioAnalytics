import streamlit as st
from helpers.portfolio import Portfolio

def dashboard(filename):
    portfolio = Portfolio(filename)
    portfolio.run()
    col11, col12 = st.columns(2)
    with col11:
        st.subheader('Portfolio Value (USD)')
        st.line_chart(portfolio.value)
        st.subheader('Portfolio vs SPY')
        st.line_chart(portfolio.benchmark('SPY'))

    with col12:
        st.subheader('Portfolio Holdings')
        st.line_chart(portfolio.holdings)
        st.subheader('Portfolio Cash Flow')
        st.bar_chart(portfolio.cash_flows)

st.set_page_config(layout="wide")
st.title('iPortfolio Dashboard')
uploaded_file = st.file_uploader('Upload your transactions', type='csv')

if uploaded_file is not None:
    dashboard(uploaded_file)

# st.button('Run App', on_click=dashboard, args=(uploaded_file,))