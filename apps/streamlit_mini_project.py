# import pandas as pd
# import numpy as np
# import streamlit as st

# st.title("Mini Sales Dashboard")

# # Upload data
# uploaded = st.file_uploader("Upload Sales CSV", type=["csv"])

# if uploaded:
#     df = pd.read_csv(uploaded)
#     df['revenue'] = df['units'] * df["unit_price"]
#     st.write("Data Preview:", df.head())

#     # Filters
#     all_regions = df['region'].unique().tolist()
#     region = st.sidebar.selectbox("Region", ["All"] + all_regions)
#     if region != "All":
#         df = df[df["region"]== region]
    
#     # KPIs
#     st.metric("Total Revenue:", f"${df['revenue'].sum():,.2f}")
#     st.metric("Orders",len(df))

#     # Chart: Revenue by day

#     by_day = df.groupby("date", as_index=False)['revenue'].sum().sort_values('date')
#     st.line_chart(by_day, x="date",y="revenue")