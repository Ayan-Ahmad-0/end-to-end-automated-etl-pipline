import pandas as pd
import psycopg2
from sklearn.linear_model import LogisticRegression

# -----------------------------
# Database connection
# -----------------------------
conn = psycopg2.connect(
    host="postgres",
    database="airflow",
    user="airflow",
    password="airflow"
)

# -----------------------------
# Load & AGGREGATE data
# -----------------------------
query = """
SELECT
    pickup_location,
    EXTRACT(HOUR FROM to_timestamp(timestamp)) AS hour,
    SUM(passenger_count) AS total_passengers
FROM demand_output
GROUP BY pickup_location, hour
"""
df = pd.read_sql(query, conn)

# -----------------------------
# Define BUSY label (top 25%)
# -----------------------------
df = df.sort_values("total_passengers", ascending=False).reset_index(drop=True)

# Mark top 30% rows as busy
top_n = max(1, int(len(df) * 0.3))  # always at least 1

df["is_busy"] = 0
df.loc[:top_n - 1, "is_busy"] = 1
print(
    df[["pickup_location", "hour", "total_passengers", "is_busy"]]
    .head(10)
)

# -----------------------------
# Prepare features
# -----------------------------
df["pickup_encoded"] = df["pickup_location"].astype("category").cat.codes

# -----------------------------
# Train model OR fallback
# -----------------------------
unique_classes = df["is_busy"].nunique()

if unique_classes < 2:
    # Fallback: rule-based prediction
    df["prediction"] = df["is_busy"]
    print("⚠️ Only one class found. Using rule-based busy detection.")
else:
    from sklearn.linear_model import LogisticRegression

    X = df[["pickup_encoded", "hour"]]
    y = df["is_busy"]

    model = LogisticRegression()
    model.fit(X, y)
    df["prediction"] = model.predict(X)

# -----------------------------
# Save predictions
# -----------------------------
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS busy_location_prediction (
    pickup_location TEXT,
    hour INT,
    total_passengers INT,
    is_busy INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# OPTIONAL: clear previous predictions to avoid duplicates
cursor.execute("TRUNCATE TABLE busy_location_prediction")

for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO busy_location_prediction
        (pickup_location, hour, total_passengers, is_busy)
        VALUES (%s, %s, %s, %s)
    """, (
        row["pickup_location"],
        int(row["hour"]),
        int(row["total_passengers"]),
        int(row["is_busy"])
    ))

conn.commit()
cursor.close()
conn.close()

print("✅ Busy location prediction (aggregation-based) completed")
