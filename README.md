# Building Interactive Dashboards with Streamlit
---

## 1. Introduction to Streamlit

* **Lecture**:

  * What is Streamlit?
  * Why it’s useful (simplicity, quick prototyping, data-to-web).
  * Real-world use cases: dashboards, internal tools, prototypes.
* **Demo**: Show a simple “Hello World” Streamlit app.

```bash
pip install streamlit
streamlit hello
```

---

## 2. Getting Started

* **Lecture**: Streamlit workflow (`streamlit run app.py`).
* **Hands-On**: Create a starter app.

```python
import streamlit as st

st.title("My First Streamlit App")
st.write("Hello, world! This is a simple interactive web app.")
```

* **Activity**: Students run their first app locally.

---

## 3. Widgets & Interactivity

* **Lecture**: Input widgets (`st.button`, `st.slider`, `st.text_input`, `st.selectbox`).
* **Hands-On**: Build a small app that responds to input.

```python
import streamlit as st

st.title("Interactive Widgets")

name = st.text_input("Enter your name:")
age = st.slider("Select your age", 0, 100, 25)

if st.button("Submit"):
    st.write(f"Hello {name}, you are {age} years old!")
```

* **Activity**: Students add one more widget (e.g., dropdown for favorite color).

---

## 4. Displaying Data

* **Lecture**: Showing text, tables, and charts.
* **Hands-On**:

```python
import pandas as pd
import numpy as np

st.header("Displaying Data")

df = pd.DataFrame({
    "Products": ["A", "B", "C"],
    "Sales": [100, 200, 150]
})
st.table(df)

chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=["Product A", "Product B", "Product C"]
)
st.line_chart(chart_data)
```

* **Activity**: Students create their own table or try a different chart type.

---

## 5. File Upload & Filtering

* **Lecture**: Using `st.file_uploader` to bring in CSVs.
* **Hands-On**:

```python
uploaded = st.file_uploader("Upload a CSV file", type=["csv"])
if uploaded:
    data = pd.read_csv(uploaded)
    st.write("Preview of Data", data.head())

    # Simple filter
    column = st.selectbox("Choose a column", data.columns)
    st.write(data[column])
```

* **Activity**: Students upload their own dataset and view/filter columns.

---

## 6. Layouts & Organization

* **Lecture**: Organizing content with sidebar and columns.
* **Hands-On**:

```python
st.sidebar.header("Sidebar Filters")
option = st.sidebar.selectbox("Choose an option", ["Overview", "Details"])

col1, col2 = st.columns(2)
col1.metric("Sales", "200K")
col2.metric("Profit", "50K")
```

* **Activity**: Students move one of their earlier widgets into the sidebar.

---

## 7. Wrap-Up & Q\&A

* Recap: running apps, widgets, data display, uploads, layouts.
* Show where to learn more (Streamlit docs, gallery).
* Mention deployment with **Streamlit Community Cloud**.
* Open floor for questions.

---

✅ By the end of this session, students will:

* Run Streamlit apps locally.
* Use basic widgets for interactivity.
* Display tables and charts.
* Upload and filter CSV data.
* Organize apps with sidebar and layouts.

