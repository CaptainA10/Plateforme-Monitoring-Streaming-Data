-- BigQuery DDL for Monitoring Platform

-- 1. Create Dataset
CREATE SCHEMA IF NOT EXISTS `monitoring_platform`
OPTIONS (
  location = 'EU'
);

-- 2. User Activity Table (Partitioned by Day)
CREATE TABLE IF NOT EXISTS `monitoring_platform.user_activity` (
  event_id STRING NOT NULL,
  user_id STRING NOT NULL,
  event_type STRING NOT NULL,
  timestamp TIMESTAMP NOT NULL,
  page_id STRING,
  metadata STRING, -- JSON string or STRUCT
  ingestion_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
)
PARTITION BY DATE(timestamp)
CLUSTER BY user_id, event_type;

-- 3. Wikimedia Changes Table (Partitioned by Day)
CREATE TABLE IF NOT EXISTS `monitoring_platform.wikimedia_changes` (
  id INT64,
  user STRING,
  title STRING,
  comment STRING,
  wiki STRING,
  timestamp TIMESTAMP NOT NULL,
  bot BOOLEAN,
  type STRING,
  ingestion_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
)
PARTITION BY DATE(timestamp)
CLUSTER BY wiki;
