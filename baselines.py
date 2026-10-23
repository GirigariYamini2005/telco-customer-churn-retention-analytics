import sqlite3
import pandas as pd

# 1. Connect to your local SQLite database
conn = sqlite3.connect("telco_churn.db")

print("==================================================")
print("     TELCO CUSTOMER CHURN: BUSINESS BASELINES     ")
print("==================================================\n")

# 1. Total Customer Base & Overall Churn Rate
q1 = """
SELECT 
    COUNT(*) AS Total_Customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS Churned_Customers,
    ROUND(CAST(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS REAL) / COUNT(*) * 100, 2) AS Overall_Churn_Rate_Pct
FROM telco_churn;
"""
print("--- 1. Overall Churn Rate ---")
print(pd.read_sql(q1, conn))
print("\n" + "-" * 50 + "\n")

# 2. Total Monthly Revenue (MRR) & Revenue at Risk
q2 = """
SELECT 
    ROUND(SUM(MonthlyCharges), 2) AS Total_Monthly_Revenue,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN MonthlyCharges ELSE 0 END), 2) AS Monthly_Revenue_Lost,
    ROUND(SUM(CASE WHEN Churn = 'No' THEN MonthlyCharges ELSE 0 END), 2) AS Retained_Monthly_Revenue
FROM telco_churn;
"""
print("--- 2. Monthly Revenue & Revenue at Risk ---")
print(pd.read_sql(q2, conn))
print("\n" + "-" * 50 + "\n")

# 3. Average Customer Tenure
q3 = """
SELECT 
    ROUND(AVG(tenure), 1) AS Avg_Tenure_Months,
    ROUND(AVG(CASE WHEN Churn = 'Yes' THEN tenure END), 1) AS Avg_Tenure_Of_Churned_Customers,
    ROUND(AVG(CASE WHEN Churn = 'No' THEN tenure END), 1) AS Avg_Tenure_Of_Retained_Customers
FROM telco_churn;
"""
print("--- 3. Customer Tenure Analysis ---")
print(pd.read_sql(q3, conn))
print("\n" + "-" * 50 + "\n")

# 4. Average Monthly Revenue Per User (ARPU)
q4 = """
SELECT 
    ROUND(AVG(MonthlyCharges), 2) AS Overall_ARPU,
    ROUND(AVG(CASE WHEN Churn = 'Yes' THEN MonthlyCharges END), 2) AS Churned_Customer_ARPU,
    ROUND(AVG(CASE WHEN Churn = 'No' THEN MonthlyCharges END), 2) AS Retained_Customer_ARPU
FROM telco_churn;
"""
print("--- 4. ARPU (Average Revenue Per User) ---")
print(pd.read_sql(q4, conn))



print("--- 5. CHURN RATE BY CONTRACT TYPE ---")
q5 = """
SELECT 
    Contract,
    COUNT(*) AS Total_Customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS Churned_Customers,
    ROUND(CAST(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS REAL) / COUNT(*) * 100, 2) AS Churn_Rate_Pct
FROM telco_churn
GROUP BY Contract
ORDER BY Churn_Rate_Pct DESC;
"""
print(pd.read_sql(q5, conn))
print("\n" + "="*50 + "\n")

print("--- 6. CHURN RATE BY INTERNET SERVICE ---")
q6 = """
SELECT 
    InternetService,
    COUNT(*) AS Total_Customers,
    ROUND(AVG(MonthlyCharges), 2) AS Avg_Monthly_Charges,
    ROUND(CAST(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS REAL) / COUNT(*) * 100, 2) AS Churn_Rate_Pct
FROM telco_churn
GROUP BY InternetService
ORDER BY Churn_Rate_Pct DESC;
"""
print(pd.read_sql(q6, conn))

# Close the database connection
conn.close()
print("\n==================================================")
print("     BASELINE EXTRACTION COMPLETE SUCCESSFULLY    ")
print("==================================================")