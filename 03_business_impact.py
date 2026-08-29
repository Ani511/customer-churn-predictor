"""
03_business_impact.py
Converts model output into a business-facing retention targeting list + $ impact.
This is the part that makes the project read as "analytics for decisions",
not just "I trained a model". Run 02_model.py first.
"""

import pandas as pd

results = pd.read_csv("outputs/churn_predictions.csv")

# ---- Risk tiers ----
def risk_tier(p):
    if p >= 0.7:
        return "High"
    elif p >= 0.4:
        return "Medium"
    else:
        return "Low"

results["risk_tier"] = results["churn_probability"].apply(risk_tier)

# ---- Revenue at risk by tier ----
if "MonthlyCharges" in results.columns:
    revenue_by_tier = results.groupby("risk_tier")["MonthlyCharges"].sum().sort_values(ascending=False)
    print("Monthly revenue at risk by tier:\n", revenue_by_tier)

tier_counts = results["risk_tier"].value_counts()
print("\nCustomer count by tier:\n", tier_counts)

# ---- Simulated retention campaign ROI ----
# Assumption: targeting "High" risk tier with a retention offer costing $15/customer,
# with an assumed 25% success rate at preventing churn (industry-typical range 20-30%).
RETENTION_COST_PER_CUSTOMER = 15
ASSUMED_SUCCESS_RATE = 0.25

high_risk = results[results["risk_tier"] == "High"]
n_high_risk = len(high_risk)
campaign_cost = n_high_risk * RETENTION_COST_PER_CUSTOMER

if "MonthlyCharges" in results.columns:
    monthly_revenue_saved = (
        high_risk["MonthlyCharges"].sum() * ASSUMED_SUCCESS_RATE
    )
    annual_revenue_saved = monthly_revenue_saved * 12
    roi = (annual_revenue_saved - campaign_cost) / campaign_cost

    print(f"\n--- Retention Campaign Simulation (High-risk tier) ---")
    print(f"High-risk customers: {n_high_risk}")
    print(f"Campaign cost: ${campaign_cost:,.2f}")
    print(f"Assumed annual revenue saved: ${annual_revenue_saved:,.2f}")
    print(f"Estimated ROI: {roi:.1%}")

# ---- Export prioritized outreach list for "stakeholders" ----
cols_to_export = ["churn_probability", "risk_tier"]
if "MonthlyCharges" in results.columns:
    cols_to_export.insert(0, "MonthlyCharges")

outreach_list = results.sort_values("churn_probability", ascending=False)[cols_to_export]
outreach_list.to_csv("outputs/retention_priority_list.csv", index=False)

print("\nSaved outputs/retention_priority_list.csv — ready to hand to a retention/CRM team.")
