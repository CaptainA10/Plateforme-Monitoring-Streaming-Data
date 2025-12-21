# Batch Module

This module contains the Batch Processing jobs orchestrated by Airflow.

## Jobs
*   **daily_stats.py**: Reads from MongoDB and calculates daily statistics.

## Running Manually
To test the batch job without Airflow:

```bash
docker exec -it spark-master spark-submit \
  --packages org.mongodb.spark:mongo-spark-connector_2.12:10.2.1 \
  src/batch/daily_stats.py
```
