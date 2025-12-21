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

print(f"🔍 Checking tables in {PROJECT_ID}.{DATASET_ID}...\n")

# List all tables in the dataset
try:
    tables = client.list_tables(f"{PROJECT_ID}.{DATASET_ID}")
    table_list = [table.table_id for table in tables]
    
    if table_list:
        print(f"✅ Found {len(table_list)} table(s):")
        for table_name in table_list:
            print(f"   - {table_name}")
    else:
        print("❌ No tables found in the dataset!")
        print("\n💡 The dataset exists but is empty. We need to create the tables.")
        
except Exception as e:
    print(f"❌ Error listing tables: {e}")
    print("\n💡 This might mean the dataset doesn't exist or you don't have permissions.")

print("\n" + "="*50)
print("Next step: Create the tables if they don't exist")
print("="*50)
