import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from drug_data import DRUG_CATALOG

st.set_page_config(page_title="Drug Catalog", page_icon="💊", layout="wide")

st.title("💊 Drug Catalog")

with st.expander("ℹ️ About this catalog"):
    st.markdown("""
    This catalog lists specialty medications tracked within this platform along with 
    their therapeutic categories. Categories are automatically assigned to every 
    encounter entry at the time of submission based on this catalog.
    """)

st.divider()

# ---- build dataframe ----
df = pd.DataFrame(list(DRUG_CATALOG.items()), columns=["Drug Name", "Category"])
df = df.sort_values("Category").reset_index(drop=True)

# ---- summary metrics ----
col1, col2 = st.columns(2)
with col1:
    st.metric("Total Drugs in Catalog", len(df))
with col2:
    st.metric("Therapeutic Categories", df["Category"].nunique())

st.divider()

# ---- filter by category ----
categories = ["All"] + sorted(df["Category"].unique().tolist())
selected_category = st.selectbox("Filter by therapeutic category", categories)

if selected_category != "All":
    filtered_df = df[df["Category"] == selected_category]
else:
    filtered_df = df

st.subheader(f"Showing {len(filtered_df)} medications")
st.dataframe(filtered_df, use_container_width=True, hide_index=True)