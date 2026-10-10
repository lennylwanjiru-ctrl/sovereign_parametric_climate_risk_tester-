
Project: Sovereign Parametric Climate Risk Tester
Module: Relational Database Compiling & Cross-Schema Structural Auditing
Analyst: Lenny Wanjiru (DeKUT Actuarial Science)

import os
import sqlite3
import logging
import pandas as pd

# Configure enterprise logger interface for execution tracking
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define absolute file system paths
mesh_csv_path = 'data/regional_climate_mesh.csv'
loss_csv_path = 'data/historical_loss_logs.csv'
db_path = 'data/climate_risk.db'

# 1. Environment Workspace Safeguard Check
if not os.path.exists(mesh_csv_path) or not os.path.exists(loss_csv_path):
    logging.error("Execution Aborted: Missing required flat-file input registries inside /data directory.")
    raise FileNotFoundError("Please execute the primary mesh generation pipeline script first.")

# Read staging source parameters into memory cache
df_mesh = pd.read_csv(mesh_csv_path)
df_loss = pd.read_csv(loss_csv_path)

# Enforce a clean workspace by stripping stale pre-existing schema instances
if os.path.exists(db_path):
    os.remove(db_path)
    logging.info("Stale database instance purged to guarantee deterministic schema serialization.")

# STRUCTURED ARCHITECTURE: SCHEMA DEPLOYMENT via RAW DDL STATEMENTS

logging.info("Compiling local relational SQLite database instance...")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Table Definition A: Spatial-Temporal Weather Index Log Matrix
cursor.execute("""
CREATE TABLE climate_mesh_registry (
    region_id TEXT,
    calendar_year INTEGER,
    rainfall_mm REAL,
    satellite_ndvi_score REAL,
    is_stress_year INTEGER,
    PRIMARY KEY (region_id, calendar_year)
);
""")

# Table Definition B: Actuarial Portfolio Financial Loss Ledger
cursor.execute("""
CREATE TABLE historical_loss_ledger (
    claim_id TEXT PRIMARY KEY,
    calendar_year INTEGER,
    region_id TEXT,
    historical_yield_loss_metric REAL,
    direct_economic_payout_usd REAL,
    FOREIGN KEY (region_id) REFERENCES climate_mesh_registry (region_id)
);
""")

conn.commit()
logging.info("Relational table blueprints and structural constraints successfully compiled.")


# PIPELINE INSERTION: STREAMING CACHED DATAFRAMES INTO SCHEMA TABLES

logging.info("Streaming in-memory structural datasets directly to database schemas...")

df_mesh.to_sql('climate_mesh_registry', conn, if_exists='append', index=False)
df_loss.to_sql('historical_loss_ledger', conn, if_exists='append', index=False)

logging.info("Data block array pipelines successfully finalized and committed.")


# ADVANCED AUDITING SUITE: TECHNICAL CROSS-SCHEMA INNER JOIN TRACKING

logging.info("Verifying structural data integrity via cross-table relational inner joins...")

audit_query = """
SELECT 
    m.region_id,
    COUNT(m.calendar_year) AS total_years,
    SUM(m.is_stress_year) AS logged_droughts,
    ROUND(AVG(m.rainfall_mm), 2) AS avg_rainfall_mm,
    ROUND(SUM(l.direct_economic_payout_usd), 2) AS total_payouts_usd
FROM climate_mesh_registry m
INNER JOIN historical_loss_ledger l 
    ON m.region_id = l.region_id 
    AND m.calendar_year = l.calendar_year
GROUP BY m.region_id;
"""

df_audit = pd.read_sql_query(audit_query, conn)

# Safe termination of connection parameters
conn.close()
logging.info("SQL compilation cycle complete. Database instance safely written to system files.")

# Corporate Auditing Layout Reporting
print("\n" + "="*80)
print("RELATIONAL AUDIT MATRIX TABLE: STRUCTURAL INTEGRITY VERIFICATION")
print("="*80)
print(df_audit.to_string(index=False))
print("="*80 + "\n")
