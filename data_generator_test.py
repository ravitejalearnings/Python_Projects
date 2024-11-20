# Import libraries
import pandas as pd
import streamlit as st
from faker import Faker
import random
from datetime import datetime
from random import randint

# Initialize the Faker generator for 'en_IN' locale
fake = Faker()
# 'en_IN'
# Title of the app
st.title("Synthetic Data Generator")
st.divider()

# Purpose & Use Case Description
st.write("## Purpose:")
st.write(
    "This application enables users to generate realistic synthetic datasets tailored to various domains, "
    "such as HR, Retail, and Supply Chain. It allows for domain selection, customization of datasets by "
    "choosing relevant features, and the creation of data that closely replicates real-world scenarios."
)
st.divider()

# Domain selection
choose_domain = st.selectbox("Choose Domain", ["Retail", "HR", "Supply_Chain"])

# Grid layout for input
row1 = st.columns(1)
row2 = st.columns(1)

# Domain feature options
retail_features = [
    "Product_ID", "Product_Name", "Product_Category", "Product_Subcategory", "Brand",
    "Supplier_ID", "Supplier_Name", "Store_ID", "Store_Name", "Store_Location", "Customer_ID",
    "Customer_Name", "Customer_Age", "Customer_Gender", "Customer_Segment", "Transaction_ID",
    "Transaction_Date", "Quantity_Sold", "Price"]

hr_features = [
    'EmployeeID', 'Name', 'Age', 'Gender', 'MaritalStatus', 'Department', 'JobTitle', 'ManagerID',
    'HireDate', 'YearsInCompany', 'YearsInCurrentRole', 'PreviousCompanyExperience', 'EducationLevel',
    'Salary', 'WorkLocation']

supply_chain_features = ["Order_ID","Customer_ID","Product_ID","Supplier_ID","Warehouse_ID","Shipping_Method","Transporter_Name",
"Shipment_ID","Destination_Country","Destination_City","Source_Country","Source_City","Product_Category","Product_Subcategory",
"Order_Channel","Payment_Method","Shipping_Priority","Route_ID","Carrier_ID","Packaging_Type",
"Order_Status","Shipment_Status",
"Delivery_Type",  # E.g., Express, Standard
"Return_Status","Container_Type",  # E.g., Small, Medium, Large
"SKU",  # Stock Keeping Unit,
"Distribution_Center_ID"]


# Feature selection based on domain
def domain_features(choose_domain):
    if choose_domain == 'Retail':
        return retail_features
    elif choose_domain == 'HR':
        return hr_features
    elif choose_domain == 'Supply_Chain':
        return supply_chain_features
    return []

if choose_domain == 'Retail':
    min_value, max_value = 100, 50000
elif choose_domain == 'HR':
    min_value, max_value = 100, 501
elif choose_domain == 'Supply_Chain':
    min_value, max_value = 100, 50000
else:
    # Default case for other domains
    min_value, max_value = 100, 50000

# Input: Number of rows and feature selection
with row1[0]:
    nrows = st.number_input("Choose N rows", min_value=min_value, max_value=max_value, step=1)
with row2[0]:
    selected_features = st.multiselect("Choose Columns", domain_features(choose_domain))

# Predefined lists for domain-specific data
products = ['Product1', 'Product2', 'Product3']
Product_Categories = ['PC1', 'PC2', 'PC3', 'PC4', 'PC5']
Product_Subcategories = ['PSC1', 'PSC2', 'PSC3', 'PSC4', 'PSC5']
Brands = ['Brand1', 'Brand2', 'Brand3', 'Brand4', 'Brand5']
Supplier_names = ['Supplier1', 'Supplier2', 'Supplier3', 'Supplier4', 'Supplier5']
Store_Names = ['Store1', 'Store2', 'Store3', 'Store4', 'Store5']

# HR domain data
Department = ['BA', 'BI', 'Ops', 'DE', 'DS', 'Finance', 'DevOps']
JobTitle = ['Analyst', 'Consultant', 'Senior Consultant', 'Manager', 'Lead Manager', 'DoD']
WorkLocation = ['Bangalore', 'Noida', 'Chennai', 'Hyderabad', 'Kochi']
hire_date = datetime.strptime("2002-01-01", "%Y-%m-%d")
exit_date = datetime.strptime("2024-12-31", "%Y-%m-%d")

