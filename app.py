from numpy import add
import streamlit as st
import pandas as pd
import datetime
import base64
from logic import Portfolio

# FUNCTIONS

def init_table():

    st.session_state.input_data = pd.DataFrame(columns=['Date','Ticker', 'Order', 'Price', 'Quantity', 'Fee'])

def add_transaction():
    transaction = {
        'Date' : st.session_state.transaction_date,
        'Ticker' : st.session_state.transaction_ticker.upper(),
        'Order' : st.session_state.transaction_order,
        'Price' : st.session_state.transaction_price,
        'Quantity' : st.session_state.transaction_quantity,
        'Fee' : st.session_state.transaction_fee
    }
    st.session_state.input_data = st.session_state.input_data.append(transaction, ignore_index=True)

def delete_transaction():

    st.session_state.input_data = st.session_state.input_data.drop([st.session_state.del_index]).reset_index(drop=True)

def download_link(object_to_download, download_filename, download_link_text):

    b64 = base64.b64encode(object_to_download.to_csv(index=False).encode()).decode()

    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

def load_data():

    df = pd.read_csv(st.session_state.loaded_data)
    st.session_state.input_data = st.session_state.input_data.append(df, ignore_index=True)

if 'input_data' not in st.session_state:

    init_table()

# VARIABLES (updated on every session)

LEN = len(st.session_state.input_data)
EMPTY = (True if LEN == 0 else False)

# PAGE SETUP

st.title('Welcome to iPortfolio')

with st.expander('Upload transactions'):

    st.file_uploader('', type=['.csv'], key='loaded_data', on_change=load_data)

with st.expander('Add manually'):

    col11, col12= st.columns([2,3])
    col21, col22= st.columns(2)
    col31, col32, col33= st.columns([3,3,2])
    st.button('Add', on_click=add_transaction)

if not EMPTY:

    with st.expander('Edit'):

        col41, col42= st.columns([1,3])

    st.write(st.session_state.input_data)
    st.markdown(download_link(st.session_state.input_data, 'Portfolio.csv', 'Download as CSV'), unsafe_allow_html=True)

# LAYOUT ELEMENTS

with col11:

    st.date_input('Transaction Date', key='transaction_date')

with col12:

    st.selectbox('Transaction type', ['account','security'], key='transaction_type')


if st.session_state.transaction_type == 'security':

    with col21:

        st.text_input('Ticker', key='transaction_ticker')

    with col22:

        st.number_input('Price',min_value=0.0, step=10.0, key='transaction_price')
        
    with col31:

        st.selectbox('Order', ['purchase', 'sale'], key='transaction_order')
else:

    st.session_state.transaction_ticker = 'CASH.USD' # account currency
    st.session_state.transaction_price = 1

    with col31:

        st.selectbox('Order', ['deposit', 'withdrawal'], key='transaction_order')

with col32:

    st.number_input('Quantity',min_value=0.0, step=10.0, key='transaction_quantity')

with col33:

    st.number_input('Fee',min_value=0.0, step=10.0, key='transaction_fee')


if not EMPTY:

    with col41:

        st.button('Clear Table', on_click=init_table)

    if LEN > 1:

        with col42:

            with st.form('del_trans', True):

                st.slider('Select row number', min_value=0, max_value=LEN-1, key='del_index')
                st.form_submit_button('Delete', on_click=delete_transaction)

def load(df2):
    df = df2.copy()
    df['Date'] = pd.to_datetime(df['Date'])
    st.session_state.portfolio = Portfolio(df.set_index(['Date']), 'USD')

st.button('Load', on_click=load(st.session_state.input_data))