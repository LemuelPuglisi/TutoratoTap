# Spark

> Apache Spark è un motore di analisi unificato per l'elaborazione di dati su vasta scala con moduli integrati per SQL, flussi di dati, machine  learning ed elaborazione di grafici. 
>
> -- Google

Una volta installato Spark (vedremo come), andremo a scrivere un programma che analizzi un batch di dati in maniera statica. Nelle lezioni successive ci occuperemo dello streaming. Ma prima di capire come funziona Spark, vediamo la sua architettura. Le componenti di più alto livello sono 3 e sono: 

1. Lo Spark Driver
2. Il Cluster Manager
3. Gli Executors



## Il ruolo del driver

> Spark Driver - Il master node di un'applicazione Spark. 

È il punto centrale ed entry point della [Spark Shell](https://spark.apache.org/docs/latest/quick-start.html#interactive-analysis-with-the-spark-shell), un programma che permette di utilizzare le funzionalità di Spark da riga di comando.  Il driver avvia la funzione `main()` dell'applicazione da noi scritta, si occupa della creazione dello Spark Context e degli RDD, e inoltre applica le trasformazioni e azioni sugli RDD (di cui parleremo dopo). Il driver contiene molte componenti al suo interno (es. DAGScheduler, TaskScheduler, etc.) che servono a tradurre il codice utente in task eseguiti nel cluster. I task principali eseguiti dal driver sono per l'appunto due: 

1. Convertire il programma utente in task 
2. Pianificare l'esecuzione dei task con gli Executors



## Il ruolo degli executors

Un executor è un distributed agent responsabile dell'esecuzione di un task. Ogni applicazione Spark ha il proprio processo executor. Un executor permane solitamente per tutta la durata dell'applicazione Spark, questo fenomeno è chiamato **allocazione statica** degli executors. L'utente può comunque scegliere di variare il numero di executor a runtime in base al workload (carico di lavoro), in tal caso si parla di **allocazione dinamica**. Le principali funzioni svolte da un executor sono le seguenti: 

1. Eseguono il data processing e ritornano il risultato al programma driver. 
2. Leggono e scrivono dati da e su sorgenti esterne. 
3. Conservano i risultati della computazione in memoria, in cache o in memoria secondaria. 
4. Interagiscono con lo storage system. 



## Il ruolo del cluster manager

Un servizio esterno è responsabile per l'acquisizione e l'allocazione delle risorse di un cluster Spark. Possiamo utilizzare uno Standalone Cluster Manager, Hadoop YARN, Apache Mesos o Kubernetes. 



### Standalone cluster manager

Il metodo più semplice: consiste nel utilizzare un master node e più workers. Attraverso le configurazione è possibile assegnare ad ognuno di essi core di CPU e quantitativi prefissati di memoria. Il cluster manager standalone può essere deployato in due modi diversi: 

* **client mode**, il driver verrà eseguito nella macchina in cui viene lanciato lo `spark-submit`
* **cluster mode**, il driver verrà eseguito all'interno di un nodo worker. 

Un punto importante da notare sul standalone cluster manager è che di default distribuisce ogni applicazione sul numero massimo di executor.



## Astrazione 1: RDD

Gli RDD sono insiemi di dati divisi in partizioni e conservati in memoria dai nodi workers del cluster Spark. Un RDD permette due tipi di operazioni - le trasformazioni (transformation) e le azioni (actions). Possiamo vedere le trasformazioni come un mapping del dato, mentre le azioni come delle elaborazioni del dato. Gli RDD sono **immutabili**, quindi le trasformazioni generano un <u>nuovo</u> RDD a partire dal precedente. Quando una azione viene applicata ad un RDD, la richiesta viene valutata al momento (comportamento eager), mentre nelle trasformazioni è possibile adottare un comportamento lazy. 



## Astrazione 2: Directed Acyclic Graph (DAG)

Il DAG rappresenta una sequenza di calcoli eseguiti sui dati dove ogni nodo è un RDD ed un arco tra due nodi è una trasformazione. L'astrazione DAG permette di eliminare il paradigma multi-stage introdotto da Hadoop, e incrementa le performance del sistema. 





## Credits

* [Apache Spark Architecture Explained](https://www.projectpro.io/article/apache-spark-architecture-explained-in-detail/338#toc-1)
* [Mastering Apache Spark - Gitbook](https://mallikarjuna_g.gitbooks.io/spark/content/spark-overview.html)

