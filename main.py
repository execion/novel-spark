from pyspark.sql import SparkSession, SQLContext
from etl.get_html import create_sqlite
from config import * # "db", "novel"
from etl.load_in_database import load_in_database
from pyspark.sql.functions import *

create_sqlite(novel["url"], "./sqlites")

# TABLE novel( 
#     novel_title text,
#     chapter_title text,
#     chapter_phrase text
# ) In Cassandra and SQLITE

spark = SparkSession.builder.master("local[*]").getOrCreate()
sql_ctx = SQLContext(spark)

df = sql_ctx.read.format("jdbc").options(
    url ="jdbc:sqlite:{}".format(novel["path"]),
    driver="org.sqlite.JDBC",
    dbtable="novel"
).load()

df = spark.createDataFrame(df.toPandas())
df = df.dropna().drop_duplicates()
clean_rows = df.filter((length(col("novel_title")) > 3) & (length(col("chapter_title")) > 3) & (length(col("chapter_phrase")) > 12))
df.foreach(lambda x: load_in_database(x,db))
