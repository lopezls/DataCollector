import streamlit as st
import sqlite3
import os

# ---- page config MUST be first ----
st.set_page_config(
    page_title="Specialty Pharmacy Analytics",
    page_icon="💊",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* {
    font-family: 'Inter', sans-serif !important;
}


</style>
""", unsafe_allow_html=True)

#--base data-----
# ---- database functions ----
def get_connection():
    return sqlite3.connect("pharmacy_data.db")

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

def seed_data():
    conn = get_connection()
    count = conn.execute("SELECT COUNT(*) FROM entries").fetchone()[0]
    if count == 0:
        sample_entries = [
            #--sample data starts here--#
            #--('timestamp', 'drug_name', 'category', 'counseling', 'language', 'depression_survey', 'adherence_survey', 'food_insecurity_survey', 'ades_reported', ades_details),--#
            ('2026-06-01 12:12:00', 'Dupixent', 'Autoimmune', 'Yes', 'English', 'Yes', 'Yes', 'No', 'No', None),
            ('2026-06-01 12:12:00', 'Dupixent', 'Autoimmune', 'Yes', 'Spanish', 'Yes', 'No', 'No', 'No', None),
            ('2026-06-01 12:12:00', 'Rezdiffra', 'Hepatology', 'Yes', 'Spanish', 'Yes', 'Yes', 'Yes', 'Yes', 'Diarrhea'),
            ('2026-06-01 12:12:00', 'Jascayd', 'Respiratory', 'Yes', 'Spanish', 'Yes', 'Yes', 'Yes', 'Yes', 'Diarrhea'),
            ('2026-06-01 12:12:00', 'Cabometyx', 'Oncology', 'Yes', 'Spanish', 'Yes', 'Yes', 'Yes', 'Yes', 'Fatigue'),
            ('2026-06-01 12:12:00', 'Nemluvio', 'Autoimmune', 'Yes', 'English', 'Yes', 'No', 'No', 'No', None),
            ('2026-06-01 12:12:00', 'Jascayd', 'Respiratory', 'Yes', 'English', 'Yes', 'Yes', 'Yes', 'Yes', 'Headache'),
            ('2026-06-01 12:12:00', 'Nemluvio', 'Autoimmune', 'Yes', 'English', 'Yes', 'No', 'No', 'No', None),
            ('2026-06-01 12:12:00', 'Jascayd', 'Respiratory', 'Yes', 'English', 'Yes', 'Yes', 'Yes', 'Yes', 'Depression'),
            ('2026-06-01 12:12:00', 'Nemluvio', 'Autoimmune', 'Yes', 'English', 'Yes', 'No', 'No', 'No', None),
            ('2026-06-01 12:12:00', 'Austedo', 'Neurology', 'Yes', 'English', 'Yes', 'Yes', 'Yes', 'Yes', 'Dry Mouth'),
            ('2026-06-01 12:12:00', 'Ohtuvayre', 'Respiratory', 'Yes', 'English', 'Yes', 'Yes', 'Yes', 'Yes', 'Back Pain'),
        ]
        conn.executemany("""
            INSERT INTO entries (
                timestamp, drug_name, category, counseling, language,
                depression_survey, adherence_survey,
                food_insecurity_survey, ades_reported, ades_details
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, sample_entries)
        conn.commit()
    conn.close()

# ---- runs once on startup ----
create_table()
seed_data()


# ---- header ----
st.title("💊 Specialty Pharmacy Clinical Documentation & Analytics Platform")
st.markdown("*Purpose-built for specialty pharmacy patient management program interactions*")
st.divider()

# ---- three column overview ----
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### ★ Document")
    st.markdown("""
    Capture structured clinical encounter data including:
    - Drug counseling sessions
    - Clinical screenings (PHQ-2, PHQ-9, UCLA)
    - Adverse drug event reporting
    - Language of interaction
    """)

with col2:
    st.markdown("### ★ Analyze")
    st.markdown("""
    Real-time analytics dashboard surfacing:
    - KPI metrics by month
    - Drug distribution trends
    - Survey completion rates
    - ADE tracking and severity
    """)

with col3:
    st.markdown("### ★ Impact")
    st.markdown("""
    Built to quantify clinical impact for:
    - Performance documentation
    - Audit readiness
    - Board certification evidence
    - Data-driven decision making
    """)

st.divider()

# ---- quick stats if data exists ----
db_path = "pharmacy_data.db"

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    total = conn.execute("SELECT COUNT(*) FROM entries").fetchone()[0]
    counseled = conn.execute("SELECT COUNT(*) FROM entries WHERE counseling = 'Yes'").fetchone()[0]
    ades = conn.execute("SELECT COUNT(*) FROM entries WHERE ades_reported = 'Yes'").fetchone()[0]
    
    top_drug_result = conn.execute("""
        SELECT drug_name, COUNT(*) as count
        FROM entries
        GROUP BY drug_name
        ORDER BY count DESC
        LIMIT 1
    """).fetchone()
    
    top_drug = top_drug_result[0] if top_drug_result else "N/A"
    
    conn.close()
    
    st.subheader("★Platform Summary")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Encounters Logged", total)
    with m2:
        st.metric("Counseling Sessions", counseled)
    with m3:
        st.metric("ADEs Tracked", ades)
    with m4:
        st.metric("Top Drug", f"{top_drug}")
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