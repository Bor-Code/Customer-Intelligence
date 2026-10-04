import duckdb
import os

os.makedirs("data/gold", exist_ok=True)
db_path = "data/gold/features.db"

# Remove old db if exists
if os.path.exists(db_path):
    os.remove(db_path)

print("Connecting to DuckDB and processing 1.5 Million rows in memory...")
conn = duckdb.connect(db_path)

# 1. Load CSVs directly into DuckDB tables
conn.execute("""
    CREATE TABLE raw_customers AS SELECT * FROM read_csv_auto('data/raw/customers.csv')
""")

conn.execute("""
    CREATE TABLE raw_transactions AS SELECT * FROM read_csv_auto('data/raw/transactions.csv')
""")

# 2. Perform RFM (Recency, Frequency, Monetary) and Feature Engineering
print("Performing Feature Engineering (RFM, CLV, Churn Risk)...")

query = """
CREATE TABLE customers AS
WITH rfm AS (
    SELECT 
        customer_id,
        MAX(timestamp) as last_purchase_date,
        COUNT(transaction_id) as frequency,
        SUM(amount) as monetary_value,
        EXTRACT(DAY FROM (CURRENT_DATE - MAX(timestamp))) as recency_days
    FROM raw_transactions
    GROUP BY customer_id
)
SELECT 
    c.customer_id,
    c.name,
    c.company,
    r.frequency,
    r.monetary_value,
    r.recency_days,
    -- Simple CLV proxy: monetary_value * 1.2
    r.monetary_value * 1.2 AS predicted_clv,
    -- Churn Risk logic based on recency and frequency
    CASE 
        WHEN r.recency_days > 180 THEN 'High'
        WHEN r.recency_days > 90 AND r.frequency < 5 THEN 'Medium'
        ELSE 'Low'
    END AS churn_risk,
    -- Status
    CASE
        WHEN r.recency_days > 200 THEN 'Kaybedildi'
        WHEN r.recency_days > 90 THEN 'Riskli'
        ELSE 'Aktif'
    END AS status,
    -- Segmentation
    CASE
        WHEN r.frequency > 50 AND r.monetary_value > 3000 THEN 'Champions'
        WHEN r.frequency > 20 THEN 'Loyal Customers'
        WHEN r.recency_days > 180 THEN 'At Risk'
        ELSE 'Regulars'
    END AS segment_name
FROM raw_customers c
JOIN rfm r ON c.customer_id = r.customer_id
"""

conn.execute(query)

# 3. Create segments summary table
conn.execute("""
CREATE TABLE segments AS
SELECT 
    segment_name,
    COUNT(customer_id) as user_count,
    AVG(monetary_value) as avg_spend
FROM customers
GROUP BY segment_name
""")

# Validate
total = conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
print(f"Successfully processed {total} customers into the Gold Feature Store.")
conn.close()
print(f"Database saved to {db_path}")
