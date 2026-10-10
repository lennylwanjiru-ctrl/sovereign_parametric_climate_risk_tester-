"""

Module: Climate Risk Machine Learning Calibration & Feature Importance Analytics
"""


import os
import logging
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

# Configure enterprise logger interface for execution tracking
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define input path boundaries
mesh_csv_path = 'data/regional_climate_mesh.csv'

# 1. Environment Workspace Safeguard Check
if not os.path.exists(mesh_csv_path):
    logging.error(f"Execution Aborted: Base data registry missing at destination path: {mesh_csv_path}")
    raise FileNotFoundError("Please ensure regional_climate_mesh.csv is generated inside the /data directory first.")

# Ingest historical observational matrices into memory
df_raw = pd.read_csv(mesh_csv_path)


# FEATURE ENGINEERING & ENSEMBLE TRAINING SPLITS

logging.info("Isolating data dimensions and engineering training/testing cohorts...")

# Features (X) and Target Label (y) definitions
X = df_raw[['rainfall_mm', 'satellite_ndvi_score']]
y = df_raw['is_stress_year']

# Execute an 80/20 train/test partition using stratified distribution bounds
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

logging.info(f"Cohort sets generated successfully. Training Observations: {len(X_train)} | Evaluation Observations: {len(X_test)}")


# MACHINE LEARNING ENGINE: PARAMETRIC RANDOM FOREST CALIBRATION

logging.info("Deploying Ensemble Random Forest Classifier optimization routines...")

# Initialize and calibrate bounded tree structures
model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
model.fit(X_train, y_train)

logging.info("Model training cycle complete. Commencing out-of-sample evaluative testing...")


# MODEL DIAGNOSTICS & FEATURE IMPORTANCE EXTRACTION

y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]  # Extract structural dynamic risk probability index

# Extract relative spatial-temporal actuarial feature drivers
feature_importances = model.feature_importances_

# Serialize updated hazard risk indices back to file system layers
df_raw['predicted_drought_risk_score'] = model.predict_proba(X)[:, 1]
df_raw.to_csv('data/regional_climate_mesh.csv', index=False)
logging.info("Dynamic predictive risk scores successfully updated inside regional_climate_mesh.csv for downstream BI ingestion.")

# AUDITING TELEMETRY MATRIX REPORTING

print("\n" + "="*80)
print("PREDICTIVE VALIDATION EXECUTIVE BRIEF: ENSEMBLE CLASSIFIER MATRIX")
print("="*80)
print("Out-of-Sample Classification Report Metrics:")
print(classification_report(y_test, y_pred))
print("-"*80)
print("Calculated Confusion Matrix Array:")
print(confusion_matrix(y_test, y_pred))
print("-"*80)
print("Actuarial Feature Driver Relative Weight Profiles:")
print(f" -> Precipitation Volatility (Rainfall Impact): {feature_importances[0]*100:.2f}% Importance")
print(f" -> Vegetation Anomaly Proxy (NDVI Impact):     {feature_importances[1]*100:.2f}% Importance")
print("="*80 + "\n")
