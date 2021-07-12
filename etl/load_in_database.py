from cassandra.cluster import Cluster
from pyspark.sql import Row

def load_in_database(row: Row, conf: dict):
    cluster = Cluster()

    session = cluster.connect(keyspace=conf["keyspace"])

    session.execute("INSERT INTO novel(novel_title, chapter_title, chapter_phrase) VALUES (%s,%s,%s)", (row.novel_title, row.chapter_title, row.chapter_phrase))
