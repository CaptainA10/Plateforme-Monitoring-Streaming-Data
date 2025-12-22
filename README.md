# 🚀 Streaming & Batch Monitoring Platform
Modern Data Stack – Data Pipeline for Real-Time Activity Analysis

[![Kafka](https://img.shields.io/badge/Apache-Kafka-black?style=for-the-badge&logo=apachekafka)](https://kafka.apache.org/)
[![Spark](https://img.shields.io/badge/Apache-Spark-E25A1C?style=for-the-badge&logo=apachespark&logoColor=white)](https://spark.apache.org/)
[![BigQuery](https://img.shields.io/badge/Google-BigQuery-blue?style=for-the-badge&logo=googlecloud)](https://cloud.google.com/bigquery)
[![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![dbt](https://img.shields.io/badge/dbt-orange?style=for-the-badge&logo=dbt&logoColor=white)](https://www.getdbt.com/)
[![Airflow](https://img.shields.io/badge/Apache-Airflow-017CEE?style=for-the-badge&logo=apacheairflow&logoColor=white)](https://airflow.apache.org/)
[![Live Dashboard](https://img.shields.io/badge/QlikSense-Dashboard-009845?style=for-the-badge&logo=qlik&logoColor=white)](https://yr9pfbp2oxzezb5.fr.qlikcloud.com/sense/app/05d3b740-87d3-4ba7-9215-2f8479c83132)

---

## ⭐ Features

- Complete **Lambda Architecture** (Streaming & Batch)
- Real-time ingestion via **Kafka & Schema Registry** (Avro)
- Distributed processing with **PySpark Structured Streaming**
- Cloud Data Warehouse on **Google BigQuery**
- Full orchestration with **Apache Airflow**
- Modular transformations and testing with **dbt**
- Interactive dashboards: **Streamlit** (Operational) & **QlikSense** (Analytical)
- 100% reproducible environment via **Docker**

---

## 🧠 Lambda Architecture & Concepts

This project implements a **Lambda Architecture**, a robust approach for massive data processing by combining two flows:

### 1. Speed Layer (Real-Time)
- **Flow**: Kafka → PySpark Streaming → MongoDB.
- **Why "drip-feed" (Streaming)?**: To achieve minimal latency. Each event is processed as soon as it arrives to detect anomalies or monitor activity live on the Streamlit dashboard. This is ideal for immediate responsiveness.

### 2. Batch Layer (Historical)
- **Flow**: MongoDB → Airflow → BigQuery → dbt.
- **Role**: Provide a comprehensive and highly accurate view of all historical data. This is where dbt transforms raw data into reliable KPIs for the QlikSense dashboard.

### 3. Serving Layer
- Delivers results to users via dashboards (Streamlit for live, Qlik for analytics).

---

## 🏗️ Architecture Overview

This platform processes massive event streams (user activity and Wikimedia changes) to provide real-time Key Performance Indicators (KPIs) and historical analysis.

### 🔧 Components

| Layer | Technology | Role |
|-------|------------|---------|
| **Ingestion** | Kafka, Schema Registry | Collecting Avro streams (User Activity & Wikimedia) |
| **Streaming** | PySpark | Sliding aggregations, Watermarking & Cleaning |
| **Storage** | MongoDB & BigQuery | Raw Data Lake (NoSQL) & Data Warehouse (Cloud) |
| **Orchestration** | Airflow | DAG scheduling, batch jobs and dbt |
| **Transformation** | dbt Core | SQL modeling, KPIs & Data Quality |
| **Visualization** | Streamlit / Qlik | Real-time dashboards and BI monitoring |

---

## 📊 Analytical Results & KPIs

The pipeline produces analysis-ready tables in BigQuery:

### **`monitoring_datalake.fct_daily_user_metrics`**

#### Key Indicators
- **Event Volume** → `event_count`
- **Unique Users** → `unique_users`

#### Analysis Dimensions
- `activity_date`
- `event_type` (CLICK, VIEW, PURCHASE, etc.)

---

## 📈 Dashboard Preview

Access the platform's control interfaces:

| Tool | URL / Access | Purpose |
| :--- | :--- | :--- |
| **QlikSense** | [Live Dashboard](https://yr9pfbp2oxzezb5.fr.qlikcloud.com/sense/app/05d3b740-87d3-4ba7-9215-2f8479c83132) | Analytical Dashboard (BigQuery) |
| **Streamlit** | [http://localhost:8501](http://localhost:8501) | Real-Time Dashboard (MongoDB) |
| **Airflow** | [http://localhost:8082](http://localhost:8082) | Pipeline Orchestration & Monitoring |
| **Kafka UI** | [http://localhost:9021](http://localhost:9021) | Topics & Avro Schemas Management |
| **Spark UI** | [http://localhost:9090](http://localhost:9090) | Streaming Jobs Monitoring |

---

## 🔐 Data Quality (DataOps via dbt)

Data reliability is ensured through automated dbt tests:
- `not_null` on primary keys and critical dimensions.
- KPI validity tests.

**Status:** ✔️ *PASS — All quality tests validated*

---

## 🛠️ Tech Stack

### Languages & Frameworks
- **Python 3.9+** (Ingestion, Spark, Streamlit)
- **SQL** (BigQuery Standard SQL, dbt)
- **Avro** (Data serialization)

### Infrastructure
- **Docker & Docker Compose**
- **Google Cloud Platform** (BigQuery)
- **Confluent Kafka Stack**

---

## 🧩 Installation & Setup

```bash
# 1. Launch infrastructure (Kafka, Spark, Airflow, Mongo)
docker-compose up -d

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Start data producers
python src/ingestion/main.py           # User activity
python src/ingestion/wikimedia_producer.py # Wikimedia stream
```

### dbt Configuration
Create or edit your `~/.dbt/profiles.yml` file:
```yaml
monitoring_platform:
  target: dev
  outputs:
    dev:
      type: bigquery
      method: service-account
      keyfile: "config/gcp/service-account.json"
      project: "effidic-stage-2026"
      dataset: "monitoring_datalake"
      threads: 4
```

---

## 📚 Advanced Documentation

*   🔍 **[BigQuery Connection Guide](docs/BIGQUERY_CONNECTION_GUIDE.md)**: Simba/ODBC parameters for BI.
*   📂 **[Data Sources](docs/DATA_SOURCES.md)**: Origin and meaning of data.
*   🚀 **[Industrialization Report](docs/INDUSTRIALIZATION.md)**: Security, CI/CD, FinOps.

---

## 👨‍💻 Author

**NGUETTE FANE Gad**
Data Engineer – Streaming Monitoring Platform

📧 Contact: [nguettefanegad@gmail.com]
