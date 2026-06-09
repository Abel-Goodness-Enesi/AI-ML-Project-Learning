import pandas as pd
import numpy as np
import re 
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

reviews = [
    ("This product is absolutely amazing, I love it!", 1),
    ("Terrible quality, broke after one day", 0),
    ("Best purchase I have ever made, highly recommend", 1),
    ("Complete waste of money, do not buy this", 0),
    ("Works perfectly, very happy with this", 1),
    ("Awful product, nothing like the description", 0),
    ("Exceeded my expectations, fantastic quality", 1),
    ("Stopped working after a week, very disappointed", 0),
    ("Great value for money, works as described", 1),
    ("Poor quality, fell apart immediately", 0),
    ("Absolutely love this, perfect in every way", 1),
    ("Horrible experience, customer service was useless", 0),
    ("Outstanding product, will definitely buy again", 1),
    ("Cheap and nasty, complete rubbish", 0),
    ("Very satisfied with my purchase, works great", 1),
    ("Disappointed with the quality, not worth it", 0),
    ("Incredible product, changed my life", 1),
    ("Waste of time and money, avoid this", 0),
    ("So happy with this purchase, excellent", 1),
    ("Broken on arrival, terrible experience", 0)
]

df = pd.DataFrame(reviews, columns=["review", "sentiment"])
print(df.head())
print("\n Sentence Distribution")
print(df["sentiment"].value_counts())


lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def clean_text(text):
    text = text.lower()
    text = (re.sub(r'[^a-zA-Z\s]', '', text))
    text = text.split()
    text = [word for word in text if word not in stop_words]
    text = [lemmatizer.lemmatize(word) for word in text]
    return ' '.join(text)

df["cleaned"] = df["review"].apply(clean_text)
print("\nCleaned reviews:")
print(df[["review", "cleaned"]].head())

X = df["cleaned"]
y = df["sentiment"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

vectorizer =  TfidfVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

model = LogisticRegression()
model.fit(X_train_vec, y_train)

predictions = model.predict(X_test_vec)

print("\n Accuracy Score", accuracy_score(y_test, predictions))
print(classification_report(y_test, predictions))

def predict_sentiment(review):
    cleaned = clean_text(review)
    vec = vectorizer.transform([cleaned])
    prediction = model.predict(vec)[0]
    probability = model.predict_proba(vec)[0]
    label = "POSITIVE" if prediction == 1 else "NEGATIVE"
    print(f"Review: {review}")
    print(f"Sentiment: {label}")
    print(f"Confidence: {max(probability):.2%}\n")

predict_sentiment("This is the best product I have ever bought")
predict_sentiment("Absolute garbage, complete waste of money")
predict_sentiment("It is okay, nothing special")