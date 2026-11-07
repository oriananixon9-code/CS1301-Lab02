# This creates the page for displaying data visualizations.

import streamlit as st
import json
import pandas as pd
import altair as alt

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Data Visualizations 📈")


# PART 1: GRAPHS FROM data.json

with open("data.json", "r") as infile:
    data = json.load(infile)

subjects = []
hours = []

for item in data["data_points"]:
    subjects.append(item["label"])
    hours.append(item["value"])

st.header("Study Hours by Subject")

study_data = pd.DataFrame({
    "Subject": subjects,
    "Hours": hours
})
line_chart = alt.Chart(study_data).mark_line(point=True).encode(
    x=alt.X("Subject:N", axis=alt.Axis(labelAngle=0)),
    y="Hours:Q"
    )
st.altair_chart(line_chart, use_container_width=True)

st.header("Interactive Study Hours")

if "minimum" not in st.session_state:
    st.session_state.minimum = 0

minimum = st.slider(
    "Minimum study hours",
    0,
    10,
    key="minimum"
)

df = pd.DataFrame({
    "Subject": subjects,
    "Hours": hours
})

filtered = df[df["Hours"] >= minimum]
mean_hours = filtered["Hours"].mean()
median_hours = filtered["Hours"].median()

if "previous_mean" not in st.session_state:
    st.session_state.previous_mean = mean_hours

if "previous_median" not in st.session_state:
    st.session_state.previous_median = median_hours

chart = alt.Chart(filtered).mark_bar().encode(
    x=alt.X("Subject:N", axis=alt.Axis(labelAngle=0)),
    y="Hours:Q",
    color="Subject:N"
).properties(
    title="Study Hours by Subject"
)

st.altair_chart(chart, use_container_width=True)
mean_change = mean_hours - st.session_state.previous_mean
median_change = median_hours - st.session_state.previous_median

st.metric("Mean Study Hours", round(mean_hours, 2),
          delta=round(mean_change, 2))

st.metric("Median Study Hours", round(median_hours, 2),
          delta=round(median_change, 2))

st.session_state.previous_mean = mean_hours
st.session_state.previous_median = median_hours

# PART 2: GRAPHS FROM data.csv

st.header("Study Hours Survey Results")
csv_data = pd.read_csv("data.csv")
st.subheader("Study Hours by Subject")
st.bar_chart(csv_data, x="Category", y="Value", horizontal=True)

st.header("Interactive Survey Results")

if "csv_minimum" not in st.session_state:
    st.session_state.csv_minimum = 0

csv_minimum = st.slider(
    "Minimum survey study hours",
    0,
    20,
    key="csv_minimum"
)

filtered_csv = csv_data[csv_data["Value"] >= csv_minimum]
csv_mean = filtered_csv["Value"].mean()
csv_median = filtered_csv["Value"].median()
if "previous_csv_mean" not in st.session_state:
    st.session_state.previous_csv_mean = csv_mean
if "previous_csv_median" not in st.session_state:
    st.session_state.previous_csv_median = csv_median

csv_chart = alt.Chart(filtered_csv).mark_circle().encode(
    x=alt.X("Category:N", axis=alt.Axis(labelAngle=0)),
    y="Value:Q",
    color="Category:N"
    ).properties(
        title = "Interactive Study Hours Survey"
    )

st.altair_chart(csv_chart, use_container_width=True)

if len(filtered_csv) > 0:
    mean_change = csv_mean - st.session_state.previous_csv_mean
    median_change = csv_median - st.session_state.previous_csv_median
    st.metric("Mean Survey Study Hours", round(csv_mean, 2),
              delta=round(mean_change, 2)
              )
    st.metric("Median Survey Study Hours", round(csv_median, 2),
              delta=round(median_change, 2)
              )
    st.session_state.previous_csv_mean = csv_mean
    st.session_state.previous_csv_median = csv_median
else:
    st.warning("No survey responses meet the selected minimum.")
