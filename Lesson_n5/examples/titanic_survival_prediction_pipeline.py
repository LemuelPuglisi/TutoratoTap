""" Train an Random Forest Classifier model that can predict if an actor 
    survived on the Titanic. 
"""

import shutil
import pyspark.sql.functions as funcs

from pyspark import SparkFiles
from pyspark.sql import SparkSession
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.classification import MultilayerPerceptronClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml import Pipeline

APP_NAME = 'Titanic Survival'
APP_DATASET_PATH = './data/titanic.csv'
APP_DATASET_FILE = 'titanic.csv'


def clear():
    shutil.rmtree('./model', ignore_errors=True)


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

    required_features = ['Pclass', 'Age', 'Fare', 'Gender', 'Boarded']

    mlp_parameters = {
        "labelCol":     'Survived', 
        "featuresCol":  'features',
        "maxIter":      100, 
        "layers":       [5, 12, 2], 
        "blockSize":    64, 
        "seed":         1234
    }

    stage_1 = StringIndexer(inputCol='Sex', outputCol='Gender', handleInvalid='keep')
    stage_2 = StringIndexer(inputCol='Embarked', outputCol='Boarded', handleInvalid='keep')
    stage_3 = VectorAssembler(inputCols=required_features, outputCol='features')
    stage_4 = MultilayerPerceptronClassifier(**mlp_parameters)
    pipeline = Pipeline(stages=[stage_1, stage_2, stage_3, stage_4])

    (training_data, test_data) = dataset.randomSplit([ .8, .2 ])

    pipeline_model = pipeline.fit(training_data)
    predictions = pipeline_model.transform(test_data)

    evaluator = MulticlassClassificationEvaluator(
        labelCol='Survived', 
        predictionCol='prediction', 
        metricName='accuracy'
    )

    accuracy = evaluator.evaluate(predictions)
    print('Test accuracy = ', accuracy)

    pipeline_model.save('model')

if __name__ == '__main__': 
    clear()
    main()