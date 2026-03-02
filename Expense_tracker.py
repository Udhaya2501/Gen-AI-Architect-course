import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px

st.title("💰 Interactive Expense Tracker")

# -----------------------------
# Initialize session state
# -----------------------------
if "expenses" not in st.session_state:
    st.session_state["expenses"] = []

# -----------------------------
# Input fields
# -----------------------------
amount = st.number_input("Enter Amount", min_value=0.0, step=0.1)
category = st.selectbox("Category", ["Food", "Travel", "Shopping", "Bills", "Other"])
description = st.text_input("Description")
date = st.date_input("Date", value=datetime.today())

if st.button("Add Expense"):
    st.session_state.expenses.append({
        "Date": pd.to_datetime(date),
        "Amount": amount,
        "Category": category,
        "Description": description
    })
    st.success("Expense Added!")

# -----------------------------
# Show expenses
# -----------------------------
if st.session_state.expenses:
    df = pd.DataFrame(st.session_state.expenses)
    
    # Format date for display
    df_display = df.copy()
    df_display["Date"] = df_display["Date"].dt.strftime("%d-%b-%y")
    
    st.subheader("📊 Expense List")
    st.dataframe(df_display)

    st.subheader("Total Spent")
    st.write(df["Amount"].sum())

    # -----------------------------
    # Charts
    # -----------------------------
    st.subheader("Expense Analysis")

    selected_category = st.selectbox(
        "Select Category for Analysis",
        ["All"] + df["Category"].unique().tolist()
    )

    df_filtered = df if selected_category == "All" else df[df["Category"] == selected_category]

    # Prepare Month and Year columns for charts
    df_filtered["Month"] = df_filtered["Date"].dt.strftime("%b-%y")
    df_filtered["Year"] = df_filtered["Date"].dt.year

    # Monthly Expense Chart
    monthly_expense = df_filtered.groupby("Month")["Amount"].sum().reset_index()
    fig_month = px.bar(
        monthly_expense,
        x="Month",
        y="Amount",
        title="📅 Monthly Expenses",
        text="Amount",
        labels={"Amount": "Amount Spent ($)", "Month": "Month"}
    )
    fig_month.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig_month.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_month, use_container_width=True)

    # Yearly Expense Chart
    yearly_expense = df_filtered.groupby("Year")["Amount"].sum().reset_index()
    fig_year = px.bar(
        yearly_expense,
        x="Year",
        y="Amount",
        title="🗓️ Yearly Expenses",
        text="Amount",
        labels={"Amount": "Amount Spent ($)", "Year": "Year"}
    )
    fig_year.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    st.plotly_chart(fig_year, use_container_width=True)

    # -----------------------------
    # Next Month Prediction
    # -----------------------------
    st.subheader("🔮 Next Month Expense Prediction")
    if len(monthly_expense) >= 2:
        last_months = monthly_expense.tail(3)["Amount"]
        predicted = last_months.mean()
        st.info(f"Predicted Expense for Next Month: ${predicted:.2f}")
    else:
        st.info("Add more monthly data to predict next month expense.")