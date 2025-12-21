# Storage Module

This module handles the persistence of data into the Data Lake (MongoDB) and Data Warehouse (BigQuery).

## Components
1.  **MongoDB (Raw Layer)**: Stores all incoming events as JSON documents.
2.  **BigQuery (Analytical Layer)**: Stores structured, partitioned data for analysis.

## Running the MongoDB Consumer
This consumer subscribes to all topics and dumps data into MongoDB.

```bash
python src/storage/mongo_consumer.py
```

## Verifying Data
1.  **MongoDB**: Access Mongo Express at http://localhost:8083 (User: `admin`, Pass: `password`).
    *   Check database `monitoring_datalake`.
    *   Check collections `raw_user_activity` and `raw_wikimedia_changes`.

2.  **BigQuery**: Run the DDL scripts in `config/bigquery/ddl_tables.sql` in your GCP Console.
