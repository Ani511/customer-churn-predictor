# Customer Churn Prediction

An end-to-end **Machine Learning and Analytics project** that predicts whether a telecom customer is likely to churn.

The project combines **Exploratory Data Analysis, Machine Learning, SQL, Streamlit, and Power BI** to build a complete customer churn analysis and prediction workflow.

---

## Project Overview

Customer churn is a major challenge for subscription-based businesses. Identifying customers who are likely to leave can help companies take proactive retention actions.

This project analyzes telecom customer data and builds a machine learning model to predict customer churn based on factors such as:

* Customer demographics
* Contract type
* Tenure
* Monthly and total charges
* Internet service
* Payment method
* Online services
* Customer support services

The final solution includes:

**Data → EDA & Preprocessing → SQL Analysis → Machine Learning → Streamlit Prediction App → Power BI Dashboard**

---

## Objectives

The main objectives of this project are to:

* Understand customer churn patterns through EDA
* Clean and preprocess the telecom customer dataset
* Identify important factors associated with churn
* Handle class imbalance using **SMOTE**
* Compare multiple machine learning models
* Select the best-performing model
* Perform business analysis using SQL
* Build an interactive churn prediction application with Streamlit
* Visualize business insights through Power BI

---

## Dataset

The project uses the **Telco Customer Churn** dataset.

The dataset contains **7,043 customers and 21 columns** before preprocessing. Features include customer demographics, services, contract information, billing information, and the churn target.

### Key Features

| Feature            | Description                              |
| ------------------ | ---------------------------------------- |
| `gender`           | Customer gender                          |
| `SeniorCitizen`    | Whether the customer is a senior citizen |
| `Partner`          | Whether the customer has a partner       |
| `Dependents`       | Whether the customer has dependents      |
| `tenure`           | Number of months the customer has stayed |
| `PhoneService`     | Phone service subscription               |
| `MultipleLines`    | Multiple phone lines                     |
| `InternetService`  | Internet service type                    |
| `OnlineSecurity`   | Online security subscription             |
| `OnlineBackup`     | Online backup subscription               |
| `DeviceProtection` | Device protection subscription           |
| `TechSupport`      | Technical support subscription           |
| `StreamingTV`      | Streaming TV subscription                |
| `StreamingMovies`  | Streaming movies subscription            |
| `Contract`         | Contract duration                        |
| `PaperlessBilling` | Paperless billing status                 |
| `PaymentMethod`    | Payment method                           |
| `MonthlyCharges`   | Monthly customer charges                 |
| `TotalCharges`     | Total customer charges                   |
| `Churn`            | Target variable                          |

---

## Exploratory Data Analysis

The EDA phase focuses on understanding the structure of the dataset, cleaning incorrect values, and identifying patterns related to customer churn.

### Data Cleaning

The following preprocessing steps were performed:

1. Loaded the telecom customer dataset using Pandas.
2. Converted `TotalCharges` from object/string format to numeric.
3. Converted invalid values to missing values using `errors='coerce'`.
4. Removed missing records.
5. Removed the irrelevant `customerID` column.
6. Converted categorical variables into machine-readable features.
7. Split the processed dataset into training and testing sets.

### Important EDA Insights

The analysis identified several important churn patterns:

* Approximately **26% of customers churn**.
* **Month-to-month contract** customers show the highest churn.
* Many churned customers leave within their **first 1–2 years**.
* Lower `TotalCharges` are associated with higher churn.
* **Fiber optic** customers show higher churn in this dataset.
* Customers using **electronic check** have the highest churn probability.

### Visual Analysis

The project includes visualizations for:

* Customer churn distribution
* Churn by contract type
* Total charges by churn status
* Churn vs. customer tenure
* Churn by internet service
* Churn by payment method

---

## Machine Learning

Three classification models were evaluated:

1. **Logistic Regression** — baseline model
2. **Random Forest** — robust and explainable tree-based model
3. **XGBoost** — gradient boosting model

Because the churn dataset is imbalanced, **SMOTE (Synthetic Minority Oversampling Technique)** was applied to the training data before model training.

### Model Performance

| Model               |   Accuracy |   ROC-AUC |
| ------------------- | ---------: | --------: |
| Logistic Regression |     74.20% |     0.707 |
| **Random Forest**   | **77.33%** | **0.718** |
| XGBoost             |     75.98% |     0.702 |

Based on the evaluated results, **Random Forest performed the best** among the three models.

### Final Model

The final model selected for deployment is:

**Random Forest Classifier**

Performance:

* **Accuracy:** 77.33%
* **ROC-AUC:** 0.718
* **Churn recall:** 60%
* **Churn F1-score:** 0.58

Hyperparameter tuning was also performed using `RandomizedSearchCV` for Random Forest and `GridSearchCV` for XGBoost.

---

## Feature Importance

Feature importance was analyzed using the trained Random Forest model.

The project generates a **Top 10 Feature Importance** visualization to identify which encoded customer attributes contribute most to the model's predictions. The final notebook explicitly selects Random Forest as the best model.

This helps translate the machine learning model into actionable business insights.

---

## SQL Analysis

SQL was integrated into the project using **SQLite**.

