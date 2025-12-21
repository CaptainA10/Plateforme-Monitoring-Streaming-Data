    B -->|Streaming| C[PySpark Streaming]
    B -->|Sink| D[MongoDB (Raw Lake)]
    C -->|Aggregations| E[Console / BigQuery]
    D -->|Batch| F[Airflow (Daily Stats)]
    D -->|Real-time| G[Streamlit Dashboard]
```

## 🛠 Prérequis

*   **Docker Desktop** (avec au moins 8GB de RAM alloués).
*   **Python 3.9+**.
*   **Git**.

## 🚀 Démarrage Rapide

### 1. Lancer l'Infrastructure
Démarrez Kafka, Zookeeper, Schema Registry, Spark, Airflow et Mongo.

```bash
docker-compose up -d
```
*Attendez quelques minutes que tous les services soient "Healthy".*

### 2. Installer les Dépendances Python
```bash
pip install -r requirements.txt
```

### 3. Lancer les Producteurs (Ingestion)
Dans un terminal :
```bash
# Générer du trafic utilisateur simulé
python src/ingestion/main.py
```
Dans un autre terminal (optionnel) :
```bash
# Écouter les changements Wikimedia en temps réel
python src/ingestion/wikimedia_producer.py
```

### 4. Lancer le Stockage (Consumer)
Pour sauvegarder les données brutes dans MongoDB :
```bash
python src/storage/mongo_consumer.py
```

### 5. Lancer le Dashboard (Visualisation)
```bash
streamlit run src/visualization/dashboard.py
```
Accédez à **http://localhost:8501**.

---

## 📦 Modules du Projet

### Module 1 : Infrastructure
*   Fichier : `docker-compose.yml`
*   Services : Kafka (Confluent 7.5), Spark (3.5), Airflow (2.8), MongoDB (6.0).

### Module 2 : Ingestion
*   Code : `src/ingestion/`
*   Features : Producteurs Kafka robustes, Sérialisation Avro, Gestion du Backpressure.

### Module 3 : Stockage
*   Code : `src/storage/`
*   Features : MongoDB Sink (Idempotent), BigQuery DDL (`config/bigquery/`).

### Module 4 : Streaming (PySpark)
*   Code : `src/streaming/`
*   Features : Structured Streaming, Watermarking (10min), Windowing (1min).
*   **Run** :
    ```bash
    docker exec -it spark-master spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.apache.spark:spark-avro_2.12:3.5.0 src/streaming/jobs/process_user_activity.py
    ```

### Module 5 : Fiabilité
*   Features : Checkpointing (`/tmp/checkpoints`), Fault Tolerance.

### Module 6 : Orchestration (Airflow)
*   Code : `dags/`, `src/batch/`
*   UI : **http://localhost:8082** (user: airflow, pass: airflow).
*   Features : DAG quotidien pour le calcul de statistiques.

### Module 7 : Visualisation
*   Code : `src/visualization/`
*   Features : Dashboard Streamlit temps réel connecté à MongoDB.

---

---

## 🖥️ Monitoring & Pilotage

Accédez aux interfaces de contrôle de la plateforme :

| Outil | URL / Accès | Utilité |
| :--- | :--- | :--- |
| **Airflow** | [http://localhost:8082](http://localhost:8082) (airflow/airflow) | Orchestration des DAGs & Batchs |
| **BigQuery** | [Console GCP](https://console.cloud.google.com/bigquery?project=effidic-stage-2026) | Data Warehouse & Requêtes SQL |
| **Streamlit** | [http://localhost:8501](http://localhost:8501) | Dashboard Temps Réel |
| **Spark UI** | [http://localhost:9090](http://localhost:9090) | Monitoring des jobs Spark |
| **Kafka UI** | [http://localhost:9021](http://localhost:9021) | Gestion des topics & Schema Registry |

---

## ✅ Vérification du Projet

Pour vérifier que tout fonctionne correctement :

1.  **Logs du Consumer** : Vérifiez que les messages sont insérés dans BigQuery.
    ```bash
    docker logs -f bigquery_consumer (ou via votre terminal)
    ```
2.  **Aperçu BigQuery** : Allez dans la console GCP > `monitoring_datalake` > `user_activity` > Onglet **Aperçu**.
3.  **Statut dbt** : Vérifiez les tables transformées dans BigQuery (`fct_daily_user_metrics`).

---

## 📚 Documentation Avancée

Pour approfondir les aspects techniques et l'industrialisation :

*   📖 **[Concepts & Notions](docs/COURS_ET_NOTIONS.md)** : Lambda vs Kappa, Avro, Schema Registry.
*   🚀 **[Rapport d'Industrialisation](docs/INDUSTRIALIZATION.md)** : Sécurité, CI/CD, FinOps.
*   📊 **[Guide QlikSense](docs/QLIKSENSE_SETUP.md)** : Connexion BI à BigQuery.
*   ☁️ **[Setup BigQuery](docs/README_BIGQUERY.md)** : Détails de configuration GCP.

---

## 🔧 Troubleshooting Rapide

*   **Docker Error `npipe://...`** : Docker Desktop n'est pas lancé.
*   **403 Forbidden (BigQuery)** : Vérifiez que la facturation est activée sur GCP.
*   **Kafka Connection Refused** : Vérifiez que les conteneurs sont UP (`docker-compose ps`).

