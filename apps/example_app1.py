import streamlit as st

st.title("Layout Demo")

# Sidebar
with st.sidebar:
    st.header("Controls")
    region = st.selectbox("Region", ["North", "South", "East", "West"])
    show_raw = st.checkbox("Show raw data")

# Columns
left, right = st.columns([1,2])
left.metric("Active Users", 1243, delta=+35)
right.info(f"Selected region: {region}")

# Tabs
tab1, tab2 = st.tabs(["Summary", "Details"])
with tab1:
    st.write("KPIs, charts…")
with tab2:
    st.write("Tables, explanations…")
