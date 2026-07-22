import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import sqlite3
from datetime import datetime
from drug_data import DRUG_CATALOG

# ---- page config MUST be first ----
st.set_page_config(page_title="Data Collection", layout="wide")

# ---- simple password protection ----
password = st.text_input("Enter password to access this form", type="password")
if password != st.secrets["form_password"]:
    st.warning("Please enter the correct password to access this form.")
    st.stop()

# ---- database setup ----
def get_connection():
    conn = sqlite3.connect("pharmacy_data.db")
    return conn

def create_table():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS entries (
            id                     INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp              TEXT NOT NULL,
            drug_name              TEXT,
            category               TEXT,
            counseling             TEXT,
            language               TEXT,
            depression_survey      TEXT,
            adherence_survey       TEXT,
            food_insecurity_survey TEXT,
            ades_reported          TEXT,
            ades_details           TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_entry(entry):
    conn = get_connection()
    conn.execute("""
        INSERT INTO entries (
            timestamp, drug_name, category, counseling, language,
            depression_survey, adherence_survey,
            food_insecurity_survey, ades_reported, ades_details
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        entry["timestamp"],
        entry["drug_name"],
        entry["category"],
        entry["counseling"],
        entry["language"],
        entry["depression_survey"],
        entry["adherence_survey"],
        entry["food_insecurity_survey"],
        entry["ades_reported"],
        entry["ades_details"]
    ))
    conn.commit()
    conn.close()

# ---- runs once on startup ----
create_table()

# ---- header ----
st.title("📋 Clinical Encounter Data Collection")

with st.expander("About this Form"):
    st.markdown("""
    This form documents patient interaction sessions conducted during specialty pharmacy 
    patient management program calls.

    **This form collects:**
    - Medication name and auto-assigned therapeutic category
    - Whether counseling was provided and in which language
    - Completion status of depression, adherence, and food insecurity surveys
    - Adverse drug event reporting with free-text detail capture
    """)

st.divider()

# ---- form ----
with st.form("data_collection_form"):
    st.subheader("New Encounter Entry")

    drug_name = st.selectbox("Select medication", list(DRUG_CATALOG.keys()))
    counseling = st.radio("Counseling given?", ("Yes", "No"), horizontal=True)
    language = st.selectbox("Language of counseling", ("English", "Spanish", "Vietnamese", "Russian", "Lao", "Other"))
    depression_survey = st.radio("Depression Survey given?", ("Yes", "No"), horizontal=True)
    adherence_survey = st.radio("Adherence Survey given?", ("Yes", "No"), horizontal=True)
    food_insecurity_survey = st.radio("Food Insecurity Survey given?", ("Yes", "No"), horizontal=True)
    ades_reported = st.radio("ADEs reported?", ("Yes", "No"), horizontal=True)

    ades_details = ""
    if ades_reported == "Yes":
        ades_details = st.text_area("Describe the adverse event(s) — separate multiple with '/'")

    submitted = st.form_submit_button("Submit Encounter", use_container_width=True)

    if submitted:
        if not drug_name:
            st.warning("Please select a medication before submitting.")
        else:
            entry = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "drug_name": drug_name,
                "category": DRUG_CATALOG.get(drug_name, "Uncategorized"),
                "counseling": counseling,
                "language": language,
                "depression_survey": depression_survey,
                "adherence_survey": adherence_survey,
                "food_insecurity_survey": food_insecurity_survey,
                "ades_reported": ades_reported,
                "ades_details": ades_details if ades_reported == "Yes" else None,
            }
            save_entry(entry)
            st.success(f"✅ Encounter saved for {drug_name}!")