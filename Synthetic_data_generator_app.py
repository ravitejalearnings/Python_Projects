import streamlit as st
import pandas as pd
from faker import Faker
import random

# Initialize Faker
faker = Faker()

# App Title
st.title("🛠️ Synthetic Data Generator App")
st.divider()

# App Description
st.markdown("""
Purpose: Generate synthetic data for testing, prototyping, or educational purposes. Define columns, choose data types, and download the output in your desired format.
""")

# Prerequisites Section
with st.expander("ℹ️ Supported Data Formats", expanded=False):
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
st.write("### Define Your Table Structure")
st.write("###### Create columns based on your need")


# Initialize session state to store columns
if "columns" not in st.session_state:
    st.session_state.columns = []

# Function to add a new row with column name and data type
def add_column():
    st.session_state.columns.append({"name": "", "dtype": "number", "min": 0, "max": 1})

# Function to remove the last column
def remove_column():
    if st.session_state.columns:
        st.session_state.columns.pop()

# Add "Add Column" and "Remove Column" buttons
col1, col2 = st.columns(2)
with col1:
    st.button("+ Add Column", on_click=add_column)
with col2:
    st.button("- Remove Column", on_click=remove_column)


# Define data formats
diff_formats = ["number", "float", "date", "name", "alphanumeric", "address",
                "city", "M/F","Yes/No","1/0","region","country","state","city",
                "email","phone_numbers","zip_code","status_flags","age",
                "sku","percentages","ratings","levels","product_name"]

# Dynamic input for columns

for i, col in enumerate(st.session_state.columns):
    col1, col2, col3, col4 = st.columns([3, 3, 2, 2])
    with col1:
        st.session_state.columns[i]["name"] = st.text_input(
            f"Col_name", value=col["name"], key=f"col_name_{i}", placeholder="Enter column name")
    with col2:
        st.session_state.columns[i]["dtype"] = st.selectbox(
            "format", diff_formats,
            index=diff_formats.index(col["dtype"]),
            key=f"col_dtype_{i}",)

    # Additional Min and Max Input for Numeric Data
    if (col["dtype"] == "number" or
            col["dtype"] == "ratings" or
            col["dtype"] == "float" or
            col["dtype"] == "age" or
            col["dtype"] == "levels"):
        with col3:
            st.session_state.columns[i]["min"] = st.number_input(
                f"Min ({col['name']})", value=0, key=f"min_val_{i}", step=1)
        with col4:
            st.session_state.columns[i]["max"] = st.number_input(
                f"Max ({col['name']})", value=1, key=f"max_val_{i}", step=1)

st.divider()
# Display metadata table
if st.session_state.columns:
    st.write("### Table Metadata")
    metadata = pd.DataFrame(st.session_state.columns)
    st.dataframe(metadata)
else:
    st.warning("Please define at least one column to generate data.")

# User Input for Number of Rows
row_count = st.number_input("Number of Rows", min_value=1, max_value=1000, step=1)

# Generate Fake Data
if st.button("Generate Synthetic Data"):
    if not st.session_state.columns:
        st.error("No columns defined. Please add at least one column.")
    else:
        # Create fake data based on the metadata
        fake_data = []
        for _ in range(row_count):
            row = {}
            for col in st.session_state.columns:
                # if col["dtype"] == "text":
                #     row[col["name"]] = faker.word()
                if col["dtype"] == "name":
                    name = faker.name()
                    row[col["name"]] = name
                elif col["dtype"] == "number":
                    min_val = col.get("min", 0)
                    max_val = col.get("max", 100)
                    row[col["name"]] = faker.random_int(min=min_val, max=max_val)
                elif col["dtype"] == "float":
                    row[col["name"]] = round(faker.random.uniform(0.0, 100.0), 2)
                elif col["dtype"] == "date":
                    row[col["name"]] = faker.date_this_century()
                elif col["dtype"] == "alphanumeric":
                    row[col["name"]] = faker.bothify(text=random.choice(['##??', '??##', '#?#?', '???']))
                elif col["dtype"] == "address":
                    row[col["name"]] = faker.address()
                elif col["dtype"] == "city":
                    row[col["name"]] = faker.city()
                elif col["dtype"] == "M/F":
                    row[col["name"]] = random.choice(['M', 'F'])
                elif col["dtype"] == "Yes/No":
                    row[col["name"]] = random.choice(['Y', 'N'])
                elif col["dtype"] == "1/0":
                    row[col["name"]] = random.choice([1, 0])
                elif col["dtype"] == "region":
                    row[col["name"]] = faker.bothify(text=random.choice(['reg_##']))
                elif col["dtype"] == "country":
                    row[col["name"]] = faker.bothify(text=random.choice(['country_###']))
                elif col["dtype"] == "state":
                    row[col["name"]] = faker.bothify(text=random.choice(['state_###']))
                elif col["dtype"] == "city":
                    row[col["name"]] = faker.bothify(text=random.choice(['city_###']))
                elif col["dtype"] == "email":
                    name_parts = name.lower().replace(".", "").split()
                    email = f"{name_parts[0]}.{name_parts[-1]}@domain.com"
                    row[col["name"]] = email
                elif col["dtype"] == "phone_numbers":
                    row[col["name"]] = faker.bothify(text=random.choice(['###-###-#####']))
                elif col["dtype"] == "zip_code":
                    row[col["name"]] = faker.bothify(text=random.choice(['###-###']))
                elif col["dtype"] == "status_flags":
                    row[col["name"]] = faker.bothify(text=random.choice(['Active','Inactive']))
                elif col["dtype"] == "age":
                    row[col["name"]] = faker.random_int(min=0,max=100)
                elif col["dtype"] == "product_name":
                    row[col["name"]] = faker.bothify(text=random.choice(['product_###']))
                elif col["dtype"] == "ratings":
                    min_val = col.get("min", 0)
                    max_val = col.get("max", 5)
                    row[col["name"]] = faker.random_int(min=min_val, max=max_val)

            fake_data.append(row)

        # Convert to DataFrame
        df = pd.DataFrame(fake_data)
        st.divider()

        # Display fake data
        st.write("### Generated Synthetic Data")
        st.dataframe(df)

        # Download fake data as CSV
        csv = df.to_csv(index=False)
        st.download_button("Download Fake Data", data=csv, file_name="fake_data.csv", mime="text/csv")