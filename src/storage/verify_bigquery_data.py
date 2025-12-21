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

print("🔍 Checking data in BigQuery...\n")

# Query user_activity table
query = f"""
SELECT COUNT(*) as total_rows
FROM `{PROJECT_ID}.{DATASET_ID}.user_activity`
"""

try:
    result = client.query(query).result()
    for row in result:
        print(f"✅ Total rows in user_activity: {row.total_rows}")
        
    if row.total_rows > 0:
        print("\n📊 Sample data (first 5 rows):")
        sample_query = f"""
        SELECT *
        FROM `{PROJECT_ID}.{DATASET_ID}.user_activity`
        LIMIT 5
        """
        sample_result = client.query(sample_query).result()
        for row in sample_result:
            print(f"  - {row.event_id}: {row.user_id} | {row.event_type} | {row.timestamp}")
    else:
        print("\n❌ No data found in user_activity table.")
        print("\n💡 Possible reasons:")
        print("   1. The producer hasn't been run yet")
        print("   2. The consumer is running but no data has been sent")
        print("   3. There was an error during insertion")
        
except Exception as e:
    print(f"❌ Error querying BigQuery: {e}")
