import pandas as pd

cust_data = pd.read_csv("customer_data.csv")
cust_data['InvoiceDate'] = pd.to_datetime(cust_data['InvoiceDate'])
cust_data['Revenue'] =cust_data['Quantity'] *cust_data['UnitPrice']

snapshot_date =cust_data['InvoiceDate'].max()

features =cust_data.groupby('CustomerID').agg(
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

print(features.shape)
print(features.head())