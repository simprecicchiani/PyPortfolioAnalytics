import streamlit as st
from helpers.multiapp import MultiApp
from pages import transactions

app = MultiApp()

# Add all your application here
app.add_app("Home", transactions.app)

# The main app
app.run()