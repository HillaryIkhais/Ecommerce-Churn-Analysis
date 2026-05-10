import sqlite3
import pandas as pd
from pathlib import Path

RAW = Path("datasets/customer_data.csv")
DB  = Path("datasets/olist.db")

print("Loading transactions...")
df = pd.read_csv(RAW, encoding="ISO-8859-1")
print(f"  Raw rows: {len(df):,}")

# Same cleaning you already do
df = df.dropna(subset=["CustomerID"])
df = df[df["Quantity"] > 0]
df = df[df["UnitPrice"] > 0]
df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]
df["CustomerID"] = df["CustomerID"].astype(int)
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
df["Revenue"]     = df["Quantity"] * df["UnitPrice"]

print(f"  Clean rows: {len(df):,}")

conn = sqlite3.connect(DB)
df.to_sql("transactions", conn, if_exists="replace", index=False)
conn.close()

print(f"✓ Database saved → datasets/olist.db")
print(f"  Table: transactions ({len(df):,} rows, 9 columns)")