from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib

app = FastAPI()

# ✅ CORS FIX (IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow chrome extension
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load("models/phishing_model.pkl")
vectorizer = joblib.load("models/vectorizer.pkl")

class Email(BaseModel):
    text: str

@app.get("/")
def home():
    return {"status": "PhishGuard AI backend running"}

@app.post("/predict")
def predict(email: Email):
    X = vectorizer.transform([email.text])
    prob = model.predict_proba(X)[0][1]

    if prob > 0.85:
        verdict = "Phishing"
    elif prob > 0.65:
        verdict = "Suspicious"
    else:
        verdict = "Safe"

    return {
        "score": round(prob * 100, 2),
        "verdict": verdict
    }
