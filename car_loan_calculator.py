import streamlit as st

# App Title
st.title("🚗 Car Buying Calculator")

# Creating a 2x2 grid for input parameters
col1, col2 = st.columns(2)

with col1:
    salary = st.number_input(
        '💰 Salary Per Month (₹)',
        min_value=10000.0,
        max_value=1000000.0,
        step=1000.0,
        format="%.1f"
    )
    interest = st.number_input(
        "📉 Rate of Interest on the Loan (%)",
        min_value=6.0,
        max_value=20.0,
        step=0.1,
        format="%.1f"
    )

with col2:
    emi = st.number_input(
        "📊 Percentage of Salary for EMI (%)",
        min_value=10.0,
        max_value=100.0,
        step=0.1,
        format="%.1f"
    )
    years = st.number_input(
        "📅 Number of Years for Loan",
        min_value=1.0,
        max_value=15.0,
        step=0.1,
        format="%.1f"
    )

# Calculations
max_monthly_emi = round((salary * (emi / 100)), 2)
vehicle_amount = round((salary * 12 * years * (20 / 100)), 2)
down_payment = round(vehicle_amount * (20 / 100), 2)
loan_amount = round(vehicle_amount - down_payment, 2)

# Display Results
if st.button("📊 Click to View Results"):
    # st.subheader(" Results")
    st.write(f"**Vehicle Amount:** ₹{vehicle_amount:,}")
    st.write(f"**Maximum Monthly EMI:** ₹{max_monthly_emi:,}")
    st.write(f"**Down Payment:** ₹{down_payment:,}")
    st.write(f"**Loan Amount:** ₹{loan_amount:,}")

# Adding an informative footer
st.markdown(
    """
    ---
    *Use this tool to calculate your car affordability based on your financial capacity.*
    """
)




