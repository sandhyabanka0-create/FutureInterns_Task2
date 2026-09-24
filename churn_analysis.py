import pandas as pd
import matplotlib.pyplot as plt

# Load the customer churn dataset
df = pd.read_csv("data/telco_churn.csv")

print("Dataset loaded successfully!")

# -----------------------------------
# 1. Basic dataset information
# -----------------------------------

print("\nDataset shape:")
print(df.shape)

print("\nColumn names:")
print(df.columns.tolist())

# -----------------------------------
# 2. Clean TotalCharges
# -----------------------------------

df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"],
    errors="coerce"
)

print("\nTotalCharges data type after cleaning:")
print(df["TotalCharges"].dtype)

print("\nMissing values after cleaning:")
print(df.isnull().sum())

# -----------------------------------
# 3. Check duplicates
# -----------------------------------

print("\nDuplicate rows:")
print(df.duplicated().sum())

# -----------------------------------
# 4. Churn distribution
# -----------------------------------

print("\nChurn distribution:")
print(df["Churn"].value_counts())

# -----------------------------------
# 5. Overall churn percentage
# -----------------------------------

churn_rate = (df["Churn"] == "Yes").mean() * 100

print("\nOverall churn rate:")
print(f"{churn_rate:.2f}%")

# -----------------------------------
# 6. Churn rate by contract type
# -----------------------------------

contract_churn = pd.crosstab(
    df["Contract"],
    df["Churn"],
    normalize="index"
) * 100

print("\nChurn rate by contract type:")
print(contract_churn.round(2))

# -----------------------------------
# 7. Churn rate by tenure group
# -----------------------------------

df["TenureGroup"] = pd.cut(
    df["tenure"],
    bins=[-1, 12, 24, 48, 60, float("inf")],
    labels=[
        "0-12 months",
        "13-24 months",
        "25-48 months",
        "49-60 months",
        "61+ months"
    ]
)

tenure_churn = pd.crosstab(
    df["TenureGroup"],
    df["Churn"],
    normalize="index"
) * 100

print("\nChurn rate by tenure group:")
print(tenure_churn.round(2))

# -----------------------------------
# 8. Churn rate by monthly charges
# -----------------------------------

df["MonthlyChargeGroup"] = pd.cut(
    df["MonthlyCharges"],
    bins=[0, 30, 60, 90, float("inf")],
    labels=[
        "0-30",
        "31-60",
        "61-90",
        "90+"
    ]
)

monthly_charges_churn = pd.crosstab(
    df["MonthlyChargeGroup"],
    df["Churn"],
    normalize="index"
) * 100

print("\nChurn rate by monthly charges:")
print(monthly_charges_churn.round(2))

# -----------------------------------
# 9. Churn rate by internet service
# -----------------------------------

internet_churn = pd.crosstab(
    df["InternetService"],
    df["Churn"],
    normalize="index"
) * 100

print("\nChurn rate by internet service:")
print(internet_churn.round(2))

# -----------------------------------
# 10. Churn rate by payment method
# -----------------------------------

payment_churn = pd.crosstab(
    df["PaymentMethod"],
    df["Churn"],
    normalize="index"
) * 100

print("\nChurn rate by payment method:")
print(payment_churn.round(2))

# -----------------------------------
# 11. Churn rate by Tech Support
# -----------------------------------

tech_support_churn = pd.crosstab(
    df["TechSupport"],
    df["Churn"],
    normalize="index"
) * 100

print("\nChurn rate by Tech Support:")
print(tech_support_churn.round(2))

# -----------------------------------
# 12. Churn rate by Online Security
# -----------------------------------

security_churn = pd.crosstab(
    df["OnlineSecurity"],
    df["Churn"],
    normalize="index"
) * 100

print("\nChurn rate by Online Security:")
print(security_churn.round(2))

# -----------------------------------
# 13. Customer lifetime analysis
# -----------------------------------

lifetime_summary = df.groupby("Churn").agg(
    AverageTenure=("tenure", "mean"),
    AverageMonthlyCharges=("MonthlyCharges", "mean"),
    AverageTotalCharges=("TotalCharges", "mean")
)

print("\nCustomer lifetime summary:")
print(lifetime_summary.round(2))

# -----------------------------------
# 14. Customer lifetime by tenure group
# -----------------------------------

lifetime_by_tenure = df.groupby(
    "TenureGroup",
    observed=True
).agg(
    Customers=("customerID", "count"),
    AverageMonthlyCharges=("MonthlyCharges", "mean"),
    AverageTotalCharges=("TotalCharges", "mean"),
    ChurnRate=("Churn", lambda x: (x == "Yes").mean() * 100)
)

print("\nCustomer lifetime by tenure group:")
print(lifetime_by_tenure.round(2))

# -----------------------------------
# 15. Overall churn chart
# -----------------------------------

churn_counts = df["Churn"].value_counts()

plt.figure(figsize=(7, 5))

plt.bar(
    churn_counts.index,
    churn_counts.values
)

plt.title("Customer Churn Distribution")
plt.xlabel("Churn")
plt.ylabel("Number of Customers")

for i, value in enumerate(churn_counts.values):
    plt.text(
        i,
        value + 50,
        str(value),
        ha="center"
    )

plt.tight_layout()

plt.savefig(
    "charts/churn_distribution.png",
    dpi=300
)

plt.close()

print("\nChart saved: charts/churn_distribution.png")

# -----------------------------------
# 16. Churn rate by contract chart
# -----------------------------------

contract_churn_rate = (
    df.groupby("Contract")["Churn"]
    .apply(lambda x: (x == "Yes").mean() * 100)
)

plt.figure(figsize=(8, 5))

