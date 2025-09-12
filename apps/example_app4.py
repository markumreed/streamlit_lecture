import streamlit as st
import pandas as pd

uploaded = st.file_uploader("Upload CSV", type=["csv"])
if uploaded:
    df = pd.read_csv(uploaded)
    st.success(f"Loaded {len(df):,} rows")
    st.dataframe(df.head())
