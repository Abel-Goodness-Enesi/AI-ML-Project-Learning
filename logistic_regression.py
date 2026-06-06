import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


np.random.seed(42)
n = 200

age = np.random.randint(18, 65, n)
monthly_spend = np.random.randint(1000, 50000, n)
months_subscribed = np.random.randint(1, 60, n)
support_calls = np.random.randint(0, 10, n)

churn = ((support_calls > 5) | (monthly_spend <5000) | (months_subscribed < 6)).astype(int)

df = pd.DataFrame({
    "age":age,
    "monthly_spend": monthly_spend,
    "months_subscribed": months_subscribed,
    "support_calls": support_calls,
    "churn": churn

})

print(df.head())
print("\n Churn distribution")
print(df["churn"].value_counts())


X = df.drop("churn", axis=1)
y = df["churn"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression(max_iter=100)
model.fit(X_train, y_train)

predictions = model.predict(X_test)

print("Accuracy", accuracy_score(y_test, predictions))
print("Classification Report\n", classification_report(y_test, predictions))


def predict_churn(age, monthly_spend, months_subscribed, support_calls):
    input_data = pd.DataFrame({
        "age":[age],
        "monthly_spend":[monthly_spend],
        "months_subscribed":[months_subscribed],
        "support_calls":[support_calls]
    })

    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]
    status = "WILL CHURN" if prediction == 1 else "WILL STAY"

    print(f"Status: {status}")
    print(f"Churn Probability: {probability:.2%}")

predict_churn(25, 3000, 3, 7)
predict_churn(45, 30000, 48, 1)