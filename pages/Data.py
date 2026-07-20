import sqlite3
import pandas as pd
import streamlit as st
import os

st.set_page_config(page_title="Raw Data", page_icon="📄", layout="wide")

st.title("📄 Raw Data")

with st.expander("About this dataset"):
    st.markdown("""
    Each row represents a single patient encounter submitted via the Data Collection form.
    Data includes medication name, therapeutic category, counseling status, survey completion,
    adverse drug event reporting, and language of interaction.
    """)

st.divider()

# ---- load data ----
db_path = "pharmacy_data.db"

if not os.path.exists(db_path):
    st.info("No data yet — submit your first encounter using the Data Collection form.")
else:
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM entries ORDER BY timestamp DESC", conn)
    conn.close()

    if df.empty:
        st.info("No entries found in the database yet.")
    else:
        # ---- summary row ----
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Entries", len(df))
        with col2:
            st.metric("Unique Drugs", df["drug_name"].nunique())
        with col3:
            st.metric("ADEs Reported", len(df[df["ades_reported"] == "Yes"]))

        st.divider()

        # ---- filters ----
        col_filter1, col_filter2 = st.columns(2)
        with col_filter1:
            drug_filter = st.multiselect(
                "Filter by drug",
                options=sorted(df["drug_name"].unique()),
                default=[]
            )
        with col_filter2:
            category_filter = st.multiselect(
                "Filter by category",
                options=sorted(df["category"].unique()),
                default=[]
            )

        # apply filters
        filtered_df = df.copy()
        if drug_filter:
            filtered_df = filtered_df[filtered_df["drug_name"].isin(drug_filter)]
        if category_filter:
            filtered_df = filtered_df[filtered_df["category"].isin(category_filter)]

        st.subheader(f"Showing {len(filtered_df)} of {len(df)} entries")
        st.dataframe(filtered_df, use_container_width=True)

        st.divider()

        # ---- download ----
        st.download_button(
            label="⬇️ Download as CSV",
            data=filtered_df.to_csv(index=False),
            file_name="pharmacy_encounters.csv",
            mime="text/csv",
            use_container_width=True
        )