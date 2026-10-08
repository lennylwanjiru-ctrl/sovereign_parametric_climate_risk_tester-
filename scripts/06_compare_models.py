import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, StratifiedKFold

print("\n Initializing Phase 4C: Side-by-Side Model Comparison Engine...")

# 1. Ingest clean flat files
if not os.path.exists('data/regional_climate_mesh.csv'):
    print(" Error: Baseline data not found! Run script 01 first.")
    exit()

df = pd.read_csv('data/regional_climate_mesh.csv')
X = df[['rainfall_mm', 'satellite_ndvi_score']]
y = df['is_stress_year']

# 2. Configure a matching Stratified 5-Fold validation tracker
cv_structure = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# 3. Instantiate both competitive baselines
rf_model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
lr_model = LogisticRegression(random_state=42)

# 4. Compute cross-validation tracks for both architectures
print(" Calculating validation matrices across both frameworks...")
rf_scores = cross_val_score(rf_model, X, y, cv=cv_structure, scoring='accuracy')
lr_scores = cross_val_score(lr_model, X, y, cv=cv_structure, scoring='accuracy')

# 5. Output comparison results
print("\n===  MODEL BENCHMARKING PERFORMANCE SCOREBOARD 🥊 ===")
print(f" [Random Forest] Mean Accuracy:     {np.mean(rf_scores)*100:.2f}%  | Volatility (SD): {np.std(rf_scores)*100:.2f}%")
print(f" [Logistic Reg]  Mean Accuracy:     {np.mean(lr_scores)*100:.2f}%  | Volatility (SD): {np.std(lr_scores)*100:.2f}%")

print("\n---  Actuarial Portfolio Narrative Insights ---")
rf_mean = np.mean(rf_scores)
lr_mean = np.mean(lr_scores)

if rf_mean > lr_mean:
    margin = (rf_mean - lr_mean) * 100
    print(f"Result: Random Forest OUTPERFORMS Logistic Regression by a margin of {margin:.2f}%.")
    print("        This proves the environmental dataset contains key non-linear climate")
    print("        triggers and threshold combinations that traditional linear curves miss.")
else:
    print("Result: Models score with identical performance ranges.")
    print("        The baseline underlying risk dataset functions on clean linear splits.")
print("")