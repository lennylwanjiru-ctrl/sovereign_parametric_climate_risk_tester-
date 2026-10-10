# Quantitative Risk & Actuarial Methodology Specifications
**Project:** Sovereign Parametric Climate Risk Tester  
**Lead Analyst:** Lenny Wanjiru | *Dedan Kimathi University of Technology (DeKUT)*



## 1. Parametric Payout Vector Mapping (Geometric Brownian Motion Variant)
To track and model volatile climate hazard dependencies over a multi-year horizon, the asset-liability engine transitions away from static historical baselines by simulating multi-region exposure paths using a non-linear stochastic drift expression.

The localized climate severity vectors are computed recursively across the 10-year outlook horizon using the following Geometric Brownian Motion (GBM) differential transformation:

$$S_t = S_0 \times \exp\left(\left(\mu - \frac{1}{2}\sigma^2\right)dt + \sigma\sqrt{dt} \cdot z\right)$$

### Parameter Baseline Constants:
*   **$S_0$ (Historical Baseline Payout Scale):** $1,425,000.00 USD  
    Represents the expected base historical loss payout anchor across evaluated regions.
*   **$\mu$ (Multi-Year Climate Severity Drift Coefficient):** 0.02 (2% annual positive drift loading).
*   **$\sigma$ (Environmental Tracking Volatility Scale Factor):** 0.35 (35% climate variance index).
*   **$z$ (Independent Stochastic Shock Vector):** $z \sim N(0, 1)$  
    Independent standard normal random variables drawn to simulate unexpected weather anomalies per iteration cycle step.
*   **$dt$ (Annual Discretization Step Window):** 1.0 (Year-by-year operational execution steps).



## 2. Capital Reserve Balance Projections
The primary sovereign emergency treasury balances are modeled recursively to evaluate the conditional probability of reserve exhaustion (fund depletion) under severe multi-region cash accumulation pressure.

The capital reserve trajectory updates at each temporal step according to the following boundary cash flow expression:

$$C_t = \max(C_{t-1} + P - S_t, 0)$$

### Operational Cash Flow Anchors:
*   **$C_t$:** Real-time available sovereign emergency fund capital at the current calendar year step.
*   **$C_{t-1}$:** Available fund capital carried over from the previous temporal iteration step.
*   **$P$ (Annual Incoming Premium Inflow):** $1,200,000.00 USD  
    The static annual incoming premium backing used to restore emergency fund liquidity levels.
*   **$S_t$:** The simulated parametric claim payout triggered during the current calendar year step.
*   **Lower Bounded Constraint ($\max(\dots, 0)$):** Enforces a strict operational floor at 0.0 to capture absolute points of structural insolvency (fund depletion events) where cumulative liabilities breach available liquid capital reserves.



## 3. Tail-Risk Measurement Layouts
To protect multilateral development funds and sovereign treasuries against cascading insolvency during unexpected back-to-back disaster years, portfolio capital adequacy requirements are evaluated at extreme tail intervals.

### A. Value at Risk (VaR) Solvency Metric
Establishes the maximum potential capital loss expected within a specific confidence boundary ($\alpha$), cutting off the absolute worst-case extreme tail scenarios over the 10-year horizon:

$$\text{VaR}_\alpha(X) = \inf \{ x \in \mathbb{R} : P(X \le x) \ge \alpha \}$$

### B. Tail Value at Risk (TVaR / Expected Shortfall)
Because VaR fails to measure the catastrophic severity of losses that completely breach the percentile ceiling, the system enforces Tail Value at Risk (TVaR) to evaluate capital buffers. TVaR calculates the conditional mathematical expectation of losses exceeding the established $\alpha$ threshold:

$$\text{TVaR}_\alpha(X) = \mathbb{E}[X \mid X > \text{VaR}_\alpha]$$

The ratemaking framework computes both risk metrics at a strict **99% regulatory confidence level ($\alpha = 0.99$)** to map capital adequacy guidelines and verify international reinsurance or donor backstop requirements.
   
