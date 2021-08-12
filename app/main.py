import streamlit as st
from helpers.multiapp import MultiApp
from pages import transactions, dashboard, instructions

st.set_page_config(layout="wide")
environment = MultiApp()

# Add pages
environment.add_app('Instructions', instructions.app)
environment.add_app('Transaction builder', transactions.app)
environment.add_app('Portfolio dashboard', dashboard.app)

environment.run()