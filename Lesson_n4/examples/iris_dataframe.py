from pyspark import SparkFiles
from pyspark.sql import SparkSession
from pyspark.sql import types as st

IRIS_DATASET_URL = 'https://gist.githubusercontent.com/curran/a08a1080b88344b0c8a7/raw/0e7a9b0a5d22642a06d3d5b9bcbad9890c8ee534/iris.csv'

if __name__ == '__main__':
    
    schema = st.StructType([
        st.StructField('sepal_length',  st.FloatType()), 
        st.StructField('sepal_width',   st.FloatType()), 
        st.StructField('petal_length',  st.FloatType()), 
        st.StructField('petal_width',   st.FloatType()), 
        st.StructField('species',      st.StringType()), 
    ])

    spark = SparkSession.builder.getOrCreate()
    spark.sparkContext.addFile(IRIS_DATASET_URL)
    filepath = 'file://' + SparkFiles.get('iris.csv')
    # df = spark.read.csv(filepath, header=True, inferSchema=True)
    df = spark.read.csv(filepath, header=True, schema=schema)
    df.show(5)
