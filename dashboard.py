import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Customer Retention & Churn Dashboard",
    page_icon="📊",
    layout="wide"
)

# =========================================================
# LOAD DATA
# =========================================================

df = pd.read_csv("data/telco_churn.csv")

# Convert TotalCharges to numeric
df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"],
    errors="coerce"
)

# =========================================================
# CREATE TENURE GROUPS
# =========================================================

df["TenureGroup"] = pd.cut(
    df["tenure"],
    bins=[0, 12, 24, 48, 60, float("inf")],
    labels=["0-12", "13-24", "25-48", "49-60", "61+"],
    include_lowest=True
)

# =========================================================
# TITLE
# =========================================================

st.title("📊 Customer Retention & Churn Analysis")

st.write(
    "This dashboard analyzes customer churn, contract type, "
    "tenure, internet service, payment method, and support services."
)

st.info(
    "Note: The relationships shown in this dashboard are "
    "associations in the dataset and should not be interpreted "
    "as proof of causation."
)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.header("Dashboard Information")

st.sidebar.write(
    "Use this dashboard to explore customer churn and retention patterns."
)

st.sidebar.write("### Dataset")
st.sidebar.write(f"Customers: {len(df):,}")
st.sidebar.write(f"Columns: {len(df.columns):,}")
st.sidebar.write(
    f"Missing TotalCharges: {df['TotalCharges'].isna().sum():,}"
)

# =========================================================
# KEY PERFORMANCE INDICATORS
# =========================================================

total_customers = len(df)
churned_customers = (df["Churn"] == "Yes").sum()
churn_rate = (churned_customers / total_customers) * 100
average_tenure = df["tenure"].mean()

st.header("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Customers",
        f"{total_customers:,}"
    )

with col2:
    st.metric(
        "Churned Customers",
        f"{churned_customers:,}"
    )

with col3:
    st.metric(
        "Overall Churn Rate",
        f"{churn_rate:.2f}%"
    )

with col4:
    st.metric(
        "Average Tenure",
        f"{average_tenure:.2f} months"
    )

# =========================================================
# HELPER FUNCTION
# =========================================================

def create_bar_chart(data, title, xlabel, ylabel="Churn Rate (%)"):
    fig, ax = plt.subplots(figsize=(8, 5))

    ax.bar(
        data.index.astype(str),
        data.values
    )

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)


# =========================================================
# 1. CHURN RATE BY CONTRACT TYPE
# =========================================================

st.header("1. Churn Rate by Contract Type")

contract_churn = (
    df.groupby("Contract", observed=False)["Churn"]
    .apply(lambda x: (x == "Yes").mean() * 100)
)

create_bar_chart(
    contract_churn,
    "Churn Rate by Contract Type",
    "Contract Type"
)

# =========================================================
# 2. CHURN RATE BY CUSTOMER TENURE
# =========================================================

st.header("2. Churn Rate by Customer Tenure")

tenure_churn = (
    df.groupby("TenureGroup", observed=False)["Churn"]
    .apply(lambda x: (x == "Yes").mean() * 100)
)

create_bar_chart(
    tenure_churn,
    "Churn Rate by Customer Tenure",
    "Tenure Group"
)

# =========================================================
# 3. CHURN RATE BY INTERNET SERVICE
# =========================================================

st.header("3. Churn Rate by Internet Service")

internet_churn = (
    df.groupby("InternetService")["Churn"]
    .apply(lambda x: (x == "Yes").mean() * 100)
)

create_bar_chart(
    internet_churn,
    "Churn Rate by Internet Service",
    "Internet Service"
)

# =========================================================
# 4. CHURN RATE BY PAYMENT METHOD
# =========================================================

st.header("4. Churn Rate by Payment Method")

payment_churn = (
    df.groupby("PaymentMethod")["Churn"]
    .apply(lambda x: (x == "Yes").mean() * 100)
)

create_bar_chart(
    payment_churn,
    "Churn Rate by Payment Method",
    "Payment Method"
)

# =========================================================
# 5. CHURN RATE BY TECH SUPPORT
# =========================================================

st.header("5. Churn Rate by Tech Support")

