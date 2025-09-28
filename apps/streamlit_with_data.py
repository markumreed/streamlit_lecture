import streamlit as st
import pandas as pd

# Example 1: Table
# df = pd.DataFrame({
#     "Products":["A","B","C"],
#    "Sales":[100,200, 300]
# })

# st.table(df)

# Example 2: Line Chart
# import numpy as np
# chart_data = pd.DataFrame(
#     np.random.randn(20,3),
#     columns = ["Product A","Product B","Product C"]
# )

# st.line_chart(chart_data)

# Example 3: Bar Chart
# st.bar_chart(df.set_index("Products"))

# File Uploads
uploaded = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded:
    data = pd.read_csv(uploaded)
    st.write("Preview of Data", data.head())