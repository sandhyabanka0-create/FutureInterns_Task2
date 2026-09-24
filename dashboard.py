import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# ---------------------------------------------------------
# PAGE SETTINGS
# ---------------------------------------------------------

st.set_page_config(
    page_title="Customer Retention & Churn Dashboard",
    page_icon="📊",
    layout="wide"
)


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

df = pd.read_csv("data/telco_churn.csv")

# Convert TotalCharges to numeric
df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"],
    errors="coerce"
)


# ---------------------------------------------------------
# CREATE TENURE GROUPS
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------

st.title("📊 Customer Retention & Churn Analysis")

st.markdown(
    """
    **Customer Retention & Churn Dashboard**

    This dashboard analyzes customer churn, contract type,
    tenure, internet service, payment method, and support services.

    **Note:** The relationships shown in this dashboard are
    associations in the dataset and should not be interpreted
    as proof of causation.
    """
)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

st.sidebar.header("Dashboard Information")

st.sidebar.write(
    "Use this dashboard to explore customer churn "
    "and retention patterns."
)

st.sidebar.markdown("---")

st.sidebar.subheader("Dataset")

st.sidebar.write(f"Customers: {len(df):,}")
st.sidebar.write(f"Columns: {len(df.columns):,}")

missing_total = df["TotalCharges"].isna().sum()

st.sidebar.write(
    f"Missing TotalCharges: {missing_total}"
)


# ---------------------------------------------------------
# KPI CALCULATIONS
# ---------------------------------------------------------

total_customers = len(df)

churned_customers = (df["Churn"] == "Yes").sum()

churn_rate = (
    churned_customers / total_customers
) * 100

average_tenure = df["tenure"].mean()

average_monthly_charges = df["MonthlyCharges"].mean()


# ---------------------------------------------------------
# KPI CARDS
# ---------------------------------------------------------

st.subheader("Key Performance Indicators")

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


# ---------------------------------------------------------
# HELPER FUNCTION
# ---------------------------------------------------------

def calculate_churn_rate(data, column):

    result = data.groupby(column)["Churn"].apply(
        lambda x: (x == "Yes").mean() * 100
    )

    return result


def create_bar_chart(
    values,
    title,
    xlabel,
    ylabel="Churn Rate (%)",
    rotation=0
):

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.bar(
        values.index.astype(str),
        values.values
    )

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    plt.xticks(
        rotation=rotation,
        ha="right"
    )

    for i, value in enumerate(values.values):

        ax.text(
            i,
            value + 1,
            f"{value:.2f}%",
            ha="center"
        )

    plt.tight_layout()

    return fig


# ---------------------------------------------------------
# CHART 1 - CHURN BY CONTRACT
# ---------------------------------------------------------

st.subheader("1. Churn Rate by Contract Type")

contract_churn = calculate_churn_rate(
    df,
    "Contract"
)

fig = create_bar_chart(
    contract_churn,
    "Churn Rate by Contract Type",
    "Contract"
)

st.pyplot(fig)

plt.close(fig)


# ---------------------------------------------------------
# CHART 2 - CHURN BY TENURE
# ---------------------------------------------------------

st.subheader("2. Churn Rate by Customer Tenure")

tenure_churn = calculate_churn_rate(
    df,
    "TenureGroup"
)

fig = create_bar_chart(
    tenure_churn,
    "Churn Rate by Tenure Group",
    "Tenure Group"
)

st.pyplot(fig)

plt.close(fig)


# ---------------------------------------------------------
# CHART 3 - INTERNET SERVICE
# ---------------------------------------------------------

st.subheader("3. Churn Rate by Internet Service")

internet_churn = calculate_churn_rate(
    df,
    "InternetService"
)

fig = create_bar_chart(
    internet_churn,
    "Churn Rate by Internet Service",
    "Internet Service"
)

st.pyplot(fig)

plt.close(fig)


# ---------------------------------------------------------
# CHART 4 - PAYMENT METHOD
# ---------------------------------------------------------

st.subheader("4. Churn Rate by Payment Method")

payment_churn = calculate_churn_rate(
    df,
    "PaymentMethod"
)

fig = create_bar_chart(
    payment_churn,
    "Churn Rate by Payment Method",
    "Payment Method",
    rotation=20
)

