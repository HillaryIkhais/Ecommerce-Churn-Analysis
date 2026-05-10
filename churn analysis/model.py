import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

cust_data = pd.read_csv("datasets/features.csv")

FEATURES = ['total_orders', 'total_items', 'total_revenue', 'avg_order_value',
            'unique_products', 'customer_lifespan', 'purchase_frequency', 
            'total_active_months', 'returned_second_month']

X = cust_data[FEATURES]
y = cust_data['churned']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test  = scaler.transform(X_test)

model = LogisticRegression()
model.fit(X_train, y_train)

# ── Predict probabilities (now uses all 10 features) ──
cust_data['churn_probability'] = model.predict_proba(
    scaler.transform(cust_data[FEATURES])
)[:, 1]

# ── Evaluate ──
y_pred = model.predict(X_test)
print(f"Accuracy:  {accuracy_score(y_test, y_pred):.2f}")
print(f"Precision: {precision_score(y_test, y_pred):.2f}")
print(f"Recall:    {recall_score(y_test, y_pred):.2f}")

# ── Feature importance ──
importance = pd.DataFrame({
    'feature':     FEATURES,
    'coefficient': model.coef_[0],
    'abs_impact':  np.abs(model.coef_[0])
}).sort_values('abs_impact', ascending=False)

print("\nTop churn predictors:")
print(importance[['feature', 'coefficient']].to_string(index=False))

# ── Save ──
cust_data.to_csv("datasets/features.csv", index=False)
print(f"\n✓ Saved → datasets/features.csv")

# ── Confusion matrix ──
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='YlOrBr',
            xticklabels=['Not Churned', 'Churned'],
            yticklabels=['Not Churned', 'Churned'])
plt.title('Confusion Matrix')
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.tight_layout()
plt.savefig('visualizations/confusion_matrix.png', dpi=150)
plt.show()