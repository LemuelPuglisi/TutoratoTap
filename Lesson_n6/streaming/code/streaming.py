from pyspark.ml import PipelineModel
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
from pyspark.sql import types as st
from pyspark.sql.functions import from_json, col

APP_NAME = 'ha-streaming-prediction'
APP_BATCH_INTERVAL = 1

def get_record_schema():
    return st.StructType([
        st.StructField('age',         st.FloatType()),
        st.StructField('sex',         st.FloatType()),
        st.StructField('cp',          st.FloatType()),
        st.StructField('trtbps',      st.FloatType()),
        st.StructField('chol',        st.FloatType()),
        st.StructField('fbs',         st.FloatType()),
        st.StructField('restecg',     st.FloatType()),
        st.StructField('exng',        st.FloatType()),
        st.StructField('oldpeak',     st.FloatType()),
        st.StructField('slp',         st.FloatType()),
        st.StructField('caa',         st.FloatType()),
        st.StructField('thall',       st.FloatType()),
    ])


def main():

    spark = SparkSession.builder.appName(APP_NAME).getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")

    model = PipelineModel.load("model")
    schema = get_record_schema()

    df = spark.readStream.format('kafka') \
        .option('kafka.bootstrap.servers', 'broker:29092') \
        .option('subscribe', 'cardiology') \
        .load() \
        .select(from_json(col("value").cast("string"), schema).alias("data")) \
        .selectExpr("data.*")

    results = model.transform(df)
    results.writeStream \
        .format("console") \
        .outputMode("append") \
        .start() \
        .awaitTermination()


if __name__ == '__main__': main()

