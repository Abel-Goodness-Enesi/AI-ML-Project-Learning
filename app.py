import streamlit as st
import csv
import os
import matplotlib.pyplot as plt
import pandas as pd

st.title("EXPETR - Expense Tracker App")
st.write("Welcome to Expetr, This is an Expense Tracking App, it helps tracks your expenses as inputted, providing you without an accountability evidence of your Spending! \nEnjoy EXPETR")
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Go to", ["Home", "Add Expense", "View Expense", "Summary"])

if page == "Home":
    st.subheader("Getting Started!")
    st.write("USe the side bar to navigate the app.")

elif page == "Add Expense":
    st.subheader("Add a New Expense")
    amount = st.number_input("Enter Amount: #")
    category= st.text_input("What category is this expense? e.g (food, transport, clothing)")
    description = st.text_input("Brief description: ")
    expense_date = st.date_input("Input date if not today")
    df = pd.read_csv("expenses.csv")
    new_id = max([int(x) for x in df["id"]], default=0) + 1
    if st.button('Save Expense'):
        if category and description:
            if os.path.exists("expenses.csv"):
                existing = pd.read_csv("expenses.csv")
                new_id = max(existing["id"].astype(int), default=0) + 1
            else:
                new_id = 1
            file_exists = os.path.exists("expenses.csv")
            with open("expenses.csv", "a", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=["id", "date", "amount", "category", "description"])
                if not file_exists:
                    writer.writeheader()
                writer.writerow({
                    "id": new_id,
                    "date": expense_date,
                    "amount": amount,
                    "category": category,
                    "description": description
                })
            st.success(f"Added ₦{amount} for {category}!")
        else:
            st.error("Please fill in Category and Description")
elif page == "View Expense":
    st.subheader("Your Expenses")
    if os.path.exists("expenses.csv"):
        df = pd.read_csv("expenses.csv")
        st.dataframe(df, hide_index=True)
    else:
        st.info("No expenses yet, Go to Add Expense to get started.")

elif page == "Summary":
    st.subheader("Spending Summary")
    if os.path.exists("expenses.csv"):
        df = pd.read_csv("expenses.csv")
        grouped = df.groupby("category")["amount"].sum()
        

        fig, ax = plt.subplots()
        grouped.plot(kind="bar", ax=ax, color="steelblue", edgecolor="black")
        ax.set_title("Spending by Category")
        ax.set_xlabel("Category")
        ax.set_ylabel("Amount (₦)")
        ax.tick_params(axis="x", rotation=45)
        plt.tight_layout()
        st.pyplot(fig)
        st.metric("Total Spent", f"#{df["amount"].sum():,.2f}")