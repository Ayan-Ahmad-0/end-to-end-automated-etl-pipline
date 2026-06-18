import pandas as pd
import psycopg2
from prophet import Prophet

# DB connection
conn = psycopg2.connect(
    host="postgres",
    database="airflow",
    user="airflow",
    password="airflow"
)

# Load data
query = """
SELECT
    to_timestamp(timestamp) AS event_time,
    passenger_count
FROM demand_output
ORDER BY event_time
"""
df = pd.read_sql(query, conn)

# Aggregate to 15-min windows
df = df.set_index("event_time")
df = df.resample("15min").sum().reset_index()

df = df.rename(columns={"event_time": "ds", "passenger_count": "y"})
df["ds"] = df["ds"].dt.tz_localize(None)


# Train model
model = Prophet()
model.fit(df)

# Predict next 1 hour (4 × 15min)
future = model.make_future_dataframe(periods=4, freq="15min")
forecast = model.predict(future).tail(4)

# Store predictions
cursor = conn.cursor()
for _, row in forecast.iterrows():
    cursor.execute("""
        INSERT INTO demand_forecast (forecast_time, predicted_passengers)
        VALUES (%s, %s)
    """, (row["ds"], row["yhat"]))

conn.commit()
cursor.close()
conn.close()

print("✅ Demand forecasting completed")
