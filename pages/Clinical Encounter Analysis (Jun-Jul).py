import streamlit as st

st.set_page_config(page_title="Clinical Encounter Analysis", layout="wide")

st.title("Clinical Encounter Analysis")
st.caption(
    "Specialty Pharmacy Clinical Documentation & Analytics Platform  |  "
    "Author: Lorelei Lee Lopez, PharmD, MBA"
)

c1, c2, c3 = st.columns(3)
c1.metric("Encounters analyzed", "41")
c2.metric("Period covered", "Jun – Jul 2026")
c3.metric("Encounters in Spanish", "31.7%")

st.divider()

# ---------------- Overview ----------------
st.header("Overview")
st.write(
    "Specialty pharmacy patient management programs generate thousands of clinical "
    "interactions annually that go undocumented at the aggregate level. This analysis "
    "examines clinical encounter data collected through a structured form on this "
    "documentation platform over a two-month period. The platform collected, stored, "
    "and displayed data from each patient encounter."
)
st.write(
    "Each encounter was performed by a licensed Senior Specialty Pharmacist working with "
    "a range of specialty therapies, including oncology, autoimmune, neuromuscular, and "
    "more. The platform was created independently to address the absence of encounter "
    "tracking in the workflow once the clinician completed the call."
)
st.write(
    "The data collected includes drug name, therapeutic category, language of counseling, "
    "survey completion status, and adverse drug event reporting. This analysis applies "
    "descriptive analytics to surface patterns in drug volume, therapeutic category "
    "distribution, language access, and adverse event frequency."
)

# ---------------- Key Findings ----------------
st.header("Key Findings")

with st.expander("Drug Volume", expanded=True):
    st.write(
        "The most frequently encountered specialty medication during this time frame was "
        "**Jascayd**, a PDE4 inhibitor used to treat idiopathic pulmonary fibrosis (IPF) "
        "and progressive pulmonary fibrosis (PPF). The second most encountered was "
        "**Rezdiffra**, which acts on THR-β receptors to decrease liver fat content in "
        "patients with noncirrhotic MASH and fibrosis. These two drugs represent the "
        "pulmonary and hepatology categories, respectively."
    )

with st.expander("Therapeutic Category Distribution", expanded=True):
    st.write(
        "The largest therapeutic category represented was **autoimmune**. This category "
        "covers a wide variety of diseases, including arthritis, atopic dermatitis, bullous "
        "pemphigoid, Crohn's disease, psoriasis, psoriatic arthritis, ulcerative colitis, "
        "and more, along with the many drugs used to treat them. In contrast, the smallest "
        "category was **osteoporosis**, a single condition treated with a single drug, Tymlos."
    )
    st.write(
        "The large presence of autoimmune diseases and their accompanying drugs suggests "
        "clinical training should prioritize thorough education in this area to ensure "
        "patients are adequately served."
    )

with st.expander("Language Access", expanded=True):
    st.write(
        "All clinicians in this department have access to a language line providing live "
        "medical interpreters in over 290 languages. One encounter was conducted in "
        "Mandarin using a medical interpreter. While interpreters provide access, "
        "communicating through one can still be a barrier."
    )
    st.write(
        "This clinician is a native bilingual English and Spanish speaker and has passed "
        "testing to communicate with Spanish-speaking patients without an interpreter. "
        "This is reflected in the **31.7%** of encounters conducted in Spanish, highlighting "
        "the impact of removing a language barrier on patient care and the need for patient "
        "and clinician resources written in Spanish."
    )

with st.expander("Adverse Drug Event Reporting", expanded=True):
    st.write(
        "All adverse drug events were interpreted by the clinician to standardize wording "
        "and ensure accurate tallying. Each event was tied to the specific specialty drug "
        "the patient was using."
    )
    st.write(
        "For **Jascayd**, the most frequently encountered drug, depression and diarrhea "
        "were tied as the most reported ADEs (26.8% each). For **Rezdiffra**, the most "
        "reported side effect was also diarrhea (33.3%). This suggests counseling for new "
        "patients on these drugs should focus on side effect management strategies so "
        "patients can continue therapy for the best outcomes."
    )

with st.expander("Survey Completion", expanded=True):
    st.write(
        "Counseling and depression screenings (PHQ-2 and PHQ-9) were the most prevalent "
        "surveys across the board. Food insecurity had a lower completion rate, but it is "
        "assessed only once every 12 months, versus every 6 months for adherence and "
        "depression. Counseling should be performed on every call."
    )

# ---------------- Clinical Implications ----------------
st.header("Clinical Implications")

st.subheader("Counseling")
st.write(
    "Due to the large volume of autoimmune drug encounters, clinical training should focus "
    "on these disease states and their accompanying drugs, since the majority of patients "
    "served fall into this category."
)

st.subheader("Language Resources")
st.write(
    "The large population served in Spanish supports the clinical value of written "
    "resources in Spanish for easier understanding and delivery of patient education. "
    "Expanding multilingual resources beyond English and Spanish can be considered once "
    "more data is collected and prevalent language groups are identified."
)

st.subheader("ADE Monitoring")
st.write(
    "Diarrhea was the most reported ADE across the top two drugs and is a potential "
    "barrier to continuing treatment. Proactive counseling on diarrhea management at the "
    "start of therapy may improve patients' quality of life and support continued treatment."
)

st.subheader("Survey Completion")
st.write(
    "Depression screening using PHQ-2 and PHQ-9 was administered across the majority of "
    "encounters, reflecting the clinical responsibility to assess psychosocial risk factors "
    "in patients managing complex chronic conditions. Adherence and food insecurity surveys "
    "showed variable completion rates, consistent with the dynamic nature of patient "
    "management program calls and individual program requirements. Future data could explore "
    "whether food insecurity assessment, patient-reported food insecurity, and connection to "
    "local resources are linked."
)

# ---------------- Limitations ----------------
st.header("Limitations")
st.write(
    "This analysis is based on a small, single-pharmacist dataset over a short period. "
    "These findings should be treated as a starting point for further data collection, "
    "exploration, and hypothesis generation rather than as statistically definitive. A "
    "larger dataset covering the full department of 40+ pharmacists over a longer period "
    "would support more concrete conclusions and meaningful department and workflow changes."
)

# ---------------- Tools & Disclaimer ----------------
st.header("Tools Used")
st.write("Python · SQL · SQLite · Plotly · Streamlit")
st.markdown("Platform source code: [github.com/lopezls/DataCollector](https://github.com/lopezls/DataCollector)")

st.divider()
st.caption(
    "Disclaimer: This analysis was conducted using de-identified encounter data collected "
    "through an independently developed clinical documentation platform. No real patient "
    "identifying information was used or stored at any point in this project."
)