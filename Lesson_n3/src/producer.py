import socket
import random
import json
import confluent_kafka as ck

conf = {
    'bootstrap.servers': 'localhost:9092', 
    'client.id': socket.gethostname()
}


def notify_ack(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). 
    """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))


if __name__ == '__main__': 

    producer = ck.Producer(conf)

    menu = {
        'burger':  5., # € 
        'pizza':   6., # €
        'kebab':   4.  # €
    }

    for order_idx in range(10):   
        dish = random.choice(list(menu.keys()))
        price = str(menu.get(dish))
        key = str(order_idx)

        order = {
            "user": "Tony", 
            "order": order_idx,
            "Address": "Central Ave Street, 23A, Compton", 
            "dish": dish, 
        }

        payment = {
            "user": "Tony", 
            "order": order_idx,
            "amount": price, 
            "dish": dish
        }        

        json_order = json.dumps(order)
        json_payment = json.dumps(payment)
        producer.produce('orders', key=key, value=json_order, callback=notify_ack)
        producer.produce('payments', key=key, value=json_payment, callback=notify_ack)

    producer.flush() 