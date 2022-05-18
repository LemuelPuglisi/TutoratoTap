from pyspark.streaming import StreamingContext
from pyspark.sql import SparkSession

APP_NAME = 'network_wordcount'
APP_BATCH_INTERVAL = 1

if __name__ == '__main__':
    spark = SparkSession.builder.appName(APP_NAME).getOrCreate()
    ssc = StreamingContext(spark.sparkContext, APP_BATCH_INTERVAL)
    lines = ssc.socketTextStream('0.0.0.0', 9999)
    words = lines.flatMap(lambda line: line.split(" "))
    pairs = words.map(lambda word: (word, 1))
    wordCounts = pairs.reduceByKey(lambda x, y: x + y)
    wordCounts.pprint()
    ssc.start()
    ssc.awaitTermination()