# app.py
import streamlit as st
import pandas as pd

st.set_page_config(page_title="KPI Dashboard", layout="wide")
st.title("Business KPI Dashboard")

uploaded = st.file_uploader("Upload Orders CSV", type=["csv"])

@st.cache_data
def load_data(file):
    df = pd.read_csv(file, parse_dates=["date"])
    df["revenue"] = df["units"] * df["unit_price"]
    return df

if uploaded:
    df = load_data(uploaded)
    with st.sidebar:
        st.header("Filters")
        regions = ["All"] + sorted(df["region"].dropna().unique().tolist())
        region = st.selectbox("Region", regions)
        date_min, date_max = df["date"].min(), df["date"].max()
        date_range = st.date_input("Date Range", (date_min, date_max))

    # Filter
    d1, d2 = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    f = (df["date"].between(d1, d2))
    if region != "All":
        f &= (df["region"] == region)
    view = df.loc[f].copy()

    # KPIs
    total_rev = view["revenue"].sum()
    orders = view["order_id"].nunique()
    avg_order = total_rev / max(orders, 1)

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Revenue", f"${total_rev:,.0f}")
    c2.metric("Orders", f"{orders:,}")
    c3.metric("Avg Order Value", f"${avg_order:,.2f}")

    # Charts
    rev_by_date = view.groupby(view["date"].dt.to_period("D"))["revenue"].sum().reset_index()
    rev_by_date["date"] = rev_by_date["date"].dt.to_timestamp()
    st.subheader("Revenue Over Time")
    st.line_chart(rev_by_date, x="date", y="revenue")

    st.subheader("Revenue by Product")
    rev_by_prod = view.groupby("product", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False)
    st.bar_chart(rev_by_prod, x="product", y="revenue")

    # Details
    with st.expander("Show sample rows"):
        st.dataframe(view.head(50), use_container_width=True)
else:
    st.info("Upload a CSV to get started. Expected columns: order_id, date, region, product, units, unit_price.")
