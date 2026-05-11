import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib, os

os.makedirs("models", exist_ok=True)

# Better dataset (demo but realistic)
data = {
    "text": [
        "Verify your bank account immediately",
        "Your account is suspended click here",
        "Urgent password reset required",
        "Free gift card claim now",
        "Meeting scheduled for tomorrow",
        "Project update attached",
        "Lunch plan for today",
        "Invoice for last month",
        "Team meeting agenda",
        "Your OTP is 123456"
    ],
    "label": [1,1,1,1,0,0,0,0,0,0]
}

df = pd.DataFrame(data)

vectorizer = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1,2),
    max_df=0.9
)

X = vectorizer.fit_transform(df["text"])
y = df["label"]

model = LogisticRegression(class_weight="balanced", max_iter=1000)
model.fit(X, y)

joblib.dump(model, "models/phishing_model.pkl")
joblib.dump(vectorizer, "models/vectorizer.pkl")

print("Model trained successfully")
