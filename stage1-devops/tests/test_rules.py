import pytest
from app.rules import calculate_churn_risk

def test_high_risk_tickets():
    data = {"tickets_last_30_days": 6, "contract_type": "Two year"}
    assert calculate_churn_risk(data) == "High"

def test_medium_risk():
    data = {"monthly_charges_increased": True, "total_tickets": 3, "tickets_last_30_days": 1}
    assert calculate_churn_risk(data) == "Medium"