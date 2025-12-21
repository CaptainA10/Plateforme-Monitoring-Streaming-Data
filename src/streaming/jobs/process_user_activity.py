from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import os

# Configuration
KAFKA_BOOTSTRAP_SERVERS = "broker:29092"
TOPIC_NAME = "user_activity"
SCHEMA_PATH = "/opt/bitnami/spark/src/config/schemas/user_activity.avsc" # Path inside Docker

def main():
    spark = SparkSession.builder \
        .appName("UserActivityAggregation") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

    # 1. Read from Kafka
    # Note: We read the binary value. To deserialize Avro without external Schema Registry service dependency in Spark,
    # we can use the 'from_avro' function if we provide the schema JSON.
    # Alternatively, for this demo, we can assume the producer sends JSON or we manually parse.
    # BUT, our producer sends Avro (binary).
    # So we MUST use 'from_avro' with the schema definition.
    
    # Load Schema from file
    # In a real cluster, we would use ABRIS to fetch from Schema Registry.
    # Here, we read the local .avsc file.
    try:
        with open("config/schemas/user_activity.avsc", "r") as f:
            avro_schema = f.read()
    except FileNotFoundError:
        # Fallback if running locally vs docker
        with open("../../config/schemas/user_activity.avsc", "r") as f:
            avro_schema = f.read()

    df_kafka = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
        .option("subscribe", TOPIC_NAME) \
        .option("startingOffsets", "latest") \
        .load()

    # 2. Deserialize Avro
    # We skip the first 5 bytes (Magic Byte + Schema ID) because Confluent adds them.
    # Spark's from_avro expects pure Avro binary.
    # expr("substring(value, 6)") removes the Confluent header.
    
    from pyspark.sql.avro.functions import from_avro
    
    df_parsed = df_kafka.select(
        from_avro(expr("substring(value, 6)"), avro_schema).alias("data"),
        col("timestamp").alias("kafka_timestamp")
    ).select("data.*")

    # 3. Transformations
    # Convert timestamp (long millis) to TimestampType
    df_transformed = df_parsed.withColumn("event_time", (col("timestamp") / 1000).cast(TimestampType()))

    # Watermark: Handle late data (10 minutes tolerance)
    df_watermarked = df_transformed.withWatermark("event_time", "10 minutes")

    # Aggregation: Count events by Type per 1-minute window
    df_aggregated = df_watermarked \
        .groupBy(
            window(col("event_time"), "1 minute"),
            col("event_type")
        ) \
        .count()

    # 4. Write to Console (Debugging)
    # Added Checkpointing for Fault Tolerance
    query = df_aggregated.writeStream \
        .outputMode("update") \
        .format("console") \
        .option("truncate", "false") \
        .option("checkpointLocation", "/tmp/checkpoints/user_activity_agg") \
        .start()

    query.awaitTermination()

if __name__ == "__main__":
    main()
