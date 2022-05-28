from flask import Flask
from kafka import KafkaConsumer
from flask import request
import json

app = Flask('message-service')
LOCAL_STORAGE = []

def consume_from_kafka():
    """
    Consumes all available data from kafka topic and store to local storage
    :return: Null
    """
    consumerp = consumer.poll(timeout_ms=100, max_records=20)
    for item in  consumerp.values():
        for record in item:
            print(record.value)
            value = record.value
            if isinstance(value, bytes):
                value = value.decode()
                LOCAL_STORAGE.append(value)

@app.route('/')
def go_to():
    """
    The main page of the app. Open it in browser and data consuming will start
    :return: web page link
    """
    return '<a href=/message> Go to App </a>'

@app.route('/message', methods=['GET'])
def message_app():
    """
    The app page from where the GET request can be sent.
    :return: string - GET response result
    """
    if request.method == 'GET':
        consume_from_kafka()
        return ' / '.join(LOCAL_STORAGE)
    else:
        raise Exception('method not implemented')

if __name__ == '__main__':
    with open("../../configs/ports.json", 'r') as file:
        ports = json.load(file)
    with open("../../configs/kafka.json", 'r') as file:
        kafka_conf = json.load(file)
    consumer = KafkaConsumer(kafka_conf['topic'],
                             bootstrap_servers=kafka_conf['bootstraps'],
                             auto_offset_reset='latest',
                             )
    app.run(port=ports['message1'])