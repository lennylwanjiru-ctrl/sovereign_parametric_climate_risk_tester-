# Relational Database Schema Blueprints

The relational database architecture translates flat-file climate metrics and logs into structural data tables optimized for low-latency asset-liability evaluations.

##  Database Structural Views

### 1. `climate_mesh_registry`
   `region_id` (TEXT, PRIMARY KEY / FOREIGN KEY) -> Regional identifier string.
   `calendar_year` (INTEGER, PRIMARY KEY) -> Calendar data tracking window.
   `rainfall_mm` (REAL) -> Precipitation metric tracking array.
   `satellite_ndvi_score` (REAL) -> Vegetation index marker proxy.
   `is_stress_year` (INTEGER) -> Boolean flag identifying extreme regional drought anomalies.

### 2. `historical_loss_ledger`
   `claim_id` (TEXT, PRIMARY KEY) -> Unique insurance case key tracking ledger entry.
   `region_id` (TEXT, FOREIGN KEY) -> Links transaction footprint back to climate boundaries.
   `calendar_year` (INTEGER) -> Historical calendar timeline window.
   `historical_yield_loss_metric` (REAL) -> Agricultural loss recording coefficient.
   `direct_economic_payout_usd` (REAL) -> Disbursed financial capital response volume.
*