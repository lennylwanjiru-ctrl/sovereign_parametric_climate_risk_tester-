# Sovereign Parametric Climate-Risk Ledger & ESG Solvency Stress-Tester for Emerging Economies

##  Project Architecture & Overview
This repository implements an end-to-end automated **Parametric Insurance Underwriting & Capital Solvency Core** engineered to bridge the **\$300 Billion global climate protection gap** in emerging markets (calibrated directly to agricultural tea-growing regions in Kenya). 

Traditional crop indemnity insurance frameworks fail during systemic climate shock events due to extreme operational claims latency, taking **3 to 6 months** to deploy human adjusters for loss assessments. This operational delay triggers a cascading economic failure loop: smallholder farming networks slide into immediate poverty cycles, and sovereign states are forced into unexpected fiscal stress, relying on expensive international debt to finance emergency emergency bailouts.

This platform replaces manual loss verification loops with a **Sovereign Parametric Financial Shield**. By connecting directly to independent satellite data streams, the system monitors regional environmental thresholds in real time. If predefined historical limits are breached, an automated payout is triggered, slashing the capital deployment cycle down to **less than 24 hours** to secure sovereign solvency before a crisis cascades.

---

##  The 5-Phase Technical Blueprint
The platform's data engine is built on a modular, multi-tier architectural structure:
1. **Data Engineering Layer (`01_generate_climate_data.py`):** Synthesizes a 31-year multi-regional weather mesh time series (1996–2026) modeling precipitation volumes and satellite vegetation index proxies (**MODIS NDVI**) across distinct Kenyan macro-climatic zones.
2. **Actuarial Statistics Core (`01_generate_climate_data.py`):** Runs automated statistical tests via `scipy.stats` and `statsmodels` (including Two-Sample t-Tests, Augmented Dickey-Fuller stationarity tests, and One-Way ANOVA) to mathematically validate regional variances and reject a "one-size-fits-all" underwriting template.
3. **Relational Data Warehouse (`02_compile_sql_database.py`):** Compiles flat data into a secure local `SQLite3` database instance utilizing raw Data Definition Language (DDL) schemas, primary keys, and foreign keys to establish relational integrity.
4. **Machine Learning Pipeline (`04_train_climate_model` & `05_evaluate_model_reliability`):** Implements an algorithmic predictive model to map out dynamic risk indicators, running side-by-side benchmarking scoring against linear baselines.
5. **Stochastic Capital Simulator (`03_run_stochastic_simulation.py` & `test_actuarial_engine.py`):** Runs a parallel 10,000-trial Monte Carlo solvency stress test over a 10-year outlook horizon to evaluate capital reserve health under extreme 1-in-100-year drought risks.

---

##  Repository Directory Structure
```text
sovereign_parametric_climate_risk_tester/
│
├── data/
│   ├── regional_climate_mesh.csv           # 30-year climate dataset with predictive risk metrics
│   ├── historical_loss_logs.csv           # Baseline agricultural economic claims footprints
│   ├── anova_table_results.csv            # Cached statistical indicators validation ledgers
│   ├── stochastic_solvency_metrics.csv    # 10,000-trial Monte Carlo VaR/TVaR summaries
│   └── climate_risk.db                     # Compiled relational SQL container
│
├── documentation/
│   ├── database_schema.md                  # Relational tables DDL blueprints
│   ├── actuarial_methodology.md            # Advanced quantitative financial risk equations
│   └── machine_learning_blueprint.md       # Cross-validation and model reliability audits
│
├── scripts/
│   ├── 01_generate_climate_data.py         # Data intake pipeline, t-tests, and ANOVA equations
│   ├── 02_compile_sql_database.py          # SQL staging table setup and relational multi-table JOINs
│   ├── 03_run_stochastic_simulation.py     # Monte Carlo parallel simulation & tail risk compiler
│   ├── 04_train_climate_model.py          # Random Forest predictive training core
│   ├── 05_evaluate_model_reliability.py    # Stratified 5-Fold Cross-Validation test script
│   ├── 06_compare_models.py                # Side-by-side Logistic Regression benchmarking scoreboard
│   └── test_actuarial_engine.py          # Automated integration verification unit tests
│
├── requirements.txt                        # Production-grade workspace dependency manifest
├── sovereign_climate_dashboard.pbix        # Interactive Power BI ESG Solvency Cockpit
└── README.md                               # Project master profile documentation
```

---

##  Actuarial Mathematics & Model Specifications

