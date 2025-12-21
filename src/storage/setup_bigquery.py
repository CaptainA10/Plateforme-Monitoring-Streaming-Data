from google.cloud import bigquery
from google.oauth2 import service_account
import os

# Configuration
PROJECT_ID = "effidic-stage-2026"
DATASET_ID = "monitoring_datalake"
SERVICE_ACCOUNT_PATH = os.path.join(os.path.dirname(__file__), "../../config/gcp/service-account.json")

# Authenticate
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_PATH)
client = bigquery.Client(credentials=credentials, project=PROJECT_ID)

print(f"✅ Using dataset: {PROJECT_ID}.{DATASET_ID}")

# Create user_activity table
print("\n📊 Creating table: user_activity...")
user_activity_schema = [
    bigquery.SchemaField("event_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("user_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("event_type", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("timestamp", "TIMESTAMP", mode="REQUIRED"),
    bigquery.SchemaField("page_id", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("metadata", "JSON", mode="NULLABLE"),
]

table_id = f"{PROJECT_ID}.{DATASET_ID}.user_activity"
table = bigquery.Table(table_id, schema=user_activity_schema)
table.time_partitioning = bigquery.TimePartitioning(
    type_=bigquery.TimePartitioningType.DAY,
    field="timestamp"
)
table.clustering_fields = ["event_type", "user_id"]

try:
    table = client.create_table(table, exists_ok=True)
    print(f"✅ Table {table_id} created successfully!")
except Exception as e:
    print(f"❌ Error creating user_activity: {e}")
    print("\n💡 If you see a permission error, the table might already exist.")
    print("   Check in BigQuery Console: https://console.cloud.google.com/bigquery")

# Create wikimedia_changes table
print("\n📊 Creating table: wikimedia_changes...")
wikimedia_schema = [
    bigquery.SchemaField("id", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("type", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("title", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("user", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("bot", "BOOLEAN", mode="NULLABLE"),
    bigquery.SchemaField("timestamp", "TIMESTAMP", mode="NULLABLE"),
    bigquery.SchemaField("server_name", "STRING", mode="NULLABLE"),
]

table_id = f"{PROJECT_ID}.{DATASET_ID}.wikimedia_changes"
table = bigquery.Table(table_id, schema=wikimedia_schema)
table.time_partitioning = bigquery.TimePartitioning(
    type_=bigquery.TimePartitioningType.DAY,
    field="timestamp"
)

try:
    table = client.create_table(table, exists_ok=True)
    print(f"✅ Table {table_id} created successfully!")
except Exception as e:
    print(f"❌ Error creating wikimedia_changes: {e}")
    print("\n💡 If you see a permission error, the table might already exist.")
    print("   Check in BigQuery Console: https://console.cloud.google.com/bigquery")

print("\n🎉 Setup complete! Check your tables in BigQuery Console.")
