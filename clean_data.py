import sqlite3
import pandas as pd

# 1. Connect to SQLite and load the raw table
conn = sqlite3.connect("telco_churn.db")
df = pd.read_sql("SELECT * FROM telco_churn", conn)
conn.close()

# 2. Handle missing/blank values in 'TotalCharges'
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df["TotalCharges"] = df["TotalCharges"].fillna(0)

# 3. Feature Engineering: Create Tenure Cohorts
def assign_tenure_cohort(tenure):
    if tenure <= 12:
        return "0-1 Year"
    elif tenure <= 24:
        return "1-2 Years"
    elif tenure <= 48:
        return "2-4 Years"
    else:
        return "4+ Years"

df["Tenure_Cohort"] = df["tenure"].apply(assign_tenure_cohort)

# 4. Feature Engineering: Total Add-ons Count
addon_cols = [
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
]
df["Total_Addons"] = (df[addon_cols] == "Yes").sum(axis=1)

# 5. Save the cleaned table back into SQLite
conn = sqlite3.connect("telco_churn.db")
df.to_sql("telco_churn_cleaned", conn, if_exists="replace", index=False)
conn.close()

print("✓ Cleaned table 'telco_churn_cleaned' successfully created in SQLite!")