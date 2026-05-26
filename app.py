import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Page Configuration
st.set_page_config(
    page_title="Data Cleaning & Reporting Automation",
    layout="wide"
)

# Title
st.title("🧹 Data Cleaning & Reporting Automation")

# File Upload
uploaded_file = st.file_uploader(
    "Upload CSV or Excel File",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:

    # Read File
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Original Data
    st.subheader("📋 Original Dataset")
    st.dataframe(df)

    # Missing Values Report
    st.subheader("❌ Missing Values Report")

    missing_values = df.isnull().sum()

    missing_df = pd.DataFrame({
        "Column": missing_values.index,
        "Missing Values": missing_values.values
    })

    st.dataframe(missing_df)

    # Fill Missing Values
    cleaned_df = df.ffill()

    # Remove Duplicates
    cleaned_df = cleaned_df.drop_duplicates()

    # Cleaned Data
    st.subheader("✅ Cleaned Dataset")

    st.dataframe(cleaned_df)

    # Dataset Summary
    st.subheader("📊 Summary Statistics")

    st.write(cleaned_df.describe())

    # Select Numeric Columns
    numeric_cols = cleaned_df.select_dtypes(include=np.number).columns

    # Visualization
    if len(numeric_cols) > 0:

        selected_column = st.selectbox(
            "Select Column for Visualization",
            numeric_cols
        )

        fig = px.histogram(
            cleaned_df,
            x=selected_column,
            title=f"{selected_column} Distribution"
        )

        st.plotly_chart(fig, use_container_width=True)

    # Download Cleaned Data
    csv = cleaned_df.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="📥 Download Cleaned Dataset",
        data=csv,
        file_name="cleaned_data.csv",
        mime="text/csv"
    )

else:
    st.info("Please upload dirty_data.csv")