### 1. Stochastic Claims Modeling (Geometric Brownian Motion Variant)
Annual simulated parametric payout trajectories ($S_t$) are modeled using a non-linear stochastic drift expression:
$$S_t = S_0 \cdot \exp\left( (\mu - \frac{1}{2}\sigma^2)dt + \sigma \sqrt{dt} \cdot Z \right)$$
*Where $S_0$ represents the historical base claim reference (\$1.42M), $\mu$ is the severity drift factor ($0.02$), $\sigma$ is the climate volatility index scale ($0.35$), and $Z \sim N(0, 1)$ captures stochastic environmental randomness.*

### 2. Tail Risk Capital Solvency Constraints
The capital balance of the sovereign reserve fund ($C_t$) updates recursively, bounded by a hard insolvency boundary floor at zero:
$$C_t = \max\left( C_{t-1} + P - S_t, \, 0 \right)$$
Using the terminal asset distributions from **10,000 Monte Carlo trials**, the engine isolates the worst-case extreme losses across a 99% confidence threshold using **Value-at-Risk (VaR)** and **Tail Value-at-Risk (TVaR)** calculations:
$$\text{VaR}_{0.99}(X) = \inf \{ x \in \mathbb{R} : P(X \le x) \ge 0.99 \}$$
$$\text{TVaR}_{0.99}(X) = \mathbb{E}[X \mid X \ge \text{VaR}_{0.99}(X)]$$

---

##  Machine Learning Performance Evaluation

### Algorithmic Benchmarking Scoreboard
To justify the complexity of an ensemble tree network over a traditional linear underwriting curve, the predictive layer was evaluated against an industry-standard Logistic Regression model:
*    **Random Forest Classifier (Ensemble Core):** Mean Validation Accuracy: **95.13%** | Score Volatility (SD): **3.98%**
*    **Logistic Regression (Linear Benchmark):** Mean Validation Accuracy: **93.53%** | Score Volatility (SD): **2.02%**

### Key Structural Insights
*   **Non-Linear Superiority:** The Random Forest Classifier outperforms the linear model by a clear margin of **1.60%**. This confirms that climate risks do not scale along a simple linear gradient. Instead, risks compound when overlapping thresholds are breached simultaneously—such as a drop in rainfall occurring while vegetation indicators are already stressed.
*   **Underwriting Stability:** Running a **Stratified 5-Fold Cross-Validation** test yielded low score variance (SD: 3.98%), mathematically proving that the model generalizes robustly and resists overfitting to background noise.
*   **Actuarial Transparency:** The ensemble framework outputs explicit feature weights, avoiding the "black box" risks of deep neural networks to satisfy regulatory compliance tracking:
    *   *Vegetation Index Tracking (Satellite MODIS NDVI Proxy):* **52.84%** of predictive weight.
    *   *Precipitation Deficit Tracking (Rainfall Impact):* **47.16%** of predictive weight.

---

##  Power BI ESG Solvency Command Cockpit

The backend relational structure connects directly into a dashboard workspace using an internal table layout mapping.

### Advanced DAX Expressions Library

*   **Dynamic Underwriting Status Warning Light System:**
    ```dax
    Sovereign Underwriting Status = 
    IF(
        AVERAGE(regional_climate_mesh[predicted_drought_risk_score]) >= 0.70, 
        " CRITICAL EXPOSURE RISK", 
        IF(
            AVERAGE(regional_climate_mesh[predicted_drought_risk_score]) >= 0.35, 
            " WATCHLIST STRESS", 
            " OPTIMAL SYSTEMIC STABILITY"
        )
    )
    ```
*   **Total Allocated Parametric Capital Outflows:**
    ```dax
    Total Emergency Outflows USD = 
    SUM(historical_loss_logs[direct_economic_payout_usd])
    ```
*   **Expected Sovereign Capital Tail Drawdown Depth (99% TVaR Indicator):**
    ```dax
    99% Tail Risk Capital Exposure = 
    CALCULATE(
        MAX(stochastic_solvency_metrics[metric_value]), 
        stochastic_solvency_metrics[metric_name] = "TVAR_99_USD"
    )
    ```

---

##  Environment Replicability & Deployment Setup
To configure the environment locally and replicate these results on your machine, clone this repository and initialize the dependency stack using your command prompt terminal:

```bash
# Clone the repository workspace
git clone https://github.com
cd sovereign_parametric_climate_risk_tester

# Install all workspace libraries via the dependency manifest
pip install -r requirements.txt

# Run the complete data analysis pipeline in order
python scripts/01_generate_climate_data.py       # Computes statistical checks
python scripts/02_compile_sql_database.py       # Compiles the relational tables
python scripts/04_train_climate_model.py        # Trains the ML classifier
python scripts/05_evaluate_model_reliability.py  # Computes the 5-Fold cross validation
python scripts/06_compare_models.py              # Evaluates competitive models
python scripts/03_run_stochastic_simulation.py   # Computes Monte Carlo VaR/TVaR
python -m unittest scripts/test_actuarial_engine.py  # Executes automated unit tests
```