import sys
import json
from kafka import KafkaConsumer
from datetime import datetime
import psycopg2

# Make sure print flushes immediately
sys.stdout.reconfigure(line_buffering=True)

# Kafka setup
consumer = KafkaConsumer(
    'taxi_data_new',
    bootstrap_servers='kafka:9092',
    group_id='taxi_test_group_2',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Postgres setup
try:
    conn = psycopg2.connect(
        host='postgres',
        database='airflow',
        user='airflow',
        password='airflow'
    )
    cursor = conn.cursor()
    print("Connected to PostgreSQL")
except Exception as e:
    print("PostgreSQL connection error:", e)
    sys.exit(1)

print("📡 Kafka consumer started. Polling for messages on 'taxi_data_new'...")

# Poll messages with timeout, collect all fetched messages
messages = consumer.poll(timeout_ms=5000)  # wait max 5 seconds

if not messages:
    print("No messages found, exiting...")
    sys.exit(0)

count = 0
for tp, msgs in messages.items():
    for message in msgs:
        data = message.value
        print(f"📩 Received message: {data}")

        # Validate data has required fields
        required_keys = ['taxi_id', 'timestamp', 'pickup_location', 'dropoff_location', 'passenger_count']
        if not all(k in data for k in required_keys):
            print(f"Skipping incomplete message: {data}")
            continue

        try:
            insert_data = (
                int(data['taxi_id']),
                float(data['timestamp']),
                data['pickup_location'],
                data['dropoff_location'],
                int(data['passenger_count'])
            )

            cursor.execute("""
                INSERT INTO demand_output (taxi_id, timestamp, pickup_location, dropoff_location, passenger_count)
                VALUES (%s, %s, %s, %s, %s)
            """, insert_data)
            conn.commit()
            print("Insert successful")
            count += 1

        except Exception as e:
            print("Insert failed:", e)
            conn.rollback()

print(f"Processed {count} messages. Exiting.")
consumer.close()
conn.close()
