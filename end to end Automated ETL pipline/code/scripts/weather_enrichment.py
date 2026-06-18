import requests
import psycopg2
from datetime import datetime

# -----------------------------
# OpenWeather API Key (yours)
# -----------------------------
API_KEY = "65b2bc290a5fd07d306d941f55fc3f6f"

# Cities mapping
CITIES = {
    "Karachi": "Karachi,PK",
    "Lahore": "Lahore,PK",
    "Islamabad": "Islamabad,PK",
    "Sialkot": "Sialkot,PK"
}

def fetch_weather(city_query):
    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q={city_query}&appid={API_KEY}&units=metric"
    )
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()

    temperature = data["main"]["temp"]
    weather_main = data["weather"][0]["main"]

    return temperature, weather_main

def generate_alert(weather_main, temperature):
    if weather_main in ["Fog", "Mist"]:
        return "Fog Alert"
    elif weather_main == "Rain":
        return "Rain Alert"
    elif temperature >= 35:
        return "Heat Alert"
    else:
        return "No Alert"

# -----------------------------
# PostgreSQL connection
# -----------------------------
conn = psycopg2.connect(
    host="postgres",
    database="airflow",
    user="airflow",
    password="airflow"
)
cursor = conn.cursor()

# -----------------------------
# Update weather data
# -----------------------------
for city, query in CITIES.items():
    try:
        temperature, weather_main = fetch_weather(query)
        weather_alert = generate_alert(weather_main, temperature)


        cursor.execute("""
            UPDATE demand_output
            SET
                temperature = %s,
                weather_main = %s,
                weather_alert = %s,       
                weather_fetched_at = %s
            WHERE pickup_location = %s
        """, (
            temperature,
            weather_main,
            weather_alert,
            datetime.utcnow(),
            city
        ))

        print(f"✅ Weather updated for {city} | {temperature}°C | {weather_main}| {weather_alert}")

    except Exception as e:
        print(f"❌ Weather fetch failed for {city}: {e}")

conn.commit()
cursor.close()
conn.close()

print("🌦️ Weather enrichment completed successfully")
