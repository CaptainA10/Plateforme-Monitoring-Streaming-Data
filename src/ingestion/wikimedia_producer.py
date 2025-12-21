import json
import time
from confluent_kafka import Producer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
import sseclient
import requests

# Configuration
SCHEMA_REGISTRY_URL = "http://localhost:8085"
BROKER_URL = "localhost:9092"
TOPIC_NAME = "wikimedia_changes"
SCHEMA_PATH = "../../config/schemas/wikimedia_change.avsc"
WIKIMEDIA_STREAM_URL = "https://stream.wikimedia.org/v2/stream/recentchange"

# Filters
FILTER_WIKI = "frwiki"  # Only French Wikipedia
FILTER_BOTS = True      # Exclude bots

class WikimediaProducer:
    def __init__(self):
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
            lambda obj, ctx: obj
        )
        self.string_serializer = StringSerializer('utf_8')
        
        # 4. Setup Producer
        producer_conf = {'bootstrap.servers': BROKER_URL}
        self.producer = Producer(producer_conf)

    def delivery_report(self, err, msg):
        if err is not None:
            print(f"Delivery failed for record {msg.key()}: {err}")
        # else:
            # print(f"Record produced to {msg.topic()} [{msg.partition()}] @ offset {msg.offset()}")

    def process_stream(self):
        print(f"Connecting to {WIKIMEDIA_STREAM_URL}...")
        print(f"Filters: Wiki={FILTER_WIKI}, ExcludeBots={FILTER_BOTS}")
        
        response = requests.get(WIKIMEDIA_STREAM_URL, stream=True)
        client = sseclient.SSEClient(response)
        
        count = 0
        start_time = time.time()

        for event in client.events():
            if event.event == 'message':
                try:
                    change = json.loads(event.data)
                    
                    # --- FILTERING LOGIC ---
                    if change.get('wiki') != FILTER_WIKI:
                        continue
                    if FILTER_BOTS and change.get('bot') is True:
                        continue
                    # -----------------------

                    # Prepare record for Avro
                    record = {
                        "id": change.get('id'),
                        "user": change.get('user'),
                        "title": change.get('title'),
                        "comment": change.get('comment'),
                        "wiki": change.get('wiki'),
                        "timestamp": change.get('timestamp', int(time.time())),
                        "bot": change.get('bot', False),
                        "type": change.get('type')
                    }

                    self.producer.produce(
                        topic=TOPIC_NAME,
                        key=self.string_serializer(str(change.get('meta', {}).get('id', ''))),
                        value=self.avro_serializer(record, SerializationContext(TOPIC_NAME, MessageField.VALUE)),
                        on_delivery=self.delivery_report
                    )
                    
                    self.producer.poll(0)
                    count += 1
                    
                    if count % 10 == 0:
                        elapsed = time.time() - start_time
                        print(f"Produced {count} events ({count/elapsed:.2f} events/sec)")

                except json.JSONDecodeError:
                    pass
                except Exception as e:
                    print(f"Error processing event: {e}")

if __name__ == "__main__":
    import os
    # If running from project root
    if os.path.exists("config/schemas/wikimedia_change.avsc"):
        SCHEMA_PATH = "config/schemas/wikimedia_change.avsc"
    # If running from src/ingestion
    elif os.path.exists("../../config/schemas/wikimedia_change.avsc"):
        SCHEMA_PATH = "../../config/schemas/wikimedia_change.avsc"
        
    producer = WikimediaProducer()
    try:
        producer.process_stream()
    except KeyboardInterrupt:
        print("\nStopping producer...")
        producer.producer.flush()