The customer CSV data is loaded into a SQLite database and stored in a `customers` table.

SQL analysis is used to investigate important business metrics such as:

* Total number of churned customers
* Overall churn rate
* Churn rate by contract type
* Average monthly charges of churned vs. retained customers
* Customer-level churn patterns

All SQL queries are organized inside the:

```text
sql/
└── queries.sql
```

The SQL workflow is documented in:

```text
sql_analysis.ipynb
```

---

## Power BI Dashboard

A Power BI dashboard was created to transform the analysis into business-friendly visual insights.

### Dashboard Focus

The dashboard provides insights into:

* Churn rate by contract type
* Monthly charges
* Customer tenure
* Payment method trends
* Customer churn patterns

Power BI file:

```text
churn_dashboard.pbix
```

The dashboard complements the machine learning model by providing a business-level view of customer churn.

---

## Streamlit Web Application

The project includes an interactive **Streamlit** application for real-time churn prediction.

The application allows users to enter customer information such as:

* Gender
* Senior citizen status
* Partner and dependents
* Tenure
* Phone service
* Internet service
* Online security
* Online backup
* Device protection
* Tech support
* Streaming services
* Contract type
* Paperless billing
* Payment method
* Monthly charges
* Total charges

After submitting the form, the trained model predicts whether the customer is likely to churn and displays the estimated churn probability.

### Prediction Output

The application provides two outcomes:

**High risk of churn**

or

**Customer likely to stay**

The prediction is generated using the saved trained model.

---

## Project Structure

```text
customer-churn-predictor/
│
├── app/
│   ├── app.py
│   └── churn_model.pkl
│
├── data/
│   ├── WA_Fn-UseC_-Telco-Customer-Churn.csv
│   └── telco_churn.db
│
├── images/
│   ├── powerbi.png
│   └── EDA screenshots
│
├── sql/
│   └── queries.sql
│
├── EDA.ipynb
├── sql_analysis.ipynb
├── churn_dashboard.pbix
├── requirements.txt
└── README.md
```

---

##  Tech Stack

### Programming & Data

* Python
* Pandas
* NumPy

### Machine Learning

* Scikit-learn
* Random Forest
* Logistic Regression
* XGBoost
* Imbalanced-learn / SMOTE
* Joblib

### Data Analysis

* Matplotlib
* Seaborn
* Jupyter Notebook

### Database

* SQLite
* SQL

### Visualization

* Power BI

### Deployment

* Streamlit

---

## Installation & Setup

Clone the repository:

```bash
git clone https://github.com/Ani511/customer-churn-predictor.git
cd customer-churn-predictor
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the environment.

### Windows

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Run the Streamlit App

From the project root directory:

```bash
streamlit run app/app.py
```

The application will open in your browser.

---

## Notebooks

### EDA & Machine Learning

```text
EDA.ipynb
```

Contains:

* Dataset exploration
* Data cleaning
* EDA visualizations
* Feature preprocessing
* SMOTE
* Model training
* Model comparison
* Hyperparameter tuning
* Feature importance
* Final model selection

### SQL Analysis

```text
sql_analysis.ipynb
```

Contains the SQLite database integration and SQL-based customer churn analysis.

---

## Key Business Insights

The project demonstrates that customer churn is strongly associated with several customer characteristics.

### Contract Type

Month-to-month customers represent an important churn-risk segment.

### Tenure

Customers with shorter tenure are more likely to churn, highlighting the importance of early customer retention.

### Payment Method

Electronic check users show a comparatively higher churn probability.

### Internet Service

Fiber optic customers show higher churn in the analyzed dataset.

### Customer Charges

Lower total charges are associated with churn, which is consistent with many churned customers having relatively shorter tenure.

These insights can help businesses design targeted retention strategies.

---

## Business Use Case

A telecom company can use this solution to:

* Identify high-risk customers
* Prioritize retention campaigns
* Offer targeted discounts or plans
* Understand customer churn drivers
* Monitor churn trends through dashboards
* Support data-driven customer retention decisions

The model should be treated as a **decision-support tool**, rather than an automatic replacement for business judgment.

---

## Future Improvements

Possible improvements for the project include:

* Feature engineering for stronger predictive performance
* Cross-validation with additional evaluation metrics
* Probability calibration
* Churn-risk segmentation into low, medium, and high-risk groups
* SHAP-based model explainability
* Automated model retraining
* API-based model serving
* Cloud deployment
* Automated Power BI data refresh
* Monitoring model performance after deployment

---

## Project Results

| Metric             |        Result |
| ------------------ | ------------: |
| Customers analyzed |         7,043 |
| Approx. churn rate |          ~26% |
| Best model         | Random Forest |
| Accuracy           |    **77.33%** |
| ROC-AUC            |     **0.718** |
| Churn recall       |       **60%** |
| Churn F1-score     |      **0.58** |

The reported model metrics come from the project's test-set evaluation after applying SMOTE to the training data.

---

## Project Links

**GitHub Repository:**
https://github.com/Ani511/customer-churn-predictor

**Live Streamlit App:**
https://rqksaqtxnqpiqt9nh5nmpw.streamlit.app/

---
