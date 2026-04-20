# Real-Time Taxi Demand Forecasting Pipeline

An end-to-end data engineering project — real-time ingestion, weather enrichment, ML forecasting, and live Power BI dashboard.

![Airflow](https://img.shields.io/badge/Apache_Airflow-017CEE?style=flat&logo=apacheairflow&logoColor=white)
![Kafka](https://img.shields.io/badge/Apache_Kafka-231F20?style=flat&logo=apachekafka&logoColor=white)
![Spark](https://img.shields.io/badge/Apache_Spark-E25A1C?style=flat&logo=apachespark&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white)
![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=flat&logo=powerbi&logoColor=black)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)

## Overview
This project simulates a production-grade transportation demand analytics platform. It continuously ingests real-time trip data, enriches it with live weather via OpenWeatherMap API, runs machine learning models to classify busy zones and forecast future demand, and visualizes everything in a 5-page interactive Power BI dashboard — all orchestrated automatically with Apache Airflow running inside Docker.

## Pipeline Architecture

Every stage is orchestrated by Apache Airflow as a DAG (`Taxi_data_pipeline`) that runs on a scheduled interval, retries on failure, and logs every run.

## Dashboard Pages
| Page | Description |
|---|---|
| Page 1 — Trip Overview | Live gauges, Azure Maps, area charts showing real-time trip and passenger activity |
| Page 2 — Busy Zones | Logistic Regression classifies top 30% pickup zones as busy. Slicers by location and hour |
| Page 3 — Demand Forecast | Prophet forecasts next-hour demand in 15-min intervals. High/Medium/Low demand split |
| Page 4 — Weather Impact | Live weather conditions, alerts, and temperature effect on passenger demand per city |
| Page 5 — Financials | Profit KPIs and summary metrics across all cities |

## Project Structure
├── dags/
│   └── newproject.py          # Airflow DAG definition
├── scripts/
│   ├── data_generator.py      # Real-time trip data simulator
│   ├── weather_enrichment.py  # OpenWeatherMap API integration
│   ├── busy_location.py       # Logistic Regression classifier
│   └── ml_demand_forecast.py  # Prophet forecasting model
├── docker-compose.yml         # Airflow + PostgreSQL services
├── requirements.txt
└── README.md
## Quick Start
```bash
git clone https://github.com/Ayan-Ahmad-0/end-to-end-automated-etl-pipline.git
cd end-to-end-automated-etl-pipline
docker-compose up -d
```
Airflow UI will be available at `http://localhost:8085`. Enable the `Taxi_data_pipeline` DAG to start the pipeline.

## Tech Stack
| Layer | Technology |
|---|---|
| Orchestration | Apache Airflow 2.x (Dockerized) |
| Data Processing | Apache Spark, Databricks, Apache Kafka |
| Storage | PostgreSQL (data warehouse) |
| ML & Forecasting | Facebook Prophet, Scikit-learn (Logistic Regression) |
| Weather Enrichment | OpenWeatherMap API |
| Visualization | Microsoft Power BI (live connection) |
| Infrastructure | Docker, Docker Compose |
| Language | Python 3.9+ |

## Cities Covered
Karachi · Lahore · Islamabad · Sialkot

## Author
Ayan Ahmad · ayanahmedc360@gmail.com
