import json
from confluent_kafka import Consumer, KafkaError
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import SerializationContext, MessageField
from google.cloud import bigquery
from google.oauth2 import service_account
import os
from datetime import datetime

# Configuration
SCHEMA_REGISTRY_URL = "http://localhost:8085"
BROKER_URL = "localhost:9092"
GCP_PROJECT_ID = "effidic-stage-2026"  # Extracted from your service account filename
DATASET_ID = "monitoring_datalake"
SERVICE_ACCOUNT_PATH = "../../config/gcp/service-account.json"

# Topics to consume
TOPICS = ["user_activity"]  # wikimedia_changes topic not created yet

class BigQuerySinkConsumer:
    def __init__(self):
        # 1. BigQuery Connection
        credentials_path = os.path.join(os.path.dirname(__file__), SERVICE_ACCOUNT_PATH)
        credentials = service_account.Credentials.from_service_account_file(credentials_path)
        self.bq_client = bigquery.Client(credentials=credentials, project=GCP_PROJECT_ID)
        print(f"Connected to BigQuery: {GCP_PROJECT_ID}.{DATASET_ID}")

        # 2. Schema Registry
        schema_registry_conf = {'url': SCHEMA_REGISTRY_URL}
        self.schema_registry_client = SchemaRegistryClient(schema_registry_conf)
        self.avro_deserializer = AvroDeserializer(self.schema_registry_client)

        # 3. Kafka Consumer
        consumer_conf = {
            'bootstrap.servers': BROKER_URL,
            'group.id': 'bigquery_sink_group_v3',
            'auto.offset.reset': 'earliest'
        }
        self.consumer = Consumer(consumer_conf)
        self.consumer.subscribe(TOPICS)

    def process_message(self, msg):
        topic = msg.topic()
        
        # Deserialize Value
        try:
            value = self.avro_deserializer(msg.value(), SerializationContext(topic, MessageField.VALUE))
        except Exception as e:
            print(f"Deserialization Error: {e}")
            return

        if value is None:
            return

        # Prepare BigQuery Row
        table_id = f"{GCP_PROJECT_ID}.{DATASET_ID}.{topic}"
        
        # Convert timestamp (ms) to TIMESTAMP format for BigQuery
        if 'timestamp' in value:
            value['timestamp'] = datetime.fromtimestamp(value['timestamp'] / 1000).isoformat()
        
        # Convert metadata (dict) to JSON string for BigQuery JSON column
        if 'metadata' in value and isinstance(value['metadata'], dict):
            value['metadata'] = json.dumps(value['metadata'])
        
        # Insert into BigQuery
        try:
            errors = self.bq_client.insert_rows_json(table_id, [value])
            if errors:
                print(f"BigQuery Insert Errors: {errors}")
            else:
                print(f"✅ Successfully inserted 1 row into {table_id}")
        except Exception as e:
            print(f"BigQuery Error: {e}")

    def run(self):
        print(f"Subscribed to {TOPICS}. Sending data to BigQuery...")
        try:
            while True:
                msg = self.consumer.poll(1.0)

                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        print(f"Consumer Error: {msg.error()}")
                        continue

                print(f"📩 Received message from topic {msg.topic()} at offset {msg.offset()}")
                self.process_message(msg)

        except KeyboardInterrupt:
            print("Stopping consumer...")
        finally:
            self.consumer.close()

if __name__ == "__main__":
    consumer = BigQuerySinkConsumer()
    consumer.run()
