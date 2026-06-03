import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("expenses.csv")
df["date"] = pd.to_datetime(df["date"])

print("Shape:", df.shape)
print("\nFirst 3 rows:")
print(df.head(3))
print("\nBasic stats:")
print(df["amount"].describe())

print("\n--- Spending by category ---")
category_totals = df.groupby("category")["amount"].sum().sort_values(ascending=False)
print(category_totals)

print("\n--- Daily average ---")
daily_avg = df.groupby("date")["amount"].sum().mean()
print(f"Daily average spend: ₦{daily_avg:,.2f}")

print("\n--- Most expensive expense ---")
most_expensive = df.loc[df["amount"].idxmax()]
print(most_expensive)

print("\n--- Number of expenses per category ---")
print(df["category"].value_counts())

print(f"\nCheapest category: {category_totals.idxmin()} — ₦{category_totals.min():,.2f}")

food_pct = (category_totals["food"] / category_totals.sum()) * 100
print(f"\nFood is {food_pct:.1f}% of total spending")

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

category_totals.plot(kind="bar", ax=axes[0], color="steelblue", edgecolor="black")
axes[0].set_title("Total Spending by Category")
axes[0].set_xlabel("Category")
axes[0].set_ylabel("Amount (₦)")
axes[0].tick_params(axis="x", rotation=45)

df.groupby("category")["amount"].sum().plot(
    kind="pie",
    ax=axes[1],
    autopct="%1.1f%%",
    startangle=90
)
axes[1].set_title("Spending Distribution")
axes[1].set_ylabel("")

plt.tight_layout()
plt.savefig("spending_chart.png")
plt.show()
print("Chart saved as spending_chart.png")