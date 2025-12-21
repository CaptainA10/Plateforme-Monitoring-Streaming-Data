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

table_id = f"{PROJECT_ID}.{DATASET_ID}.user_activity"
table = client.get_table(table_id)

print(f"Table: {table_id}")
print("Schema:")
for field in table.schema:
    print(f" - {field.name}: {field.field_type} ({field.mode})")
