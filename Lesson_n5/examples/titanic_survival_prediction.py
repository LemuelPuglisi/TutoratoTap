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


def main():

    # "Accendiamo" la nostra applicazione Spark e 
    # passiamo il file contenente il dataset con cui
    # andremo ad allenare il nostro modello.

    spark = SparkSession.builder.appName(APP_NAME) \
        .config("spark.files.overwrite", "true") \
        .getOrCreate()

    spark.sparkContext.addFile(APP_DATASET_PATH)
    dataset_path = SparkFiles.get(APP_DATASET_FILE)

    df = spark.read.format('csv') \
        .option('header', True) \
        .load(dataset_path)


    #--------------------------------------------------------#
    # Preprocessing.
    #--------------------------------------------------------#

    # manual feature extraction, estraiamo solo una porzione
    # degli attributi associati ad ogni record, che sembrano 
    # poter essere coerenti con la label "Survived" da predire.  

    dataset = df.select(
        funcs.col('Survived').cast('float'), 
        funcs.col('Pclass').cast('float'), 
        funcs.col('Sex'), 
        funcs.col('Age').cast('float'), 
        funcs.col('Fare').cast('float'), 
        funcs.col('Embarked')
    )

    # Il dataset contiene vari elementi posti a NaN, che vogliamo
    # assolutamente escludere per garantire un corretto allenamento
    # del nostro modello di classificazione. 

    dataset = dataset.replace('?', None).dropna(how='any')

    # Il campo "Sex" ed il campo "Embarked" contengono informazioni
    # utili, tuttavia il training del modello richiede che le feature
    # siano numeriche, per cui dobbiamo trasformare tali valori testuali
    # in valori categoriali (es. ("Femmina", "Maschio") -> (1, 2))

    stringIndexer = StringIndexer(inputCol='Sex', outputCol='Gender', handleInvalid='keep')
    model = stringIndexer.fit(dataset=dataset)
    dataset = model.transform(dataset=dataset)

    stringIndexer = StringIndexer(inputCol='Embarked', outputCol='Boarded', handleInvalid='keep')
    model = stringIndexer.fit(dataset=dataset)
    dataset = model.transform(dataset=dataset)

    dataset = dataset.drop('Sex')
    dataset = dataset.drop('Embarked')

    # Spark richiede l'esistenza di una colonna che tenga
    # al suo interno tutte le feature sotto forma di array.
    # Es. altezza: 175 cm, peso: 80kg -> features: [175cm, 80kg]
    # Questo è facilmente ottenibile tramite la classe VectorAssembler

    required_features = ['Pclass', 'Age', 'Fare', 'Gender', 'Boarded']

    assembler = VectorAssembler(inputCols=required_features, outputCol='features')
    transformed_data = assembler.transform(dataset)

    #--------------------------------------------------------#
    # Modeling.
    #--------------------------------------------------------#

    # Dividiamo il nostro dataset in due: un training set, che 
    # verrà utilizzato nella procedura di training, ed un test 
    # set, che verrà utilizzato per valutare le performance del modello. 

    (training_data, test_data) = transformed_data.randomSplit([ .8, .2 ])

    # Utilizziamo una Random Forest come modello, nel gergo di Spark
    # questo è un Estimatore, perché prende in input un dataset e da
    # in output un transformer (il vero modello) in grado di predire 
    # la label con una certa accuratezza.

    mlp = MultilayerPerceptronClassifier(
        labelCol='Survived', 
        featuresCol='features',
        maxIter=100, 
        layers=[5, 12, 2], 
        blockSize=64, 
        seed=1234
    )

    model = mlp.fit(training_data)


    #--------------------------------------------------------#
    # Evaluation.
    #--------------------------------------------------------#

    # Una volta ottenuto il modello, calcoliamo le predizioni sul test set. 
    # L'oggetto in output, predictions, è un dataframe contenente le stesse
    # colonne di prima più una colonna 'prediction', contenente l'inferenza 
    # del modello. 

    predictions = model.transform(test_data)

    # Valutiamo l'accuratezza del modello tramite una classe che ci mette
    # a disposizione la libreria MLLIB. 

    evaluator = MulticlassClassificationEvaluator(
        labelCol='Survived', 
        predictionCol='prediction', 
        metricName='accuracy'
    )

    accuracy = evaluator.evaluate(predictions)
    print('Test accuracy = ', accuracy)

    
if __name__ == '__main__': main()