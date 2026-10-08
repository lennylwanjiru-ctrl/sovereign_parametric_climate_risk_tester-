import os; os.environ["OPENBLAS_NUM_THREADS"] = "1"
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller

print("\n Starting Phase 2: Initializing Climate Mesh Data Pipeline...")

# Set up reproducibility seed for your portfolio data validation
np.random.seed(42)

# Define Kenya's 4 distinct agricultural tracking regions
regions = ['Region_Alpha_West', 'Region_Beta_East', 'Region_Gamma_Highlands', 'Region_Delta_Rift']
years = list(range(1996, 2027)) # 31-year timeline (1996 to 2026)

mesh_records = []
loss_records = []
claim_id_counter = 1001

for region in regions:
    # Calibrate baselines: West/Highlands are high-precipitation; East/Rift are semi-arid
    if region in ['Region_Alpha_West', 'Region_Gamma_Highlands']:
        base_rainfall = 1400.0
        base_ndvi = 0.65
    else:
        base_rainfall = 750.0
        base_ndvi = 0.42
        
    for year in years:
        # Define historical severe regional drought milestone anchor cycles
        is_stress_year = 1 if year in [2000, 2009, 2017, 2022] else 0
        
        if is_stress_year:
            # Generate severe downward shifts for drought cycles
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
print(" Flat-file database arrays generated successfully inside /data directory!")

# =========================================================================
#  PHASE 3: ACTUARIAL HYPOTHESIS TESTING CORE
# =========================================================================
print("\n Running Actuarial Statistics Core Evaluations...")

# 1. Independent Two-Sample t-Test (Anomalies Validation Check)
stress_ndvi = df_mesh[df_mesh['is_stress_year'] == 1]['satellite_ndvi_score']
normal_ndvi = df_mesh[df_mesh['is_stress_year'] == 0]['satellite_ndvi_score']
t_stat, t_pvalue = stats.ttest_ind(stress_ndvi, normal_ndvi, equal_var=False)

print("\n--- [Test 1: Satellite Anomaly Validation] ---")
print(f"Calculated t-Statistic: {t_stat:.4f}")
print(f"Empirical p-Value: {t_pvalue:.8f}")
if t_pvalue < 0.05:
    print("Verdict: REJECT Null Hypothesis. Satellite NDVI significantly flags crop degradation.")
else:
    print("Verdict: FAIL TO REJECT Null Hypothesis. Satellite tracking is an ineffective proxy.")

# 2. Augmented Dickey-Fuller (ADF) Unit-Root Test (Time-Series Stationarity)
print("\n--- [Test 2: Precipitation Time-Series Stationarity] ---")
for region in regions:
    region_rain = df_mesh[df_mesh['region_id'] == region]['rainfall_mm']
    adf_result = adfuller(region_rain)
    print(f"📍 {region} ADF Statistic: {adf_result[0]:.4f} | p-Value: {adf_result[1]:.4f}")

# 3. One-Way ANOVA (Cross-Regional Variance Evaluation)
print("\n--- [Test 3: Cross-Regional Environmental Variance] ---")
region_groups = [df_mesh[df_mesh['region_id'] == r]['rainfall_mm'] for r in regions]
f_stat, anova_pvalue = stats.f_oneway(*region_groups)

print(f"Calculated F-Statistic: {f_stat:.4f}")
print(f"ANOVA p-Value: {anova_pvalue:.8f}")
if anova_pvalue < 0.05:
    print("Verdict: REJECT Null Hypothesis. Regional climate variation is statistically significant.")
    print("         Custom, localized parametric trigger limits are mathematically required.")
else:
    print("Verdict: FAIL TO REJECT Null Hypothesis. National one-size-fits-all underwriting applies.")

# Save mathematical validation metrics to summary ledger logs
summary_df = pd.DataFrame([{
    'metric_id': 'ANOVA_REGIONAL_F', 'calculated_value': round(f_stat, 4), 'p_value': round(anova_pvalue, 6)
}, {
    'metric_id': 'T_TEST_NDVI_T', 'calculated_value': round(t_stat, 4), 'p_value': round(t_pvalue, 6)
}])
summary_df.to_csv('data/anova_table_results.csv', index=False)
print("\n Verification complete! Statistical verdicts cached to 'data/anova_table_results.csv'.\n")
