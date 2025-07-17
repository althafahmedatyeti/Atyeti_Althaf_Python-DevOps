from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

spark = SparkSession.builder \
    .appName("IOT Stream Processor") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Define schema
schema = StructType([
    StructField("device_id", StringType(), True),
    StructField("temperature", FloatType(), True),
    StructField("pressure", FloatType(), True),
    StructField("humidity", FloatType(), True),
    StructField("co2_level", FloatType(), True),
    StructField("gas_leak", BooleanType(), True),
    StructField("timestamp", StringType(), True)
])

# Read stream
df = spark.readStream.format("json") \
    .schema(schema) \
    .load("gs://iot-stream-output-2025/iot-raw/")

df = df.withColumn("event_time", to_timestamp(col("timestamp")))

# Enrich with features
df = df.withColumn("hour", hour("event_time")) \
       .withColumn("day", dayofmonth("event_time")) \
       .withColumn("weekday", date_format("event_time", "EEEE")) \
       .withColumn("month", month("event_time")) \
       .withColumn("year", year("event_time")) \
       .withColumn("temp_anomaly", when((col("temperature") > 45) | (col("temperature") < 10), True).otherwise(False)) \
       .withColumn("air_quality_bucket", when(col("co2_level") < 500, "Good")
                   .when(col("co2_level") < 900, "Moderate").otherwise("Poor")) \
       .withColumn("humidity_level", when(col("humidity") < 30, "Low")
                   .when(col("humidity") < 60, "Normal").otherwise("High")) \
       .withColumn("heat_index", expr("""
           -8.784695 + 1.61139411 * temperature + 2.338549 * humidity -
           0.14611605 * temperature * humidity
       """)) \
       .withColumn("pressure_anomaly", (col("pressure") > 1050) | (col("pressure") < 950)) \
       .withColumn("system_failure", when(
           (col("co2_level") > 2000) |
           (col("gas_leak") == True) |
           (col("temperature") > 50) |
           (col("temperature") < 5) |
           ((col("pressure") > 1050) | (col("pressure") < 950)),
           True
       ).otherwise(False))

# Write batch-wise to BigQuery
def process_batch(batch_df, batch_id):
    batch_df.write \
        .format("bigquery") \
        .option("table", "iot-stream-project.iot_processed_data.iot_enriched") \
        .option("temporaryGcsBucket", "iot-stream-output-2025") \
        .mode("append") \
        .save()

# Start streaming
query = df.writeStream \
    .foreachBatch(process_batch) \
    .option("checkpointLocation", "gs://iot-stream-output-2025/temp/") \
    .start()

query.awaitTermination()