# Supply_chain data
Shipping_Method = ['Air','Ocean','Road']
Transporter_Name = ['TP1','TP2','TP3','TP4','TP5']
Source_Country = ['USA','Canada','Germany','India','Japan','Australia','Brazil','China','SA','UK']
Source_city = ['NY','Toronto','Berlin','Mumbai','Tokyo','Sydney','Paulo','Shanghai','Johannesburg','London']
Destination_Country = ['France','Italy','Mexico','Russia','Spain','UAE','SK','Singapore','Argentina','Netherlands']
Destination_city = ['Paris','Rome','Mexico','Moscow','Madrid','Dubai','Seoul','Singapore','Buenos','Amsterdam']
Product_Categories = ['PC1', 'PC2', 'PC3', 'PC4', 'PC5']
Product_Subcategories = ['PSC1', 'PSC2', 'PSC3', 'PSC4', 'PSC5']
Order_Channel = ['Third-party Logistics Partner','Corporate Portal']
Payment_Method = ['Online','offline']
Packaging_types = ["Box","Pallet","Drum","Plastic Wrap","Bubble Mailer"]
Delivery_types = ["Standard","Express","Same-Day"]
Container_Type = ['Small', 'Medium', 'Large']


# Retail data generation
start_date = datetime.strptime("2022-01-01", "%Y-%m-%d")
end_date = datetime.strptime("2024-12-31", "%Y-%m-%d")
def generate_retail_data(nrows):
    return {
        "Product_ID": [fake.numerify(text='#######') for _ in range(nrows)],
        "Product_Name": [random.choice(products) for _ in range(nrows)],
        "Product_Category": [random.choice(Product_Categories) for _ in range(nrows)],
        "Product_Subcategory": [random.choice(Product_Subcategories) for _ in range(nrows)],
        "Brand": [random.choice(Brands) for _ in range(nrows)],
        "Supplier_ID": [fake.bothify(text='#?#?') for _ in range(nrows)],
        "Supplier_Name": [random.choice(Supplier_names) for _ in range(nrows)],
        "Store_ID": [fake.bothify(text='#?#?') for _ in range(nrows)],
        "Store_Name": [random.choice(Store_Names) for _ in range(nrows)],
        "Store_Location": [fake.city() for _ in range(nrows)],
        "Customer_ID": [fake.bothify(text='#######???') for _ in range(nrows)],
        "Customer_Name": [fake.name() for _ in range(nrows)],
        "Customer_Age": [random.randint(18, 80) for _ in range(nrows)],
        "Customer_Gender": [random.choice(['M', 'F']) for _ in range(nrows)],
        "Transaction_ID": [fake.bothify(text='???####') for _ in range(nrows)],
        "Transaction_Date": [fake.date_between(start_date=start_date, end_date=end_date) for _ in range(nrows)],
        "Quantity_Sold": [random.randint(2, 100) for _ in range(nrows)],
        "Price": [random.randint(100, 1000) for _ in range(nrows)]
    }


# HR data generation
def generate_hr_data(nrows):
    return {
        'EmployeeID': [f"EMP{randint(1, 501)}" for _ in range(nrows)],
        'Name': [fake.name() for _ in range(nrows)],
        "Age": [random.randint(20, 60) for _ in range(nrows)],
        "Gender": [random.choice(['M', 'F']) for _ in range(nrows)],
        "MaritalStatus": [random.choice(['Y', 'N']) for _ in range(nrows)],
        "Department": [random.choice(Department) for _ in range(nrows)],
        "JobTitle": [random.choice(JobTitle) for _ in range(nrows)],
        "ManagerID": [f"EMP{randint(1, 31)}" for _ in range(nrows)],
        "HireDate": [fake.date_between(start_date=hire_date, end_date=exit_date) for _ in range(nrows)],
        "YearsInCompany": [fake.random_int(1, 10) for _ in range(nrows)],
        "YearsInCurrentRole": [fake.random_int(1, 5) for _ in range(nrows)],
        "PreviousCompanyExperience": [fake.random_int(1, 5) for _ in range(nrows)],
        "EducationLevel": [f"LVL{randint(1, 5)}" for _ in range(nrows)],
        "Salary": [fake.random_int(3, 100) for _ in range(nrows)],
        "WorkLocation": [random.choice(WorkLocation) for _ in range(nrows)]
    }

