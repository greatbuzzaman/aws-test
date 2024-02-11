from pyspark.sql import SparkSession

# Initialize SparkSession
spark = SparkSession.builder \
    .appName("Read and Write S3") \
    .getOrCreate()

# Define S3 input and output paths
input_path = "{SPARK_INPUT_PATH}"
output_path = "{SPARK_OUTPUT_PATH}"

# Read file from S3
df = spark.read.csv(input_path, header=True, inferSchema=True)

# Perform processing (example: convert column to uppercase)
df_processed = df.withColumn("processed_column", df["firstname"].cast("string").upper())

# Write processed data back to S3
df_processed.write \
    .mode("overwrite") \
    .csv(output_path)

# Stop SparkSession
spark.stop()
