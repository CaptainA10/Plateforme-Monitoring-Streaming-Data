import json
from confluent_kafka import Consumer, KafkaError
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import SerializationContext, MessageField
from pymongo import MongoClient, UpdateOne
import os

# Configuration
SCHEMA_REGISTRY_URL = "http://localhost:8085"
BROKER_URL = "localhost:9092"
MONGO_URL = "mongodb://admin:password@localhost:27017/"
DB_NAME = "monitoring_datalake"

# Topics to consume
TOPICS = ["user_activity", "wikimedia_changes"]

class MongoSinkConsumer:
    def __init__(self):
        # 1. MongoDB Connection
        self.mongo_client = MongoClient(MONGO_URL)
        self.db = self.mongo_client[DB_NAME]
        print(f"Connected to MongoDB: {DB_NAME}")

        # 2. Schema Registry
        schema_registry_conf = {'url': SCHEMA_REGISTRY_URL}
        self.schema_registry_client = SchemaRegistryClient(schema_registry_conf)
        self.avro_deserializer = AvroDeserializer(self.schema_registry_client)

        # 3. Kafka Consumer
        consumer_conf = {
            'bootstrap.servers': BROKER_URL,
            'group.id': 'mongo_sink_group',
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

        # Prepare MongoDB Document
        # Use Topic name as Collection name (prefix with 'raw_')
        collection_name = f"raw_{topic}"
        collection = self.db[collection_name]

        # Idempotency Strategy:
        # - For user_activity: use 'event_id' as _id
        # - For wikimedia: use 'id' (or meta.id) as _id
        
        doc_id = None
        if 'event_id' in value:
            doc_id = value['event_id']
        elif 'id' in value:
            doc_id = value['id']
        
        # If we have an ID, use upsert to prevent duplicates
        if doc_id:
            value['_id'] = doc_id
            try:
                collection.replace_one({'_id': doc_id}, value, upsert=True)
                # print(f"Upserted into {collection_name}: {doc_id}")
            except Exception as e:
                print(f"Mongo Error: {e}")
        else:
            # Fallback: Insert without custom ID
            collection.insert_one(value)
            # print(f"Inserted into {collection_name}")

    def run(self):
        print(f"Subscribed to {TOPICS}. Waiting for messages...")
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

                self.process_message(msg)

        except KeyboardInterrupt:
            print("Stopping consumer...")
        finally:
            self.consumer.close()
            self.mongo_client.close()

if __name__ == "__main__":
    consumer = MongoSinkConsumer()
    consumer.run()
