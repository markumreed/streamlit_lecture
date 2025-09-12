# app.py — Solution Branch
import io
import pandas as pd
import numpy as np
import streamlit as st
from datetime import timedelta

st.set_page_config(page_title="Sales Snapshot — Solution", layout="wide")
st.title("Sales Snapshot — Solution")
st.caption("Upload a CSV, filter by date/region/product, and explore KPIs, trends, and top products. Includes stretch goals.")

# =========================
# 1) Upload & Preparation
# =========================

uploaded = st.file_uploader("Upload Orders CSV", type=["csv"])

REQUIRED_COLS = {"date", "region", "product", "units", "unit_price"}

@st.cache_data(show_spinner=False)
def prepare(raw_csv) -> pd.DataFrame:
    """
    Reads CSV-like input and returns a cleaned DataFrame with:
    - normalized column names
    - parsed types (date, numeric)
    - computed 'revenue'
    Requires at least: date, region, product, units, unit_price
    """
    if isinstance(raw_csv, (io.BytesIO, io.StringIO)):
        df = pd.read_csv(raw_csv)
    else:
        df = pd.read_csv(raw_csv)

    # Normalize headers
    df.columns = [c.strip().lower() for c in df.columns]
    missing = REQUIRED_COLS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required column(s): {', '.join(sorted(missing))}")

    # Types
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["units"] = pd.to_numeric(df["units"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")

    # Drop incomplete rows
    df = df.dropna(subset=["date", "region", "product", "units", "unit_price"])

    # Feature
    df["revenue"] = df["units"] * df["unit_price"]

    # Sort for predictable behavior
    return df.sort_values("date").reset_index(drop=True)

if not uploaded:
    st.info("Upload a CSV to begin. Required columns (case-insensitive): "
            "`date, region, product, units, unit_price`. Optional: `order_id`.")
    with st.expander("Example rows"):
        st.code("""order_id,date,region,product,units,unit_price
10001,2024-01-03,North,Widget,3,14.50
10002,2024-01-03,West,Gadget,2,29.00
10003,2024-01-04,South,Thingamajig,5,9.99
""", language="csv")
    st.stop()

try:
    df = prepare(uploaded)
    st.success("CSV loaded.")
except Exception as e:
    st.error(f"Could not read CSV: {e}")
    st.stop()

# =========================
# 2) Sidebar Filters
# =========================

st.sidebar.header("Filters")

# Date range defaults to min/max in data
dmin, dmax = df["date"].min().date(), df["date"].max().date()
date_range = st.sidebar.date_input(
    "Date range",
    (dmin, dmax),
    min_value=dmin,
    max_value=dmax
)
if isinstance(date_range, tuple):
    start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
else:
    start_date = end_date = pd.to_datetime(date_range)

# Region multiselect (default: all)
all_regions = sorted(df["region"].dropna().unique().tolist())
regions = st.sidebar.multiselect("Region", options=all_regions, default=all_regions)

# Product multiselect (default: all) — Stretch Goal
all_products = sorted(df["product"].dropna().unique().tolist())
products = st.sidebar.multiselect("Product", options=all_products, default=all_products)

# Apply filters
mask = (
    df["date"].between(start_date, end_date)
    & df["region"].isin(regions)
    & df["product"].isin(products)
)
f = df.loc[mask].copy()

if f.empty:
    st.warning("No rows match your filters. Try expanding the date range or selecting more regions/products.")
    st.stop()

# =========================
# 3) KPIs (with delta)
# =========================

# Current period stats
total_revenue = float(f["revenue"].sum())
units_sold = int(f["units"].sum())
orders = f["order_id"].nunique() if "order_id" in f.columns else len(f)
aov = (total_revenue / orders) if orders else 0.0

# Prior period: same length immediately before start_date — Stretch Goal
period_days = max(1, (end_date.date() - start_date.date()).days + 1)
prev_start = start_date - timedelta(days=period_days)
prev_end = start_date - timedelta(days=1)

prev_mask = (
    df["date"].between(prev_start, prev_end)
    & df["region"].isin(regions)
    & df["product"].isin(products)
)
prev = df.loc[prev_mask]

prev_revenue = float(prev["revenue"].sum()) if not prev.empty else 0.0
prev_units = int(prev["units"].sum()) if not prev.empty else 0
prev_orders = (prev["order_id"].nunique() if "order_id" in df.columns else len(prev)) if not prev.empty else 0
prev_aov = (prev_revenue / prev_orders) if prev_orders else 0.0

# Deltas
rev_delta = total_revenue - prev_revenue
units_delta = units_sold - prev_units
orders_delta = orders - prev_orders
aov_delta = aov - prev_aov

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Revenue", f"${total_revenue:,.2f}", delta=f"${rev_delta:,.2f}")
c2.metric("Units Sold", f"{units_sold:,}", delta=f"{units_delta:,}")
c3.metric("Orders", f"{orders:,}", delta=f"{orders_delta:,}")
c4.metric("Avg Order Value", f"${aov:,.2f}", delta=f"${aov_delta:,.2f}")

st.divider()

# =========================
# 4) Visuals
# =========================

left, right = st.columns((2, 1), gap="large")

with left:
    st.subheader("Revenue Over Time")
    by_day = (
        f.groupby("date", as_index=False)["revenue"]
         .sum()
         .sort_values("date")
    )
    st.line_chart(by_day, x="date", y="revenue", height=300)

with right:
    st.subheader("Top Products by Revenue (Top 5)")
    top_prod = (
        f.groupby("product", as_index=False)["revenue"]
         .sum()
         .sort_values("revenue", ascending=False)
         .head(5)
    )
    if top_prod.empty:
        st.info("No product data after filters.")
    else:
        st.bar_chart(top_prod, x="product", y="revenue", height=300)

st.divider()

# =========================
# 5) Tables & Download
# =========================

tab1, tab2 = st.tabs(["Filtered Rows", "Region/Product Summary"])

with tab1:
    st.write("First 100 filtered rows")
    st.dataframe(f.head(100), use_container_width=True)

    # Download filtered CSV — Stretch Goal
    st.download_button(
        label="Download filtered data as CSV",
        data=f.to_csv(index=False).encode("utf-8"),
        file_name="filtered_orders.csv",
        mime="text/csv",
        use_container_width=True
    )

with tab2:
    # Region summary
    reg = (
        f.groupby("region", as_index=False)
         .agg(revenue=("revenue", "sum"), units=("units", "sum"))
         .sort_values("revenue", ascending=False)
    )
    st.write("By Region")
    st.dataframe(reg, use_container_width=True)

    # Product summary
    prod = (
        f.groupby("product", as_index=False)
         .agg(revenue=("revenue", "sum"), units=("units", "sum"))
         .sort_values("revenue", ascending=False)
    )
    st.write("By Product")
    st.dataframe(prod, use_container_width=True)

# =========================
# 6) Notes
# =========================

with st.expander("Notes & Tips"):
    st.markdown("""
- Required columns: **date, region, product, units, unit_price**. Optional: **order_id**.
- KPI deltas compare to the immediately preceding period of equal length.
- Use the sidebar to narrow by date, region, and product.
- Charts and metrics update instantly as filters change.
""")
