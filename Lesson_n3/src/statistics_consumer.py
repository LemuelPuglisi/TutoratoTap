""" The statistics consumer analyze the arriving 
    order and payments and create a dictionary containing 
    the dishes as keys, and their count / total profit as 
    values. 
"""

import json
import confluent_kafka as ck 

from time import sleep


conf = {
    'bootstrap.servers': 'localhost:9092', 
    'group.id': 'statistics.app', 
    'auto.offset.reset': 'smallest'
}


class DishesTotalProfit:

    def __init__(self):
        self.dishes_infos = {}
        
    def process_order_event(self, message: ck.Message):
        order = self._from_message(message)
        dish = order.get('dish')
        dish_info = self.dishes_infos.setdefault(dish, {'count': 1, 'profit': 0.})
        self.dishes_infos[dish]['count'] = dish_info.get('count') + 1

    def process_payment_event(self, message: ck.Message):
        payment = self._from_message(message)
        dish = payment.get('dish')
        amount = float(payment.get('amount'))
        dish_info = self.dishes_infos.setdefault(dish, {'count': 0, 'profit': 0.})
        self.dishes_infos[dish]['profit'] = dish_info.get('profit') + amount

    def _from_message(self, message: ck.Message):
        """ Converts the message payload from bytes to JSON 
        """
        payload = message.value().decode('utf-8')
        return json.loads(payload)

    def print_statistics(self):
        print('-'*50)
        for dish, dish_info in self.dishes_infos.items():
            count = dish_info['count'] if 'count' in dish_info else 0
            profit = dish_info['profit'] if 'profit' in dish_info else 0
            print(f"{dish}\t count: {count}\t profit: {profit}")
        print('-'*50)


if __name__ == '__main__':
    dtp = DishesTotalProfit()
    consumer = ck.Consumer(conf)
    topics = ['orders', 'payments']
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
                if msg.topic() == 'orders': 
                    dtp.process_order_event(msg)
                elif msg.topic() == 'payments': 
                    dtp.process_payment_event(msg)
                else: 
                    print(f'funknown topic \'{msg.topic()}\'')
                dtp.print_statistics()
            sleep(1.5)
    finally:
        consumer.close()
