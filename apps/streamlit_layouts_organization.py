# import streamlit as st
# import pandas as pd
# import numpy as np


# # Example 1: Sidebar
# st.title("My Dashboard")
# # option = st.sidebar.selectbox("Choose View", ["Overview", "Details"])

# # st.write("You picked:", option)

# # Example 2: Columns

# # col1, col2 = st.columns(2)
# # col1.write("Left Column")
# # col2.write("Right Column")

#  # Example 3: Metrics

# # col1, col2 = st.columns(2)

# # with col1:
# #     st.metric("Sales","200K")

# # with col2:
# #     st.metric("Profit","50k")

# # Column Chart Example

# chart_data = pd.DataFrame(
#     np.random.randn(20,3),
#     columns = ["Product A","Product B","Product C"]
# )

# # Create up two equal-width columns
# col1, col2 = st.columns(2)

# with col1:
#     st.header("Bar Chart")
#     st.bar_chart(chart_data)

# with col2:
#     st.header("Line Chart")
#     st.line_chart(chart_data)