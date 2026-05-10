import pandas as pd
import sqlite3

# ── Load from database ──
conn = sqlite3.connect("datasets/olist.db")
cust_data = pd.read_sql("SELECT * FROM transactions", conn)
conn.close()

# ── Feature engineering ──
cust_data['InvoiceDate'] = pd.to_datetime(cust_data['InvoiceDate'])
cust_data['Revenue'] = cust_data['Quantity'] * cust_data['UnitPrice']
snapshot_date = cust_data['InvoiceDate'].max()

features = cust_data.groupby('CustomerID').agg(
    total_orders=('InvoiceNo', 'nunique'),
    total_items=('Quantity', 'sum'),
    total_revenue=('Revenue', 'sum'),
    avg_order_value=('Revenue', 'mean'),
    unique_products=('StockCode', 'nunique'),
    first_purchase=('InvoiceDate', 'min'),
    last_purchase=('InvoiceDate', 'max')
).reset_index()

features['days_since_last_purchase'] = (snapshot_date - features['last_purchase']).dt.days
features['customer_lifespan'] = (features['last_purchase'] - features['first_purchase']).dt.days
features['purchase_frequency'] = features['total_orders'] / (features['customer_lifespan'] + 1)

# ── Cohort Feature (SQL) ──
conn = sqlite3.connect("datasets/olist.db")
cohort_query = """
WITH customer_first_month AS (
    SELECT
        CustomerID,
        strftime('%Y-%m', MIN(InvoiceDate)) AS cohort_month
    FROM transactions
    GROUP BY CustomerID
),
monthly_activity AS (
    SELECT
        t.CustomerID,
        strftime('%Y-%m', t.InvoiceDate)    AS active_month,
        c.cohort_month
    FROM transactions t
    JOIN customer_first_month c ON t.CustomerID = c.CustomerID
)
SELECT
    CustomerID,
    COUNT(DISTINCT active_month)            AS total_active_months,
    CASE
        WHEN COUNT(DISTINCT active_month) > 1 THEN 1
        ELSE 0
    END                                     AS returned_second_month
FROM monthly_activity
GROUP BY CustomerID
"""
cohort_df = pd.read_sql(cohort_query, conn)
conn.close()

# ── Merge cohort into features ──
features = features.merge(cohort_df, on="CustomerID", how="left")
features['returned_second_month'] = features['returned_second_month'].fillna(0).astype(int)
features['total_active_months'] = features['total_active_months'].fillna(1).astype(int)

print(features.shape)
print(f"\nSecond-month return rate: {features['returned_second_month'].mean()*100:.1f}%")
print(features[['CustomerID', 'total_active_months', 'returned_second_month']].head())

# ── Churn label ──
features['churned'] = (features['days_since_last_purchase'] >= 90).astype(int)

# ── Save ──
features.to_csv("datasets/features.csv", index=False)

print(f"\nChurned:     {features['churned'].sum():,} ({features['churned'].mean()*100:.1f}%)")
print(f"Not churned: {(features['churned']==0).sum():,}")
print("\n✓ Saved to datasets/features.csv")