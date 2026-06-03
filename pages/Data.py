import sqlite3
import pandas as pd
import streamlit as st


st.set_page_config(page_title="Raw Data", page_icon="📊", layout="wide")

st.title("📊 Raw Data")
with st.expander("About this Dataset"):
    st.write("""
    This dataset was collected using the Data Collection Form in the Data Collector app. 
    Each row represents a single patient counseling session submitted by a clinical pharmacist. 
    Data collected includes drug information, counseling provided, adherence and depression 
    screening results, adverse drug event reporting, and follow up plans. This data is used 
    to track intervention rates, counseling volume, and patient outcomes across the pharmacy team.
    """)

conn = sqlite3.connect('pharmacy_data.db')
df = pd.read_sql_query("SELECT * FROM entries", conn)
conn.close()

st.subheader("Raw Data")
st.dataframe(df)