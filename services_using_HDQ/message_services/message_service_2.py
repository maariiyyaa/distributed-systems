from flask import Flask
from hazelcast import HazelcastClient
from flask import request
import json
import time

import consul_functions.consul_functions as cf


app = Flask('message-service2')
LOCAL_STORAGE = []

def consume_from_HDQ(queue):
    """
    Takes all available data from queue and store to local storage
    :param queue: Queue object
    :param sleep: seconds
    :return: Null
    """
    while True:
        if queue.is_empty():
            print("queue is empty")
        item = queue.take()
        time.sleep(1)
        LOCAL_STORAGE.append(item)
        print("Consumer 2: item - ", item)


@app.route('/')
def go_to():
    """
    The main page of the app. Open it in browser and data consuming will start
    :return: web page link
    """
    consume_from_HDQ(queue)
    return '<a href=/message> Go to App </a>'

@app.route('/message', methods=['GET'])
def message_app():
    """
    The app page from where the GET request can be sent.
    :return: string - GET response result
    """
    if request.method == 'GET':
        return ' / '.join(LOCAL_STORAGE)
    else:
        raise Exception('method not implemented')

if __name__ == '__main__':
    ports = cf.get_kv("ports")
    client = HazelcastClient()
    queue = client.get_queue(cf.get_kv("hz_queue")["name"]).blocking()
    cf.register_service(name="message-service", host="localhost", port=ports['message2'], service_id="message2")
    app.run(host='localhost', port=ports['message2'])
    client.shutdown()