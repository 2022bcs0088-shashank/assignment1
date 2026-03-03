import pandas as pd

def engineer_features(raw_data):
    df = pd.DataFrame([raw_data])
    
    df['ticket_freq_30d'] = df['tickets_last_30_days'] / 30
    sentiment_map = {"complaint": -1.0, "inquiry": 0.0, "praise": 1.0}
    df['sentiment_score'] = df['latest_ticket_type'].map(sentiment_map).fillna(0.0)
    df['charge_change'] = 1.1 if raw_data.get('monthly_charges_increased') else 1.0
    
    df['MonthlyCharges'] = raw_data.get('MonthlyCharges', 0.0)
    df['tenure'] = raw_data.get('Tenure', 0) 
    
    return df[['ticket_freq_30d', 'sentiment_score', 'charge_change', 'MonthlyCharges', 'tenure']]