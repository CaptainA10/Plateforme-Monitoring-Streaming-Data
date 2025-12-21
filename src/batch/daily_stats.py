from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# Configuration
MONGO_URI = "mongodb://admin:password@mongo:27017/monitoring_datalake.raw_user_activity"

def main():
    spark = SparkSession.builder \
        .appName("DailyUserActivityStats") \
        .config("spark.mongodb.input.uri", MONGO_URI) \
        .config("spark.mongodb.output.uri", MONGO_URI) \
        .getOrCreate()

    # 1. Read from MongoDB (Raw Data)
    # Requires: org.mongodb.spark:mongo-spark-connector_2.12:3.0.1 (Check compatibility with Spark 3.5)
    # For Spark 3.5, we might need a newer connector.
    df = spark.read.format("mongo").load()

    # 2. Calculate Stats
    # Example: Count events per user
    df_stats = df.groupBy("user_id").count().withColumnRenamed("count", "total_events")

    # 3. Show Results (or write back to Mongo/BigQuery)
    df_stats.show()

    spark.stop()

if __name__ == "__main__":
    main()
