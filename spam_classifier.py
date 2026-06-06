import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
import joblib

data = {
    "message": [
        "Win free cash now click here",
        "Congratulations you won a prize",
        "Free money waiting for you",
        "Click here to claim your reward",
        "Buy cheap meds online now",
        "Hey are we still meeting tomorrow",
        "Can you send me the report",
        "Lunch at 1pm works for me",
        "Please review the attached document",
        "Are you coming to the meeting",
        "Your account has been credited",
        "Call me when you get this",
        "Win a brand new iPhone today",
        "Limited offer expires tonight",
        "See you at the office tomorrow"
    ],
    "label": [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0]
}

df = pd.DataFrame(data)
print(df)


X = df["message"]
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Training samples:", len(X_train))
print("Test samples:", len(X_test))

vectorizer = TfidfVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

model = MultinomialNB()
model.fit(X_train_vec, y_train)

predictions = model.predict(X_test_vec)

print("Accuracy:", accuracy_score(y_test, predictions))
print(classification_report(y_test, predictions))


def predict_message(message):
    vec = vectorizer.transform([message])
    prediction = model.predict(vec)[0]
    probability = model.predict_proba(vec)[0]
    label = "SPAM" if prediction == 1 else "NOT SPAM"
    print(f"Message: {message}")
    print(f"Prediction: {label}")
    print(f"Confidence: {max(probability):.2%}\n")

predict_message("Win a free iPhone click now")
predict_message("Can we reschedule our meeting")
predict_message("Claim your free reward today")

joblib.dump(model, "spam_model.pk1")
joblib.dump(vectorizer, "spam_vectorizer.pk1")
print("Model Saved.")