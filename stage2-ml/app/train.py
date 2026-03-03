import pandas as pd
import numpy as np
import joblib
import json
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, roc_auc_score, precision_score, recall_score
import os



BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(BASE_DIR, '..', 'data', 'telco_churn.csv')

MODEL_DIR = os.path.join(BASE_DIR, 'models')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
METRICS_DIR = os.path.join(OUTPUT_DIR, 'metrics')

print(f"Attempting to load data from: {os.path.abspath(data_path)}")
df = pd.read_csv(data_path)

if 'tenure' not in df.columns and 'Tenure' in df.columns:
    df = df.rename(columns={'Tenure': 'tenure'})

np.random.seed(42)
df['tickets_last_30_days'] = np.random.poisson(2, len(df))
df['total_tickets'] = df['tickets_last_30_days'] + np.random.poisson(5, len(df))
df['latest_ticket_type'] = np.random.choice(['complaint', 'inquiry', 'praise'], len(df))


df['ticket_freq_30d'] = df['tickets_last_30_days'] / 30

sentiment_map = {'complaint': -1.0, 'inquiry': 0.0, 'praise': 1.0}
df['sentiment_score'] = df['latest_ticket_type'].map(sentiment_map)


df['prev_monthly_charges'] = df['MonthlyCharges'] * np.random.uniform(0.9, 1.1, len(df))
df['charge_change'] = df['MonthlyCharges'] - df['prev_monthly_charges']

X = df[['ticket_freq_30d', 'sentiment_score', 'charge_change', 'MonthlyCharges', 'tenure']]
y = df['Churn'].apply(lambda x: 1 if x == 'Yes' else 0)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)


y_pred = model.predict(X_test)
y_probs = model.predict_proba(X_test)[:, 1]

metrics = {
    "f1_score": float(f1_score(y_test, y_pred)),
    "roc_auc": float(roc_auc_score(y_test, y_probs)),
    "precision": float(precision_score(y_test, y_pred)),
    "recall": float(recall_score(y_test, y_pred))
}

os.makedirs(METRICS_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)

joblib.dump(model, os.path.join(MODEL_DIR, 'churn_model.pkl'))
with open(os.path.join(OUTPUT_DIR, 'metrics.json'), 'w') as f:
    json.dump(metrics, f, indent=4)


print(f"Artifacts saved in {OUTPUT_DIR} and {MODEL_DIR}")