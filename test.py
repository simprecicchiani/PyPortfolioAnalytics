import streamlit as st
import pandas as pd

def basic_skeleton() -> tuple:
    """Prepare the basic UI for the app"""
    st.sidebar.title('User Inputs')
    beta_expander = st.sidebar.beta_expander("Upload csv")
    with beta_expander:
        user_file_path = st.sidebar.file_uploader(
            label='Random Data',
            type='csv'
        )
    return user_file_path

def get_filtered_dataframe(df):
    columns_list = df.columns
    with st.form(key='Selecting Columns'):
        columns_to_aggregate = st.multiselect(
            label='Select columns to summarize',
            options=columns_list
        )
        submit_button = st.form_submit_button(label='Submit')
    if submit_button:
        df1 = df[columns_to_aggregate]
        return df1

def main():
    """Central wrapper to control the UI"""
    # add title
    st.header('Streamlit Testing')

    # add high level site inputs
    user_file_path = basic_skeleton()
    if user_file_path:
        load = st.sidebar.checkbox(label='Load Data')

        if load:
            df = pd.read_csv(user_file_path)
            st.dataframe(df)
            clean_df = get_filtered_dataframe(df)

            if clean_df is not None:
                result = clean_df.describe()
                st.dataframe(result)

main()