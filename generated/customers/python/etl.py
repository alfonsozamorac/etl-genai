from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# Configure Spark session
spark = SparkSession.builder.appName("SalesETL").getOrCreate()

# Define file paths
sales_path = "gs://sales-etl-bucket/input/sales/*.csv"
customers_path = "gs://sales-etl-bucket/input/customers/*.csv"

# Read CSV files into DataFrames
sales_df = spark.read.csv(sales_path, header=True, inferSchema=True)
customers_df = spark.read.csv(customers_path, header=True, inferSchema=True)

# Write tables to BigQuery
sales_df.write.format("bigquery") \
    .option("temporaryGcsBucket", "temporary-files-dataproc") \
    .option("table",  "raw_sales_data.sales_table") \
    .mode("overwrite") \
    .save()
customers_df.write.format("bigquery") \
    .option("temporaryGcsBucket", "temporary-files-dataproc") \
    .option("table",  "raw_sales_data.customer_table") \
    .mode("overwrite") \
    .save()

# Join sales and customers tables
bigtable_info_df = sales_df.join(customers_df, on="customer_id", how="inner")

# Write joined table to BigQuery
bigtable_info_df.write.format("bigquery") \
    .option("temporaryGcsBucket", "temporary-files-dataproc") \
    .option("table",  "master_sales_data.bigtable_info") \
    .mode("overwrite") \
    .save()

# Stop the Spark session
spark.stop()