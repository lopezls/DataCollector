import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import sqlite3
from datetime import datetime
from drug_data import DRUG_CATALOG


# ---- simple password protection ----
password = st.text_input("Enter password to access this form", type="password")

if password != "SweetPotato123!":
    st.warning("Please enter the correct password to access this form")
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
            timestamp, drug_name, category, counseling,
            depression_survey, adherence_survey,
            food_insecurity_survey, ades_reported, ades_details
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        entry["timestamp"],
        entry["drug_name"],
        entry["category"],
        entry["counseling"],
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

#-----Header-----
st.set_page_config(page_title="Data Collection", page_icon="📊", layout="wide")
with st.expander("About this Collection Form"):
    st.markdown("""   
    This form is used to document patient interaction sessions conducted by a clinical pharmacist.
    
    **This form collects:**
    - Drug name and auto-populated category
    - Whether counseling was provided
    - Whether depression, adherence, and food insecurity surveys were conducted
    - Whether any adverse drug events (ADEs) were reported, and details if so
    """)
# ---- form ----
with st.form("data_collection_form"):
    st.subheader("Data Collection Form")

    drug_name = st.selectbox("Select medication", list(DRUG_CATALOG.keys()))
    counseling = st.radio("Counseling given?", ("Yes", "No"))
    depression_survey = st.radio("Depression Survey given?", ("Yes", "No"))
    adherence_survey = st.radio("Adherence Survey given?", ("Yes", "No"))
    food_insecurity_survey = st.radio("Food Insecurity Survey given?", ("Yes", "No"))
    ades_reported = st.radio("ADEs reported?", ("Yes", "No"))

    ades_details = ""
    if ades_reported == "Yes":
        ades_details = st.text_input("Enter ADEs reported separated by '/'")

    submitted = st.form_submit_button("Submit")

    if submitted:
        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "drug_name": drug_name,
            "category": DRUG_CATALOG.get(drug_name, "Uncategorized"),
            "counseling": counseling,
            "depression_survey": depression_survey,
            "adherence_survey": adherence_survey,
            "food_insecurity_survey": food_insecurity_survey,
            "ades_reported": ades_reported,
            "ades_details": ades_details if ades_reported == "Yes" else None,
        }
        save_entry(entry)
        st.success(f"Data saved for {drug_name}!")
    else:
        st.info("Please fill out the form and submit to save data.")