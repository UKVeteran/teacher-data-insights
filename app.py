import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import sqlite3

st.set_page_config(page_title="Teacher Data Insights", page_icon="📊", layout="wide")

st.markdown("""
<style>
    .main-header { font-size: 2.3rem; font-weight: 700; color: #1E3A8A; margin-bottom: 0px; }
    .sub-header { font-size: 1.05rem; color: #4B5563; margin-bottom: 1.5rem; }
    .privacy-box { background-color: #EFF6FF; padding: 1rem; border-left: 4px solid #3B82F6; border-radius: 0.25rem; }
</style>
""", unsafe_allow_html=True)

st.sidebar.title("📊 Teacher Data Insights")
app_mode = st.sidebar.selectbox("Select Module", [
    "1. Data Import & Anonymization",
    "2. Class Performance & Score Distribution",
    "3. Item Analysis & Gap Identification",
    "4. Progress Tracking Across Assessments",
    "5. Automated Intervention & Summary Generator",
    "6. Data Protection & Compliance Framework"
])

def generate_synthetic_data(num_students=30):
    np.random.seed(42)
    aliases = [f"Student_{i:02d}" for i in range(1, num_students + 1)]
    q_scores = np.random.binomial(n=5, p=0.68, size=(num_students, 10))
    q_scores[:, 3] = np.random.binomial(n=5, p=0.42, size=num_students)
    q_scores[:, 6] = np.random.binomial(n=5, p=0.35, size=num_students)
    total_scores = q_scores.sum(axis=1)
    data = {"Student Alias": aliases, "Score": total_scores}
    for q_idx in range(10):
        data[f"Q{q_idx+1}"] = q_scores[:, q_idx]
    return pd.DataFrame(data)

if app_mode == "1. Data Import & Anonymization":
    st.markdown('<p class="main-header">Data Import & Anonymization</p>', unsafe_allow_html=True)
    st.markdown('<div class="privacy-box">🔒 <b>Data Protection Notice:</b> Ensure all pupil names are replaced with anonymous student aliases.</div>', unsafe_allow_html=True)
    if st.button("Generate Synthetic Markbook (30 Students)"):
        st.session_state['df_data'] = generate_synthetic_data()
        st.success("Synthetic dataset loaded!")
    if 'df_data' in st.session_state:
        st.dataframe(st.session_state['df_data'].head(10), use_container_width=True)
elif app_mode == "2. Class Performance & Score Distribution":
    st.markdown('<p class="main-header">Class Performance Overview</p>', unsafe_allow_html=True)
    df = st.session_state.get('df_data', generate_synthetic_data())
    scores = df['Score']
    col1, col2, col3 = st.columns(3)
    col1.metric("Class Average (Mean)", f"{scores.mean():.1f} / 50")
    col2.metric("Median Score", f"{scores.median():.1f}")
    col3.metric("Standard Deviation", f"{scores.std():.2f}")
    fig = px.histogram(df, x="Score", nbins=10, title="Score Distribution")
    st.plotly_chart(fig, use_container_width=True)
elif app_mode == "3. Item Analysis & Gap Identification":
    st.markdown('<p class="main-header">Question-Level Item Analysis</p>', unsafe_allow_html=True)
    df = st.session_state.get('df_data', generate_synthetic_data())
    q_cols = [c for c in df.columns if c.startswith('Q')]
    q_facility = (df[q_cols].mean() / 5.0) * 100
    df_q = pd.DataFrame({"Question": q_cols, "Facility Index (%)": q_facility.values})
    fig = px.bar(df_q, x="Question", y="Facility Index (%)", color="Facility Index (%)", title="Question Facility Index")
    st.plotly_chart(fig, use_container_width=True)
elif app_mode == "4. Progress Tracking Across Assessments":
    st.markdown('<p class="main-header">Longitudinal Progress Tracking</p>', unsafe_allow_html=True)
    st.write("Track cohort progress across multiple assessment terms.")
elif app_mode == "5. Automated Intervention & Summary Generator":
    st.markdown('<p class="main-header">Automated Intervention & Summary Generator</p>', unsafe_allow_html=True)
    df = st.session_state.get('df_data', generate_synthetic_data())
    pct = (df['Score'] / 50) * 100
    st.success(f"Stretch Group (>=80%): {len(df[pct >= 80])} students")
    st.warning(f"Borderline (45-59%): {len(df[(pct >= 45) & (pct < 60)])} students")
    st.error(f"Urgent Intervention (<45%): {len(df[pct < 45])} students")
else:
    st.markdown('<p class="main-header">Data Protection & School Compliance</p>', unsafe_allow_html=True)
    st.write("UK GDPR, Data Protection Act 2018, and DPIA guidance for schools.")
