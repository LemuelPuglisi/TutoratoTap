# Connecting Spark to Elasticsearch 

> The wrong way :)

Siamo tutti stanchi di specificare JAR per la versione giusta e ottenere errori di ogni genere. Mentre il professore vi ha mostrato la giusta via  scrivendo su Elasticsearch attraverso le funzioni built-in di Spark, io oggi vi mostrerò un accrocco che risparmierà vari mal di testa, nel caso abbiate perso la vostra pazienza a pochi giorni dall'esame. 

## Elasticsearch secure-by-default

Abbiamo bisogno dei certificati, è un dato di fatto. Ma effettivamente il docker-compose che vi ho fornito durante la lezione 7 li genera per voi, senza alcuno sforzo! Nello specifico, i risultati vengono depositati all'interno del volume `certs`. Quello che farò e montare il volume anche nel container spark, andando a riutilizzare i certificati generati in precedenza. 

Ma la storia non finisce qui! Per qualche motivo di sicurezza, i creatori del docker-compose hanno impostato dei permessi molto stretti nelle cartelle che contengono i certificati. Noi, *for the sake of the science*, andremo brutalmente a cambiare i permessi aggiungendo nell'ultima riga del servizio `setup` il seguente comando: 

```bash
chmod 777 -R config/certs
```

Ovviamente impostare i permessi a `777` è l'errore più grande che un programmatore possa fare :) (che vi aspettate? Che la frase continui? Siamo dei pressappochisti, penseremo dopo alla sicurezza).

Alla fine andremo ad instanziare un client `Elasticsearch` della libreria python `elasticsearch` come segue, andando a specificare i certificati: 

```python
es = Elasticsearch(
    "https://es01:9200",
    ca_certs="/app/certs/ca/ca.crt",
    basic_auth=("elastic", "tutoratotap"), 
)     
```

Abbiamo già visto qualcosa del genere nella lezione 7, ma questa volta anziché specificare `localhost` specfichiamo `es01`, che è l'hostname del servizio elasticsearch con cui comunicherà spark. 

## Sorgente dati streaming

Per non appesantire la demo, anziché fare il setup di Kafka e tirare i dati da lì, ho utilizzato un CSV che viene letto da Spark. 

```python
df = spark.readStream \
    .option('sep', ',') \
    .schema(schema) \
    .csv("/app/*.csv", header=True)
```

Ovviamente bisogna inserire i dati nel container attraverso il Dockerfile, che sarà il seguente:

```Docker
FROM jupyter/pyspark-notebook:spark-3.1.1

RUN pip3 install pyspark numpy elasticsearch

WORKDIR /app

COPY ./data .
COPY ./code .

ENTRYPOINT ["spark-submit", "--master", "local[*]", "streaming.py"]
```

## foreachBatch

L'ultimo degli accrocchi (l'accrocco padre) consiste nel processare con una funzione separata il batch che arriva attraverso `foreachBatch`

```python
df.writeStream \
    .foreachBatch(process_batch) \
    .start() \
    .awaitTermination()
```

Il dataframe si riempirà man mano dei dati che arrivano in streaming in un certo intervallo. Quando scatta la fine dell'intervallo, viene chiamata la funzione che andiamo a specificare, ovvero `process_batch`, definita come segue: 

```python
def process_batch(batch_df, batch_id):
    for idx, row in enumerate(batch_df.collect()):
        row_dict = row.asDict()
        id = f'{batch_id}-{idx}'
        resp = es.index(
            index=ES_INDEX, 
            id=id, 
            document=row_dict)
        print(resp)
```

Abbiamo già visto come funziona il client `Elasticsearch`, quindi dovreste riconoscere il funzionamento del metodo `es.index(...)`. Il resto della storia lo vedremo in aula... per qualsiasi domanda contattatemi in privato 😉