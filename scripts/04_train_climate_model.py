import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

print("\n Initializing Phase 4: Training Climate Machine Learning Pipeline...")

# 1. Ingest your compiled database flat files 
if not os.path.exists('data/regional_climate_mesh.csv'):
    print(" Error: Baseline climate mesh data not found! Run script 01 first.")
    exit()

df = pd.read_csv('data/regional_climate_mesh.csv')

# 2. Engineer features and targets
# Features (X): Real-time satellite NDVI and Precipitation metrics
# Target (y): Whether the conditions trigger a critical stress/drought event
X = df[['rainfall_mm', 'satellite_ndvi_score']]
y = df['is_stress_year']

# Partition data into 80% Training and 20% Testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print(f" Training Set Size: {len(X_train)} records | Testing Set Size: {len(X_test)} records")

# 3. Initialize and train the Random Forest Classifier
# We use Random Forest because it gracefully handles non-linear thresholds without overfitting
model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
model.fit(X_train, y_train)

# 4. Generate Predictions and Evaluate the Model
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1] # Extract the dynamic probability of drought

print("\n--- [Machine Learning Model Evaluation Matrix] ---")
print("\n Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\n Classification Metrics Report:")
print(classification_report(y_test, y_pred))

# Isolate feature importances to show actuarial drivers
importances = model.feature_importances_
print("🧬 Feature Importance Metrics:")
print(f"  • Precipitation (Rainfall Impact):    {importances[0]*100:.2f}%")
print(f"  • Vegetation Proxy (NDVI Impact):    {importances[1]*100:.2f}%")

# 5. Cache predictive probability scores back onto your dataset for Power BI visualization
df['predicted_drought_risk_score'] = model.predict_proba(X)[:, 1]
df.to_csv('data/regional_climate_mesh.csv', index=False)

print("\n Machine learning core complete! Dynamic risk scores cached into 'data/regional_climate_mesh.csv'.\n")