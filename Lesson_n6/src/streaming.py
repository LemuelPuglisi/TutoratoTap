from pyspark.ml import PipelineModel
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext


APP_NAME = 'ha-streaming-prediction'
APP_BATCH_INTERVAL = 1


def main():

    spark = SparkSession.builder.appName(APP_NAME).getOrCreate()
    ssc = StreamingContext(spark.sparkContext, APP_BATCH_INTERVAL)
    model = PipelineModel.load("model")

    spark.readStream.format('kafka') \
        .option('kafka.bootstrap.servers', 'localhost:9092') \
        .option('subscribe', 'cardiology') \
        .load()


if __name__ == '__main__': main()

