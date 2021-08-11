from numpy import add
import streamlit as st
import pandas as pd
import datetime
import base64
from logic import Portfolio


class Table():

    def new(self):
        COLS = ['Date','Ticker', 'Order', 'Price', 'Quantity', 'Fee']
        self.data = pd.DataFrame(columns=COLS)

    def __init__(self):
        self.new()

    def add(self, rows):
        self.data = self.data.append(rows, ignore_index=True)

    def delete(self, index):
        self.data = self.data.drop([index]).reset_index(drop=True)

    def download(self):
        b64 = base64.b64encode(self.data.to_csv(index=False).encode()).decode()
        return f'<a href="data:file/txt;base64,{b64}" download="Portfolio.csv">Download as CSV</a>'

    

if 'table' not in st.session_state:
    st.session_state.table = Table()

# VARIABLES (updated on every session)

LEN = len(st.session_state.table.data)
EMPTY = (True if LEN == 0 else False)

# PAGE SETUP

st.title('Welcome to iPortfolio')

with st.expander('Upload transactions'):

    uploaded_file = st.file_uploader('', type=['.csv'])
    if uploaded_file != None:
        df = pd.read_csv(uploaded_file)
        st.button('Load', on_click=st.session_state.table.add, args=(df,))


with st.expander('Add manually'):

    col11, col12= st.columns([2,3])
    col21, col22= st.columns(2)
    col31, col32, col33= st.columns([3,3,2])

    with col11:
        transaction_date = st.date_input('Transaction Date')
    with col12:
        transaction_type = st.selectbox('Transaction type', ['Account','Security'])
        SECURITY = (True if transaction_type == 'Security' else False)
        
    if SECURITY:
        with col21:
            transaction_ticker = st.text_input('Ticker')
        with col22:
            transaction_price = st.number_input('Price', 0.0, None, 0.0, 10.0)
        with col31:
            transaction_order = st.selectbox('Order', ['purchase', 'sale'])
    
    else:
        transaction_ticker = 'CASH.USD' # account currency
        transaction_price = 1
        with col31:
            transaction_order = st.selectbox('Order', ['deposit', 'withdrawal'])

    with col32:
        transaction_quantity = st.number_input('Quantity', 0.0, None, 0.0, 10.0)
    with col33:
        transaction_fee = st.number_input('Fee', 0.0, None, 0.0, 10.0)

    st.button('Add', on_click=st.session_state.table.add, args=({
        'Date' : transaction_date,
        'Ticker' : transaction_ticker.upper(),
        'Order' : transaction_order,
        'Price' : transaction_price,
        'Quantity' : transaction_quantity,
        'Fee' : transaction_fee
    },))

if not EMPTY:

    with st.expander('Edit'):

        col41, col42= st.columns([1,2])

        with col41:
            st.button('Clear Table', on_click=st.session_state.table.new)

        if LEN > 1:
            with col42:
                index = st.slider('Select row number', 0, LEN-1,0,1)
                st.button('Delete row', on_click=st.session_state.table.delete, args=(index,))

    st.write(st.session_state.table.data)
    st.markdown(st.session_state.table.download(), unsafe_allow_html=True)

    def run_logic(df2):
        df = df2.copy()
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.set_index('Date').sort_index()
        st.session_state.portfolio = Portfolio(df, 'USD')
        st.session_state.portfolio.run()

    st.button('Run App', on_click=run_logic, args=(st.session_state.table.data,))

def plot(data):
    st.line_chart(data)

if 'portfolio' in st.session_state:
    st.button('Plot', on_click=plot, args=(st.session_state.portfolio.holdings,))