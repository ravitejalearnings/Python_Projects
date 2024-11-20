import streamlit as st
import pandas as pd
import numpy as np
from faker import Faker

# Title and Description
st.title("Data Quality Dashboard")
st.write("Upload your dataset to analyze its quality metrics.")

# File Uploader
uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Read the uploaded file
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.write("### Dataset Preview")
        st.dataframe(df.head())

        # Data Quality Metrics
        st.write("### Data Quality Metrics")
        
        # Completeness Rate
        completeness = (df.count().sum() / df.size) * 100
        st.metric(label="Completeness Rate", value=f"{completeness:.2f}%")
        
        # Duplicate Records
        duplicate_percentage = (df.duplicated().sum() / len(df)) * 100
        st.metric(label="Duplicate Records", value=f"{duplicate_percentage:.2f}%")
        
        # Column-wise Null Percentage
        st.write("#### Column-wise Null Percentage")
        null_percentage = df.isnull().mean() * 100
        st.bar_chart(null_percentage)

        # Optionally, download cleaned data
        if st.button("Download Cleaned Data"):
            cleaned_df = df.drop_duplicates().dropna()
            csv = cleaned_df.to_csv(index=False).encode('utf-8')
            st.download_button(label="Download CSV", data=csv, file_name="cleaned_data.csv", mime="text/csv")
    
    except Exception as e:
        st.error(f"Error processing file: {e}")

else:
    st.info("Awaiting file upload. Upload a CSV or Excel file to get started!")

