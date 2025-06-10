import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="Campus Placement Tracker", layout="wide")

st.title("🎓 Campus Placement Tracker Dashboard")

# 🔶 Disclaimer at top
st.markdown("#### ℹ️ Disclaimer")
st.info(
    "The data shown below is generated using Python for demo purposes only. "
    "It represents synthetic placement information of 500 students and does not reflect actual data from any institution."
)

# Load the data
@st.cache_data
def load_data():
    df = pd.read_csv("Campus_Placement_Tracker_500.csv")
    return df

df_all = load_data()

# Sidebar filter
st.sidebar.header("🎯 Offer Type Filter")
show_all = st.sidebar.checkbox("Show All Offers", value=True)
show_dream = st.sidebar.checkbox("Show Dream Offers (CTC > 8 LPA)", value=False)
show_normal = st.sidebar.checkbox("Show Normal Offers (CTC ≤ 8 LPA)", value=False)

# Filter logic
if show_dream and not show_all and not show_normal:
    df = df_all[df_all["CTC (LPA)"] > 8]
    st.markdown("🎯 Showing **Dream Offers** (CTC > 8 LPA)")
elif show_normal and not show_all and not show_dream:
    df = df_all[df_all["CTC (LPA)"] <= 8]
    st.markdown("🎯 Showing **Normal Offers** (CTC ≤ 8 LPA)")
else:
    df = df_all
    st.markdown("🎯 Showing **All Offers**")

# 🔶 CTC Summary Stats
st.subheader("📊 Key CTC Statistics")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Number of Selections", len(df))
col2.metric("Average CTC", f"{df['CTC (LPA)'].mean():.2f} LPA")
col3.metric("Maximum CTC", f"{df['CTC (LPA)'].max():.2f} LPA")
col4.metric("Minimum CTC", f"{df['CTC (LPA)'].min():.2f} LPA")
col5.metric("Median CTC", f"{df['CTC (LPA)'].median():.2f} LPA")

# Placements by Branch
st.subheader("🏫 Placements by Branch")
branch_counts = df['Branch'].value_counts()
fig_branch, ax_branch = plt.subplots(figsize=(6, 4))
branch_counts.plot(kind='bar', ax=ax_branch, color='skyblue')
ax_branch.set_ylabel("Number of Students")
st.pyplot(fig_branch)

# Gender Distribution (smaller)
st.subheader("⚖️ Gender Distribution")
gender_counts = df['Gender'].value_counts()
fig_gender, ax_gender = plt.subplots(figsize=(3.5, 3.5))
ax_gender.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', startangle=90)
ax_gender.axis('equal')
st.pyplot(fig_gender)

# Job Role Distribution
st.subheader("🧑‍💼 Job Roles Distribution")
job_counts = df['Job Role'].value_counts().head(10)
fig_jobs, ax_jobs = plt.subplots(figsize=(8, 4))
job_counts.plot(kind='barh', ax=ax_jobs, color='orchid')
st.pyplot(fig_jobs)

# Average CTC by Company
st.subheader("🏢 Average CTC by Company")
avg_ctc_company = df.groupby('Company')['CTC (LPA)'].mean().reset_index().sort_values(by='CTC (LPA)', ascending=False)
fig_company = px.bar(avg_ctc_company.head(10), x='Company', y='CTC (LPA)', color='Company',
                     title='Top Companies by Avg CTC',
                     color_discrete_sequence=px.colors.sequential.Plasma)
st.plotly_chart(fig_company, use_container_width=True)

# Average CTC by Job Role
st.subheader("💼 Average CTC by Job Role")
avg_ctc_role = df.groupby('Job Role')['CTC (LPA)'].mean().reset_index().sort_values(by='CTC (LPA)', ascending=False)
fig_role = px.bar(avg_ctc_role.head(10), x='Job Role', y='CTC (LPA)', color='Job Role',
                  title='Top Job Roles by Avg CTC',
                  color_discrete_sequence=px.colors.qualitative.Bold)
st.plotly_chart(fig_role, use_container_width=True)
