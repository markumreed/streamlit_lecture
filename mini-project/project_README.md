# Mini-Project: “Sales Snapshot” (Streamlit)

## Goal

Build a small data app that loads a CSV of orders, lets the user filter by date and region, and shows 3 KPIs, a trend chart, and a simple table.

## Learning outcomes

* Run a Streamlit app locally.
* Use sidebar widgets to filter a `pandas` DataFrame.
* Compute simple KPIs from filtered data.
* Plot a quick time series using `st.line_chart`.
* Present a tidy results table with `st.dataframe`.

---

## Requirements (MVP)

1. **Data input**

   * Load a CSV via `st.file_uploader`.
   * Required columns (case-insensitive): `date, region, product, units, unit_price`.
   * Coerce `date` to datetime; `units` and `unit_price` to numeric.
   * Add a computed column `revenue = units * unit_price`.

2. **Filters (sidebar)**

   * A **date range** picker, defaulting to min/max in the data.
   * A **region** selector with options: All + unique regions.

3. **KPIs (4 metrics)**

   * Total Revenue
   * Units Sold
   * Orders (row count is fine)
   * Average Order Value (Total Revenue / Orders)

4. **Visuals & table**

   * **Line chart:** revenue by day (after filters).
   * **Table:** first 50 filtered rows.

5. **Empty-state handling**

   * If filters return no rows, show a friendly `st.warning`.

---

## Stretch goals (choose any 1–2)

* Bar chart of **Top Products by Revenue** (top 5).
* **Download** button for the filtered data as CSV.
* KPI deltas vs prior period of equal length.
* Add a **product** multiselect filter.

---

## Starter dataset (students can copy/paste to a file named `orders_sample.csv`)

```csv
order_id,date,region,product,units,unit_price
10001,2024-01-03,North,Widget,3,14.50
10002,2024-01-03,West,Gadget,2,29.00
10003,2024-01-04,South,Thingamajig,5,9.99
10004,2024-01-04,East,Widget,4,14.50
10005,2024-01-05,North,Gadget,1,29.00
10006,2024-01-05,West,Widget,6,14.50
10007,2024-01-06,South,Thingamajig,2,9.99
10008,2024-01-06,East,Gadget,3,29.00
```

---

## Scaffold: `scaffold_app.py` (students fill in the TODOs)

Download the scaffold code `scaffold_app.py` make sure to fill out the TODOs.

### Solution:
See the `solution_app.py`.
---

## Setup & Run

```bash
pip install streamlit pandas
streamlit run app.py
```

---

## Checkpoints (in-class guidance)

* **Checkpoint A (Load)**: App runs, CSV loads without errors.
* **Checkpoint B (Filter)**: Changing date or region updates the table.
* **Checkpoint C (KPIs)**: Numbers update when filters change.
* **Checkpoint D (Chart)**: Line chart renders and updates with filters.

---





