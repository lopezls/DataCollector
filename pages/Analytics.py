import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Analytics", page_icon="📈", layout="wide")
st.title("📈 Analytics Dashboard")
st.caption("All metrics reflect current month unless otherwise noted.")
st.divider()

db_path = "pharmacy_data.db"

if not os.path.exists(db_path):
    st.info("No data yet — submit your first encounter using the Data Collection form.")
    st.stop()

# ---- database connection ----
def get_connection():
    return sqlite3.connect(db_path)

# ---- query functions ----
def get_count(column, value="Yes", this_month=True):
    conn = get_connection()
    if this_month:
        result = conn.execute(f"""
            SELECT COUNT(*) FROM entries
            WHERE {column} = ?
            AND strftime('%Y-%m', timestamp) = strftime('%Y-%m', 'now')
        """, (value,)).fetchone()
    else:
        result = conn.execute(f"""
            SELECT COUNT(*) FROM entries
            WHERE {column} = ?
            AND strftime('%Y-%m', timestamp) = strftime('%Y-%m', datetime('now', '-1 month'))
        """, (value,)).fetchone()
    conn.close()
    return result[0]

# ---- load full dataframe ----
conn = get_connection()
df = pd.read_sql_query("SELECT * FROM entries ORDER BY timestamp DESC", conn)
conn.close()

if df.empty:
    st.info("No entries found yet — submit your first encounter using the Data Collection form.")
    st.stop()

# ---- KPI metrics ----
st.subheader("This Month at a Glance")

this_month = get_count("counseling")
last_month = get_count("counseling", this_month=False)
delta = this_month - last_month

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total Encounters", len(df[df["timestamp"].str.startswith(pd.Timestamp.now().strftime("%Y-%m"))]))
with col2:
    st.metric("Counseling Sessions", this_month, delta=f"{delta:+d} vs last month")
with col3:
    st.metric("Depression Screenings", get_count("depression_survey"))
with col4:
    st.metric("Adherence Surveys", get_count("adherence_survey"))
with col5:
    st.metric("ADEs Reported", get_count("ades_reported"))

st.divider()

# ---- row 1: drug distribution + language distribution ----
st.subheader("Distribution Overview")
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    drug_counts = df["drug_name"].value_counts().reset_index()
    drug_counts.columns = ["Drug", "Count"]
    fig1 = px.pie(
        drug_counts,
        values="Count",
        names="Drug",
        title="Encounters by Drug",
        hole=0.4
    )
    fig1.update_traces(textinfo="percent+label")
    fig1.update_layout(showlegend=False)
    st.plotly_chart(fig1, use_container_width=True)

with chart_col2:
    if "language" in df.columns and df["language"].notna().any():
        lang_counts = df["language"].value_counts().reset_index()
        lang_counts.columns = ["Language", "Count"]
        fig2 = px.pie(
            lang_counts,
            values="Count",
            names="Language",
            title="Counseling Language Distribution",
            hole=0.4,
            color_discrete_map={
                "English": "#378ADD",
                "Spanish": "#1D9E75",
                "Vietnamese": "#F59E0B",
                "Russian": "#EF4444",
                "Lao": "#8B5CF6",
                "Other": "#6B7280"
            }
        )
        fig2.update_traces(textinfo="percent+label")
        fig2.update_layout(showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No language data available yet.")

st.divider()

# ---- row 2: category distribution + survey completion ----
chart_col3, chart_col4 = st.columns(2)

with chart_col3:
    cat_counts = df["category"].value_counts().reset_index()
    cat_counts.columns = ["Category", "Count"]
    fig3 = px.bar(
        cat_counts,
        x="Count",
        y="Category",
        orientation="h",
        title="Encounters by Therapeutic Category",
        color="Category",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig3.update_layout(showlegend=False, yaxis_title="", xaxis_title="Encounters")
    st.plotly_chart(fig3, use_container_width=True)

with chart_col4:
    survey_data = {
        "Survey": ["Counseling", "Depression", "Adherence", "Food Insecurity"],
        "Completion Rate": [
            round(len(df[df["counseling"] == "Yes"]) / len(df) * 100, 1),
            round(len(df[df["depression_survey"] == "Yes"]) / len(df) * 100, 1),
            round(len(df[df["adherence_survey"] == "Yes"]) / len(df) * 100, 1),
            round(len(df[df["food_insecurity_survey"] == "Yes"]) / len(df) * 100, 1),
        ]
    }
    survey_df = pd.DataFrame(survey_data)
    fig4 = px.bar(
        survey_df,
        x="Completion Rate",
        y="Survey",
        orientation="h",
        title="Survey Completion Rates (All Time)",
        color="Completion Rate",
        color_continuous_scale="Blues",
        range_x=[0, 100]
    )
    fig4.update_layout(
        showlegend=False,
        yaxis_title="",
        xaxis_title="Completion Rate (%)",
        coloraxis_showscale=False
    )
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

# ---- ADE distribution by top drugs ----
st.subheader("ADE Distribution — Top Drugs")

ade_df = df[df["ades_reported"] == "Yes"].copy()

if ade_df.empty:
    st.success("No ADEs reported in the current dataset.")
else:
    # get top 3 drugs with most ADEs
    top_drugs = ade_df["drug_name"].value_counts().head(3).index.tolist()

    if len(top_drugs) == 0:
        st.info("Not enough ADE data to display distribution.")
    else:
        ade_cols = st.columns(len(top_drugs))

        for i, drug in enumerate(top_drugs):
            drug_ades = ade_df[ade_df["drug_name"] == drug]["ades_details"].dropna()

            # split by / to get individual ADEs per entry
            all_ades = []
            for entry in drug_ades:
                split = [a.strip() for a in entry.split("/") if a.strip()]
                all_ades.extend(split)

            if not all_ades:
                with ade_cols[i]:
                    st.info(f"No ADE details recorded for {drug}")
                continue

            ade_counts = pd.Series(all_ades).value_counts().reset_index()
            ade_counts.columns = ["ADE", "Count"]

            fig = px.pie(
                ade_counts,
                values="Count",
                names="ADE",
                title=f"{drug}",
                hole=0.4
            )
            fig.update_traces(textinfo="percent+label")
            fig.update_layout(
                showlegend=False,
                title_font_size=14,
                margin=dict(t=40, b=0, l=0, r=0)
            )

            with ade_cols[i]:
                total = len(drug_ades)
                st.metric(f"{drug} — Total ADEs", total)
                st.plotly_chart(fig, use_container_width=True)