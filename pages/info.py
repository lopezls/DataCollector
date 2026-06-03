import streamlit as st
st.set_page_config(page_title="Information Page", page_icon="📊", layout="wide")
st.title("Info Page")
with st.expander("Project Overview"):
    st.header("**Purpose:** Collect and analyze specialty medication data for insights on trends")
    st.subheader("**Data Collection:**")
    st.subheader("Data Sources: My own work")
st.subheader("Data Types: Specialty medication names, services provided, and ADEs reported")