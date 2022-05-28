from datetime import datetime
from elasticsearch import Elasticsearch

ES_INDEX = 'python-messages'

if __name__ == '__main__':

    es = Elasticsearch(
        "https://localhost:9200",
        ca_certs="./certs/ca.crt",
        basic_auth=("elastic", "tutoratotap"), 
        # verify_certs=False # Potreste disabilitare i certificati 
        # ma questo è sconsigliato in ambiente di produzione. 
    )

    doc = {
        'author': 'Lemuel Puglisi', 
        'text': 'Elasticsearch is awesome', 
        'timestamp': datetime.now()
    }

    resp = es.index(index=ES_INDEX, id=1, document=doc)
    print(resp['result'])

    resp = es.get(index=ES_INDEX, id=1)
    print(resp['_source'])

    es.indices.refresh(index=ES_INDEX)

    query = {
        "match": {
            "author": "Lemuel"
        }
    }

    resp = es.search(index=ES_INDEX, query=query)
    print("Got %d Hits" % resp['hits']['total']['value'])
    for hit in resp['hits']['hits']:
        print("%(timestamp)s %(author)s: %(text)s" % hit['_source'])