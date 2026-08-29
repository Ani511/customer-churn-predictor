"""
02_model.py
Feature engineering + LightGBM churn model + SHAP explainability.
Run 01_eda.py first to generate data/telco_cleaned.csv
"""

import pandas as pd
import numpy as np
import lightgbm as lgb
import shap
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    roc_auc_score,
    classification_report,
    confusion_matrix,
    precision_recall_curve,
)

df = pd.read_csv("data/telco_cleaned.csv")

# ---- Drop ID + leakage cols ----
df = df.drop(columns=["customerID", "Churn"])  # Churn_Flag is the target

# ---- Feature engineering ----
df["avg_monthly_spend"] = df["TotalCharges"] / df["tenure"].replace(0, 1)
df["is_new_customer"] = (df["tenure"] <= 6).astype(int)
df["num_services"] = df[
    ["PhoneService", "OnlineSecurity", "OnlineBackup", "DeviceProtection",
     "TechSupport", "StreamingTV", "StreamingMovies"]
].apply(lambda row: sum(v == "Yes" for v in row), axis=1)

# ---- Encode categoricals ----
cat_cols = df.select_dtypes(include="object").columns.tolist()
for c in cat_cols:
    df[c] = df[c].astype("category")

X = df.drop(columns=["Churn_Flag", "tenure_bucket"], errors="ignore")
y = df["Churn_Flag"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ---- LightGBM model ----
model = lgb.LGBMClassifier(
    n_estimators=300,
    learning_rate=0.05,
    num_leaves=31,
    class_weight="balanced",  # churn datasets are usually imbalanced
    random_state=42,
)

model.fit(
    X_train, y_train,
    eval_set=[(X_test, y_test)],
    eval_metric="auc",
    callbacks=[lgb.early_stopping(30), lgb.log_evaluation(0)],
)

# ---- Evaluate ----
y_pred_proba = model.predict_proba(X_test)[:, 1]
y_pred = model.predict(X_test)

auc = roc_auc_score(y_test, y_pred_proba)
print(f"\nTest AUC: {auc:.4f}")
print("\nClassification report:\n", classification_report(y_test, y_pred))
print("\nConfusion matrix:\n", confusion_matrix(y_test, y_pred))

# ---- Precision-recall curve (better than accuracy for imbalanced churn) ----
precision, recall, thresholds = precision_recall_curve(y_test, y_pred_proba)
plt.figure(figsize=(6, 4))
plt.plot(recall, precision)
plt.xlabel("Recall")
plt.ylabel("Precision")
plt.title("Precision-Recall Curve — Churn Model")
plt.tight_layout()
plt.savefig("outputs/precision_recall_curve.png", dpi=150)
plt.close()

# ---- SHAP explainability (this is the differentiator recruiters notice) ----
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

# shap_values may be a list for binary classifiers depending on version
sv = shap_values[1] if isinstance(shap_values, list) else shap_values

plt.figure()
shap.summary_plot(sv, X_test, show=False)
plt.tight_layout()
plt.savefig("outputs/shap_summary.png", dpi=150, bbox_inches="tight")
plt.close()

plt.figure()
shap.summary_plot(sv, X_test, plot_type="bar", show=False)
plt.tight_layout()
plt.savefig("outputs/shap_importance_bar.png", dpi=150, bbox_inches="tight")
plt.close()

# ---- Save predictions for business impact script ----
results = X_test.copy()
results["actual_churn"] = y_test.values
results["churn_probability"] = y_pred_proba
results.to_csv("outputs/churn_predictions.csv", index=False)

model.booster_.save_model("outputs/lgbm_churn_model.txt")

print("\nSaved: outputs/churn_predictions.csv, SHAP plots, PR curve, model file.")
