import pandas as pd

cust_data = pd.read_excel("/Users/ikhaisoshuare/Downloads/customer.xlsx")

# Clean the dataset
print(cust_data.shape)
print(cust_data.dtypes)
print(cust_data.head())
print(cust_data.isnull().sum())
print(cust_data.duplicated().sum())

# Drop rows with no CustomerID (can't track users without it)
cust_data = cust_data.dropna(subset=['CustomerID'])

# Drop duplicates
cust_data = cust_data.drop_duplicates()

# Fix CustomerID to int
cust_data['CustomerID'] = cust_data['CustomerID'].astype(int)

# Drop missing descriptions (optional but clean)
cust_data = cust_data.dropna(subset=['Description'])

# Remove cancellations
cust_data = cust_data[~cust_data['InvoiceNo'].astype(str).str.startswith('C')]

# Remove zero/negative prices
cust_data = cust_data[cust_data['UnitPrice'] > 0]

# Remove zero/negative quantities
cust_data = cust_data[cust_data['Quantity'] > 0]

# Confirm
print(cust_data.shape)
print(cust_data.isnull().sum())
print(cust_data.duplicated().sum())
cust_data.to_csv("customer_data.csv", index=False)