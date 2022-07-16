from datetime import date, datetime
from itertools import cycle
from typing import get_args
import requests
import streamlit as st
import pandas as pd
from metrics import get_portfolio_metrics
from helpers import load_tickers, TOBAY


from models import OrderType, Transaction, Portfolio

st.set_page_config(page_title="Python Portfolio Analytics", layout="wide")

st.title("Python Portfolio Analytics")

ss = st.session_state

if not ss.get("portfolio"):
    ss.portfolio = Portfolio(transactions=[])
    ss.session = requests.Session()


def add_transactions_from_file():
    if not ss.uploaded_file:
        return
    try:
        transactions_df = pd.read_csv(ss.uploaded_file)
        transactions_df.date = pd.to_datetime(transactions_df.date)
        ss.portfolio.transactions.extend(
            Transaction(**t) for t in transactions_df.to_dict("records")
        )
    except Exception:
        st.error("Error reading file. Please check the format.")


TICKERS = load_tickers("assets/yahoo_securities.json")

with st.expander("Add Transaction"):
    col_left, col_right = st.columns(2)
    new_transaction: Transaction = Transaction(
        date=col_left.date_input(
            label="Date",
            value=date(2020, 1, 1),
            max_value=TOBAY(),
        ),
        order=col_right.selectbox(label="Order", options=get_args(OrderType)),
        ticker=col_left.selectbox(
            label="Asset",
            options=TICKERS,
            format_func=lambda x: " | ".join(y for y in (x["ticker"], x["name"]) if y),
        )["ticker"],
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

    st.file_uploader(
        label="Add Transactions from file",
        type=["csv"],
        accept_multiple_files=False,
        key="uploaded_file",
        on_change=add_transactions_from_file,
    )


if ss.portfolio.transactions:
    with st.expander("Remove Transaction"):

        rm_transaction_i = st.selectbox(
            label="",
            options=[
                (idx, t._asdict()) for idx, t in enumerate(ss.portfolio.transactions)
            ],
            format_func=lambda x: " | ".join(str(y) for y in x[1].values()),
        )[0]
        st.button(
            label=f"Remove Transaction",
            on_click=ss.portfolio.transactions.pop,
            args=(rm_transaction_i,),
        )

    st.subheader("Transactions")
    st.table(ss.portfolio.transactions)
    st.download_button(
        label="Download Transactions",
        data=pd.DataFrame(ss.portfolio.transactions)
        .to_csv(index=False)
        .encode("utf-8"),
        file_name="transactions.csv",
        mime="text/csv",
    )

    # process portfolio
    inv, nav, ret = ss.portfolio.process()

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
    metrics = get_portfolio_metrics(nav, inv, ret)
    for (field, value), col in zip(metrics._asdict().items(), cycle(st.columns(3))):
        col.metric(
            label=field.replace("_", " ").replace("pct", "(%)").title(),
            value=value.strftime("%-d %b. %Y")
            if isinstance(value, datetime)
            else value,
        )

else:
    st.warning("Please add a transaction first")
