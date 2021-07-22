import streamlit as st
import datetime
import pandas as pd

sec_order = ['purchase', 'sale', 'split']
cash_order = ['deposit', 'withdrawal', 'dividend', 'reinvestment']

st.write('Upload your transactions here')
st.file_uploader('', type=['.csv'])
st.write('or')
st.write('Add transactions manually')

if 'input_data' not in st.session_state:
    st.session_state.input_data = pd.DataFrame(columns=['ID', 'Date','Ticker', 'Order', 'Price', 'Quantity', 'Fee'])

def update_trans():
    trans = {
        'ID' : st.session_state.id,
        'Date' : st.session_state.date,
        'Ticker' : st.session_state.ticker.upper(),
        'Order' : st.session_state.order,
        'Price' : st.session_state.quantity,
        'Quantity' : st.session_state.price,
        'Fee' : st.session_state.fee}
    st.session_state.input_data = st.session_state.input_data.append(trans, ignore_index=True)

# with st.form(key='infos'):
col1, col2 = st.beta_columns(2)
with col1:
    asset = st.selectbox('Asset Type', ('Security', 'Cash'), key='asset_type')
with col2:
    st.date_input(label='Transaction Date', value=datetime.datetime.today(), key='date')
if asset == 'Cash':
    options = ('deposit', 'withdrawal')
    st.session_state.ticker = 'CASH$'
    st.session_state.price = 1
    st.session_state.fee = 0
    col1, col2 = st.beta_columns(2)
    with col1:
        st.selectbox('Order', options, key='order')
    with col2:
        st.number_input('Amount', step=1, key='quantity')
else:
    options = ('purchase', 'sale')
    col1, col2 = st.beta_columns(2)
    with col1:
        st.text_input('Ticker (Short Name)', key='ticker')
    with col2:
        st.selectbox('Transaction', options, key='order')
    col1, col2, col3 = st.beta_columns(3)
    with col1:
        st.number_input('Shares', step=1, key='quantity')
    with col2:
        st.number_input('Price', step=1, key='price')
    with col3:
        st.number_input('Fees (Optional)', step=1, key='fee')

submit = st.button(label='Insert', on_click=update_trans)

st.write(st.session_state.input_data)