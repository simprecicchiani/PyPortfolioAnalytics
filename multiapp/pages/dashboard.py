import streamlit as st
import altair as alt

def app():
    if 'portfolio' in st.session_state:
        portfolio = st.session_state.portfolio
        st.title('iPortfolio Dashboard')
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
            
    else:
        st.write('Import your transactions first')