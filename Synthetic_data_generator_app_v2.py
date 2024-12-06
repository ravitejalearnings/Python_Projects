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
    - **Name:** Synthetic names
    - **Alphanumeric:** Random alphanumeric strings (e.g., 'edgx123')
    - **Address:** Random full addresses
    - **City:** Generalized city names (e.g., 'city_24')
    - **M/F:** Male/Female values
    - **1/0:** Binary values (1 or 0)
    - **Yes/No:** Boolean values (Yes/No)
    - **Region:** Geographic region labels (e.g., 'Region_01')
    - **Country/State/City:** Geographic labels (e.g., 'Country_101')
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
        st.session_state.tables[table_id] = {"columns": [], "rows": 10, "metadata": None}

with col2:
    if st.button("➖ Remove Table") and st.session_state.tables:
        st.session_state.tables.popitem()

# Table Configuration Section
for table_name in st.session_state.tables.keys():
    st.markdown(f"### 📝 Configuration for `{table_name}`")
    st.divider()

    # Table Name and Row Count
    new_name = st.text_input(f"Table Name", value=table_name, key=f"table_name_{table_name}")
    row_count = st.number_input(f"Rows for `{new_name}`", min_value=1, max_value=1000, step=1, key=f"rows_{table_name}")
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
    diff_formats = [
        "number", "float", "date", "name", "alphanumeric", "address",
        "city", "M/F", "Yes/No", "1/0", "region", "country", "state",
        "email", "phone_numbers", "zip_code", "status_flags", "age",
        "product_name", "ratings"
    ]

    # Column Configuration
    for i, col in enumerate(st.session_state.tables[table_name]["columns"]):
        col1, col2, col3, col4,col5, col6 = st.columns([2, 2, 2, 2, 3, 3])
        with col1:
            col["name"] = st.text_input(f"Cols({new_name})", value=col["name"], key=f"{table_name}_col_name_{i}")
        with col2:
            col["dtype"] = st.selectbox(
                "Format", diff_formats,
                index=diff_formats.index(col["dtype"]),
                key=f"{table_name}_col_dtype_{i}",
            )
        if col["dtype"] in ["number", "float", "ratings", "age"]:
            with col3:
                col["min"] = st.number_input(
                    f"Min ({col['name']})", value=col["min"], step=1, key=f"min_{table_name}_{i}")
            with col4:
                col["max"] = st.number_input(
                    f"Max  ({col['name']})", value=col["max"], step=1, key=f"max_{table_name}_{i}")
        elif col["dtype"] == "date":
            with col5:
                start_date =st.date_input(
                    f"Start Date ({col['name']})", key=f"start_date_{table_name}_{i}")
                col["start_date"] = start_date
            with col6:
                end_date = st.date_input(
                    f"End Date ({col['name']})", key=f"end_date_{table_name}_{i}")
                col["end_date"] = end_date
    st.divider()

# Generate Fake Data Section
st.subheader("🔄 Generate Data")
if st.button("Click to View Synthetic Data"):
    for table_id, table_data in st.session_state.tables.items():
        rows = table_data["rows"]
        columns = table_data["columns"]
        fake_data = []

        for _ in range(rows):
            row = {}
            for col in columns:
                if col["dtype"] == "name":
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
                elif col["dtype"] == "address":
                    row[col["name"]] = faker.address()
                elif col["dtype"] == "city":
                    row[col["name"]] = faker.city()
                elif col["dtype"] == "M/F":
                    row[col["name"]] = random.choice(["M", "F"])
                elif col["dtype"] == "Yes/No":
                    row[col["name"]] = random.choice(["Yes", "No"])
                elif col["dtype"] == "1/0":
                    row[col["name"]] = random.choice([1, 0])
                elif col["dtype"] == "region":
                    row[col["name"]] = faker.bothify("Region_##")
                elif col["dtype"] == "country":
                    row[col["name"]] = faker.country()
                elif col["dtype"] == "state":
                    row[col["name"]] = faker.state()
                elif col["dtype"] == "email":
                    name_parts = name.lower().replace(".", "").split()
                    email = f"{name_parts[0]}.{name_parts[-1]}@domain.com"
                    row[col["name"]] = email
                elif col["dtype"] == "phone_numbers":
                    row[col["name"]] = faker.phone_number()
                elif col["dtype"] == "zip_code":
                    row[col["name"]] = faker.zipcode()
                elif col["dtype"] == "status_flags":
                    row[col["name"]] = random.choice(["Active", "Inactive"])
                elif col["dtype"] == "age":
                    row[col["name"]] = faker.random_int(min=0, max=100)
                elif col["dtype"] == "product_name":
                    row[col["name"]] = faker.bs()
                elif col["dtype"] == "ratings":
                    row[col["name"]] = round(random.uniform(1, 5), 1)

            fake_data.append(row)

        st.session_state.tables[table_id]["data"] = pd.DataFrame(fake_data)
        df = pd.DataFrame(fake_data)
        st.dataframe(df.head())

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
