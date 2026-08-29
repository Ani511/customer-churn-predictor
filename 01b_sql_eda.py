"""
01b_sql_eda.py
Same core insights as 01_eda.py, but via SQL queries against data/churn.db.
Put this file/queries directly in your README or portfolio to show SQL skill.
Run AFTER 00_load_to_sql.py.
"""

import sqlite3
import pandas as pd

conn = sqlite3.connect("data/churn.db")

queries = {
    "Overall churn rate": """
        SELECT
            ROUND(AVG(Churn_Flag) * 100, 2) AS churn_rate_pct,
            COUNT(*) AS total_customers
        FROM customers;
    """,

    "Churn rate by contract type": """
        SELECT
            Contract,
            COUNT(*) AS customers,
            ROUND(AVG(Churn_Flag) * 100, 2) AS churn_rate_pct
        FROM customers
        GROUP BY Contract
        ORDER BY churn_rate_pct DESC;
    """,

    "Churn rate by tenure bucket": """
        SELECT
            CASE
                WHEN tenure <= 12 THEN '0-12mo'
                WHEN tenure <= 24 THEN '13-24mo'
                WHEN tenure <= 48 THEN '25-48mo'
                WHEN tenure <= 60 THEN '49-60mo'
                ELSE '61-72mo'
            END AS tenure_bucket,
            COUNT(*) AS customers,
            ROUND(AVG(Churn_Flag) * 100, 2) AS churn_rate_pct
        FROM customers
        GROUP BY tenure_bucket
        ORDER BY churn_rate_pct DESC;
    """,

    "Top 5 highest-revenue churned customers": """
        SELECT customerID, MonthlyCharges, tenure, Contract, PaymentMethod
        FROM customers
        WHERE Churn_Flag = 1
        ORDER BY MonthlyCharges DESC
        LIMIT 5;
    """,

    "Revenue at risk by internet service": """
        SELECT
            InternetService,
            ROUND(SUM(CASE WHEN Churn_Flag = 1 THEN MonthlyCharges ELSE 0 END), 2) AS monthly_revenue_lost,
            COUNT(CASE WHEN Churn_Flag = 1 THEN 1 END) AS churned_customers
        FROM customers
        GROUP BY InternetService
        ORDER BY monthly_revenue_lost DESC;
    """,

    "Churn rate: no tech support AND month-to-month (compounded risk)": """
        SELECT
            COUNT(*) AS segment_size,
            ROUND(AVG(Churn_Flag) * 100, 2) AS churn_rate_pct
        FROM customers
        WHERE TechSupport = 'No' AND Contract = 'Month-to-month';
    """,
}

for title, sql in queries.items():
    print(f"\n--- {title} ---")
    result = pd.read_sql_query(sql, conn)
    print(result.to_string(index=False))

conn.close()
