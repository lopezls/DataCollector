import streamlit as st
import pandas as pd

st.set_page_config(page_title="Drug Catalog", page_icon="💊", layout="wide")

st.title("💊 Drug Catalog")
with st.expander("Specialty Medications and Their Categories"):
    st.write("""This catalog lists commonly used specialty medications along with their therapeutic categories""")

DRUG_CATALOG = {
    "Dupixent": "Autoimmune",
    "Stelara": "Autoimmune",
    "Skyrizi": "Autoimmune",
    "Humira": "Autoimmune",
    "Nubeqa": "Oncology",
    "Rinvoq": "Autoimmune",
    "Rezdiffra": "Hepatology",
    "Ibrance": "Oncology",
    "Cosentyx": "Rheumatology",
    "Nemluvio": "Autoimmune",
    "Tremfya": "Autoimmune",
    "Epclusa": "Hepatology",
    "Verzenio": "Oncology",
    "Kevzara": "Autoimmune",
    "Otezla": "Autoimmune",
    "Tymlos": "Osteoporosis",
    "Ohtuvayre": "Respiratory",
    "Pomolidomide": "Oncology",
    "Fasenra": "Respiratory",
    "Jascayd": "Respiratory",
    "Austedo": "Neurology",
}

df = pd.DataFrame(list(DRUG_CATALOG.items()), columns=["Drug Name", "Category"])

st.dataframe(df, width='stretch')