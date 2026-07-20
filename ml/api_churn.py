"""
FastAPI — /predict/churn endpoint
Add this to your main api.py alongside other model endpoints.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal
import joblib
import pandas as pd
import os

app = FastAPI(title="Customer Behavior ML API")

# Load model once at startup
MODEL_PATH = "models/churn_rf_model.pkl"
pipeline = None

@app.on_event("startup")
def load_model():
    global pipeline
    if not os.path.exists(MODEL_PATH):
        raise RuntimeError(f"Model not found at {MODEL_PATH}. Run train_churn.py first.")
    pipeline = joblib.load(MODEL_PATH)
    print(f"[startup] Churn model loaded from {MODEL_PATH}")


# Input schema — mirrors the dataset columns used during training
class ChurnInput(BaseModel):
    age: int = Field(..., ge=18, le=100, example=34)
    gender: Literal["Male", "Female"] = Field(..., example="Male")
    category: str = Field(..., example="Clothing")
    purchase_amount_usd: float = Field(..., ge=0, example=65.0)
    location: str = Field(..., example="California")
    size: str = Field(..., example="M")
    season: Literal["Spring", "Summer", "Fall", "Winter"] = Field(..., example="Fall")
    review_rating: float = Field(..., ge=1.0, le=5.0, example=3.1)
    subscription_status: Literal["Yes", "No"] = Field(..., example="No")
    shipping_type: str = Field(..., example="Free Shipping")
    discount_applied: Literal["Yes", "No"] = Field(..., example="Yes")
    promo_code_used: Literal["Yes", "No"] = Field(..., example="No")
    previous_purchases: int = Field(..., ge=0, example=3)
    payment_method: str = Field(..., example="Credit Card")


class ChurnResponse(BaseModel):
    churn_prediction: int          # 0 = retained, 1 = likely to churn
    churn_probability: float       # probability of churn (0.0 – 1.0)
    risk_level: str                # "Low", "Medium", "High"
    recommendation: str


@app.post("/predict/churn", response_model=ChurnResponse)
def predict_churn(data: ChurnInput):
    if pipeline is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    # Map request fields → dataframe column names used during training
    input_df = pd.DataFrame([{
        "Age": data.age,
        "Gender": data.gender,
        "Category": data.category,
        "Purchase Amount (USD)": data.purchase_amount_usd,
        "Location": data.location,
        "Size": data.size,
        "Season": data.season,
        "Review Rating": data.review_rating,
        "Subscription Status": data.subscription_status,
        "Shipping Type": data.shipping_type,
        "Discount Applied": data.discount_applied,
        "Promo Code Used": data.promo_code_used,
        "Previous Purchases": data.previous_purchases,
        "Payment Method": data.payment_method,
    }])

    prediction = int(pipeline.predict(input_df)[0])
    probability = float(pipeline.predict_proba(input_df)[0][1])

    if probability < 0.35:
        risk = "Low"
        recommendation = "Customer is stable. Continue standard engagement."
    elif probability < 0.65:
        risk = "Medium"
        recommendation = "Send targeted retention offer or loyalty incentive."
    else:
        risk = "High"
        recommendation = "Immediate outreach required. High churn risk detected."

    return ChurnResponse(
        churn_prediction=prediction,
        churn_probability=round(probability, 4),
        risk_level=risk,
        recommendation=recommendation,
    )


@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": pipeline is not None}
