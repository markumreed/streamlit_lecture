import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Hello Streamlit", page_icon="📊", layout="wide")

st.title("Hello, Streamlit")
st.write("This is a simple interactive app.")

# Widget
discount = st.slider("Discount (%)", 0, 50, 10)

# Data
df = pd.DataFrame({
    "price": np.random.randint(50, 200, 20)
})
df["price_after_discount"] = df["price"] * (1 - discount/100)

st.subheader("Sample Data")
st.dataframe(df)

st.bar_chart(df.set_index(df.index)["price_after_discount"])
