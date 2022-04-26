""" Delivery consumer prints the delivery informations.
"""

import json
import confluent_kafka as ck 

from time import sleep


conf = {
    'bootstrap.servers': 'localhost:9092', 
    'group.id': 'delivery.app', 
    'auto.offset.reset': 'smallest'
}


class Delivery:

    def from_message(msg: ck.Message):
        payload = msg.value().decode('utf-8')
        order = json.loads(payload)
        delivery = Delivery()
        delivery.dish = order.get('dish')
        delivery.user = order.get('user')
        delivery.address = order.get('Address')
        delivery.order = order.get('order')
        return delivery

    def __str__(self):
        return (f'[ord: {self.order}] User {self.user} ordered {self.dish} '
                f'to deliver at {self.address}')


if __name__ == '__main__':
    consumer = ck.Consumer(conf)
    topics = ['orders']
    running = True

    try: 
        consumer.subscribe(topics)
        while running:
            print('Iteration started.\nFetching a message...')
            msg = consumer.poll(timeout=1.0)
            if msg is None: 
                print('no messages.')
                continue
            if msg.error():
                if msg.error().code() == ck.KafkaError._PARTITION_EOF:
                    print(f"{msg.topic()} [{msg.partition()}] reached end at offset {msg.offset()}\n")
                elif msg.error():
                    raise ck.KafkaException(msg.error())
            else:
                delivery = Delivery.from_message(msg)
                print(delivery)
            sleep(1.5)
    finally:
        consumer.close()
