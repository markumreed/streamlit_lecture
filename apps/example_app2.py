import streamlit as st

name = st.text_input("Customer Name", placeholder="Acme Corp")
qty  = st.number_input("Quantity", min_value=1, value=10)
price = st.number_input("Unit Price ($)", min_value=0.0, value=19.99)
confirm = st.button("Add to Cart")

if confirm:
    st.success(f"Added {qty} x ${price:.2f} for {name}")

with st.form("order_form"):
    sku = st.text_input("SKU")
    qty = st.number_input("Qty", 1, 100, 5)
    submitted = st.form_submit_button("Submit Order")
if submitted:
    st.success(f"Order placed for {sku} x {qty}")
