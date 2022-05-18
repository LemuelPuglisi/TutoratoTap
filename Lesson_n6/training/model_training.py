import pyspark.sql.functions as funcs

from pyspark import SparkFiles
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.ml.classification import LinearSVC
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml import Pipeline


APP_NAME = 'heart_attack_pred_model_training'
APP_DATASET_PATH = './data/heart.csv'
APP_DATASET_FILE = 'heart.csv'

#--------------------------------------------------------#
#|
#|  Descrizione delle features.
#|
#--------------------------------------------------------#

REQUIRED_FEATURES = [
    'age',      # età del paziente
    'sex',      # sesso del paziente
    'cp',       # Tipo di dolore al petto (categoriale)
    'trtbps',   # pressione sanguigna a riposo
    'chol',     # colesterolo in mg/dL (mg per decilitro di sangue)
    'fbs',      # glicemia a digiuno (1 se >= 120 mg/dL, 0 altrimenti)
    'restecg',  # ECG a riposo (1 normale, 0 altrimenti)
    'exng',     # Dolore al petto indotto da sforzo fisico
    'oldpeak',  # - non specificato
    'slp',      # - non specificato
    'caa',      # - non specificato
    'thall',    # - non specificato
]


def main():

    #--------------------------------------------------------#
    #|
    #|  Inizializzazione SparkSession e caricamento dataset
    #|
    #--------------------------------------------------------#


    spark = SparkSession.builder.appName(APP_NAME) \
        .config("spark.files.overwrite", "true") \
        .getOrCreate()

    spark.sparkContext.addFile(APP_DATASET_PATH)
    dataset_path = SparkFiles.get(APP_DATASET_FILE)

    df = spark.read.format('csv') \
            .option('header', True) \
            .load(dataset_path)

    #--------------------------------------------------------#
    #|
    #|  Feature selection e casting a float.
    #|
    #--------------------------------------------------------#


    dataset = df.select(
        funcs.col('age').cast('float'),
        funcs.col('sex').cast('float'),
        funcs.col('cp').cast('float'),
        funcs.col('trtbps').cast('float'),
        funcs.col('chol').cast('float'),
        funcs.col('fbs').cast('float'),
        funcs.col('restecg').cast('float'),
        funcs.col('exng').cast('float'),
        funcs.col('oldpeak').cast('float'),
        funcs.col('slp').cast('float'),
        funcs.col('caa').cast('float'),
        funcs.col('thall').cast('float'),
        funcs.col('output').cast('float'),
    )


    #--------------------------------------------------------#
    #|
    #|  Creazione della pipeline.
    #|
    #--------------------------------------------------------#


    asb = VectorAssembler(inputCols=REQUIRED_FEATURES, outputCol='features')
    scl = StandardScaler(inputCol='features', outputCol='scaled_features', withMean=True, withStd=True)
    svm = LinearSVC(labelCol='output', featuresCol='scaled_features', maxIter=100, regParam=.1)
    pipeline = Pipeline(stages=[asb, scl, svm])


    #--------------------------------------------------------#
    #|
    #|  Training ed Evaluation
    #|
    #--------------------------------------------------------#

    (training_data, test_data) = dataset.randomSplit([ .8, .2 ])

    pipeline_model = pipeline.fit(training_data)
    predictions = pipeline_model.transform(test_data)

    evaluator = MulticlassClassificationEvaluator(
        labelCol='output', 
        predictionCol='prediction', 
        metricName='accuracy'
    )

    accuracy = evaluator.evaluate(predictions)
    print('Test accuracy = ', accuracy)

    #--------------------------------------------------------#
    #|
    #|  Salvataggio della pipeline
    #|
    #--------------------------------------------------------#

    pipeline_model.save('model')



if __name__ == '__main__': main()