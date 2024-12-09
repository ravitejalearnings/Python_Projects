import numpy as np

import streamlit as st
import pandas as pd
from faker import Faker
import random
import zipfile
import io

# Initialize Faker
faker = Faker()

# App Title
st.title("🛠️ Synthetic Data Generator")
st.divider()

# App Description
st.markdown("""
Purpose: Generate synthetic data for testing, prototyping, or educational purposes. Define columns, choose data types, and download the output in your desired format.
""")

# Prerequisites Section
with st.expander("Supported Data Formats", expanded=False):
    st.write("""
    - **Number:** Random integer values
    - **Float:** Random decimal values
    - **Date:** User can choose start date & end date
    - **Name:** Synthetic names
    - **Alphanumeric:** Random alphanumeric strings (e.g., 'edgx123')
    - **City:** Random city names
    - **Email:** Synthetic Emails (e.g., 'john@domain.com')
    - **Custom:** User can provide list of values seperated by comma (e.g., 'region_1','region_2','region_3' etc)
    """)

st.divider()

# Session state to track tables
if "tables" not in st.session_state:
    st.session_state.tables = {}

# Table Management Section
st.subheader(" 📑 Manage Tables")
col1, col2 = st.columns(2)

# Add and Remove Table Buttons
with col1:
    if st.button("➕ Add Table"):
        table_id = f"Table_{len(st.session_state.tables) + 1}"
        st.session_state.tables[table_id] = {"columns": [{"name": "index", "dtype": "index"}], "rows": 10, "metadata": None}

with col2:
    if st.button("➖ Remove Table") and st.session_state.tables:
        st.session_state.tables.popitem()

# Table Configuration Section
for table_name in st.session_state.tables.keys():
    st.markdown(f"### 📝 Configuration for `{table_name}`")
    st.divider()

    # Table Name and Row Count
    new_name = st.text_input(f"Table Name", value=table_name, key=f"table_name_{table_name}")
    row_count = st.number_input(f"Rows for `{new_name}`", min_value=1, max_value=50000, step=1, key=f"rows_{table_name}")
    st.session_state.tables[table_name]["rows"] = row_count
    st.session_state.tables[table_name]["name"] = new_name

    # Column Management
    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"➕ Add Column for `{new_name}`"):
            st.session_state.tables[table_name]["columns"].append({"name": "", "dtype": "number", "min": 0, "max": 1})
    with col2:
        if st.button(f"➖ Remove Column for `{new_name}`") and st.session_state.tables[table_name]["columns"]:
            st.session_state.tables[table_name]["columns"].pop()

    # Data Type Options
    diff_formats = ["number", "float", "date", "name", "alphanumeric","city", "email", "custom","index"]

    # Column Configuration
    for i, col in enumerate(st.session_state.tables[table_name]["columns"]):
        col1, col2, col3, col4,col5,col6,col7 = st.columns([2, 2, 2, 2, 3, 3,1])
        with col1:
            col["name"] = st.text_input(f"Cols({new_name})", value=col["name"], key=f"{table_name}_col_name_{i}")
        with col2:
            col["dtype"] = st.selectbox(
                "Format", diff_formats,
                index=diff_formats.index(col["dtype"]),
                key=f"{table_name}_col_dtype_{i}",
            )
        if col["dtype"] in ["number", "float"]:
            with col4:
                col["min"] = st.number_input(
                    f"Min ({col['name']})", value=col["min"], step=1, key=f"min_{table_name}_{i}")
            with col5:
                col["max"] = st.number_input(
                    f"Max  ({col['name']})", value=col["max"], step=1, key=f"max_{table_name}_{i}")
        elif col["dtype"] == "date":
            with col4:
                start_date =st.date_input(
                    f"Start Date ({col['name']})", key=f"start_date_{table_name}_{i}")
                col["start_date"] = start_date
            with col5:
                end_date = st.date_input(
                    f"End Date ({col['name']})", key=f"end_date_{table_name}_{i}")
                col["end_date"] = end_date
        elif col["dtype"] == "custom":
            with col3:
                col["custom_values"] = st.text_input(
                    f"""Input values in " , " seperated format""", value=col.get("custom_values", ""),
                    key=f"custom_values_{table_name}_{i}"
                )

    st.divider()

# Generate Fake Data Section
st.subheader("🔄 Generate Data")
if st.button("Click to View Synthetic Data"):
    for table_id, table_data in st.session_state.tables.items():
        rows = table_data["rows"]
        columns = table_data["columns"]
        fake_data = []

        for row_index in range(1, rows + 1):  # Start generating rows
            row = {}
            for col in columns:
                if col["dtype"] == "index":
                    row[col["name"]] = row_index  # Generate index values
                elif col["dtype"] == "name":
                    name = faker.name()
                    row[col["name"]] = name
                elif col["dtype"] == "number":
                    row[col["name"]] = faker.random_int(min=col.get("min", 0), max=col.get("max", 100))
                elif col["dtype"] == "float":
                    row[col["name"]] = round(faker.random.uniform(col.get("min", 0), col.get("max", 100)), 2)
                elif col["dtype"] == "date":
                    row[col["name"]] = faker.date_between(start_date=start_date, end_date=end_date)
                elif col["dtype"] == "alphanumeric":
                    row[col["name"]] = faker.bothify(text="??##")
                elif col["dtype"] == "city":
                    row[col["name"]] = faker.city()
                elif col["dtype"] == "email":
                    name_parts = name.lower().replace(".", "").split()
                    email = f"{name_parts[0]}.{name_parts[-1]}@domain.com"
                    row[col["name"]] = email
                elif col["dtype"] == "custom":
                    custom_values = col.get("custom_values", "").split(",")
                    if custom_values:
                        row[col["name"]] = random.choice(custom_values).strip()


            fake_data.append(row)

        st.session_state.tables[table_id]["data"] = pd.DataFrame(fake_data)
        df = pd.DataFrame(fake_data)
        # st.dataframe(df.head())
        show_index = st.checkbox(f"Show Index for {table_data['name']}", key=f"show_index_{table_id}")

        # Display DataFrame with or without index based on user selection
        if show_index:
            st.dataframe(df.head())
        else:
            st.dataframe(df.reset_index(drop=True))

        st.session_state.tables[table_id]["show_index"] = show_index

    st.success("Synthetic data generated for all tables!")
st.divider()

# Download Section
st.subheader("⏬ Download Data")
if st.button("Download All Tables"):
    if not st.session_state.tables:
        st.error("No tables available to download.")
    else:
        # Create an in-memory ZIP file
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for table_id, table_data in st.session_state.tables.items():
                csv_data = table_data["data"].to_csv(index=False)
                zip_file.writestr(f"{table_data['name']}.csv", csv_data)

        zip_buffer.seek(0)
        st.download_button(
            "Download All Tables (ZIP)",
            data=zip_buffer,
            file_name="synthetic_tables.zip",
            mime="application/zip",
        )
