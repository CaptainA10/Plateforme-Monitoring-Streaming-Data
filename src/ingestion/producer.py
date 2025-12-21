import time
import random
import uuid
from confluent_kafka import Producer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from faker import Faker

import os

# Configuration
SCHEMA_REGISTRY_URL = "http://localhost:8085"
BROKER_URL = "localhost:9092"
TOPIC_NAME = "user_activity"
# Resolve path relative to this script
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "../../config/schemas/user_activity.avsc")

class UserActivityProducer:
    def __init__(self):
        self.faker = Faker()
        
        # 1. Setup Schema Registry Client
        self.schema_registry_conf = {'url': SCHEMA_REGISTRY_URL}
        self.schema_registry_client = SchemaRegistryClient(self.schema_registry_conf)
        
        # 2. Load Avro Schema
        with open(SCHEMA_PATH, 'r') as f:
            schema_str = f.read()
            
        # 3. Setup Serializer
        self.avro_serializer = AvroSerializer(
            self.schema_registry_client,
            schema_str,
            lambda obj, ctx: obj # ToDict function (identity here as we generate dicts)
        )
        self.string_serializer = StringSerializer('utf_8')
        
        # 4. Setup Producer
        producer_conf = {'bootstrap.servers': BROKER_URL}
        self.producer = Producer(producer_conf)

    def generate_event(self):
        """Generates a mock user activity event matching the Avro schema."""
        return {
            "event_id": str(uuid.uuid4()),
            "user_id": f"user_{random.randint(1, 1000)}",
            "event_type": random.choice(["CLICK", "VIEW", "PURCHASE", "LOGIN", "LOGOUT"]),
            "timestamp": int(time.time() * 1000),
            "page_id": self.faker.uri_path(),
            "metadata": {
                "browser": self.faker.user_agent(),
                "campaign": random.choice(["summer_sale", "black_friday", "none"])
            }
        }

    def delivery_report(self, err, msg):
        """Callback called once message is delivered or failed."""
        if err is not None:
            print(f"Delivery failed for record {msg.key()}: {err}")
        else:
            print(f"Record {msg.key()} produced to {msg.topic()} [{msg.partition()}] @ offset {msg.offset()}")

    def produce_events(self, count=10, delay=1.0):
        """Produces a sequence of events."""
        print(f"Starting production of {count} events to topic '{TOPIC_NAME}'...")
        
        for i in range(count):
            event = self.generate_event()
            
            self.producer.produce(
                topic=TOPIC_NAME,
                key=self.string_serializer(event['user_id']),
                value=self.avro_serializer(event, SerializationContext(TOPIC_NAME, MessageField.VALUE)),
                on_delivery=self.delivery_report
            )
            
            # Poll to trigger callbacks
            self.producer.poll(0)
            time.sleep(delay)
            
        print("Flushing records...")
        self.producer.flush()
        print("Done.")

if __name__ == "__main__":
    # Check if we are running from the correct directory or adjust path
    import os
    if not os.path.exists(SCHEMA_PATH):
        # Fallback if running from src/ingestion
        SCHEMA_PATH = "../../config/schemas/user_activity.avsc"
        
    producer = UserActivityProducer()
    producer.produce_events(count=20, delay=0.5)
