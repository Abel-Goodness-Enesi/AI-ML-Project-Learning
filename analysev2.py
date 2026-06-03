import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("expenses.csv")
df["date"] = pd.to_datetime(df["date"])

print(f"Shape : {df.shape}")
print(df.head(3))
print(df["amount"].describe())

category_totals = df.groupby("category")['amount'].sum().sort_values(ascending=False)
print(category_totals)

daily_avg = df.groupby("date")["amount"].sum().mean()
print(f"\nDaily average spend: ₦{daily_avg:,.2f}")

print(f"\n ---- Most Expensive Item ---- ")
most_expensive = df.loc[df["amount"].idxmax()]

print(f"The most expensive item here is {most_expensive["amount"]}")

print(df["category"].value_counts())

print("\n ---- Food Percentage Calculation ---")
print(f"The Food percentage is {(category_totals["food"]/category_totals.sum()) *100:.1f}%")

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

category_totals.plot(kind="bar", ax=axes[0], color="steelblue", edgecolor="black")
axes[0].set_title("Total Spending by Category")
axes[0].set_xlabel("Category")
axes[0].set_ylabel("Amount in Naira")
axes[0].tick_params(axis="x", rotation=45)

df.groupby("category")["amount"].sum().plot(
    kind="pie", 
    ax=axes[1],
    autopct="%1.1f%%",
    startangle=90
)

axes[1].set_title("Total Spending Distribution")
axes[1].set_ylabel("")

plt.tight_layout()
plt.savefig("Spending_chart.png")
plt.show()
print("Chart saved as 'Spending_chart.png'")