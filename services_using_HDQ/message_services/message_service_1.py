from flask import Flask
from hazelcast import HazelcastClient
from flask import request
import json
import time

app = Flask('message-service')
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
        print("Consumer 1: item - ", item)


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
    with open("../../configs/ports.json", 'r') as file:
        ports = json.load(file)
    client = HazelcastClient()
    queue = client.get_queue("msg-queue").blocking()
    app.run(port=ports['message1'], )
    client.shutdown()