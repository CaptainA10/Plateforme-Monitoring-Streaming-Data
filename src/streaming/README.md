# Streaming Module

This module contains the PySpark Structured Streaming jobs.

## Prerequisites
1.  **Infrastructure**: Ensure Docker stack is running (Kafka, Spark).
2.  **Spark Packages**: We need `spark-sql-kafka` and `spark-avro`.

## Running the Job (Docker)
We submit the job to the Spark Master container.

```bash
docker exec -it spark-master spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,org.apache.spark:spark-avro_2.12:3.5.0 \
  src/streaming/jobs/process_user_activity.py
```

## What it does
1.  Reads `user_activity` topic (Kafka).
2.  Deserializes Avro (skipping Confluent header).
3.  Aggregates counts by `event_type` in 1-minute windows.
4.  Prints results to the console.
