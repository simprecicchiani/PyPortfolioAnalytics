from datetime import date
from typing import get_args
import requests
import streamlit as st
import pandas as pd
from helpers import TOBAY

from app.models import OrderType, Transaction, Portfolio

ss = st.session_state

if not ss.get("portfolio"):
    ss.portfolio = Portfolio(transactions=[])
    ss.session = requests.Session()

if not ss.portfolio.transactions:
    st.warning("Please add a transaction first")
else:
    st.subheader("Transactions")
    st.dataframe(ss.portfolio.transactions)
    st.download_button(
        label="Download Transactions",
        data=pd.DataFrame(ss.portfolio.transactions).to_csv().encode("utf-8"),
        file_name="transactions.csv",
        mime="text/csv",
    )


TICKERS = ["AAPL", "MSFT"]

with st.expander("Add Transaction"):
    col_left, col_right = st.columns(2)
    new_transaction: Transaction = Transaction(
        date=col_left.date_input(
            label="Date",
            value=date(2020, 1, 1),
            max_value=TOBAY(),
        ),
        order=col_right.selectbox(label="Order", options=get_args(OrderType)),
        ticker=col_left.selectbox(label="Ticker", options=TICKERS),
        shares=col_right.number_input(
            label="Shares",
            min_value=0.0,
            step=10.0,
            format="%a",
        ),
        price=col_left.number_input(
            label="Price",
            step=10.0,
            format="%a",
        ),
    )

    st.button(
        label="Add Transaction",
        on_click=ss.portfolio.transactions.append,
        args=(new_transaction,),
    )


if ss.portfolio.transactions:
    with st.expander("Remove Transaction"):

        rm_transaction_i = st.selectbox(
            label="Transaction index", options=range(len(ss.portfolio.transactions))
        )
        st.button(
            label=f"Remove Transaction {rm_transaction_i}",
            on_click=ss.portfolio.transactions.pop,
            args=(rm_transaction_i,),
        )

if ss.portfolio.transactions:

    inv, nav, ret = ss.portfolio.process()

    # process portfolio
    history_df = pd.concat([nav, inv], axis=1)
    st.subheader("History")
    st.line_chart(history_df)
    st.download_button(
        label="Download History",
        data=history_df.to_csv().encode("utf-8"),
        file_name="portfolio_history.csv",
        mime="text/csv",
    )
    st.subheader("Performance")
    return_df = ret.to_frame()
    st.line_chart(return_df)
    st.download_button(
        label="Download Returns",
        data=return_df.to_csv().encode("utf-8"),
        file_name="portfolio_returns.csv",
        mime="text/csv",
    )
    st.subheader("Metrics")
    st.dataframe()
