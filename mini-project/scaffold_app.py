# app.py
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Sales Snapshot", layout="wide")
st.title("Sales Snapshot")
st.caption("Upload a CSV, filter by date and region, and explore KPIs and trends.")

# ---------- 1) Upload ----------
uploaded = st.file_uploader("Upload Orders CSV", type=["csv"])

def prepare(df: pd.DataFrame) -> pd.DataFrame:
    # Normalize column names
    df.columns = [c.strip().lower() for c in df.columns]
    # Basic validation
    required = {"date", "region", "product", "units", "unit_price"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required column(s): {', '.join(sorted(missing))}")
    # Types
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["units"] = pd.to_numeric(df["units"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    df = df.dropna(subset=["date", "region", "product", "units", "unit_price"])
    # Feature
    df["revenue"] = df["units"] * df["unit_price"]
    return df

if uploaded:
    try:
        df = prepare(pd.read_csv(uploaded))
        st.success("CSV loaded.")
    except Exception as e:
        st.error(f"Could not read CSV: {e}")
        st.stop()
else:
    st.info("Upload a CSV to begin. See the expected columns in the expander below.")
    with st.expander("Expected columns"):
        st.code("date, region, product, units, unit_price", language="text")
    st.stop()

# ---------- 2) Filters (sidebar) ----------
st.sidebar.header("Filters")
# Date range
dmin, dmax = df["date"].min().date(), df["date"].max().date()
date_range = st.sidebar.date_input("Date range", (dmin, dmax), min_value=dmin, max_value=dmax)
if isinstance(date_range, tuple):
    start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
else:
    start = end = pd.to_datetime(date_range)

# Region
regions = ["All"] + sorted(df["region"].dropna().unique().tolist())
region = st.sidebar.selectbox("Region", regions, index=0)

# Apply filters
mask = df["date"].between(start, end)
if region != "All":
    mask &= df["region"].eq(region)

f = df.loc[mask].copy()

if f.empty:
    st.warning("No rows match your filters. Try expanding the date range or selecting another region.")
    st.stop()

# ---------- 3) KPIs ----------
total_revenue = f["revenue"].sum()
units_sold = int(f["units"].sum())
orders = len(f)  # or f["order_id"].nunique() if present
aov = (total_revenue / orders) if orders else 0.0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Revenue", f"${total_revenue:,.2f}")
c2.metric("Units Sold", f"{units_sold:,}")
c3.metric("Orders", f"{orders:,}")
c4.metric("Avg Order Value", f"${aov:,.2f}")

st.divider()

# ---------- 4) Chart ----------
st.subheader("Revenue Over Time")
by_day = f.groupby("date", as_index=False)["revenue"].sum().sort_values("date")
st.line_chart(by_day, x="date", y="revenue", height=260)

# ---------- 5) Table ----------
st.subheader("First 50 Filtered Rows")
st.dataframe(f.head(50), use_container_width=True)
