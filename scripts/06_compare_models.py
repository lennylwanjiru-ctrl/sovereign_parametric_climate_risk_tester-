
"""
Module: Cross-Architecture Benchmark Validation & Performance Scoreboard
"""


import os
import logging
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, StratifiedKFold

# Configure enterprise logger interface for execution tracking
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define input path boundaries
mesh_csv_path = 'data/regional_climate_mesh.csv'

# 1. Environment Workspace Safeguard Check
if not os.path.exists(mesh_csv_path):
    logging.error(f"Execution Aborted: Base data registry missing at destination path: {mesh_csv_path}")
    raise FileNotFoundError("Please ensure regional_climate_mesh.csv is generated inside the /data directory first.")

# Ingest historical observational matrices into memory
df = pd.read_csv(mesh_csv_path)

# Features (X) and Target Label (y) definitions
X = df[['rainfall_mm', 'satellite_ndvi_score']]
y = df['is_stress_year']


# STRATIFIED CROSS-VALIDATION COMPARISON SETUP

logging.info("Configuring matching Stratified 5-Fold validation tracker...")
cv_structure = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# Instantiation of both competitive baseline model architectures
rf_model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
lr_model = LogisticRegression(random_state=42)


# PIPELINE EXECUTION: COMPUTE TESTING SCORES

logging.info("Calculating validation matrices across both machine learning frameworks...")

rf_scores = cross_val_score(rf_model, X, y, cv=cv_structure, scoring='accuracy')
lr_scores = cross_val_score(lr_model, X, y, cv=cv_structure, scoring='accuracy')

# Calculate mean performance metrics and standard deviations
rf_mean = np.mean(rf_scores)
rf_std = np.std(rf_scores)

lr_mean = np.mean(lr_scores)
lr_std = np.std(lr_scores)

margin = (rf_mean - lr_mean) * 100


# BENCHMARK LOGIC & METRIC LEDGER SERIALIZATION

logging.info("Analyzing architectural variances and exporting comparative table...")

if rf_mean > lr_mean:
    winning_model_id = "ENSEMBLE_RANDOM_FOREST_WINNER"
    performance_insight_code = "NON_LINEAR_THRES_DETECTED"
elif lr_mean > rf_mean:
    winning_model_id = "PARAMETRIC_LOGISTIC_REGREG_WINNER"
    performance_insight_code = "LINEAR_BOUND_SUFFICIENCY"
else:
    winning_model_id = "ARCHITECTURAL_PARITY"
    performance_insight_code = "IDENTICAL_PERFORMANCE_RANGES"

# Save benchmark metrics back to file storage records
os.makedirs('data', exist_ok=True)
df_benchmark = pd.DataFrame([
    {'model_id': 'Random_Forest_Classifier', 'mean_accuracy': round(rf_mean, 4), 'std_dev_variance': round(rf_std, 4)},
    {'model_id': 'Logistic_Regression_Model', 'mean_accuracy': round(lr_mean, 4), 'std_dev_variance': round(lr_std, 4)},
    {'model_id': 'Model_Performance_Margin', 'mean_accuracy': round(abs(margin/100), 4), 'std_dev_variance': 0.0000}
])

output_csv_path = 'data/model_comparison_benchmark_table.csv'
df_benchmark.to_csv(output_csv_path, index=False)
logging.info(f"Cross-architecture scorecard successfully written to: {output_csv_path}")


# FINANCIAL TELEMETRY AUDIT REPORT

print("\n" + "="*80)
print("MODEL BENCHMARKING PERFORMANCE SCOREBOARD: ARCHITECTURAL DEPLOYMENT RISK")
print("="*80)
print(f" -> [Random Forest] Mean Cross-Validation Accuracy: {rf_mean:.2%} | Volatility (SD): {rf_std:.2%}")
print(f" -> [Logistic Reg]  Mean Cross-Validation Accuracy: {lr_mean:.2%} | Volatility (SD): {lr_std:.2%}")
print("-"*80)
print(f"Calculated Performance Spread Margin:         {abs(margin):.2f}% Delta")
print(f"Winning Underwriting Model Selection Token:    {winning_model_id}")
print(f"Structural Portfolio Insight Tracking Code:   {performance_insight_code}")
print("="*80 + "\n")
   