st.pyplot(fig)

plt.close(fig)


# ---------------------------------------------------------
# TWO COLUMN SECTION
# ---------------------------------------------------------

col1, col2 = st.columns(2)


# ---------------------------------------------------------
# CHART 5 - TECH SUPPORT
# ---------------------------------------------------------

with col1:

    st.subheader("5. Churn Rate by Tech Support")

    tech_support_churn = calculate_churn_rate(
        df,
        "TechSupport"
    )

    fig = create_bar_chart(
        tech_support_churn,
        "Churn Rate by Tech Support",
        "Tech Support"
    )

    st.pyplot(fig)

    plt.close(fig)


# ---------------------------------------------------------
# CHART 6 - ONLINE SECURITY
# ---------------------------------------------------------

with col2:

    st.subheader("6. Churn Rate by Online Security")

    security_churn = calculate_churn_rate(
        df,
        "OnlineSecurity"
    )

    fig = create_bar_chart(
        security_churn,
        "Churn Rate by Online Security",
        "Online Security"
    )

    st.pyplot(fig)

    plt.close(fig)


# ---------------------------------------------------------
# CUSTOMER LIFETIME ANALYSIS
# ---------------------------------------------------------

st.subheader("7. Average Customer Tenure by Churn Status")

average_tenure_by_churn = (
    df.groupby("Churn")["tenure"].mean()
)

fig, ax = plt.subplots(figsize=(7, 5))

ax.bar(
    average_tenure_by_churn.index,
    average_tenure_by_churn.values
)

ax.set_title(
    "Average Customer Tenure by Churn Status"
)

ax.set_xlabel("Churn Status")
ax.set_ylabel("Average Tenure (Months)")

for i, value in enumerate(
    average_tenure_by_churn.values
):

    ax.text(
        i,
        value + 1,
        f"{value:.2f}",
        ha="center"
    )

plt.tight_layout()

st.pyplot(fig)

plt.close(fig)


# ---------------------------------------------------------
# CUSTOMER LIFETIME TABLE
# ---------------------------------------------------------

st.subheader("8. Customer Lifetime Summary")

lifetime_summary = df.groupby("Churn").agg(
    Customers=("customerID", "count"),
    AverageTenure=("tenure", "mean"),
    AverageMonthlyCharges=("MonthlyCharges", "mean"),
    AverageTotalCharges=("TotalCharges", "mean")
)

st.dataframe(
    lifetime_summary.round(2),
    use_container_width=True
)


# ---------------------------------------------------------
# KEY INSIGHTS
# ---------------------------------------------------------

st.subheader("📌 Key Insights")

st.markdown(
    f"""
    ### Overall Churn

    - The overall customer churn rate is **{churn_rate:.2f}%**.
    - There are **{churned_customers:,} churned customers**
      out of **{total_customers:,} customers**.

    ### Customer Tenure

    - Customers with shorter tenure show higher observed
      churn rates.
    - The **0-12 month** customer group has the highest
      churn rate among the tenure groups.

    ### Contract Type

    - Month-to-month customers have a substantially higher
      observed churn rate than customers on longer contracts.
    - Longer-contract customers show lower observed churn
      rates in this dataset.

    ### Customer Lifetime

    - Churned customers have a shorter average observed
      tenure than retained customers.
    - This suggests that the early customer lifecycle is
      an important area to investigate for retention efforts.

    ### Support Services

    - Customers with Tech Support show a different observed
      churn rate from customers without Tech Support.
    - Customers with Online Security also show a different
      observed churn rate from customers without the service.
    """
)


# ---------------------------------------------------------
# DATASET LIMITATIONS
# ---------------------------------------------------------

with st.expander("ℹ️ Dataset Limitations"):

    st.write(
        """
        The dataset contains customer subscription information,
        but it does not contain a signup date/month or a region
        field.

        Therefore, signup-month cohorts and region-based cohorts
        cannot be directly calculated from this dataset.

        Tenure groups are used as a practical alternative for
        analyzing customer lifetime patterns.

        The dataset also contains some missing TotalCharges
        values. These values are handled as missing during the
        analysis rather than being manually invented.
        """
    )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.markdown("---")

st.caption(
    "Future Interns – Data Science & Analytics Task 2 | "
    "Customer Retention & Churn Analysis"
)