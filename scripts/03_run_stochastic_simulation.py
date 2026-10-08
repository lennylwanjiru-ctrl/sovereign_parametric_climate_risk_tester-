import os
import numpy as np
import pandas as pd

print("\n Initializing Phase 5: Compiling Stochastic Reinsurance Simulation Engine...")

# Ensure reproducibility seed matches across your repository profile
np.random.seed(42)

# 1. Calibrate baseline parameters from your historic SQL records
historical_avg_payout = 1425000.0  # Average total annual payout across all regions
volatility = 0.35                  # 35% environmental climate volatility index factor
initial_fund_capital = 5000000.0   # $5,000,000 USD anchor emergency sovereign reserve cash

# Define forecasting parameters
num_trials = 10000                 # 10,000-trial Monte Carlo parallel paths
forecast_years = 10                # 10-year outlook asset-liability timeline
dt = 1.0                           # Annual discretization step window

# Create empty storage matrices to track fund value trajectories
fund_trajectories = np.zeros((num_trials, forecast_years + 1))
fund_trajectories[:, 0] = initial_fund_capital

# Annual incoming climate premium inflows backing the sovereign chest
annual_premium_inflow = 1200000.0 

print(f" Running {num_trials:,} Monte Carlo trials forecasting a {forecast_years}-year solvency window...")

# 2. Execute parallel Geometric Brownian Motion simulations with drift terms
for t in range(1, forecast_years + 1):
    # Standard normal distribution shocks representing climate randomness
    z = np.random.standard_normal(num_trials)
    
    # Model annual simulated payouts using a log-normal stochastic vector
    simulated_payouts = historical_avg_payout * np.exp((0.02 - 0.5 * volatility**2) * dt + volatility * np.sqrt(dt) * z)
    
    # Update the sovereign reserve balances: previous capital + premiums - parametric payouts
    fund_trajectories[:, t] = fund_trajectories[:, t-1] + annual_premium_inflow - simulated_payouts
    
    # Lower bound at $0 to capture absolute baseline insolvency points
    fund_trajectories[:, t] = np.maximum(fund_trajectories[:, t], 0.0)

# Isolate the final year terminal asset valuation matrix
terminal_balances = fund_trajectories[:, -1]
total_losses_or_drawdowns = initial_fund_capital - terminal_balances

# 3. Calculate Advanced Actuarial Solvency and Tail Risk KPIs
depletion_events = np.sum(terminal_balances == 0.0)
probability_of_depletion = (depletion_events / num_trials) * 100

# Value-at-Risk (VaR) at 99% Confidence Level
var_99 = np.percentile(total_losses_or_drawdowns, 99)

# Tail Value-at-Risk (TVaR) at 99% Confidence Level (Extreme Tail Expected Loss)
tail_losses = total_losses_or_drawdowns[total_losses_or_drawdowns >= var_99]
tvar_99 = np.mean(tail_losses)

print("\n--- [Stochastic Solvency Stress-Test Summary Results] ---")
print(f" Initial Sovereign Seed Reserve:  ${initial_fund_capital:,.2f} USD")
print(f" Empirical Fund Depletion Prob:   {probability_of_depletion:.2f}%")
print(f" 99% Value-at-Risk (VaR):         ${var_99:,.2f} USD")
print(f" 99% Tail Value-at-Risk (TVaR):    ${tvar_99:,.2f} USD")

if tvar_99 > initial_fund_capital:
    print("\nVerdict: CRITICAL EXPOSURE DETECTED. Tail risk exceeds internal liquidity.")
    print("         Sovereign requires international re-insurance backing or donor relief.")
else:
    print("\nVerdict: SUFFICIENT CAPITALIZATION. Reserve chest structure meets safety standards.")

# 4. Save simulation results out as a flat-file summary vector for Power BI ingestion
os.makedirs('data', exist_ok=True)
output_summary = pd.DataFrame([{
    'metric_name': 'FUND_DEPLETION_PCT', 'metric_value': round(probability_of_depletion, 4)
}, {
    'metric_name': 'VAR_99_USD', 'metric_value': round(var_99, 2)
}, {
    'metric_name': 'TVAR_99_USD', 'metric_value': round(tvar_99, 2)
}])
output_summary.to_csv('data/stochastic_solvency_metrics.csv', index=False)
print("\n Simulation engine run complete! Stochastic summaries cached safely.")