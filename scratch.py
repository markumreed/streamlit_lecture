import streamlit as st # getting streamlit
import pandas as pd
df = pd.read_csv("data/orders_large.csv")
df["date"] = pd.to_datetime(df["date"])
df["revenue"] = df["units"] * df["unit_price"]
regions = ["All"] + sorted(df["region"].unique().tolist())
products = ["All"] + sorted(df["product"].unique().tolist())

st.title("Layout Example")
st.sidebar.header("Filters")
region = st.sidebar.selectbox("Select Region", regions)
product = st.sidebar.selectbox("Select Product", products)
date_range = st.sidebar.date_input("Date Range", (df["date"].min(), df["date"].max()))
filtered = df.copy()

if region != "All":
    filtered = filtered[filtered["region"] == region]
if product != "All":
    filtered = filtered[filtered["product"] == product]

filtered = filtered[filtered["date"].between(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1]))]

total_revenue = filtered["revenue"].sum()
total_units = int(filtered["units"].sum())
orders = len(filtered)
avg_order_value = total_revenue / orders

c1, c2, c3 = st.columns(3)
c1.metric("Total Revenue", f"${total_revenue:,.2f}")
c2.metric("Units Sold", f"{total_units:,}")
c3.metric("Avg Order Value", f"${avg_order_value:,.2f}")

tab1, tab2 = st.tabs(["Summary", "Details"])
tab1.write("Overview of key results.")
tab2.write("Detailed data breakdown here.")

st.title("Interactive Sales Dashboard")



