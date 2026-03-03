import logging
import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator
from typing import Optional
import os

logging.basicConfig(level=logging.INFO, filename="app.log")
logger = logging.getLogger("churn-ml-api")

app = FastAPI(title="Telecom Churn API - ML Version")
Instrumentator().instrument(app).expose(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "models", "churn_model.pkl")
model = joblib.load(model_path)

class CustomerInput(BaseModel):
    customer_id: str
    tickets_last_30_days: int
    latest_ticket_type: str
    monthly_charges_increased: bool
    MonthlyCharges: float
    tenure: Optional[int] = None
    Tenure: Optional[int] = None

@app.post("/predict-risk")
def predict_risk(data: CustomerInput):
    logger.info(f"ML Inference request for: {data.customer_id}")
    tenure_value = data.tenure if data.tenure is not None else data.Tenure

    if tenure_value is None:
        return {
            "error": "Either 'tenure' or 'Tenure' must be provided"
        }
    
    sentiment_map = {'complaint': -1.0, 'inquiry': 0.0, 'praise': 1.0}
    
    input_df = pd.DataFrame([{
        'ticket_freq_30d': data.tickets_last_30_days / 30,
        'sentiment_score': sentiment_map.get(data.latest_ticket_type, 0.0),
        'charge_change': 1.0 if data.monthly_charges_increased else 0.0, # Simplified for inference
        'MonthlyCharges': data.MonthlyCharges,
        'tenure': tenure_value
    }])

    prediction = model.predict(input_df)[0]
    risk_category = "High" if prediction == 1 else "Low"
    
    logger.info(f"ML Prediction for {data.customer_id}: {risk_category}")
    
    return {
        "customer_id": data.customer_id,
        "risk_category": risk_category,
        "method": "ML Classifier Model",
        "model_version": "v1.0"
    }