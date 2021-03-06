import socket
import pandas as pd
import confluent_kafka as ck

from confluent_kafka import Producer
from time import sleep

KAFKA_TOPIC = 'cardiology'
SECONDS_BETWEEN_EMIT = 1

conf = {
    'bootstrap.servers': 'broker:29092', 
    'client.id': socket.gethostname()   
}


def get_dataset():
    """ Read heart.csv and return a dataframe containing all the data.
    """
    dataset = pd.read_csv('data/heart.csv')
    dataset = dataset.drop('output', axis=1)
    return dataset


def emit_messages(producer, dataset):
    """ Emit a record to Kafka every n seconds.
    """
    for idx, row in dataset.iterrows():
        json = row.to_json()
        producer.produce(KAFKA_TOPIC, key=str(idx), value=json)
        producer.flush()
        sleep(SECONDS_BETWEEN_EMIT)        


def main():
    """ Simulate an hospital sending clinical data to an inference 
        engine.
    """
    producer = Producer(conf)
    dataset = get_dataset()
    emit_messages(producer, dataset)



if __name__ == '__main__': main()