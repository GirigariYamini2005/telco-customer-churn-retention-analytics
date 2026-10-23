import sqlite3
import pandas as pd

# 1. Connect to SQLite (creates a local file named 'telco_churn.db' instantly)
conn = sqlite3.connect("telco_churn.db")

# 2. Read your CSV file from Downloads
file_path = r"C:\Users\girig\Downloads\Telco_Customer_Churn_Dataset .csv"
df = pd.read_csv(file_path)

# 3. Write the DataFrame into an SQLite table named 'telco_churn'
df.to_sql("telco_churn", conn, if_exists="replace", index=False)

# 4. Verify by running a quick count query
query_result = pd.read_sql(
    "SELECT COUNT(*) AS total_rows FROM telco_churn", conn
)
print(query_result)

conn.close()
print(
    "✓ Success! Your dataset is now stored locally in SQLite (`telco_churn.db`)."
)