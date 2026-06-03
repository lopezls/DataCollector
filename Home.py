import streamlit as st
import csv
import os
from datetime import datetime


st.set_page_config(page_title="Data Collector", page_icon="💊", layout= "wide")
st.title("Data Collector | 🔍")

col1, col2, col3 = st.columns([0.5, 0.5, 0.5])
with col1:
    if st.button("Home"):
        st.switch_page("Hom.py")
with col2:
    if st.button("Project Information"):
        st.switch_page("pages/info.py")
with col3:
    if st.button("Extra"):
        st.switch_page("pages/extra.py")
st.divider()



