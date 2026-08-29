"""
00_load_to_sql.py
Loads cleaned churn data into a local SQLite database so analysis
can be shown via SQL (recruiter-visible skill, not just pandas).
Run AFTER 01_eda.py (needs data/telco_cleaned.csv).
"""

import sqlite3
import pandas as pd

df = pd.read_csv("data/telco_cleaned.csv")

conn = sqlite3.connect("data/churn.db")
df.to_sql("customers", conn, if_exists="replace", index=False)

print("Loaded", len(df), "rows into data/churn.db -> table 'customers'")
conn.close()
