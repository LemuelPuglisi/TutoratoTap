FROM jupyter/pyspark-notebook:spark-3.1.1

RUN pip3 install pyspark numpy elasticsearch

WORKDIR /app

COPY ./data .
COPY ./code .

ENTRYPOINT ["spark-submit", "--master", "local[*]", "streaming.py"]