import streamlit as st
import pandas as pd

df = pd.DataFrame({"month": ["Jan","Feb","Mar"], "revenue":[12000, 14500, 13200]})

st.dataframe(df, use_container_width=True)
st.line_chart(df, x="month", y="revenue")   # quick charts

import altair as alt
chart = alt.Chart(df).mark_bar().encode(x="month", y="revenue")
st.altair_chart(chart, use_container_width=True)
