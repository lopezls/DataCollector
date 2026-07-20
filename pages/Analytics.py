import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(page_title="Analytics", page_icon="📈", layout="wide")
st.title("📈 Analytics Dashboard")

# ---- database connection ----
def get_connection():
    conn = sqlite3.connect("pharmacy_data.db")
    return conn

# ---- query functions ----
def get_counseling_count_this_month():
    conn = get_connection()
    result = conn.execute("""
        SELECT COUNT(*)
        FROM entries
        WHERE counseling = 'Yes'
        AND strftime('%Y-%m', timestamp) = strftime('%Y-%m', 'now')
    """).fetchone()
    conn.close()
    return result[0]

def get_counseling_count_last_month():
    conn = get_connection()
    result = conn.execute("""
        SELECT COUNT(*)
        FROM entries
        WHERE counseling = 'Yes'
        AND strftime('%Y-%m', timestamp) = strftime('%Y-%m', datetime('now', '-1 month'))
    """).fetchone()
    conn.close()
    return result[0]

def get_depression_count():
    conn = get_connection()
    result = conn.execute("""
        SELECT COUNT(*)
        FROM entries
        WHERE depression_survey = 'Yes'
        AND strftime('%Y-%m', timestamp) = strftime('%Y-%m', 'now')
    """).fetchone()
    conn.close()
    return result[0]

def get_ade_count():
    conn = get_connection()
    result = conn.execute("""
        SELECT COUNT(*)
        FROM entries
        WHERE ades_reported = 'Yes'
        AND strftime('%Y-%m', timestamp) = strftime('%Y-%m', 'now')
    """).fetchone()
    conn.close()
    return result[0]

def get_adherence_count():
    conn = get_connection()
    result = conn.execute("""
        SELECT COUNT(*)
        FROM entries
        WHERE adherence_survey = 'Yes'
        AND strftime('%Y-%m', timestamp) = strftime('%Y-%m', 'now')
    """).fetchone()
    conn.close()
    return result[0]

# ---- load full dataframe ----
conn = get_connection()
df = pd.read_sql_query("SELECT * FROM entries", conn)
conn.close()

# ---- KPI metrics ----
this_month = get_counseling_count_this_month()
last_month = get_counseling_count_last_month()
delta = this_month - last_month

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Counseling Sessions",
        value=this_month,
        delta=f"{delta} vs last month"
    )
with col2:
    st.metric(
        label="Depression Screenings",
        value=get_depression_count()
    )
with col3:
    st.metric(
        label="ADEs Reported",
        value=get_ade_count()
    )
with col4:
    st.metric(
        label="Adherence Surveys",
        value=get_adherence_count()
    )

st.divider()

# ---- donut chart for drug distribution ----
st.subheader("Drug Distribution")

if df.empty:
    st.info("No data yet — submit some entries to see the chart.")
else:
    drug_counts = df["drug_name"].value_counts().reset_index()
    drug_counts.columns = ["Drug", "Count"]

    fig = px.pie(
        drug_counts,
        values="Count",
        names="Drug",
        title="Drug Distribution",
        hole=0.4
    )
    fig.update_traces(
        textinfo="percent+label",
        pull=[0.1 if i == 0 else 0 for i in range(len(drug_counts))]
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Distribution of specialty medications counseled across all recorded patient sessions.")

#----donut chart for language distribution ----
st.subheader("Counseling Language Distribution")
if df.empty:
    st.info("No data yet — submit some entries to see the chart.")
else:
    language_counts = df["language"].value_counts().reset_index()
    language_counts.columns = ["Language", "Count"]

    fig2 = px.pie(
        language_counts,
        values="Count",
        names="Language",
        title="Counseling Language Distribution",
        hole=0.4
    )
    fig2.update_traces(
        textinfo="percent+label",
        pull=[0.1 if i == 0 else 0 for i in range(len(language_counts))]
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.caption("Distribution of languages used during counseling sessions across all recorded patient sessions.")