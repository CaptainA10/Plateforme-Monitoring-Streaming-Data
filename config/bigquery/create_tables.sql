-- Table 1: user_activity
CREATE TABLE `effidic-stage-2026.monitoring_datalake.user_activity` (
  event_id STRING NOT NULL,
  user_id STRING NOT NULL,
  event_type STRING NOT NULL,
  timestamp TIMESTAMP NOT NULL,
  page_id STRING,
  metadata JSON
)
PARTITION BY DATE(timestamp)
CLUSTER BY event_type, user_id;

-- Table 2: wikimedia_changes
CREATE TABLE `effidic-stage-2026.monitoring_datalake.wikimedia_changes` (
  id INT64 NOT NULL,
  type STRING,
  title STRING,
  user STRING,
  bot BOOLEAN,
  timestamp TIMESTAMP,
  server_name STRING
)
PARTITION BY DATE(timestamp);