# Supply chain data generation
def generate_supply_chain_data(nrows):
    return{
        "Order_ID":[fake.numerify(text = "########") for _ in range(nrows)],
        "Customer_ID": [fake.bothify(text = "#?#?#?#?") for _ in range(nrows)],
        "Product_ID": [fake.bothify(text = "#?#?#?#?") for _ in range(nrows)],
        "Supplier_ID": [fake.bothify(text = "#?#?#?#?") for _ in range(nrows)],
        "Warehouse_ID": [fake.bothify(text = "#?#?#?#?") for _ in range(nrows)],
        "Shipping_Method": [random.choice(Shipping_Method) for _ in range(nrows)],
        "Transporter_Name": [random.choice(Transporter_Name) for _ in range(nrows)],
        "Shipment_ID":[fake.bothify(text = "#?#?#?#?") for _ in range(nrows)],
        "Destination_Country": [random.choice(Destination_Country) for _ in range(nrows)],
        "Destination_City": [random.choice(Destination_city) for _ in range(nrows)],
        "Source_Country": [random.choice(Source_Country) for _ in range(nrows)],
        "Source_City": [random.choice(Source_city) for _ in range(nrows)],
        "Product_Category": [random.choice(Product_Categories) for _ in range(nrows)],
        "Product_Subcategory": [random.choice(Product_Subcategories) for _ in range(nrows)],
        "Order_Channel": [random.choice(Order_Channel) for _ in range(nrows)],
        "Payment_Method":[random.choice([Payment_Method]) for _ in range(nrows)],
        "Shipping_Priority": [random.choice(['Y','N']) for _ in range(nrows)],
        "Route_ID": [fake.bothify(text = "000#?#?#?#?") for _ in range(nrows)],
        "Carrier_ID": [fake.bothify(text = "CA?#?#?") for _ in range(nrows)],
        "Packaging_Type": [random.choice(Packaging_types) for _ in range(nrows)],
        "Order_Status": [random.choice(['Y','N']) for _ in range(nrows)],
        "Shipment_Status": [random.choice(['Y','N']) for _ in range(nrows)],
        "Delivery_Type": [random.choice(Delivery_types) for _ in range(nrows)],
        "Return_Status": [random.choice(['Y','N']) for _ in range(nrows)],
        "Container_Type": [random.choice(Container_Type) for _ in range(nrows)],
        "SKU": [fake.bothify(text = "SKU#?#?#?#?") for _ in range(nrows)],
        "Distribution_Center_ID": [fake.numerify(text = "#######") for _ in range(nrows)]
    }


# Generate data based on selected domain
if choose_domain == 'Retail':
    retail_data_df = pd.DataFrame(generate_retail_data(nrows))
    st.write("Retail Data Preview")
    st.write(retail_data_df[selected_features].head() if selected_features else retail_data_df.head())
elif choose_domain == 'HR':
    hr_data_df = pd.DataFrame(generate_hr_data(nrows))
    st.write("HR Data Preview")
    st.write(hr_data_df[selected_features].head() if selected_features else hr_data_df.head())
else:
    Supply_chain_data_df = pd.DataFrame(generate_supply_chain_data(nrows))
    st.write("Supply Chain Data Preview")
    st.write(Supply_chain_data_df[selected_features].head() if selected_features else Supply_chain_data_df.head())

# Download option
st.divider()
# st.write("Click button below to download CSV file")

if choose_domain == 'Retail':
    if selected_features:
        st.download_button(
            label='Download Retail Data CSV',
            data=retail_data_df[selected_features].to_csv(index=False),
            file_name='retail_data.csv',
            mime='text/csv'
        )
    else:  # If no features are selected, download the entire Retail dataset
        st.download_button(
            label='Download Full Retail Data CSV',
            data=retail_data_df.to_csv(index=False),
            file_name='retail_data_full.csv',
            mime='text/csv'
        )
elif choose_domain == 'HR':
    if selected_features:
        st.download_button(
            label='Download HR Data CSV',
            data=hr_data_df[selected_features].to_csv(index=False),
            file_name='hr_data.csv',
            mime='text/csv'
        )
    else:  # If no features are selected, download the entire HR dataset
        st.download_button(
            label='Download Full HR Data CSV',
            data=hr_data_df.to_csv(index=False),
            file_name='hr_data_full.csv',
            mime='text/csv'
        )
elif choose_domain == 'Supply_Chain':
    if selected_features:
        st.download_button(
            label='Download Supply Chain Data CSV',
            data=Supply_chain_data_df[selected_features].to_csv(index=False),
            file_name='Supply_chain_data.csv',
            mime='text/csv'
        )
    else:  # If no features are selected, download the entire HR dataset
        st.download_button(
            label='Download Full Supply Chain CSV',
            data=Supply_chain_data_df.to_csv(index=False),
            file_name='Supply_Chain_data_full.csv',
            mime='text/csv'
        )
else:
    None
