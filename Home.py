"""

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



"""

import streamlit as st

st.set_page_config(
    page_title="Specialty Pharmacy Analytics",
    page_icon="💊",
    layout="wide"
)

# ---- header ----
st.title("💊 Specialty Pharmacy Clinical Documentation & Analytics Platform")
st.markdown("*Purpose-built for specialty pharmacy patient management program interactions*")
st.divider()

# ---- three column overview ----
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📋 Document")
    st.markdown("""
    Capture structured clinical encounter data including:
    - Drug counseling sessions
    - Clinical screenings (PHQ-2, PHQ-9, UCLA)
    - Adverse drug event reporting
    - Language of interaction
    """)

with col2:
    st.markdown("### 📊 Analyze")
    st.markdown("""
    Real-time analytics dashboard surfacing:
    - KPI metrics by month
    - Drug distribution trends
    - Survey completion rates
    - ADE tracking and severity
    """)

with col3:
    st.markdown("### 🎯 Impact")
    st.markdown("""
    Built to quantify clinical impact for:
    - Performance documentation
    - Audit readiness
    - Board certification evidence
    - Data-driven decision making
    """)

st.divider()

# ---- quick stats if data exists ----
import sqlite3
import os

db_path = "pharmacy_data.db"

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    total = conn.execute("SELECT COUNT(*) FROM entries").fetchone()[0]
    counseled = conn.execute("SELECT COUNT(*) FROM entries WHERE counseling = 'Yes'").fetchone()[0]
    ades = conn.execute("SELECT COUNT(*) FROM entries WHERE ades_reported = 'Yes'").fetchone()[0]
    conn.close()

    st.subheader("📈 Platform Summary")
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Total Encounters Logged", total)
    with m2:
        st.metric("Counseling Sessions", counseled)
    with m3:
        st.metric("ADEs Reported", ades)
else:
    st.info("No data yet — submit your first encounter using the Data Collection form in the sidebar.")

st.divider()

# ---- about section ----
st.markdown("### About This Project")
st.markdown("""
This platform was designed and built by a practicing Senior Specialty Consultative Pharmacist 
to address a gap in clinical metrics tracking within specialty pharmacy patient management programs. 
Every feature was informed by firsthand clinical workflow experience.

**Tech Stack:** Python · Streamlit · SQLite · Plotly  
**Documentation:** [GitHub Wiki](https://github.com/lopezls/DataCollector/wiki)  
**Source Code:** [GitHub Repository](https://github.com/lopezls/DataCollector)
""")