plt.bar(
    contract_churn_rate.index,
    contract_churn_rate.values
)

plt.title("Churn Rate by Contract Type")
plt.xlabel("Contract Type")
plt.ylabel("Churn Rate (%)")

for i, value in enumerate(contract_churn_rate.values):
    plt.text(
        i,
        value + 1,
        f"{value:.2f}%",
        ha="center"
    )

plt.tight_layout()

plt.savefig(
    "charts/churn_rate_by_contract.png",
    dpi=300
)

plt.close()

print("\nChart saved: charts/churn_rate_by_contract.png")

# -----------------------------------
# 17. Churn rate by tenure chart
# -----------------------------------

tenure_churn_rate = (
    df.groupby("TenureGroup", observed=True)["Churn"]
    .apply(lambda x: (x == "Yes").mean() * 100)
)

plt.figure(figsize=(9, 5))

plt.bar(
    tenure_churn_rate.index.astype(str),
    tenure_churn_rate.values
)

plt.title("Churn Rate by Tenure Group")
plt.xlabel("Tenure Group")
plt.ylabel("Churn Rate (%)")

for i, value in enumerate(tenure_churn_rate.values):
    plt.text(
        i,
        value + 1,
        f"{value:.2f}%",
        ha="center"
    )

plt.tight_layout()

plt.savefig(
    "charts/churn_rate_by_tenure.png",
    dpi=300
)

plt.close()

print("\nChart saved: charts/churn_rate_by_tenure.png")

# -----------------------------------
# 18. Churn rate by internet service chart
# -----------------------------------

internet_churn_rate = (
    df.groupby("InternetService")["Churn"]
    .apply(lambda x: (x == "Yes").mean() * 100)
)

plt.figure(figsize=(8, 5))

plt.bar(
    internet_churn_rate.index,
    internet_churn_rate.values
)

plt.title("Churn Rate by Internet Service")
plt.xlabel("Internet Service")
plt.ylabel("Churn Rate (%)")

for i, value in enumerate(internet_churn_rate.values):
    plt.text(
        i,
        value + 1,
        f"{value:.2f}%",
        ha="center"
    )

plt.tight_layout()

plt.savefig(
    "charts/churn_rate_by_internet_service.png",
    dpi=300
)

plt.close()

print("\nChart saved: charts/churn_rate_by_internet_service.png")

# -----------------------------------
# 19. Churn rate by payment method chart
# -----------------------------------

payment_churn_rate = (
    df.groupby("PaymentMethod")["Churn"]
    .apply(lambda x: (x == "Yes").mean() * 100)
)

plt.figure(figsize=(10, 5))

plt.bar(
    payment_churn_rate.index,
    payment_churn_rate.values
)

plt.title("Churn Rate by Payment Method")
plt.xlabel("Payment Method")
plt.ylabel("Churn Rate (%)")

plt.xticks(
    rotation=20,
    ha="right"
)

for i, value in enumerate(payment_churn_rate.values):
    plt.text(
        i,
        value + 1,
        f"{value:.2f}%",
        ha="center"
    )

plt.tight_layout()

plt.savefig(
    "charts/churn_rate_by_payment_method.png",
    dpi=300
)

plt.close()

print("\nChart saved: charts/churn_rate_by_payment_method.png")

# -----------------------------------
# 20. Churn rate by Tech Support chart
# -----------------------------------

tech_support_churn_rate = (
    df.groupby("TechSupport")["Churn"]
    .apply(lambda x: (x == "Yes").mean() * 100)
)

plt.figure(figsize=(9, 5))

plt.bar(
    tech_support_churn_rate.index,
    tech_support_churn_rate.values
)

plt.title("Churn Rate by Tech Support")
plt.xlabel("Tech Support")
plt.ylabel("Churn Rate (%)")

for i, value in enumerate(tech_support_churn_rate.values):
    plt.text(
        i,
        value + 1,
        f"{value:.2f}%",
        ha="center"
    )

plt.tight_layout()

plt.savefig(
    "charts/churn_rate_by_tech_support.png",
    dpi=300
)

plt.close()

print("\nChart saved: charts/churn_rate_by_tech_support.png")

# -----------------------------------
# 21. Churn rate by Online Security chart
# -----------------------------------

security_churn_rate = (
    df.groupby("OnlineSecurity")["Churn"]
    .apply(lambda x: (x == "Yes").mean() * 100)
)

plt.figure(figsize=(9, 5))

plt.bar(
    security_churn_rate.index,
    security_churn_rate.values
)

plt.title("Churn Rate by Online Security")
plt.xlabel("Online Security")
plt.ylabel("Churn Rate (%)")

for i, value in enumerate(security_churn_rate.values):
    plt.text(
        i,
        value + 1,
        f"{value:.2f}%",
        ha="center"
    )

plt.tight_layout()

plt.savefig(
    "charts/churn_rate_by_online_security.png",
    dpi=300
)

plt.close()

print("\nChart saved: charts/churn_rate_by_online_security.png")

# -----------------------------------
# 22. Average customer tenure by churn
# -----------------------------------

average_tenure = df.groupby("Churn")["tenure"].mean()

plt.figure(figsize=(7, 5))

plt.bar(
    average_tenure.index,
    average_tenure.values
)

plt.title("Average Customer Tenure by Churn Status")
plt.xlabel("Churn Status")
plt.ylabel("Average Tenure (Months)")

for i, value in enumerate(average_tenure.values):
    plt.text(
        i,
        value + 1,
        f"{value:.2f}",
        ha="center"
    )

plt.tight_layout()

plt.savefig(
    "charts/average_customer_tenure_by_churn.png",
    dpi=300
)

plt.close()

print("\nChart saved: charts/average_customer_tenure_by_churn.png")