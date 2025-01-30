import numpy as np
import streamlit as st
import pandas as pd
from faker import Faker
import random
import zipfile
import io
import json

# Initialize Faker
faker = Faker()

# Ensure session state for tables is initialized
if "tables" not in st.session_state:
    st.session_state["tables"] = {}

# ==============================
# Main Data Generation Functions
# ==============================
def generate_synthetic_data(table_config):
    rows = table_config["rows"]
    columns = table_config["columns"]
    fake_data = []

    for row_index in range(1, rows + 1):
        row = {}
        for col in columns:
            null_chance = col.get("null_percentage", 0) / 100
            if col["nullable"] and random.random() < null_chance:
                row[col["name"]] = None
            elif col["dtype"] == "index":
                row[col["name"]] = row_index
            elif col["dtype"] == "name":
                name = faker.name()
                row[col["name"]] = name
            elif col["dtype"] == "number":
                row[col["name"]] = faker.random_int(
                    min=int(col.get("min", 0)), max=int(col.get("max", 100))
                )
            elif col["dtype"] == "float":
                row[col["name"]] = round(
                    faker.random.uniform(col.get("min", 0), col.get("max", 100)), 2
                )
            elif col["dtype"] == "contains":
                custom_values = [value.strip() for value in col["custom_values"].split(",") if value.strip()]
                row[col["name"]] = random.choice(custom_values) if custom_values else None
            elif col["dtype"] == "custom":
                custom_values = [value.strip() for value in col["custom_examples"].split(",") if value.strip()]
                row[col["name"]] = random.choice(custom_values) if custom_values else "No Custom Value"
            elif col["dtype"] == "date":
                row[col["name"]] = faker.date_between(
                    start_date=col.get("start_date"), end_date=col.get("end_date")
                )
            elif col["dtype"] == "alphanumeric":
                row[col["name"]] = faker.bothify(text="??##")
            elif col["dtype"] == "city":
                row[col["name"]] = faker.city()
            elif col["dtype"] == "email":
                fake_name = faker.name()  # Generate a fake name if not already defined
                name_parts = fake_name.lower().replace(".", "").split()
                row[col["name"]] = f"{name_parts[0]}.{name_parts[-1]}@domain.com"
        fake_data.append(row)

    return pd.DataFrame(fake_data)


def validate_table_config(table_config):
    for col in table_config["columns"]:
        if not col["nullable"] and col["dtype"] in ["contains", "custom"]:
            custom_values = [value.strip() for value in col.get("custom_values", "").split(",") if value.strip()]
            if not custom_values and col["dtype"] == "contains":
                st.error(f"Error: Column '{col['name']}' must have valid values or be nullable.")
                return False
            if col["dtype"] == "custom":
                custom_examples = [value.strip() for value in col.get("custom_examples", "").split(",") if value.strip()]
                if not custom_examples:
                    st.error(f"Error: Column '{col['name']}' must have valid examples.")
                    return False
        if col["dtype"] in ["number", "float"]:
            if col["max"] < col["min"]:
                st.error(f"Error: Max value for column '{col['name']}' cannot be less than Min value.")
                return False
        if col["dtype"] == "date":
            if col.get("end_date") and col.get("start_date") and col["end_date"] < col["start_date"]:
                st.error(f"Error: End Date for column '{col['name']}' cannot be earlier than Start Date.")
                return False
    return True


def prepare_config_for_saving(tables):
    clean_config = {}
    for table_name, config in tables.items():
        clean_table = config.copy()
        if "data" in clean_table:
            del clean_table["data"]
        clean_config[table_name] = clean_table
    return clean_config


# ==============================
# Streamlit Interface
# ==============================

# Title
st.title("🛠️ Synthetic Data Generator")
# Toggle Show/Hide Description
if "show_description" not in st.session_state:
    st.session_state.show_description = True

if st.button("Show/Hide Description"):
    st.session_state.show_description = not st.session_state.show_description

# Description Section
if st.session_state.show_description:
    st.markdown("""
    ### Welcome to the Synthetic Data Generator!
    This tool allows you to easily create synthetic data for testing, prototyping, or educational purposes. 
    You can define multiple tables with various columns and data types, customize constraints, and generate
    data files in CSV format.

    #### Features:
    - **Configurable Tables**: Define multiple tables with custom columns, data types, and constraints.
    - **Nullable Columns**: Specify the percentage of null values for any column.
    - **Save/Load Configurations**: Save your table configurations as a JSON file and reload them later.
    - **Data Previews**: Preview generated data directly within the app.
    - **Batch Downloads**: Download all generated tables in a single ZIP file.

    #### Supported Data Types:
    - **Number**: Integer values within a specified range.
    - **Float**: Decimal values within a specified range.
    - **Date**: Dates between a specified start and end date.
    - **Contains**: Predefined custom values (comma-separated).
    - **Alphanumeric**: Random strings with letters and numbers.
    - **Name, City, Email**: Fake but realistic names, city names, and email addresses.

    #### Note:
    You can load a previously saved configuration file via the sidebar to quickly restore your settings.
    """)
    st.divider()
