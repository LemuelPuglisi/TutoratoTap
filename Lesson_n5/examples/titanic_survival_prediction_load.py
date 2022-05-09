""" Train an Random Forest Classifier model that can predict if an actor 
    survived on the Titanic. 
"""

import pyspark.sql.functions as funcs

from pyspark import SparkFiles
from pyspark.sql import SparkSession
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.classification import MultilayerPerceptronClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml import PipelineModel

APP_NAME = 'Titanic Survival'
APP_DATASET_PATH = './data/titanic.csv'
APP_DATASET_FILE = 'titanic.csv'


def main():

    spark = SparkSession.builder.appName(APP_NAME) \
        .config("spark.files.overwrite", "true") \
        .getOrCreate()

    spark.sparkContext.addFile(APP_DATASET_PATH)
    dataset_path = SparkFiles.get(APP_DATASET_FILE)

    df = spark.read.format('csv') \
        .option('header', True) \
        .load(dataset_path)

    dataset = df.select(
        funcs.col('Survived').cast('float'), 
        funcs.col('Pclass').cast('float'), 
        funcs.col('Sex'), 
        funcs.col('Age').cast('float'), 
        funcs.col('Fare').cast('float'), 
        funcs.col('Embarked')
    )

    dataset = dataset.replace('?', None).dropna(how='any')

    (_, test_data) = dataset.randomSplit([ .8, .2 ])

    # abbiamo esportato la pipeline precedente, includendo
    # sia gli stage preliminari (StringIndexer, VectorAssembler, MLP)
    # sia i parametri del modello (parametri di MLP).

    pipeline_model = PipelineModel.load('model')
    predictions = pipeline_model.transform(test_data)

    evaluator = MulticlassClassificationEvaluator(
        labelCol='Survived', 
        predictionCol='prediction', 
        metricName='accuracy'
    )

    accuracy = evaluator.evaluate(predictions)
    print('Loaded model - Test accuracy = ', accuracy)


if __name__ == '__main__': main()