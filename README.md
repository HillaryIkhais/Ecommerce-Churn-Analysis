# Ecommerce Churn Analysis
How I Identified Revenue Leakage & Customer Churn in an E-commerce Business

# User Funnel Dropoff & Churn Prediction

## The Business Problem
The business was acquiring customers but failing to retain them.
This leads to silent revenue loss, customers buy once and never return, reducing lifetime value and slowing down revenue growth.

## The Data
- 541,909 transaction rows cleaned down to ~401,604 
- Removed missing customer IDs, cancellations, duplicates, and bad prices.

## What I Built

**Funnel Analysis**
- Analyzed customer purchase behavior across lifecycle stages
- Built a churn classification model to identify at-risk users
- Segmented customers based on churn probability

| Stage | Customers | Drop-off |
|---|---|---|
| Acquired | 4,372 | — |
| First Purchase | 4,372 | 0% |
| Repeat | 3,059 | 30% loss |
| Active | 1,536 | 49.8% loss|

The biggest revenue drop happens after the second purchase, not the first.

**Churn Model**
Model Type: Logistic regression
Purpose: Identify customers likely to stop purchasing
Note:
The dataset is imbalanced, so accuracy is not the primary metric.
The model is used to prioritize high-risk customers for intervention, not for perfect prediction.

**Risk Segmentation**
| Segment | Customers |
|---|---|
| High Risk | 1,365 |
| Medium Risk | 88 |
| Low Risk | 2,919 |

**Dashboard:** 
Built in Looker Studio: Funnel overview, churn breakdown, and customer risk segmentation.

![23A67DDD-CCE8-4669-B2DA-0A75BE3A4203_1_201_a](https://github.com/user-attachments/assets/7f85f1a7-9c0e-45c0-bbd5-02908dd197ee)

View Interactive Dashboard Here:
[Interactive Dashboard
](https://datastudio.google.com/u/0/reporting/b5183eaa-c134-4686-9563-e2ffa45b0a05/page/p_5ym6eehf2d)

## Key Insights
- 30% of customers never return after their first purchase
- Nearly 50% of repeat buyers disengage, indicating weak retention strategy
- 1 in 3 customers is at high risk of churn
- A large portion of revenue likely depends on a small active segment
- Most churn happens after the second purchase; meaning retention efforts should focus on converting first time buyers into repeat customers.
  
## What This Means for the Business
- The business is not struggling with acquisition — it’s failing at retention after initial engagement
- Losing repeat customers suggests:
    - weak post-purchase experience
    - poor follow-up/remarketing
    - low perceived product value after first use

## Recommended Actions
- Target high risk users (1,365 customers) with immediate retention campaigns
- Introduce post-purchase engagement flows (email/SMS within first 7–14 days)
- Offer incentives for second purchase conversion (critical drop-off point)
- Monitor churn risk continuously using model outputs

## Potential Impact On The Business
Even a 10–15% reduction in churn could significantly increase customer lifetime value and overall revenue.  

## Tools
Python(Pandas, Scikit-learn, Matplotlib, Seaborn)
Looker Studio
