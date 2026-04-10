import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

cust_data = pd.read_csv("features.csv")

# Features and target
X = cust_data[['total_orders', 'total_items', 'total_revenue', 'avg_order_value',
        'unique_products', 'days_since_last_purchase', 'customer_lifespan',
        'purchase_frequency']]
y = cust_data['churned']

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train
model = LogisticRegression()
model.fit(X_train, y_train)

# Predict probabilities
cust_data['churn_probability'] = model.predict_proba(scaler.transform(
    cust_data[['total_orders', 'total_items', 'total_revenue', 'avg_order_value',
        'unique_products', 'days_since_last_purchase', 'customer_lifespan',
        'purchase_frequency']]
))[:, 1]

print(cust_data[['CustomerID', 'churn_probability']].head(10))
cust_data.to_csv("features.csv", index=False)

# Evaluate
y_pred = model.predict(X_test)

print(f"Accuracy:  {accuracy_score(y_test, y_pred):.2f}")
print(f"Precision: {precision_score(y_test, y_pred):.2f}")
print(f"Recall:    {recall_score(y_test, y_pred):.2f}")

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='YlOrBr',
            xticklabels=['Not Churned', 'Churned'],
            yticklabels=['Not Churned', 'Churned'])
plt.title('Confusion Matrix')
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.tight_layout()
plt.savefig('confusion_matrix.png', dpi=150)
plt.show()