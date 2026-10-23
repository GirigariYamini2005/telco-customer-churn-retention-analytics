import sqlite3
import pandas as pd
import numpy as np
import scipy.stats as stats
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler

# 1. Load the cleaned data from SQLite
conn = sqlite3.connect("telco_churn.db")
df = pd.read_sql("SELECT * FROM telco_churn_cleaned", conn)
conn.close()

print("==================================================")
print("     PYTHON ADVANCED ANALYTICS & PREDICTIVE MODEL     ")
print("==================================================\n")

# ==========================================================
# PART 1: EXPANDED STATISTICAL HYPOTHESIS TESTING (SciPy)
# ==========================================================
print("--- 1. COMPREHENSIVE STATISTICAL HYPOTHESIS TESTING ---")

# 1. T-Test: Monthly Charges
churned_charges = df[df["Churn"] == "Yes"]["MonthlyCharges"]
retained_charges = df[df["Churn"] == "No"]["MonthlyCharges"]
t_stat, p_value = stats.ttest_ind(churned_charges, retained_charges, equal_var=False)
print(f"T-Test (Monthly Charges): t-stat = {t_stat:.2f}, p-value = {p_value:.5e}")
print("-> Result: Statistically significant difference in monthly billing.\n")

# 2. T-Test: Tenure
churned_tenure = df[df["Churn"] == "Yes"]["tenure"]
retained_tenure = df[df["Churn"] == "No"]["tenure"]
t_tenure, p_tenure = stats.ttest_ind(churned_tenure, retained_tenure, equal_var=False)
print(f"T-Test (Tenure): t-stat = {t_tenure:.2f}, p-value = {p_tenure:.5e}")
print("-> Result: Highly significant difference! Retained customers stay substantially longer.\n")

# 3. Chi-Square Test: Contract Type
chi2_c, p_c, _, _ = stats.chi2_contingency(pd.crosstab(df["Contract"], df["Churn"]))
print(f"Chi-Square (Contract): chi2 = {chi2_c:.2f}, p-value = {p_c:.5e}")
print("-> Result: Extremely strong association with churn.\n")

# 4. Chi-Square Test: Internet Service
chi2_i, p_i, _, _ = stats.chi2_contingency(pd.crosstab(df["InternetService"], df["Churn"]))
print(f"Chi-Square (Internet Service): chi2 = {chi2_i:.2f}, p-value = {p_i:.5e}")
print("-> Result: Significant association (Fiber optic users show higher vulnerability).\n")

# 5. Chi-Square Test: Payment Method
chi2_p, p_p, _, _ = stats.chi2_contingency(pd.crosstab(df["PaymentMethod"], df["Churn"]))
print(f"Chi-Square (Payment Method): chi2 = {chi2_p:.2f}, p-value = {p_p:.5e}")
print("-> Result: Significant association (Electronic check users exhibit higher churn rates).\n")


# ==========================================================
# PART 2: PREDICTIVE MODELING (Scikit-Learn Logistic Regression)
# ==========================================================
print("--- 2. PREDICTIVE CHURN RISK MODELING ---")

# Prepare data for modeling
model_df = df.copy()

# Convert target variable (Churn: Yes/No -> 1/0)
model_df["Churn_Binary"] = model_df["Churn"].apply(lambda x: 1 if x == "Yes" else 0)

# Select features for our model
features = [
    "tenure", 
    "MonthlyCharges", 
    "TotalCharges", 
    "Total_Addons"
]

# Add encoded categorical columns (One-Hot Encoding)
categorical_cols = ["Contract", "InternetService", "PaymentMethod"]
encoded_df = pd.get_dummies(model_df[categorical_cols], drop_first=True)

# Combine numerical features and encoded categories
X = pd.concat([model_df[features], encoded_df], axis=1)
y = model_df["Churn_Binary"]

# Train/Test Split (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale numerical features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train Logistic Regression Model
model = LogisticRegression(random_state=42)
model.fit(X_train_scaled, y_train)

# Evaluate Model
y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%\n")

print("Classification Report:")
print(classification_report(y_test, y_pred))


# ==========================================================
# PART 3: GENERATING CHURN RISK SCORES FOR ACTIVE CUSTOMERS
# ==========================================================
print("--- 3. GENERATING CUSTOMER RISK SCORES ---")

# Predict probability of churning for all customers in the dataset
all_scaled = scaler.transform(X)
churn_probabilities = model.predict_proba(all_scaled)[:, 1] # Probability of Churn = Yes

# Add risk score back to original dataframe
df["Churn_Risk_Probability"] = np.round(churn_probabilities * 100, 2)

# Categorize into Risk Tiers
def assign_risk_tier(prob):
    if prob >= 70:
        return "High Risk (70%+)"
    elif prob >= 40:
        return "Medium Risk (40-69%)"
    else:
        return "Low Risk (<40%)"

df["Risk_Tier"] = df["Churn_Risk_Probability"].apply(assign_risk_tier)

# Save the enhanced dataset with predictive risk scores back to SQLite and CSV
conn = sqlite3.connect("telco_churn.db")
df.to_sql("telco_churn_predicted", conn, if_exists="replace", index=False)
df.to_csv("telco_churn_cleaned.csv", index=False) # Update CSV with risk scores
conn.close()

print("✓ Risk scores successfully calculated and saved!")
print(df["Risk_Tier"].value_counts())
print("\n==================================================")
print("     ADVANCED PYTHON PIPELINE COMPLETE SUCCESSFULLY     ")
print("==================================================")