# Save and Load Configuration
st.sidebar.title("🔄 Save and Load Configuration")
if st.sidebar.button("Save Configuration"):
    config_to_save = prepare_config_for_saving(st.session_state.tables)
    config_json = json.dumps(config_to_save, indent=4)
    st.sidebar.download_button(
        label="Download Configuration",
        data=config_json,
        file_name="table_config.json",
        mime="application/json",
    )

uploaded_file = st.sidebar.file_uploader("Load Configuration", type=["json"])
if uploaded_file is not None:
    loaded_config = json.load(uploaded_file)
    st.session_state.tables = loaded_config
    st.sidebar.success("Configuration loaded successfully!")

# Table Management
st.subheader("📑 Manage Tables")
col1, col2 = st.columns(2)
with col1:
    if st.button("➕ Add Table"):
        table_id = f"Table_{len(st.session_state.tables) + 1}"
        st.session_state.tables[table_id] = {
            "columns": [{"name": "index", "dtype": "index", "null_percentage": 0}],
            "rows": 10,
            "metadata": None
        }

with col2:
    if st.button("➖ Remove Table") and st.session_state.tables:
        st.session_state.tables.popitem()

# Table Configuration
for table_name, table_config in st.session_state.tables.items():
    st.markdown(f"### 📝 Configure Table: `{table_config.get('name', table_name)}`")
    new_name = st.text_input(f"Table Name", value=table_config.get("name", table_name), key=f"table_name_{table_name}")
    row_count = st.number_input(f"Rows for `{new_name}`", min_value=1, max_value=50000, step=1, key=f"rows_{table_name}")
    st.session_state.tables[table_name]["rows"] = row_count
    st.session_state.tables[table_name]["name"] = new_name



    # Column Configuration
    for i, col in enumerate(table_config["columns"]):
        col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 2, 2, 2])
        with col1:
            col["name"] = st.text_input(f"Column Name", value=col["name"], key=f"{table_name}_col_name_{i}")
        with col2:
            col["dtype"] = st.selectbox(
                "Data Type",
                ["number", "float", "date", "name", "city", "email", "contains", "index"],
                index=0,
                key=f"{table_name}_col_dtype_{i}",
            )
        with col3:
            col["nullable"] = st.checkbox(
                "Nullable",
                value=col.get("nullable", False),
                key=f"{table_name}_nullable_{i}",
                disabled=(col["dtype"] == "index"),  # Disable for Index format
            )
        with col4:
            col["null_percentage"] = st.slider(
                "Null %",
                0,
                100,
                value=int(col.get("null_percentage", 0)),
                key=f"{table_name}_null_percentage_{i}",
                disabled=(col["dtype"] == "index"),  # Disable for Index format
            )

        # Additional Config
        if col["dtype"] in ["number", "float"]:
            with col5:
                col["min"] = st.number_input("Min Value", value=float(col.get("min", 0.0)), step=1.0, key=f"{table_name}_col_min_{i}")
            with col6:
                col["max"] = st.number_input("Max Value", value=float(col.get("max", 0.0)), step=1.0, key=f"{table_name}_col_max_{i}")
        elif col["dtype"] == "contains":
            with col5:
                col["custom_values"] = st.text_input("Contains Values (comma-separated)", value=col.get("custom_values", ""), key=f"{table_name}_col_custom_values_{i}")
        elif col["dtype"] == "custom":
            with col5:
                col["custom_examples"] = st.text_input("Custom Examples (comma-separated)", value=col.get("custom_examples", ""), key=f"{table_name}_col_custom_examples_{i}")
        elif col["dtype"] == "date":
            with col5:
                col["start_date"] = st.date_input("Start Date", key=f"{table_name}_col_start_date_{i}")
            with col6:
                col["end_date"] = st.date_input("End Date", key=f"{table_name}_col_end_date_{i}")

        # Move Buttons BELOW the column configurations
    st.markdown("---")  # Adds a separator for better UI
    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"➕ Add Column for `{new_name}`", key=f"add_col_{table_name}"):
            table_config["columns"].append({"name": "", "dtype": "number", "min": 0, "max": 1, "nullable": False, "null_percentage": 0})
    with col2:
        if st.button(f"➖ Remove Column for `{new_name}`", key=f"remove_col_{table_name}") and table_config["columns"]:
            table_config["columns"].pop()

    st.divider()

# Generate Data
st.subheader("🔄 Generate Data")
if st.button("Generate Data"):
    for table_name, table_config in st.session_state.tables.items():
        if validate_table_config(table_config):
            st.session_state.tables[table_name]["data"] = generate_synthetic_data(table_config)
            st.success(f"Data generated for table `{table_config.get('name', table_name)}`!")
            st.markdown(f"**Preview of `{table_config.get('name', table_name)}`:**")

            # Display the preview
            df = st.session_state.tables[table_name]["data"]
            st.dataframe(df.reset_index(drop=True))  # Remove index column

# Download Data
st.subheader("⏬ Download Data")
if st.button("Download All Tables"):
    if not st.session_state.tables:
        st.error("No tables available for download.")
    else:
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for table_name, table_config in st.session_state.tables.items():
                if "data" in table_config:
                    csv_data = table_config["data"].to_csv(index=False)
                    zip_file.writestr(f"{table_config.get('name', table_name)}.csv", csv_data)
        zip_buffer.seek(0)
        st.download_button("Download ZIP", data=zip_buffer, file_name="synthetic_data.zip", mime="application/zip")
