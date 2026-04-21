# Ecommerce Churn Analysis
Built a full churn prediction pipeline, from data on messy raw transactions to a dashboard that tells you exactly who's about to leave and why.

# User Funnel Dropoff & Churn Prediction

## The Problem
An ecommerce store had no visibility into where customers were dropping off 
or who was about to leave for good. This project fixes that.

## The Data
541,909 transaction rows. Cleaned down to ~401,604 after removing missing 
customer IDs, cancellations, duplicates, and bad prices.

## What I Built

**Funnel Analysis**
Tracked every customer from first purchase to active status.
30% never came back after buying once.
Of those who did, nearly half went quiet.

| Stage | Customers | Drop-off |
|---|---|---|
| Acquired | 4,372 | — |
| First Purchase | 4,372 | 0% |
| Repeat | 3,059 | 30% |
| Active | 1,536 | 49.8% |

**Churn Prediction**
Built a logistic regression model to score every customer by churn probability.
Accuracy: 99%. Caught 98% of actual churners.

**Risk Segmentation**
| Segment | Customers |
|---|---|
| High Risk | 1,365 |
| Medium Risk | 88 |
| Low Risk | 2,919 |

**Dashboard:** 
Built in Looker Studio. It contains a funnel overview, churn breakdown, risk detail table.

![23A67DDD-CCE8-4669-B2DA-0A75BE3A4203_1_201_a](https://github.com/user-attachments/assets/7f85f1a7-9c0e-45c0-bbd5-02908dd197ee)

View Interactive Dashboard Here:
[Interactive Dashboard
](https://datastudio.google.com/u/0/reporting/b5183eaa-c134-4686-9563-e2ffa45b0a05/page/p_5ym6eehf2d)

## Key Findings
- 1 in 3 customers are at high risk of permanent churn
- Biggest drop off happens between repeat and active buyers
- 1,313 customers never returned after their first purchase

## What A Business Should Do With This
- Re-engage the 1,365 high risk customers now, not later
- Fix whatever is breaking the first purchase experience
- Reward repeat buyers before they hit 90 days inactive
- Track repeat → active drop-off monthly as a retention KPI

## Tools
Python — pandas, scikit-learn, matplotlib, seaborn
Looker Studio
