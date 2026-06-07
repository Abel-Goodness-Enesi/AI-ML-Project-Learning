import pandas as pd
import numpy as np 
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

np.random.seed(42)
n = 200

age = np.random.randint(18, 65, n)
monthly_spend = np.random.randint(1000, 50000, n)
months_subscribed = np.random.randint(1, 60, n)
support_calls = np.random.randint(1, 10, n)

churn = ((support_calls > 5) | (monthly_spend <5000) | (months_subscribed < 6) ).astype(int)


df = pd.DataFrame({
    "age": age, 
    "monthly_spend": monthly_spend,
    "months_subscribed": months_subscribed, 
    "support_calls": support_calls,
    "churn": churn
})

print(df.head())
print("Churn Distribution")
print(df["churn"].value_counts())

X = df.drop("churn", axis=1)
y = df["churn"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = DecisionTreeClassifier()
model.fit(X_train, y_train)

predictions = model.predict(X_test)

print("Accuracy score:", accuracy_score(y_test, predictions))

model2 = RandomForestClassifier(n_estimators=100)
model2.fit(X_train, y_train)

predictions2 = model2.predict(X_test)

print("Random Forest Accuracy Score:", accuracy_score(y_test, predictions2))

print("\n Feature Importance (Random Forest):")
importances = pd.Series(model2.feature_importances_, index=X.columns)
print(importances.sort_values(ascending=False))