support_churn = (
    df.groupby("TechSupport")["Churn"]
    .apply(lambda x: (x == "Yes").mean() * 100)
)

create_bar_chart(
    support_churn,
    "Churn Rate by Tech Support",
    "Tech Support"
)

# =========================================================
# 6. CHURN RATE BY ONLINE SECURITY
# =========================================================

st.header("6. Churn Rate by Online Security")

security_churn = (
    df.groupby("OnlineSecurity")["Churn"]
    .apply(lambda x: (x == "Yes").mean() * 100)
)

create_bar_chart(
    security_churn,
    "Churn Rate by Online Security",
    "Online Security"
)

# =========================================================
# 7. AVERAGE CUSTOMER TENURE BY CHURN STATUS
# =========================================================

st.header("7. Average Customer Tenure by Churn Status")

average_tenure_churn = df.groupby("Churn")["tenure"].mean()

create_bar_chart(
    average_tenure_churn,
    "Average Customer Tenure by Churn Status",
    "Churn Status",
    "Average Tenure (Months)"
)

# =========================================================
# 8. CUSTOMER LIFETIME SUMMARY
# =========================================================

st.header("8. Customer Lifetime Summary")

lifetime_summary = df.groupby("Churn").agg(
    Customers=("customerID", "count"),
    AverageTenure=("tenure", "mean"),
    AverageMonthlyCharges=("MonthlyCharges", "mean"),
    AverageTotalCharges=("TotalCharges", "mean")
)

# Display lifetime summary as a Markdown table
st.markdown(
    f"""
| Churn Status | Customers | Average Tenure (Months) | Average Monthly Charges | Average Total Charges |
|---|---:|---:|---:|---:|
| No | {lifetime_summary.loc["No", "Customers"]:,} | {lifetime_summary.loc["No", "AverageTenure"]:.2f} | {lifetime_summary.loc["No", "AverageMonthlyCharges"]:.2f} | {lifetime_summary.loc["No", "AverageTotalCharges"]:.2f} |
| Yes | {lifetime_summary.loc["Yes", "Customers"]:,} | {lifetime_summary.loc["Yes", "AverageTenure"]:.2f} | {lifetime_summary.loc["Yes", "AverageMonthlyCharges"]:.2f} | {lifetime_summary.loc["Yes", "AverageTotalCharges"]:.2f} |
"""
)

# =========================================================
# KEY INSIGHTS
# =========================================================

st.header("📌 Key Insights")

st.subheader("Overall Churn")

st.write(
    f"- The overall customer churn rate is **{churn_rate:.2f}%**."
)

st.write(
    f"- There are **{churned_customers:,} churned customers** "
    f"out of **{total_customers:,} customers**."
)

st.subheader("Customer Tenure")

st.write(
    "- Customers with shorter tenure show higher observed churn rates."
)

st.write(
    "- The **0-12 month** customer group has the highest churn rate "
    "among the tenure groups."
)

st.subheader("Contract Type")

st.write(
    "- Month-to-month customers have a substantially higher observed "
    "churn rate than customers on longer contracts."
)

st.write(
    "- Longer-contract customers show lower observed churn rates "
    "in this dataset."
)

st.subheader("Customer Lifetime")

st.write(
    "- Churned customers have a shorter average observed tenure "
    "than retained customers."
)

st.write(
    "- This suggests that the early customer lifecycle is an "
    "important area to investigate for retention efforts."
)

st.subheader("Support Services")

st.write(
    "- Customers with Tech Support show a different observed "
    "churn rate from customers without Tech Support."
)

st.write(
    "- Customers with Online Security also show a different "
    "observed churn rate from customers without the service."
)

# =========================================================
# LIMITATIONS
# =========================================================

st.info("Dataset Limitations")

st.write(
    "The dataset does not contain signup month/date or customer "
    "region information. Therefore, signup-month and region-based "
    "cohort analysis could not be performed from the available data."
)

st.write(
    "The findings describe associations in the dataset and do "
    "not establish causal relationships."
)

# =========================================================
# FOOTER
# =========================================================

st.write("---")

st.caption(
    "Future Interns – Data Science & Analytics Task 2 | "
    "Customer Retention & Churn Analysis"
)