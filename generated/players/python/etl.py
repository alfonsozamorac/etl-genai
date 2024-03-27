from pyspark.sql import SparkSession
from pyspark.sql import functions as F

# Configure Spark session
spark = SparkSession.builder.appName("FootballRanking").getOrCreate()

# Read data from BigQuery
players_goals_table = spark.read.format("bigquery") \
    .option("table", "myligue.players_goals") \
    .load()

# Filter data for minutes 60 and above
filtered_df = players_goals_table.filter(F.col("minute") >= 60)

# Calculate player rankings
player_rankings = filtered_df \
    .groupBy("player") \
    .agg(F.count("goal_date").alias("goals_scored")) \
    .orderBy("goals_scored", ascending=False) \
    .limit(5)

# Write player rankings to BigQuery
player_rankings.write.format("bigquery") \
    .option("temporaryGcsBucket", "temporary-files-dataproc") \
    .option("table", "myligue.players_ranking") \
    .mode("overwrite") \
    .save()

# Stop the Spark session
spark.stop()