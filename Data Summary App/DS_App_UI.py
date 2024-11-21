import streamlit as st
import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# import DS_App_Backend
from DS_App_Backend import display_data_info
import io

# Set up the Streamlit app title
st.title("Data Summary App")

# choose data source
option = st.selectbox("Option to choose data source", ["Upload a File", "Connect to Database"])

# choose option1:
if option == "Upload a File":
    uploaded_file = st.file_uploader(" ", type=["csv", "xlsx"])
    if uploaded_file is not None:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
            st.write('#### You Uploaded CSV file')
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
            st.write('#### You Uploaded file Excel file')

        if st.button("Click to view data insights"):
            display_data_info(df)

# choose option2 (sql)
elif option == "Connect to Database":
    db_type = st.selectbox("choose data source", ["Mysql", "Snowflake"])
    if db_type == "Mysql":
        row1 = st.columns(3)
        row2 = st.columns(3)
        with row1[0]:
            user = st.text_input("Username")
        with row1[1]:
            password = st.text_input("Password")
        with row1[2]:
            db_name = st.text_input("db_name")
        with row2[0]:
            db_password = st.text_input("db_password")
        with row2[1]:
            host = st.text_input("host")
        query = st.text_area("Enter Query Statement")

# choose option2 (snowflake)
    elif db_type == 'Snowflake':
        row1 = st.columns(3)
        row2 = st.columns(3)
        with row1[0]:
            Server = st.text_input("Server Name")
        with row1[1]:
            Warehouse = st.text_input("Warehouse")
        with row2[0]:
            Role = st.text_input("Role")
        with row2[1]:
            Database = st.text_input("Database")

        query = st.text_area("Enter Query Statement")

# Hit to get data
        if st.button('Get Data'):
            if db_type == 'Mysql':
                connection_string = (f"{user}:{password}@{host}/{db_name}")
            elif db_type == 'Snowflake':
                connection_string = (f"{user}:{password}@{host}/{db_name}")
            try:
                engine = create_engine(connection_string)
                df = pd.read_sql(query, engine)
            except Exception as e:
                st.error(f"Error connecting to the database: {e}")


