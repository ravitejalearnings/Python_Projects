import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
from sqlalchemy import create_engine  # For database connection

# Set up the Streamlit app title
st.title("Data Summary App")

def display_data_info(df):
    st.write("----")
    st.write("### View Sample Data")
    st.write(df.head())
    st.write("----")
    st.write("### Data Characteristics")
    st.write(f"- **Number of Rows**: {df.shape[0]}")
    st.write(f"- **Number of Columns**: {df.shape[1]}")
    st.write(f"- **Is duplicated**: {df.duplicated().sum()}")
    st.write(f"- **Column Names**: {df.columns.tolist()}")
    st.write("----")

    # Columns datatype
    st.write("### Data Types:")
    datatype_df = pd.DataFrame(df.dtypes).reset_index()
    datatype_df.rename(columns={'index': 'Column_name', 0: 'dtypes'}, inplace=True)
    st.write(datatype_df)
    st.write("----")

    # Check for Null values
    st.write("### Check for nulls:")
    isnull_df = pd.DataFrame(df.isnull().sum()).reset_index()
    isnull_df.rename(columns={'index': 'Column_name', 0: 'Null count'}, inplace=True)
    isnull_df['Null Perc'] = round((isnull_df['Null count'] * 100 / df.shape[0]), 2)
    st.write(isnull_df)
    st.write("----")

    # Check for Completeness
    st.write("### Completeness(%):")
    total_values = df.size
    non_missing_values = df.count().sum()
    completeness_rate = round((non_missing_values / total_values) * 100, 2)
    st.write(f" Completeness Rate in Perc: {completeness_rate}")
    st.write("----")

    # Check for Memory Usage
    st.write("### Memory Usage:")
    Memory_usage_df = pd.DataFrame(df.memory_usage()).reset_index()
    Memory_usage_df.rename(columns={'index': 'Column_name', 0: 'Memory Usage'}, inplace=True)
    st.write(Memory_usage_df)
    st.write("----")

    # Distribution plots for numerical data
    st.write("### Distribution of Numerical Columns")
    numerical_cols = df.select_dtypes(include='number').columns
    fig1, axes = plt.subplots(nrows=1, ncols=len(numerical_cols), figsize=(16, 4))
    for ax, col in zip(axes, numerical_cols):
        sns.histplot(data=df, x=col, kde=True, ax=ax)
        ax.set_title(f"Distribution of {col}")
    st.pyplot(fig1)
    st.write("----")

    # Correlation Matrix
    st.write("### Correlation Matrix")
    corr_matrix = df.select_dtypes(include='number').corr()
    fig2, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig2)
    st.write("----")

    # Outlier detection
    st.write("### Box Plots for Outlier Detection")
    fig3, axes = plt.subplots(nrows=1, ncols=len(numerical_cols), figsize=(16, 4))
    for ax, col in zip(axes, numerical_cols):
        sns.boxplot(data=df, y=col, ax=ax)
        ax.set_title(f"{col}")
    st.pyplot(fig3)
    st.write("----")

    # Skewness and Kurtosis
    st.write("### Skewness and Kurtosis for Numerical Columns")
    skew_kurt_df = pd.DataFrame({
        "Skewness": df[numerical_cols].skew(),
        "Kurtosis": df[numerical_cols].kurt()
    }).reset_index().rename(columns={"index": "Column"})
    st.write(skew_kurt_df)

# Main UI
option = st.selectbox("Option to choose data source", ["Upload a File", "Connect to Database"])

if option == "Upload a File":
    uploaded_file = st.file_uploader(" ", type=["csv", "xlsx"])
    if uploaded_file is not None:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
            st.write('#### You Uploaded a CSV file')
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
            st.write('#### You Uploaded an Excel file')

        if st.button("Click to view data insights"):
            display_data_info(df)

elif option == "Connect to Database":
    db_type = st.selectbox("Choose Database", ["Mysql", "Snowflake"])
    if db_type == "Mysql":
        user = st.text_input("Username")
        password = st.text_input("Password", type="password")
        db_name = st.text_input("Database Name")
        host = st.text_input("Host")
        query = st.text_area("Enter Query Statement")
    elif db_type == 'Snowflake':
        user = st.text_input("Username")
        password = st.text_input("Password", type="password")
        account = st.text_input("Account Name")
        warehouse = st.text_input("Warehouse")
        database = st.text_input("Database")
        query = st.text_area("Enter Query Statement")

    if st.button('Get Data'):
        try:
            if db_type == 'Mysql':
                connection_string = f"mysql+pymysql://{user}:{password}@{host}/{db_name}"
            elif db_type == 'Snowflake':
                connection_string = f"snowflake://{user}:{password}@{account}/{database}?warehouse={warehouse}"
            engine = create_engine(connection_string)
            df = pd.read_sql(query, engine)
            st.write("### Query Results")
            st.write(df)
            display_data_info(df)
        except Exception as e:
            st.error(f"Error connecting to the database: {e}")
