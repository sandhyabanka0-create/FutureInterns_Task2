# Future Interns Task 2 – Customer Retention & Churn Analysis

## Project Overview

This project analyzes customer churn and retention patterns for a subscription-based business.

The analysis focuses on:

- Overall customer churn
- Churn by contract type
- Churn by customer tenure
- Churn by internet service
- Churn by payment method
- Churn by Tech Support
- Churn by Online Security
- Customer lifetime patterns

An interactive Streamlit dashboard was also created to present the findings.

## Tools Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Streamlit
- VS Code

## Dataset

The dataset contains 7,043 customer records and 21 columns.

Important customer information includes:

- Customer ID
- Tenure
- Contract type
- Internet service
- Payment method
- Monthly charges
- Total charges
- Tech Support
- Online Security
- Churn status

## Key Results

### Overall Churn

The observed overall churn rate is **26.54%**.

### Churn by Contract

- Month-to-month: **42.71%**
- One year: **11.27%**
- Two year: **2.83%**

### Churn by Tenure

- 0–12 months: **47.44%**
- 13–24 months: **28.71%**
- 25–48 months: **20.39%**
- 49–60 months: **14.42%**
- 61+ months: **6.61%**

### Other Observations

- Fiber optic customers showed an observed churn rate of **41.89%**.
- Electronic check customers showed an observed churn rate of **45.29%**.
- Customers without Tech Support showed an observed churn rate of **41.64%**, compared with **15.17%** among customers with Tech Support.
- Customers without Online Security showed an observed churn rate of **41.77%**, compared with **14.61%** among customers with Online Security.

These are observed associations in the dataset and should not be interpreted as proof that these factors cause churn.

## Customer Lifetime

Average observed tenure:

- Retained customers: **37.57 months**
- Churned customers: **17.98 months**

Average total charges:

- Retained customers: **2555.34**
- Churned customers: **1531.80**

The results show that churned customers had a shorter observed customer lifetime in this dataset.

## Business Recommendations

Based on the observed patterns, a subscription business could consider:

1. Strengthening onboarding during the first 12 months.
2. Monitoring month-to-month customers for early churn signals.
3. Investigating the experience of fiber optic customers.
4. Reviewing payment-method-related customer journeys, particularly electronic check users.
5. Promoting or improving access to Tech Support and Online Security services.
6. Monitoring customer lifetime and engagement indicators regularly.

These recommendations are based on associations in the dataset and should not be interpreted as proof that a specific factor causes churn.

## Dashboard

The project includes an interactive Streamlit dashboard.

To run the dashboard:

```text
streamlit run dashboard.py