import matplotlib.pyplot as plt
import pandas as pd

user_funnel = pd.read_csv("funnel_table.csv")
from funnel import acquired, first_purchase, repeat_buyers, active_users

stages = ['Acquired', 'First Purchase', 'Repeat', 'Active']
customers = [acquired, first_purchase, repeat_buyers, active_users]

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.barh(stages, customers, color=['#fed98e', '#fec44f', '#fe9929', '#cc4c02'])

# Add numbers on bars
for bar, val in zip(bars, customers):
    ax.text(bar.get_width() - 50, bar.get_y() + bar.get_height()/2,
            f'{val:,}', va='center', ha='right', color='white', fontweight='bold')

ax.set_xlabel('Customers')
ax.set_title('User Funnel Drop-off')
ax.invert_yaxis()
plt.tight_layout()
plt.savefig('funnel_chart.png', dpi=150)
plt.show()

dropoff = [0, 0, 30.0, 49.8]
stages = ['Acquired', 'First Purchase', 'Repeat', 'Active']

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(stages, dropoff, color=['#fed98e', '#fec44f', '#fe9929', '#cc4c02'])

for bar, val in zip(bars, dropoff):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            f'{val}%', ha='center', fontweight='bold')

ax.set_ylabel('Drop-off %')
ax.set_title('Drop-off % at Each Funnel Stage')
plt.tight_layout()
plt.savefig('dropoff_chart.png', dpi=150)
plt.show()