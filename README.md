# Customer Churn Risk Modeling & SQL-Driven Retention Intelligence System

Personal Project | Python, LightGBM, SHAP, SQL, Explainable ML

## Overview
End-to-end churn analytics pipeline on the Telco Customer Churn dataset (7,043 customers). Combines SQL-based business analysis, a LightGBM classification model, SHAP explainability, and a retention-campaign ROI simulation — built to mirror how a data analytics team would actually diagnose and act on churn, not just predict it.

## Problem
Telecom providers lose recurring revenue to churn. The business questions this project answers:
- Which customer segments churn the most, and why?
- How much monthly recurring revenue is currently being lost?
- Which model features actually drive churn risk?
- If we ran a retention campaign, who should we target, and is it worth the cost?

## Pipeline

| Step | File | What it does |
|---|---|---|
| 1 | `01_eda.py` | Cleans raw data, computes churn rate by contract/tenure/service, quantifies revenue lost |
| 2 | `00_load_to_sql.py` | Loads cleaned data into a local SQLite database |
| 3 | `01b_sql_eda.py` | Business-question SQL queries (segment churn rates, revenue-at-risk by service, compounded-risk segments) |
| 4 | `02_model.py` | Feature engineering + LightGBM classifier + SHAP explainability |
| 5 | `03_business_impact.py` | Risk-tier segmentation + retention campaign ROI simulation |

Run order:
```
python 01_eda.py
python 00_load_to_sql.py
python 01b_sql_eda.py
python 02_model.py
python 03_business_impact.py
```

## Key Findings

- **Overall churn rate:** 26.54%
- **Highest-risk segment:** Month-to-month contract + no tech support → **50.4% churn rate** (2,680 customers)
- **Contract type is the strongest churn driver:** Month-to-month (42.7%) vs. One-year (11.3%) vs. Two-year (2.8%)
- **New customers churn most:** 47.7% churn in the first 12 months, dropping to 6.6% after 5+ years
- **Revenue exposure:** $139,131 in monthly recurring revenue currently lost to churn (**$1.67M annualized**), with Fiber optic customers accounting for the largest share ($114,300/mo)

## Model Performance

- **Algorithm:** LightGBM (class-weight balanced for imbalanced churn data)
- **Test AUC:** 0.845
- **Recall (churn class):** 79% — prioritized over raw accuracy, since missing a churner is costlier than a false alarm
- **Explainability:** SHAP summary and importance plots identify contract type, tenure, monthly charges, and tech support as top churn drivers

## Business Impact Simulation

Using model-predicted churn probabilities, customers were segmented into Low/Medium/High risk tiers. A simulated retention campaign (assumed $15/customer cost, 25% offer-acceptance rate — an industry-typical estimate, not a measured figure) targeting the 308 High-risk customers projects:

- **Campaign cost:** $4,620
- **Projected annual revenue saved:** $72,270
- **Estimated ROI:** 1,464%

*Note: ROI is a modeled projection based on an assumed success rate, not an observed outcome — flagged here for transparency.*

## Outputs
- `outputs/shap_summary.png`, `outputs/shap_importance_bar.png` — model explainability
- `outputs/precision_recall_curve.png` — model evaluation
- `outputs/churn_by_contract.png`, `outputs/churn_by_tenure.png` — EDA visuals
- `outputs/retention_priority_list.csv` — ranked customer outreach list

## Tech Stack
Python (pandas, scikit-learn, LightGBM, SHAP, matplotlib/seaborn), SQL (SQLite)

## Dataset
[Telco Customer Churn — Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
