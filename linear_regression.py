import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib 

np.random.seed(42)
size = np.random.randint(50, 300, 100)
price = size * 150000 + np.random.randint(-5000000, 5000000, 100)

df = pd.DataFrame({"size": size, "price": price})
print(df.head())
print(df.describe())

X = df[["size"]]
y = df[["price"]]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

predictions = model.predict(X_test)

print("Slope (m):", model.coef_[0])
print("Intercept (b):", model.intercept_)
print("R^2 Score:", r2_score(y_test, predictions))
print("RMSE:", np.sqrt(mean_squared_error(y_test, predictions)))

plt.figure(figsize=(10, 6))
plt.scatter(X_test, y_test, color="blue", label="Actual prices")
plt.plot(X_test, predictions, color="red", linewidth=2, label="Predicted line")
plt.xlabel("Size (sqm)")
plt.ylabel("Price (₦)")
plt.title("House Price Prediction")
plt.legend()
plt.tight_layout()
plt.savefig("regression_plot.png")
plt.show()

def predict_price(size_sqm):
    input_df = pd.DataFrame({"size": [size_sqm]})
    prediction = model.predict(input_df)[0][0]
    print(f"Predicted price for {size_sqm}sqm house: ₦{prediction:,.2f}")

predict_price(100)
predict_price(200)
predict_price(250)

joblib.dump(model, "house_price_model.pk1")
joblib.dump(vectorizer if 'vectorizer' in dir() else None, "house_price_model.pk1")
print("Model saved")