# Spark MLLIB 🤖

[MLLib](https://spark.apache.org/docs/3.2.1/ml-guide.html) è una libreria di Machine Learning integrata su Spark che permette di svolgere task di ML in modo distribuito (e molto semplice). I modelli sono già implementati e pronti all'utilizzo. 



## Cosa è uno Spark Dataframe?

> Prima di tutto, cosa è uno **Spark Dataset**? Un Dataset è una collezione di dati distribuita nel cluster, e beneficia delle ottimizzazioni ottenute attraverso l'utilizzo dell'SQL execution engine. 

Un Dataframe è un Dataset organizzato in colonne nominate. Concettualmente, è equivalente ad una tabella di un database relazionale. 

|      | PassengerId | Survived | Pclass | Name                                              | Sex  | Age  | SibSp | Parch | Fare             | Cabin | Embarked |
| ---- | ----------- | -------- | ------ | ------------------------------------------------- | ---- | ---- | ----- | ----- | ---------------- | ----- | -------- |
| 1    | 1           | 0        | 3      | Braund, Mr. Owen Harris                           | M    | 22   | 1     | 0     | A/5 21171        | NaN   | S        |
| 2    | 2           | 1        | 2      | Cumings, Mrs. John Bradley (Florence Briggs Th... | F    | 38   | 1     | 0     | PC 17599         | C85   | C        |
| 3    | 3           | 1        | 3      | Heikkinen, Miss. Laina                            | M    | 26   | 0     | 0     | STON/O2. 3101282 | NaN   | S        |



## Cosa è un Transformer?

Un `Transformer` è un oggetto che implementa un metodo `transform()`, ovvero un metodo che prende in input un Dataframe e ne da in output un altro. Vediam alcuni esempi di Transformer che vedremo durante la lezione: 

| Classe                                  | Descrizione                                                  |
| --------------------------------------- | ------------------------------------------------------------ |
| StringIndexer                           | Data una colonna del dataframe in input con contenuto testuale ma categorico ( es. genere=[M, F, non-binary] ), introduce una nuova colonna il cui contenuto è numerico e categorico (es. num_genere=[1, 2, 3], dove 1=M, 2=F, 3=non-binary).  Torna in output un nuovo dataframe uguale a quello in input, meno che per la colonna aggiunta. |
| VectorAssembler                         | Dato in input un dataset ed una lista di colonne del dataset, introduce una nuova colonna che compatta in un vettore gli elementi delle colonne specificate. Se le colonne specificate sono "altezza" e "peso", la nuova colonna conterrà array di lunghezza due [altezza, peso]. Il dataframe con la colonna aggiunta viene ritornato in output. |
| MultilayerPerceptronClassificationModel | Prende in input un dataframe e inserisce una colonna contenente una predizione. Il dataframe con la colonna aggiunta viene ritornato in output. |



## Cosa è un Estimator?

Un `Estimator` astrae il concetto di algoritmo di apprendimento, o di qualsiasi tipo di algoritmo che utilizza dei dati per creare un modello (Classificatore, Regressore, Sistema di Raccomandazione). Implementa un metodo `fit()` che prende in input un dataframe e ritorna in output un `Model` (modello). Il modello è invece un Transformer (vedasi `MultilayerPerceptronClassificationModel`). 



## Cosa è una Pipeline?

Una Pipeline è una sequenza di stage (`PipelineStage`), ovvero `Transformer` ed `Estimator` combinati in sequenza. Nell'immagine sottostante abbiamo un esempio di Pipeline che, partendo da un testo, implementa 3 stage: 

* Tokenization (transformer): divide il testo in token (parole).
* HashingTF (transformer): trasforma le parole in feature vectors.
* LogisticRegression (Estimator): attraverso i dati stima i parametri di un modello di regressione logistica.

Andando a chiamare `Pipeline.fit(dataframe)` otterremo un `PipelineModel`, in cui i parametri del modello sono calcolati.



![ML Pipeline Example](readme.assets/ml-Pipeline.png)



## Let's code!

Installate i requirements tramite il comando: 

```bash
pip install -r requirements.txt
```

Tirate su il cluster Spark:

```bash
docker-compose up -d
```

Leggete e lanciate gli script:

```python
examples/
├── data/										# cartella contenente il dataset Titanic
├── model/										# cartella in cui persistiamo il modello allenato
├── titanic_survival_prediction.py				# esempio didattico 
├── titanic_survival_prediction_pipeline.py		# esempio reale di pipeline e salvataggio del modello
└── titanic_survival_prediction_load.py			# esempio di caricamento del modello per l'utilizzo
```



## Credits

* [MLLIB example with titanic data](https://towardsdatascience.com/your-first-apache-spark-ml-model-d2bb82b599dd)
* [Save and load a MLLib Model](https://stackoverflow.com/questions/34270427/how-to-save-and-load-mllib-model-in-apache-spark)
* [MLLib official documentation](https://spark.apache.org/docs/latest/ml-guide.html)
* [Titanic Dataset](https://www.kaggle.com/competitions/titanic/data)

## Give a look
* [Transfer Learning - PySpark](https://github.com/innat/Transfer-Learning-PySpark)