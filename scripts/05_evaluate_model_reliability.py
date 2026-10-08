import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, StratifiedKFold

print("\n Initializing Phase 4B: Running Actuarial Model Reliability & Cross-Validation Test...")

# 1. Ingest your data
if not os.path.exists('data/regional_climate_mesh.csv'):
    print(" Error: Baseline data not found! Run script 01 first.")
    exit()

df = pd.read_csv('data/regional_climate_mesh.csv')
X = df[['rainfall_mm', 'satellite_ndvi_score']]
y = df['is_stress_year']

# 2. Configure a Stratified 5-Fold Cross-Validation structure
# 'Stratified' ensures each fold has the exact same percentage of drought years as the whole dataset
cv_structure = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# 3. Instantiate a fresh model to prevent pre-learned bias leakage
test_model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)

# 4. Compute reliability scores across all 5 folds
print(" Spinning up cross-validation matrix iterations...")
cv_scores = cross_val_score(test_model, X, y, cv=cv_structure, scoring='accuracy')

# 5. Output reliability metrics
print("\n--- [Machine Learning Reliability & Stability Report] ---")
for idx, score in enumerate(cv_scores):
    print(f"   Fold {idx+1} Verification Accuracy:   {score*100:.2f}%")

mean_accuracy = np.mean(cv_scores)
score_variance_sd = np.std(cv_scores)

print(f"\n Mean Cross-Validation Accuracy: {mean_accuracy*100:.2f}%")
print(f" Model Score Volatility (Std Dev): {score_variance_sd*100:.2f}%")

print("\n--- [Actuarial Underwriting Audit Verdict] ---")
if score_variance_sd > 0.05:
    print("Verdict: UNRELIABLE / UNSTABLE MODEL. High variance detected across folds.")
    print("         The predictive parameters are overfitted to local noise.")
elif mean_accuracy < 0.85:
    print("Verdict: UNDERFITTED MODEL. Accuracy baseline falls short of systemic underwriting margins.")
else:
    print("Verdict: HIGHLY RELIABLE ENGINE. Low variance and strong accuracy confirmed.")
    print("         The Random Forest parameters are statistically stable for live risk forecasting.")
print("")