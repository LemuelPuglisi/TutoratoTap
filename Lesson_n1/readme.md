# Docker & Docker-compose 

Docker fornisce un modo consistente per sviluppare, confezionare (packaging) e mettere in produzione (deploy) un'applicazione su quasi tutte le piattaforme. Docker aiuta a sviluppare una applicazione in modo **agnostico** rispetto al tipo di piattaforma sottostante. 

## Virtual machines vs Docker 

Sia le virtual machine che i container hanno come obiettivo l'isolamento delle risorse. Tuttavia Docker vince sul mercato grazie alla sua natura semplice e "lightweight". 

| VM                                                           | Docker                                                       |
| :----------------------------------------------------------- | :----------------------------------------------------------- |
| Utilizza un Hypervisor sulla macchina host per gestire le macchine virtuali. | Utilizza il Docker Engine per eseguire le immagini in processi isolati, ovvero dei docker container. |
| Un'intera copia del sistema operativo (ospitato) è installata "on top" sul sistema operativo dell'host. | L'applicazione necessita solo delle librerie da cui dipende. |
| Pesante (per il motivo sopracitato)                          | Leggero e potente allo stesso tempo                          |
| Difficile da monitorare                                      | Facile da gestire. Un container viene seguito in qualche secondo. |

Per maggiori informazioni su perche usare docker, [cliccate qui](https://jstobigdata.com/docker-introduction/). 


## Docker architecture

* Il **docker daemon** è il processo eseguito in background che gestisce il tutto ed espone API REST con cui comunicare. 
* Il **docker client** (Docker CLI) è un programma che permette all'utente di interagire con il docker deamon.
* Una **docker registry** è un grande repository dove vengono conservate le immagini (es. [Docker hub](https://hub.docker.com/)), potete "pullare" le immagini dai registry.
* Una **immagine docker** è un template read-only che contiene le istruzioni da fornire a Docker per creare un container. 
* Un **container docker** è una istanza eseguibile di una immagine docker. Viene eseguito in un processo isolato, ma può comunicare con altri servizi in vari modi. 
* Il **docker host** è la macchina in cui è installato Docker. 

![docker architecture](https://docs.docker.com/engine/images/architecture.svg)


## Installazione di Docker 

Per installare Docker, [seguite questo indice](https://jstobigdata.com/docker-installation/) ed installate preferibilmente la versione `stable`. I link nell'indice rimandano alla documentazione ufficiale.


## Dockefile guidelines 

* Impareremo a creare un'immagine Docker attraverso un Dockerfile
* Il Dockerfile contiene le istruzioni per creare l'immagine
* Attraverso l'istruzione `docker build` si crea l'immagine dal Dockerfile
* La cartella in cui buildiamo l'immagine è chiamata **context**
* Dai logs della build possiamo osservare vari **step**
* Dato che l'immagine viene costruita a strati, ogni step è un'immagine intermedia
* Il sistema di caching utilizza le immagini intermedie per velocizzare il processo 


Il file `NonLayeredExample.Dockerfile` contiene il primo esempio.

Best practice: 

* Disporre i pacchetti da installare in ordine alfabetico
* Iniziare il Dockerfile con step che con molta probabilità non cambieranno
* Minimizzare il numero di step
* Utilizzare il .dockerignore per escludere file/cartelle dal context
* Un container dovrebbe avere una sola responsabilità

## Examples 

Simple Logger 

```bash
docker build --tag tap-simple-logger -f Dockerfile.Logger . 
docker run --rm -it --name simple-logger tap-simple-logger  
```

Log Server
```bash
docker build --tag tap-logs-server -f Dockerfile.Server . 
docker run --rm -it -p 5000:5000 --name logs-server tap-logs-server
```

Log Server with volume
```bash
docker build --tag tap-logs-server -f Dockerfile.Server . 
docker run --rm -it -p 5000:5000 --name logs-server -v "$(pwd)"/server/logs:/app/logs  tap-logs-server
```

Remote Logger and Log Server with volume
```bash
# build & run the remote server (detached).
docker build --tag tap-logs-server -f Dockerfile.Server . 
docker run -d -p 5000:5000 --name logs-server -v "$(pwd)"/server/logs:/app/logs  tap-logs-server

# build & run the remote logger (interactive)
docker build --tag tap-remote-logger -f Dockerfile.RemoteLogger . 
docker run -it --name remote-logger tap-remote-logger

# create a network
docker network create tap-network
docker network connect tap-network logs-server
docker network connect tap-network remote-logger
```


## Link
* [⚠️ Docker cheatsheet](https://dockerlabs.collabnix.com/docker/cheatsheet/)
* [Advanced Docker Tutorial](https://jstobigdata.com/docker/advanced-docker-tutorial/)
* [Dockerfile tutorial and best practices](https://takacsmark.com/dockerfile-tutorial-by-example-dockerfile-best-practices-2018/)