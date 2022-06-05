import pandas as pd

from pyspark.sql import SparkSession
from pyspark.sql import types as st
from elasticsearch import Elasticsearch

APP_NAME = 'spark_to_es'
ES_INDEX = 'heart'
APP_BATCH_INTERVAL = 1


es = Elasticsearch(
    "https://es01:9200",
    ca_certs="/app/certs/ca/ca.crt",
    basic_auth=("elastic", "tutoratotap"), 
)     

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


def process_batch(batch_df, batch_id):
    for idx, row in enumerate(batch_df.collect()):
        row_dict = row.asDict()
        id = f'{batch_id}-{idx}'
        resp = es.index(index=ES_INDEX, id=id, document=row_dict)
        print(resp)


def main():

    spark = SparkSession.builder.appName(APP_NAME).getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")

    schema = get_record_schema()

    df = spark.readStream \
        .option('sep', ',') \
        .schema(schema) \
        .csv("/app/*.csv", header=True)

    df.writeStream \
        .foreachBatch(process_batch) \
        .start() \
        .awaitTermination()


if __name__ == '__main__': main()