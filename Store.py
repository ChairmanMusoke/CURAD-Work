# app.py

import os
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO

# Page config
st.set_page_config(page_title="PELA Dashboard", layout="wide")

# Display organization logo on top left and right
from PIL import Image
import base64

# Load logo
logo_path = "logo.png"  # Replace with your actual logo file name
if os.path.exists(logo_path):
    logo = Image.open(logo_path)

    # Convert logo to base64
    with open(logo_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()

    # Inject HTML for dual logos
    st.markdown(
        f"""
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 0 20px;">
            <img src="data:image/png;base64,{encoded}" alt="Logo" style="height: 70px;">
            <img src="data:image/png;base64,{encoded}" alt="Logo" style="height: 70px;">
        </div>
        <br>
        """,
        unsafe_allow_html=True
    )
else:
    st.warning("Logo image not found. Please add 'logo.png' to your app folder.")

st.title("📊 PELA Production Dashboard - Nwoya District")

# Caching data loader
@st.cache_data
def load_data(file_source):
    df = pd.read_excel(file_source, sheet_name="Form Responses 1")
    df.columns = df.columns.str.strip().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')
    df = df.drop(columns=['Contact_of_PELA_chairperson'], errors='ignore')
    return df

# Check local file
local_file_path = "Copy of Untitled form (Responses).xlsx"
if os.path.exists(local_file_path):
    #st.info(f"Reading data from local file: `{local_file_path}`")
    df = load_data(local_file_path)
else:
    uploaded_file = st.file_uploader("Upload the PELA Excel file", type=["xlsx"])
    if uploaded_file:
        df = load_data(uploaded_file)
        with open(local_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"File saved locally as `{local_file_path}`")
    else:
        st.info("Please upload the Excel file to proceed.")
        st.stop()

# Sidebar filter
if 'Name_of_PELA' in df.columns:
    pela_options = df['Name_of_PELA'].dropna().unique().tolist()
    selected_pelas = st.sidebar.multiselect("Filter by PELA Name", pela_options, default=pela_options)
    filtered_df = df[df['Name_of_PELA'].isin(selected_pelas)]
else:
    filtered_df = df

# Summary Data
numeric_cols = filtered_df.select_dtypes(include='number')
summary = numeric_cols.sum().sort_values(ascending=False)

# Groupings
top_crops = summary[['Tons_of_Maize_tons', 'Tons_of_soybean', 'Tons_of_cassava', 
                     'Tons_of_Sweet_potatoes', 'Tons_of_Tomatoes_ready_for_sale']]
livestock = summary[['Number_of_fish_ready_for_sale', 'Number_of_Chicken_ready_for_sale',
                     'Number_of_pigs_ready_for_sale', 'Number_of_trays_of_eggs',
                     'Number_of_pawpaws_ready_for_sale']]
minor_crops = summary[['Tons_of_onions_ready_for_sale', 'Tons_of_Rosemary_ready_for_sale', 
                       'Tons_of_Irish_Potatoes', 'Tons_of_pepper_ready_for_sale',
                       'Tons_of_chive_ready_for_sale']]

# Download summary
def generate_excel(data):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        data.to_excel(writer, index=False, sheet_name='Summary')
    output.seek(0)
    return output

st.download_button("⬇️ Download Summary (Excel)", data=generate_excel(filtered_df), file_name="PELA_summary.xlsx")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📄 Summary", "🌾 Crops", "🐓 Livestock", "🌿 Minor Crops"])

with tab1:
    st.markdown("## 📝 Key Narrative Insights")
    st.markdown(f"""
    - **{len(filtered_df)} PELAs** are analyzed in this summary.
    - **Maize** is the leading crop, producing over **{top_crops.iloc[0]:,.0f} tons**.
    - Significant livestock production includes **fish** and **chicken**.
    - Herbal and horticultural crops contribute to income diversity among PELAs.
    """)
    st.dataframe(filtered_df)

with tab2:
    st.subheader("Top 5 Crops by Volume (Tons)")
    fig1, ax1 = plt.subplots()
    sns.barplot(x=top_crops.values, y=top_crops.index.str.replace('_', ' '), palette="viridis", ax=ax1)
    ax1.set_xlabel("Tons")
    ax1.set_ylabel("Crop")
    st.pyplot(fig1)
    st.markdown("""
    📌 **Narrative**:  
    Maize leads crop production followed by soybeans and cassava. Sweet potatoes and tomatoes are also significant contributors, reflecting a mix of staple and high-value crops.
    """)

with tab3:
    st.subheader("Livestock & Produce Counts")
    fig2, ax2 = plt.subplots()
    sns.barplot(x=livestock.values, y=livestock.index.str.replace('_', ' '), palette="magma", ax=ax2)
    ax2.set_xlabel("Count")
    ax2.set_ylabel("Item")
    st.pyplot(fig2)
    st.markdown("""
    📌 **Narrative**:  
    Fish and chicken dominate livestock production. Egg trays and pawpaws further diversify income sources. PELAs show a strong mix of protein and fruit outputs.
    """)

with tab4:
    st.subheader("Proportion of Minor Crops & Herbs")
    fig3, ax3 = plt.subplots()
    ax3.pie(minor_crops.values, labels=minor_crops.index.str.replace('_', ' '),
            autopct='%1.1f%%', startangle=140, colors=sns.color_palette("pastel"))
    ax3.axis('equal')
    st.pyplot(fig3)
    st.markdown("""
    📌 **Narrative**:  
    Minor crops like onions, rosemary, and Irish potatoes contribute to agricultural diversity. Though less in volume, they may have higher market value or niche demand.
    """)

# 🔄 Dynamic Top PELAs
with st.expander("🏅 Dynamic Top Performing PELAs"):
    st.subheader("Select Performance Indicator")
    indicator_options = {
        "Maize Output (Tons)": "Tons_of_Maize_tons",
        "Soyabean Output (Tons)": "Tons_of_soybean",
        "Fish Ready for Sale": "Number_of_fish_ready_for_sale",
        "Chicken Ready for Sale": "Number_of_Chicken_ready_for_sale"
    }

    selected_metric_label = st.selectbox("Choose indicator", list(indicator_options.keys()))
    selected_metric = indicator_options[selected_metric_label]

    if selected_metric in filtered_df.columns:
        top_performers = filtered_df[['PELA', selected_metric]].dropna()
        top_performers = top_performers.sort_values(by=selected_metric, ascending=False).head(10)
        st.table(top_performers)
    else:
        st.warning(f"Selected metric `{selected_metric}` not found in data.")



