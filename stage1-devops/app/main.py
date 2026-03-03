import logging
from fastapi import FastAPI
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator
from .rules import calculate_churn_risk

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename="app.log"
)
logger = logging.getLogger("churn-devops-api")

app = FastAPI(title="Telecom Churn Risk API - DevOps Version")


Instrumentator().instrument(app).expose(app)

class CustomerInput(BaseModel):
    customer_id: str
    contract_type: str
    tickets_last_30_days: int
    total_tickets: int
    latest_ticket_type: str
    monthly_charges_increased: bool

@app.post("/predict-risk")
def predict_risk(data: CustomerInput):
    logger.info(f"Processing risk for customer: {data.customer_id}")
    
    risk_level = calculate_churn_risk(data.dict())
    
    logger.info(f"Decision for {data.customer_id}: {risk_level}")
    
    return {
        "customer_id": data.customer_id,
        "risk_category": risk_level,
        "method": "Rule-Based Logic"
    }