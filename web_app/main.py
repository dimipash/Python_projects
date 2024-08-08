"""
Simple Data Dashboard

This Streamlit app allows users to upload a CSV file, preview the data, generate a summary, filter the data, and plot a line chart.

Features:
- File uploader to select a CSV file
- Data preview and summary
- Ability to filter data by selecting a column and a value
- Line chart generation based on selected x and y-axis columns

Usage:
1. Run the app using Streamlit.
2. Upload a CSV file when prompted.
3. Explore the data preview, summary, and filtering options.
4. Select x and y-axis columns to generate a line chart.
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Simple Data Dashboard")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("Data Preview")
    st.write(df.head())

    st.subheader("Data Summary")
    st.write(df.describe())

    st.subheader("Filter Data")
    columns = df.columns.tolist()
    selected_column = st.selectbox("Select column to filter by", columns)
    unique_values = df[selected_column].unique()
    selected_value = st.selectbox("Select value", unique_values)

    filtered_df = df[df[selected_column] == selected_value]
    st.write(filtered_df)

    st.subheader("Plot Data")
    x_column = st.selectbox("Select x-axis column", columns)
    y_column = st.selectbox("Select y-axis column", columns)

    if st.button("Generate Plot"):
        st.line_chart(filtered_df.set_index(x_column)[y_column])
else:
    st.write("Waiting on file upload...")
