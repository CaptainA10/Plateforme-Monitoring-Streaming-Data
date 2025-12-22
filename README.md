# 🚀 Plateforme de Monitoring Streaming & Batch
Modern Data Stack – Pipeline de Données pour l'Analyse d'Activité en Temps Réel

[![Kafka](https://img.shields.io/badge/Apache-Kafka-black?style=for-the-badge&logo=apachekafka)](https://kafka.apache.org/)
[![Spark](https://img.shields.io/badge/Apache-Spark-E25A1C?style=for-the-badge&logo=apachespark&logoColor=white)](https://spark.apache.org/)
[![BigQuery](https://img.shields.io/badge/Google-BigQuery-blue?style=for-the-badge&logo=googlecloud)](https://cloud.google.com/bigquery)
[![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![dbt](https://img.shields.io/badge/dbt-orange?style=for-the-badge&logo=dbt&logoColor=white)](https://www.getdbt.com/)
[![Airflow](https://img.shields.io/badge/Apache-Airflow-017CEE?style=for-the-badge&logo=apacheairflow&logoColor=white)](https://airflow.apache.org/)
[![Live Dashboard](https://img.shields.io/badge/QlikSense-Dashboard-009845?style=for-the-badge&logo=qlik&logoColor=white)](https://yr9pfbp2oxzezb5.fr.qlikcloud.com/sense/app/05d3b740-87d3-4ba7-9215-2f8479c83132)

---

## ⭐ Features

- **Architecture Lambda** complète (Streaming & Batch)
- Ingestion temps réel via **Kafka & Schema Registry** (Avro)
- Traitement distribué avec **PySpark Structured Streaming**
- Data Warehouse Cloud sur **Google BigQuery**
- Orchestration complète avec **Apache Airflow**
- Transformations modulaires et tests avec **dbt**
- Dashboards interactifs **Streamlit** (Opérationnel) & **QlikSense** (Analytique)
- Environnement 100% reproductible via **Docker**

---

## 🧠 Architecture Lambda & Concepts

Ce projet implémente une **Architecture Lambda**, une approche robuste pour traiter massivement les données en combinant deux flux :

### 1. Speed Layer (Temps Réel)
- **Flux** : Kafka → PySpark Streaming → MongoDB.
- **Pourquoi le "compte-goutte" (Streaming) ?** : Pour obtenir une latence minimale. On traite chaque événement dès qu'il arrive pour détecter des anomalies ou surveiller l'activité en direct sur le dashboard Streamlit. C'est idéal pour la réactivité immédiate.

### 2. Batch Layer (Historique)
- **Flux** : MongoDB → Airflow → BigQuery → dbt.
- **Rôle** : Fournir une vue exhaustive et ultra-précise de toutes les données historiques. C'est ici que dbt intervient pour transformer les données brutes en KPIs fiables pour le dashboard QlikSense.

### 3. Serving Layer
- Fournit les résultats aux utilisateurs via les dashboards (Streamlit pour le live, Qlik pour l'analytique).

---

## 🏗️ Architecture Overview

Cette plateforme traite des flux massifs d'événements (activité utilisateur et modifications Wikimedia) pour fournir des indicateurs de performance (KPIs) en temps réel et des analyses historiques.

### 🔧 Composants

| Couche | Technologie | Rôle |
|-------|------------|---------|
| **Ingestion** | Kafka, Schema Registry | Collecte des flux Avro (User Activity & Wikimedia) |
| **Streaming** | PySpark | Agrégations glissantes, Watermarking & Nettoyage |
| **Stockage** | MongoDB & BigQuery | Raw Data Lake (NoSQL) & Data Warehouse (Cloud) |
| **Orchestration** | Airflow | Scheduling des DAGs, jobs batch et dbt |
| **Transformation** | dbt Core | Modélisation SQL, KPIs & Qualité de données |
| **Visualisation** | Streamlit / Qlik | Dashboards temps réel et pilotage BI |

---

## 📊 Résultats Analytiques & KPIs

Le pipeline produit des tables prêtes pour l'analyse dans BigQuery :

### **`monitoring_datalake.fct_daily_user_metrics`**

#### Indicateurs Principaux
- **Volume d'événements** → `event_count`
- **Utilisateurs Uniques** → `unique_users`

#### Dimensions d'Analyse
- `activity_date`
- `event_type` (CLICK, VIEW, PURCHASE, etc.)

---

## 📈 Dashboard Preview

Accédez aux interfaces de contrôle de la plateforme :

| Outil | URL / Accès | Utilité |
| :--- | :--- | :--- |
| **QlikSense** | [Live Dashboard](https://yr9pfbp2oxzezb5.fr.qlikcloud.com/sense/app/05d3b740-87d3-4ba7-9215-2f8479c83132) | Dashboard Analytique (BigQuery) |
| **Streamlit** | [http://localhost:8501](http://localhost:8501) | Dashboard Temps Réel (MongoDB) |
| **Airflow** | [http://localhost:8082](http://localhost:8082) | Orchestration & Monitoring des Pipelines |
| **Kafka UI** | [http://localhost:9021](http://localhost:9021) | Gestion des Topics & Schémas Avro |
| **Spark UI** | [http://localhost:9090](http://localhost:9090) | Monitoring des jobs de Streaming |

---

## 🔐 Data Quality (DataOps via dbt)

La fiabilité des données est assurée par des tests automatisés dbt :
- `not_null` sur les clés primaires et dimensions critiques.
- Tests de validité des KPIs.

**Status:** ✔️ *PASS — Tous les tests de qualité validés*

---

## 🛠️ Tech Stack

### Langages & Frameworks
- **Python 3.9+** (Ingestion, Spark, Streamlit)
- **SQL** (BigQuery Standard SQL, dbt)
- **Avro** (Sérialisation des données)

### Infrastructure
- **Docker & Docker Compose**
- **Google Cloud Platform** (BigQuery)
- **Confluent Kafka Stack**

---

## 🧩 Installation & Démarrage

```bash
# 1. Lancer l'infrastructure (Kafka, Spark, Airflow, Mongo)
docker-compose up -d

# 2. Installer les dépendances Python
pip install -r requirements.txt

# 3. Lancer les producteurs de données
python src/ingestion/main.py           # Activité utilisateur
python src/ingestion/wikimedia_producer.py # Flux Wikimedia
```

### Configuration dbt
Créez ou éditez votre fichier `~/.dbt/profiles.yml` :
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

## 📚 Documentation Avancée

*   🔍 **[Guide de Connexion BigQuery](docs/BIGQUERY_CONNECTION_GUIDE.md)** : Paramètres Simba/ODBC pour BI.
*   📂 **[Sources des Données](docs/DATA_SOURCES.md)** : Origine et signification des données.
*   🚀 **[Rapport d'Industrialisation](docs/INDUSTRIALIZATION.md)** : Sécurité, CI/CD, FinOps.

---

## 👨‍💻 Author

**NGUETTE FANE Gad**
Data Engineer – Plateforme de Monitoring Streaming

📧 Contact : [nguettefanegad@gmail.com]