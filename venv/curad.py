import streamlit as st
import pandas as pd
import plotly.express as px

# --- App Config ---
st.set_page_config(page_title="CURAD Internship Summary", layout="wide")
st.title("CURAD Internship Summary Dashboard")

# --- CURAD MISSION NARRATIVE ---
st.markdown("""
### 🌱 About CURAD's Internship Mandate
The Consortium for Enhancing University Responsiveness to Agribusiness Development (CURAD) plays a crucial role in connecting academia with Uganda's agribusiness industry. A cornerstone of their mission is a strong commitment to student engagement through comprehensive internship programs...

CURAD's **"Earn As You Learn"** initiative exemplifies their practical approach, enabling students to transform agribusiness ideas into profitable ventures while still pursuing their studies...
""")

# --- Load Preloaded Excel File ---
@st.cache_data
def load_data():
    return pd.read_excel("List of Interns Engaged at CURAD.xlsx")

df = load_data()
df.columns = df.columns.str.strip()

# --- Sidebar Filters ---
st.sidebar.header("🔎 Filter Intern Data")
years = sorted(df["Year of Engamenet"].dropna().unique())
universities = sorted(df["University"].dropna().unique())

selected_years = st.sidebar.multiselect("Select Year(s)", options=years, default=years)
selected_unis = st.sidebar.multiselect("Select University(ies)", options=universities, default=universities)

filtered_df = df[df["Year of Engamenet"].isin(selected_years) & df["University"].isin(selected_unis)]

# --- Show Filtered Data Table ---
st.markdown("### 📋 Intern Data Table")
st.dataframe(filtered_df, use_container_width=True)

csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button("Download Filtered Data as CSV", data=csv, file_name="CURAD_Intern_Data.csv", mime='text/csv')

# --- Charts & Narratives ---

# 1. Pie Chart: Gender Distribution
st.markdown("### 🔵 Gender Distribution of Interns")
gender_counts = filtered_df["Gender"].value_counts()
fig_gender = px.pie(gender_counts, values=gender_counts.values, names=gender_counts.index, title="Gender Distribution")
st.plotly_chart(fig_gender, use_container_width=True)

female_pct = (gender_counts.get("Female", 0) / gender_counts.sum()) * 100
male_pct = (gender_counts.get("Male", 0) / gender_counts.sum()) * 100
st.markdown(f"**Narrative:** {female_pct:.1f}% of the interns are female and {male_pct:.1f}% are male, reflecting CURAD’s inclusive approach to gender in agribusiness education.")

# 2. Line Chart: Interns Per Year
st.markdown("### 📈 Interns Engaged Per Year")
year_counts = filtered_df["Year of Engamenet"].value_counts().sort_index()
fig_year = px.line(x=year_counts.index, y=year_counts.values, labels={"x": "Year", "y": "Number of Interns"}, markers=True)
st.plotly_chart(fig_year, use_container_width=True)

peak_year = year_counts.idxmax()
st.markdown(f"**Narrative:** The number of interns peaked in **{peak_year}**, showcasing CURAD’s growing influence and student engagement over time.")

# 3. Bar Chart: Interns by University
st.markdown("### 🏫 Interns by University")
university_counts = filtered_df["University"].value_counts().sort_values(ascending=True)
fig_uni = px.bar(x=university_counts.values, y=university_counts.index, orientation='h', labels={"x": "Number of Interns", "y": "University"})
st.plotly_chart(fig_uni, use_container_width=True)

top_uni = university_counts.idxmax()
st.markdown(f"**Narrative:** The top contributing university is **{top_uni}**, indicating strong collaboration with CURAD.")

# 4. Grouped Bar Chart: University vs Year
st.markdown("### 🔢 University Participation Over Years")
university_year = filtered_df.groupby(["Year of Engamenet", "University"]).size().reset_index(name="Count")
fig_uni_year = px.bar(university_year, x="Year of Engamenet", y="Count", color="University", barmode="group")
st.plotly_chart(fig_uni_year, use_container_width=True)
st.markdown("**Narrative:** This chart shows which universities partnered with CURAD each year. Some have consistent involvement while others are occasional contributors.")

# 5. Stacked Bar: Year vs Sex
st.markdown("### 👩‍🎓 Female Engagement Over Years")
year_gender = filtered_df.groupby(["Year of Engamenet", "Gender"]).size().reset_index(name="Count")
fig_year_gender = px.bar(year_gender, x="Year of Engamenet", y="Count", color="Gender", barmode="stack")
st.plotly_chart(fig_year_gender, use_container_width=True)
st.markdown("**Narrative:** Female intern numbers have varied across years. The peaks show the success of initiatives aimed at improving gender balance in agribusiness training.")
