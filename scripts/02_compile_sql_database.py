import os
import sqlite3
import pandas as pd

print("\n Initializing Phase 3: Compiling Relational SQL Database Layer...")

# 1. Read the newly generated flat-file metrics using your Pandas engine
if not os.path.exists('data/regional_climate_mesh.csv') or not os.path.exists('data/historical_loss_logs.csv'):
    print(" Error: Flat files not found! Run script 01 first.")
    exit()

df_mesh = pd.read_csv('data/regional_climate_mesh.csv')
df_loss = pd.read_csv('data/historical_loss_logs.csv')

# Define database destination path
db_path = 'data/climate_risk.db'

# Remove pre-existing databases to ensure clean runs
if os.path.exists(db_path):
    os.remove(db_path)

# 2. Establish connection to your brand new local SQLite instance
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 3. Formulate structural database schemas using raw DDL statements
print(" Crafting relational tables schema architecture...")
cursor.execute('''
    CREATE TABLE climate_mesh_registry (
        region_id TEXT,
        calendar_year INTEGER,
        rainfall_mm REAL,
        satellite_ndvi_score REAL,
        is_stress_year INTEGER,
        PRIMARY KEY (region_id, calendar_year)
    )
''')

cursor.execute('''
    CREATE TABLE historical_loss_ledger (
        claim_id TEXT PRIMARY KEY,
        region_id TEXT,
        calendar_year INTEGER,
        historical_yield_loss_metric REAL,
        direct_economic_payout_usd REAL,
        FOREIGN KEY (region_id) REFERENCES climate_mesh_registry (region_id)
    )
''')
conn.commit()

# 4. Insert dataframes directly into SQL tables utilizing pandas native connections
df_mesh.to_sql('climate_mesh_registry', conn, if_exists='append', index=False)
df_loss.to_sql('historical_loss_ledger', conn, if_exists='append', index=False)
print(" Data blocks appended directly into SQL staging layers successfully!")

# 5. Execute an advanced Actuarial Inner Join to prove database integrity
print("\n Verifying SQL environment using diagnostic multi-table JOIN query...")
query = """
    SELECT 
        m.region_id,
        COUNT(m.calendar_year) as total_years,
        SUM(m.is_stress_year) as logged_droughts,
        ROUND(AVG(m.rainfall_mm), 2) as avg_rainfall_mm,
        ROUND(SUM(l.direct_economic_payout_usd), 2) as total_payouts_usd
    FROM climate_mesh_registry m
    INNER JOIN historical_loss_ledger l 
        ON m.region_id = l.region_id AND m.calendar_year = l.calendar_year
    GROUP BY m.region_id;
"""

df_audit = pd.read_sql_query(query, conn)
print("\n--- [Relational Audit Matrix Table] ---")
print(df_audit.to_string(index=False))

# Terminate data channel connections safely
conn.close()
print("\n SQL compilation phase completed. Local instance saved to 'data/climate_risk.db'.\n")