-- Total Churned Customers
SELECT COUNT(*) AS total_churned
FROM customers
WHERE Churn = 'Yes';

-- Churn Rate by Contract Type
SELECT Contract, COUNT(*) AS total, 
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END)*1.0/COUNT(*) AS churn_rate
FROM customers
GROUP BY Contract
ORDER BY churn_rate DESC;

-- Average Monthly Charges by Churn
SELECT Churn, AVG(MonthlyCharges) AS avg_monthly
FROM customers
GROUP BY Churn;
