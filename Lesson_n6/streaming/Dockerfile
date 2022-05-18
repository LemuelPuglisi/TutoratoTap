FROM jupyter/pyspark-notebook:spark-3.1.1

RUN pip3 install pyspark numpy

WORKDIR /app

COPY ./model ./model
COPY ./code .

ENTRYPOINT ["spark-submit", "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1", "--master", "local[*]", "streaming.py"]