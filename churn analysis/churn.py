import pandas as pd

cust_data = pd.read_csv("features.csv")

high = cust_data['churn_probability'].quantile(0.75)
medium = cust_data['churn_probability'].quantile(0.40)

def assign_risk(prob):
    if prob >= high:
        return 'High Risk'
    elif prob >= medium:
        return 'Medium Risk'
    else:
        return 'Low Risk'

cust_data['churn_risk'] = cust_data['churn_probability'].apply(assign_risk)

print(cust_data['churn_risk'].value_counts())
cust_data.to_csv("features.csv", index=False)