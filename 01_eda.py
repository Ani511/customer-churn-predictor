"""
01_eda.py
Exploratory analysis on Telco Customer Churn dataset.
Download from: https://www.kaggle.com/datasets/blastchar/telco-customer-churn
Place CSV as: data/WA_Fn-UseC_-Telco-Customer-Churn.csv
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")

# ---- Load ----
df = pd.read_csv("data/WA_Fn-UseC_-Telco-Customer-Churn.csv")

print("Shape:", df.shape)
print(df.info())

# ---- Clean ----
# TotalCharges has blank strings for new customers -> convert
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df["TotalCharges"].fillna(0, inplace=True)

df["Churn_Flag"] = df["Churn"].map({"Yes": 1, "No": 0})

# ---- Overall churn rate ----
churn_rate = df["Churn_Flag"].mean()
print(f"\nOverall churn rate: {churn_rate:.2%}")

# ---- Churn by contract type (classic business insight) ----
contract_churn = df.groupby("Contract")["Churn_Flag"].mean().sort_values(ascending=False)
print("\nChurn rate by Contract type:\n", contract_churn)

plt.figure(figsize=(6, 4))
contract_churn.plot(kind="bar", color="indianred")
plt.title("Churn Rate by Contract Type")
plt.ylabel("Churn Rate")
plt.tight_layout()
plt.savefig("outputs/churn_by_contract.png", dpi=150)
plt.close()

# ---- Churn by tenure buckets ----
df["tenure_bucket"] = pd.cut(
    df["tenure"],
    bins=[0, 12, 24, 48, 60, 72],
    labels=["0-12mo", "13-24mo", "25-48mo", "49-60mo", "61-72mo"],
)
tenure_churn = df.groupby("tenure_bucket", observed=True)["Churn_Flag"].mean()
print("\nChurn rate by tenure bucket:\n", tenure_churn)

plt.figure(figsize=(6, 4))
tenure_churn.plot(kind="bar", color="steelblue")
plt.title("Churn Rate by Tenure Bucket")
plt.ylabel("Churn Rate")
plt.tight_layout()
plt.savefig("outputs/churn_by_tenure.png", dpi=150)
plt.close()

# ---- Churn by monthly charges ----
plt.figure(figsize=(6, 4))
sns.boxplot(data=df, x="Churn", y="MonthlyCharges")
plt.title("Monthly Charges vs Churn")
plt.tight_layout()
plt.savefig("outputs/monthlycharges_vs_churn.png", dpi=150)
plt.close()

# ---- Churn by internet service / payment method (common high-signal cols) ----
for col in ["InternetService", "PaymentMethod", "TechSupport", "OnlineSecurity"]:
    rate = df.groupby(col)["Churn_Flag"].mean().sort_values(ascending=False)
    print(f"\nChurn rate by {col}:\n", rate)

# ---- Revenue at risk (business framing) ----
revenue_at_risk = df.loc[df["Churn_Flag"] == 1, "MonthlyCharges"].sum()
print(f"\nMonthly recurring revenue currently churned: ${revenue_at_risk:,.2f}")
print(f"Annualized revenue lost to churn: ${revenue_at_risk * 12:,.2f}")

df.to_csv("data/telco_cleaned.csv", index=False)
print("\nSaved cleaned dataset to data/telco_cleaned.csv")
