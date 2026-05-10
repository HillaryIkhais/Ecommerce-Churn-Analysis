import pandas as pd

cust_data = pd.read_csv("customer_data.csv")
cust_data['InvoiceDate'] = pd.to_datetime(cust_data['InvoiceDate'])

# obtain each customer's purchase history
user_funnel = cust_data.groupby('CustomerID').agg(
    first_purchase=('InvoiceDate', 'min'),
    last_purchase=('InvoiceDate', 'max'),
    total_orders=('InvoiceNo', 'nunique')
).reset_index()

# define reference date
ref_date = cust_data['InvoiceDate'].max()

# assigning funnel stage
def assign_stage(row):
    if row['total_orders'] == 1:
        return 'One-Time'
    elif (ref_date - row['last_purchase']).days <= 30:
        return 'Active'
    else:
        return 'Churned'

user_funnel['stage'] = user_funnel.apply(assign_stage, axis=1)

# average days between first and second purchase
second_purchase = cust_data.groupby('CustomerID')['InvoiceDate'].apply(
    lambda x: sorted(x.unique())[1] if len(x.unique()) > 1 else None
).reset_index()
second_purchase.columns = ['CustomerID', 'second_purchase_date']

user_funnel = user_funnel.merge(second_purchase, on='CustomerID', how='left')
user_funnel['days_to_repeat'] = (
    user_funnel['second_purchase_date'] - user_funnel['first_purchase']
).dt.days

print(f"Avg days to repeat purchase: {user_funnel['days_to_repeat'].mean():.0f} days")

# revenue per stage
cust_data['Revenue'] = cust_data['Quantity'] * cust_data['UnitPrice']
revenue_by_customer = cust_data.groupby('CustomerID')['Revenue'].sum().reset_index()

user_funnel = user_funnel.merge(revenue_by_customer, on='CustomerID', how='left')
revenue_by_stage = user_funnel.groupby('stage')['Revenue'].mean().round(2)
print(revenue_by_stage)

# cuntry breakdown of churn
country = cust_data.groupby('CustomerID')['Country'].first().reset_index()
user_funnel = user_funnel.merge(country, on='CustomerID', how='left')

churn_by_country = user_funnel.groupby('Country')['stage'].value_counts(normalize=True).mul(100).round(1)
print(churn_by_country)

# Funnel summary
print(user_funnel['stage'].value_counts())

total = len(user_funnel)

acquired = total
first_purchase = total  # everyone in dataset made at least 1 purchase
repeat_buyers = user_funnel[user_funnel['total_orders'] > 1].shape[0]
active_users = user_funnel[user_funnel['stage'] == 'Active'].shape[0]

print(f"Acquired:       {acquired}")
print(f"First Purchase: {first_purchase}")
print(f"Repeat:         {repeat_buyers}  | Drop-off: {100 - (repeat_buyers/acquired*100):.1f}%")
print(f"Active:         {active_users}  | Drop-off: {100 - (active_users/repeat_buyers*100):.1f}%")

funnel = pd.DataFrame({
    'Stage': ['Acquired', 'First Purchase', 'Repeat', 'Active'],
    'Customers': [acquired, first_purchase, repeat_buyers, active_users]
})
funnel['Dropoff_%'] = funnel['Customers'].pct_change().mul(-100).round(1).fillna(0)
funnel.to_csv("funnel_table.csv", index=False)