from posix import environ
import streamlit as st
import pandas as pd
from os import environ
from helpers.builder import Orders, Tickers, Table
from helpers.portfolio import Portfolio
from helpers.alphavantage import av

# PAGE SETUP

def app():

    if 'table' not in st.session_state:
        st.session_state.table = Table()

    # VARIABLES (updated on every session)

    LEN = len(st.session_state.table.data)
    EMPTY = (True if LEN == 0 else False)

    
    with st.expander('Options'):

        col01, col02 = st.columns(2)

        with col01:
            environ['ACCOUNT_CURRENCY'] = st.selectbox('Portfolio Currency', Tickers.CURRENCIES, index=144)
        with col02:
            environ['ALPHAVANTAGE_API_KEY'] = st.text_input('Alpha Vantage API')
            st.write('[Get a free api key](https://www.alphavantage.co/support/#api-key)')

    if environ.get('ALPHAVANTAGE_API_KEY') != '':
        with st.expander('Upload'):
        
            uploaded_file = st.file_uploader('', type=['.csv'])

            if uploaded_file != None:
                st.button('Load on memory', on_click=st.session_state.table.add_from_csv, args=(uploaded_file,))


        with st.expander('Add manually'):

            col11, col12 = st.columns([2,3])
            col21, col22 = st.columns(2)
            col31, col32, col33 = st.columns([3,3,2])

            with col11:
                transaction_date = st.date_input('Transaction Date')
            with col12:
                transaction_type = st.selectbox('Transaction type', ['Account','Security'])
                SECURITY = (True if transaction_type == 'Security' else False)
                
            if SECURITY:
                with col21:
                    transaction_ticker = st.selectbox('Ticker', Tickers.US)
                with col22:
                    transaction_price = st.number_input('Price', 0.0, None, 0.0, 10.0)
                with col31:
                    transaction_order = st.selectbox('Order', Orders.SECURITY)
            
            else:
                transaction_ticker = 'CASH.USD' # account currency
                transaction_price = 1
                with col31:
                    transaction_order = st.selectbox('Order', Orders.ACCOUNT)

            with col32:
                transaction_quantity = st.number_input('Quantity', 0.0, None, 0.0, 10.0)
            with col33:
                transaction_fee = st.number_input('Fee', 0.0, None, 0.0, 10.0)

            st.button('Add', on_click=st.session_state.table.add, args=(
                transaction_date,
                transaction_ticker,
                transaction_order,
                transaction_price,
                transaction_quantity,
                transaction_fee
            ,))


        if not EMPTY:

            with st.expander('Edit'):

                col41, col42= st.columns([1,2])

                with col41:
                    st.button('Clear Table', on_click=st.session_state.table.new)

                if LEN > 1:
                    with col42:
                        index = st.slider('Select row number', 0, LEN-1,0,1)
                        st.button('Delete row', on_click=st.session_state.table.delete, args=(index,))

            st.subheader('')
            st.write(st.session_state.table.data)
            st.markdown(st.session_state.table.download(), unsafe_allow_html=True)

            def run_logic(df):
                df = df.set_index('Date').sort_index()
                st.session_state.portfolio = Portfolio(df)
                st.session_state.portfolio.run()

            st.button('Run App', on_click=run_logic, args=(st.session_state.table.data,))