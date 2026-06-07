import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
import matplotlib.pyplot as plt


np.random.seed(42)
n = 200

age = np.random.randint(18, 65, n)
monthly_spend = np.random.randint(1000, 50000, n)
months_subscribed = np.random.randint(1, 60, n)
support_calls =np.random.randint(0, 10, n)

churn = ((support_calls > 5) | (monthly_spend < 5000) | (months_subscribed < 6)).astype(int)

df = pd.DataFrame({
    "age": age, 
    "monthly_spend": monthly_spend,
    "months_subscribed": months_subscribed,
    "support_calls": support_calls, 
    "churn": churn
})

X = df.drop("churn", axis=1)
y = df["churn"]

X_train,X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

models = {
    "Logistic Regression": LogisticRegression(max_iter=1000), 
    "Decision Tree": DecisionTreeClassifier(),
    "Random Forest": RandomForestClassifier(n_estimators=100)
}

results = {}
for name, model in models.items():
    scores = cross_val_score(model,X, y, cv=5)
    results[name] = {"mean": scores.mean(), "std": scores.std()}
    print(f"{name}: {scores.mean():.3f} (+/-  {scores.std():.3f})")


names = list(results.keys())
means = [results[n]["mean"] for n in names]
stds = [results [n]["std"] for n in names]


plt.figure(figsize=(10, 6))
bars = plt.bar(names, means, yerr=stds, capsize=5, color=["steelblue", "green", "orange"])

plt.ylabel("Accuracy")
plt.title("Model Comparison")
plt.ylim(0.7, 1.05)

for bar, mean in zip(bars, means):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, f"{mean:.3f}", ha="center")

plt.tight_layout()
plt.savefig("model_comparison.png")
plt.show()