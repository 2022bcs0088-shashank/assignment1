def calculate_churn_risk(customer_data):
    """
    Computes churn risk using rule-based logic[cite: 119].
    Input: Dictionary containing customer and ticket history[cite: 128].
    Output: Risk category (Low / Medium / High).
    """
    tickets_30d = customer_data.get("tickets_last_30_days", 0)
    contract_type = customer_data.get("contract_type", "")
    has_complaint = customer_data.get("latest_ticket_type") == "complaint"
    charge_increase = customer_data.get("monthly_charges_increased", False)
    total_tickets = customer_data.get("total_tickets", 0)

    if tickets_30d > 5 or (contract_type == "Month-to-Month" and has_complaint):
        return "High"
    
    if charge_increase and total_tickets >= 3:
        return "Medium"
    
    return "Low"