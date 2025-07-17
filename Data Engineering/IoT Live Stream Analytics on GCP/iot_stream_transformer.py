from pyspark import *
from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
import json

spark = SparkSession.builder \
    .appName("IOT Stream Processor") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

schema = StructType([
    StructField("device_id", StringType(), True),
    StructField("temperature", FloatType(), True),  
    StructField("pressure", FloatType(), True),
    StructField("humidity", FloatType(), True),
    StructField("co2_level", FloatType(), True),
    StructField("gas_leak", BooleanType(), True),
    StructField("timestamp", StringType(), True)
]) 

df = spark.readStream.format("json").schema(schema).load("gs://iot-stream-output-2025/iot-raw/")
df = df.withColumn("event_time", to_timestamp(col("timestamp")))

df = df.withColumn("hour", hour(col("timestamp"))) \
       .withColumn("day", dayofmonth(col("timestamp"))) \
       .withColumn("Weekday", date_format("timestamp", "EEEE")) \
       .withColumn("month", month(col("timestamp"))) \
       .withColumn("year", year(col("timestamp"))) \
       .withColumn("temp_anomaly", when((col("temperature") > 45) | (col("temperature") < 10), True).otherwise(False)) \
       .withColumn("air_quality_bucket", when(col("co2_level") < 500, "Good")
                                     .when(col("co2_level") < 900, "Moderate")
                                     .otherwise("Poor")) \
       .withColumn("humidity_level", when(col("humidity") < 30, "Low")
                                    .when(col("humidity") < 60, "Normal")
                                    .otherwise("High")) \
       .withColumn("heat_index", expr("""
            -8.784695 + 1.61139411 * temperature + 2.338549 * humidity - 
            0.14611605 * temperature * humidity
        """)) \
       .withColumn("pressure_anomaly", (col("pressure") > 1050) | (col("pressure") < 950))

# Batch-wise logic (for window functions)
def process_batch(batch_df, batch_id):
    from pyspark.sql.window import Window
    from pyspark.sql.functions import lag, col, when

    w = Window.partitionBy("device_id").orderBy("event_time")

    batch_df = batch_df.withColumn("prev_temp", lag("temperature").over(w)) \
                       .withColumn("prev_pressure", lag("pressure").over(w)) \
                       .withColumn("sensor_flatline", col("prev_temp") == col("temperature")) \
                       .withColumn("pressure_flatline", col("prev_pressure") == col("pressure")) \
                       .withColumn("temp_diff", col("temperature") - col("prev_temp")) \
                       .withColumn("pressure_diff", col("pressure") - col("prev_pressure")) \
                       .withColumn("flat_temp_flag", when(col("temperature") == col("prev_temp"), 1).otherwise(0)) \
                       .withColumn("flat_pressure_flag", when(col("pressure") == col("prev_pressure"), 1).otherwise(0))

    # Write to GCS
    batch_df.write.mode("append").json("gs://iot-stream-output-2025/iot_transform_output/")

# Use foreachBatch for custom transformation
query = df.writeStream \
    .foreachBatch(process_batch) \
    .option("checkpointLocation", "gs://iot-stream-output-2025/temp/") \
    .start()

query.awaitTermination()
