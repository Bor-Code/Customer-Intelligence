import os
import random
import uuid
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# Create data directories
os.makedirs("data/raw", exist_ok=True)
os.makedirs("data/gold", exist_ok=True)

NUM_CUSTOMERS = 35000
NUM_TRANSACTIONS = 1_500_000 # 1.5 Million rows for big data feel

print(f"Generating {NUM_CUSTOMERS} customers...")
customer_ids = [f"CUST-{random.randint(10000, 99999)}" for _ in range(NUM_CUSTOMERS)]
# Make them unique
customer_ids = list(set(customer_ids))
NUM_CUSTOMERS = len(customer_ids)

companies = ["Acme Corp", "Global Tech", "Nexus Industries", "Stark Logistics", "Wayne Enterprises", "CyberDyne", "Umbrella Corp", "Massive Dynamic"]

customers_data = []
for cid in customer_ids:
    customers_data.append({
        "customer_id": cid,
        "name": f"User_{cid[-4:]}",
        "company": random.choice(companies),
        "signup_date": (datetime.now() - timedelta(days=random.randint(100, 1000))).strftime("%Y-%m-%d")
    })

df_customers = pd.DataFrame(customers_data)
df_customers.to_csv("data/raw/customers.csv", index=False)
print("Saved data/raw/customers.csv")

print(f"Generating {NUM_TRANSACTIONS} transactions. This might take a few seconds...")
# Vectorized transaction generation for speed
cids = np.random.choice(customer_ids, size=NUM_TRANSACTIONS)
amounts = np.round(np.random.gamma(shape=2.0, scale=50.0, size=NUM_TRANSACTIONS), 2)

# Generate random dates over the last 365 days
now = datetime.now()
random_days = np.random.randint(0, 365, size=NUM_TRANSACTIONS)
dates = [now - timedelta(days=int(d)) for d in random_days]

df_transactions = pd.DataFrame({
    "transaction_id": [str(uuid.uuid4()) for _ in range(NUM_TRANSACTIONS)],
    "customer_id": cids,
    "amount": amounts,
    "timestamp": dates
})
df_transactions.to_csv("data/raw/transactions.csv", index=False)
print(f"Saved data/raw/transactions.csv ({NUM_TRANSACTIONS} rows)")
