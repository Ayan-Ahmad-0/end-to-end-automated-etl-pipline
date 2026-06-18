# kafka_producer.py
from kafka import KafkaProducer
import json
import time
import random
from datetime import datetime

KAFKA_BROKER = "kafka:9092"
KAFKA_TOPIC = "taxi_data_new"

def generate_message():
    
    return {
        "taxi_id": random.randint(1000, 9999),
        "timestamp": time.time(),                     # epoch (raw)
        "pickup_location": random.choice(["Karachi", "Lahore", "Islamabad", "Sialkot"]),
        "dropoff_location": random.choice(["Karachi", "Lahore", "Islamabad", "Sialkot"]),
        "passenger_count": random.randint(1, 4)
    }

def main():
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )

    for i in range(10):
        msg = generate_message()
        producer.send(KAFKA_TOPIC, msg)
        print(f"📤 Sent: {msg}")
        time.sleep(1)

    producer.flush()
    producer.close()
    print("✅ Producer finished")

if __name__ == "__main__":
    main()
