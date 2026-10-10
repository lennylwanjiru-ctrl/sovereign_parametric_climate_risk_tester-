
Project: Sovereign Parametric Climate Risk Tester
Module: Climate Mesh Data Pipeline Simulation & Actuarial Statistics Core
Analyst: Lenny Wanjiru (DeKUT Actuarial Science)


import os
import logging
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.tsa.stattools import adfuller

# Configure enterprise logger interface for execution tracking
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set environment optimization variables
os.environ["OPENBLAS_NUM_THREADS"] = "1"

# Set reproducibility seeds for spatial portfolio validation
np.random.seed(42)

# Define tracking regions across localized precipitation lines
regions = ['Region_Alpha_West', 'Region_Beta_East', 'Region_Gamma_Highlands', 'Region_Delta_Rift']
years = list(range(1996, 2027))  # 31-year analytical horizon

mesh_records = []
loss_records = []
claim_id_counter = 1001


# PHASE 1: DATA ENGINEERING & REGIONAL MESH DATA SYNTHESIS

logging.info("Initializing regional climate mesh simulation pipeline...")

for region in regions:
    # Calibrate regional geographic baselines (High-precipitation vs. Semi-arid lines)
    if region in ['Region_Alpha_West', 'Region_Gamma_Highlands']:
        base_rainfall = 1400.0
        base_ndvi = 0.65
    else:
        base_rainfall = 750.0
        base_ndvi = 0.42
        
    for year in years:
        # Define historical severe regional drought milestone cycles
        is_stress_year = 1 if year in [2000, 2009, 2017, 2022] else 0
        
        if is_stress_year:
            # Generate negative downward variations for drought cycles
            rainfall = base_rainfall * np.random.uniform(0.45, 0.65)
            ndvi = base_ndvi * np.random.uniform(0.50, 0.70)
            yield_loss = np.random.uniform(0.35, 0.65)
            economic_payout = np.random.uniform(250000, 500000)
        else:
            # Generate standard historical weather fluctuations
            rainfall = base_rainfall * np.random.uniform(0.85, 1.15)
            ndvi = base_ndvi * np.random.uniform(0.88, 1.12)
            yield_loss = np.random.uniform(0.00, 0.10)
            economic_payout = 0.0

        mesh_records.append({
            'region_id': region,
            'calendar_year': year,
            'rainfall_mm': round(rainfall, 2),
            'satellite_ndvi_score': round(ndvi, 3),
            'is_stress_year': is_stress_year
        })
        
        loss_records.append({
            'claim_id': f"CLM_{claim_id_counter}",
            'region_id': region,
            'calendar_year': year,
            'historical_yield_loss_metric': round(yield_loss, 4),
            'direct_economic_payout_usd': round(economic_payout, 2)
        })
        claim_id_counter += 1

# Convert records into clean corporate DataFrames using Pandas
df_mesh = pd.DataFrame(mesh_records)
df_loss = pd.DataFrame(loss_records)

# Ensure data output folder structure exists safely
os.makedirs('data', exist_ok=True)

# Export processed files straight to flat-file storage data layers
df_mesh.to_csv('data/regional_climate_mesh.csv', index=False)
df_loss.to_csv('data/historical_loss_logs.csv', index=False)
logging.info("Climate matrices and historical loss registries successfully serialized to /data directory.")


# PHASE 2: ACTUARIAL STATISTICS & RECENT INFERENCE INQUIRIES

logging.info("Executing parametric and non-parametric risk validation checks...")

# 1. Independent Two-Sample t-Test (Anomalies Validation Check)
stress_ndvi = df_mesh[df_mesh['is_stress_year'] == 1]['satellite_ndvi_score']
normal_ndvi = df_mesh[df_mesh['is_stress_year'] == 0]['satellite_ndvi_score']
t_stat, t_pvalue = stats.ttest_ind(stress_ndvi, normal_ndvi, equal_var=False)

# 2. Augmented Dickey-Fuller (ADF) Unit-Root Test (Time-Series Stationarity)
adf_results_dictionary = {}
for region in regions:
    region_rain = df_mesh[df_mesh['region_id'] == region]['rainfall_mm']
    adf_result = adfuller(region_rain)
    adf_results_dictionary[region] = adf_result

# 3. One-Way ANOVA (Cross-Regional Variance Evaluation)
region_groups = [df_mesh[df_mesh['region_id'] == r]['rainfall_mm'] for r in regions]
f_stat, anova_pvalue = stats.f_oneway(*region_groups)


# SYSTEM MATRIX LEDGER CACHING

summary_df = pd.DataFrame([
    {'metric_id': 'T_TEST_NDVI_T', 'calculated_value': round(t_stat, 4), 'p_value': round(t_pvalue, 6)},
    {'metric_id': 'ANOVA_REGIONAL_F', 'calculated_value': round(f_stat, 4), 'p_value': round(anova_pvalue, 6)}
])
summary_df.to_csv('data/anova_table_results.csv', index=False)
logging.info("Statistical metrics successfully written to destination: data/anova_table_results.csv")


# FINANCIAL TELEMETRY AUDIT REPORT

print("\n" + "="*80)
print("CLIMATE ANOMALY & RISK TESTING REPORT: SOVEREIGN EXPERIMENTAL METRICS")
print("="*80)
print(f"Total Combined Panel Observations: {len(df_mesh)} Spatial-Year Logs")
print(f"Configured Temporal Range Bounds:  {min(years)} to {max(years)} ({len(years)} Continuous Cycles)")
print("-"*80)
print("Statistical Execution Summaries:")
print(f" -> Independent t-Test (NDVI Volatility Check):  t-Stat = {t_stat:.4f} | p-Value = {t_pvalue:e}")
print(f" -> Regional One-Way ANOVA (Rainfall Variance): F-Stat = {f_stat:.4f} | p-Value = {anova_pvalue:e}")
print("-"*80)
print("Sovereign Time-Series Stationarity Verification (ADF Test):")
for r, res in adf_results_dictionary.items():
    print(f" -> {r:25s}: ADF Statistic = {res[0]:.4f} | p-Value = {res[1]:.4f}")
print("="*80 + "\n")
