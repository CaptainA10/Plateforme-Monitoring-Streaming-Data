# Ingestion Module

This module contains the Kafka Producers responsible for ingesting data into the platform.

## Prerequisites
1.  **Infrastructure**: Ensure the Docker stack is running.
    ```bash
    docker-compose up -d
    ```
    Wait for `broker` and `schema-registry` to be healthy.

2.  **Dependencies**: Install Python requirements.
    ```bash
    pip install -r requirements.txt
    ```

## Running the Producer
The producer generates mock `UserActivity` events and sends them to the `user_activity` topic.

```bash
python src/ingestion/main.py
```

## Verifying Data
You can verify that data is arriving in Kafka using the Console Consumer (if you have Kafka tools installed) or by checking the logs of the producer.

To check the Schema Registry:
```bash
curl http://localhost:8081/subjects
```
You should see `user_activity-value`.

## Running the Wikimedia Producer (Real-time)
This producer connects to the Wikimedia SSE stream, filters for `frwiki` (excluding bots), and sends events to `wikimedia_changes`.

```bash
python src/ingestion/wikimedia_producer.py
```
*Note: Ensure `sseclient-py` is installed.*
