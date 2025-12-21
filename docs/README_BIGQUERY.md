# BigQuery Storage Module

This module contains consumers that sink Kafka data to BigQuery.

## Prerequisites

1. **GCP Service Account**: Place your service account JSON in `config/gcp/service-account.json`
2. **BigQuery Dataset**: Create the dataset using the script below
3. **Python Dependencies**: `pip install google-cloud-bigquery`

## Setup BigQuery Dataset

Run this Python script to create the dataset and tables:

```python
from google.cloud import bigquery
from google.oauth2 import service_account

# Configuration
PROJECT_ID = "effidic-stage-2026"
DATASET_ID = "monitoring_datalake"
SERVICE_ACCOUNT_PATH = "../../config/gcp/service-account.json"

# Authenticate
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_PATH)
client = bigquery.Client(credentials=credentials, project=PROJECT_ID)

# Create Dataset
dataset_id = f"{PROJECT_ID}.{DATASET_ID}"
dataset = bigquery.Dataset(dataset_id)
dataset.location = "EU"  # or "US"
dataset = client.create_dataset(dataset, exists_ok=True)
print(f"Dataset {dataset_id} created.")

# Create user_activity table
user_activity_schema = [
    bigquery.SchemaField("event_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("user_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("event_type", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("timestamp", "TIMESTAMP", mode="REQUIRED"),
    bigquery.SchemaField("page_id", "STRING"),
    bigquery.SchemaField("metadata", "JSON"),
]

table_id = f"{PROJECT_ID}.{DATASET_ID}.user_activity"
table = bigquery.Table(table_id, schema=user_activity_schema)
table.time_partitioning = bigquery.TimePartitioning(
    type_=bigquery.TimePartitioningType.DAY,
    field="timestamp"
)
table.clustering_fields = ["event_type", "user_id"]
table = client.create_table(table, exists_ok=True)
print(f"Table {table_id} created.")

# Create wikimedia_changes table
wikimedia_schema = [
    bigquery.SchemaField("id", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("type", "STRING"),
    bigquery.SchemaField("title", "STRING"),
    bigquery.SchemaField("user", "STRING"),
    bigquery.SchemaField("bot", "BOOLEAN"),
    bigquery.SchemaField("timestamp", "TIMESTAMP"),
    bigquery.SchemaField("server_name", "STRING"),
]

table_id = f"{PROJECT_ID}.{DATASET_ID}.wikimedia_changes"
table = bigquery.Table(table_id, schema=wikimedia_schema)
table.time_partitioning = bigquery.TimePartitioning(
    type_=bigquery.TimePartitioningType.DAY,
    field="timestamp"
)
table = client.create_table(table, exists_ok=True)
print(f"Table {table_id} created.")
```

## Running the BigQuery Consumer

```powershell
python src/storage/bigquery_consumer.py
```

This will:
1. Subscribe to `user_activity` and `wikimedia_changes` topics
2. Deserialize Avro messages
3. Insert rows into BigQuery tables

## Verification

Check your data in BigQuery:
```sql
SELECT COUNT(*) FROM `effidic-stage-2026.monitoring_datalake.user_activity`;
SELECT * FROM `effidic-stage-2026.monitoring_datalake.user_activity` LIMIT 10;
```

## Notes

- The consumer uses streaming inserts (not batch), suitable for real-time ingestion
- Timestamps are converted from milliseconds to ISO format
- Errors are logged to console
