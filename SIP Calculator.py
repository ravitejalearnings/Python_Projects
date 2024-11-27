import streamlit as st

# Title of the application
st.title("💰 SIP Calculator")
st.divider()

# Create a 2x2 grid layout for inputs
row1 = st.columns(2)
row2 = st.columns(2)

# Input fields in the grid
with row1[0]:
    investments = st.number_input("Monthly Investment (₹)", min_value=100, max_value=1000000, step=100)
with row1[1]:
    err = st.number_input("Expected Return Rate (p.a.) (%)", min_value=1.0, max_value=50.0, step=0.1, format="%.1f")
with row2[0]:
    yrs = st.number_input("Time Period (Years)", min_value=1, max_value=50, step=1)

st.divider()

# Calculate SIP final value if inputs are provided
if investments and err and yrs:
    # Convert annual return rate to monthly and calculate the number of months
    monthly_rate = err / 12 / 100
    months = yrs * 12

    # SIP formula: FV = P * ((1 + r)^n - 1) / r * (1 + r)
    final_value = investments * (((1 + monthly_rate) ** months - 1) / monthly_rate) * (1 + monthly_rate)

    # Display the result
    st.write("### SIP Results")
    st.write(f"💼 Total Investment: ₹{investments * months:,.2f}")
    st.write(f"📈 Estimated Returns: ₹{final_value - (investments * months):,.2f}")
    st.write(f"💵 Total Value: ₹{final_value:,.2f}")


