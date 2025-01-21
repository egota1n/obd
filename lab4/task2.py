from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("KafkaStreamingEventsCount") \
    .config("spark.jars.repositories", "https://repo1.maven.org/maven2/") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.4") \
    .getOrCreate()

df_raw = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "test_topic") \
    .option("startingOffsets", "latest") \
    .load()

df_events = df_raw.selectExpr("CAST(value AS STRING) as event")

from pyspark.sql.functions import current_timestamp
df_events = df_events.withColumn("event_time", current_timestamp())

from pyspark.sql.functions import window, count

events_per_minute = df_events.groupBy(
    window("event_time", "1 minute")
).agg(
    count("event").alias("event_count")
)

result_df = events_per_minute.select("window", "event_count")

query = result_df.writeStream \
    .outputMode("update") \
    .format("console") \
    .option("truncate", "false") \
    .start()

query.awaitTermination()