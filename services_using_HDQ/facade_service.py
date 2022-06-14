from flask import Flask
from hazelcast import HazelcastClient
from flask import request
import uuid
import requests
import json
from random import choice

import consul_functions.consul_functions as cf


app = Flask('facade-service')


def post_to_logging(message):
    """
    send the message to the logging service
    :param message: a message that will be sent to the logging service
    :return: response message
    """
    _id = uuid.uuid4().hex
    _choice = choice(['logging-service1', 'logging-service2', 'logging-service3'])
    print(f"{message} --> {_choice}")
    host, port = cf.get_service_params(service_name=_choice)
    resp = requests.post(f"http://{host}:{port}/logging", json={str(_id): message})
    if resp.status_code == 200:
        return f'message {json.dumps({str(_id): message})} delivered to ' \
               f'{_choice} \n{resp.content.decode("utf-8")}'
    else:
        return resp.status_code


def produce_to_HDQ(queue, message):
    """
    Put the message to the queue
    :param queue: Queue object
    :param message: a message that will be sent to the queue
    :return: response message
    """
    try:
        queue.put(message)
    except Exception as e:
        raise e
    else:
        return f"message '{message}' is sent HDQ!"


def get_response(service, ):
    """
    Send GET request to a service
    :param service: name of the service which will receive GET request
    :return: GET response data and a service number
    """
    if service == "logging":
        service_name = 'logging-service'
        _choice = choice(['logging1', 'logging2', 'logging3'])
    elif service == "message":
        service_name = 'message-service'
        _choice = choice(['message1', 'message2'])
    else:
        raise "invalid service. Use 'logging' or 'message'."
    host, port = cf.get_service_params(service_name=service_name, service_id=_choice)
    resp = requests.get(f"http://{host}:{port}/{service}")
    if resp.status_code == 200:
        return resp.content.decode("utf-8"), _choice


@app.route('/')
def go_to():
    """
    The main page of the app.
    :return: web page link
    """
    return '<a href=/facade> Go to App </a>'


@app.route('/facade', methods=['GET', 'POST'])
def facade_app():
    """
    The app page from where the POST/GET request can be sent.
    :return: string - POST or GET response results
    """
    if request.method == 'POST':
        message = request.data.decode("utf-8")
        resp1 = post_to_logging(message)
        resp2 = produce_to_HDQ(queue, message)
        return '\n'.join([resp1, resp2])
    elif request.method == 'GET':
        log_content, log_service = get_response(service="logging")
        msg_content, msg_service = get_response(service="message")
        resp1 = f"response from {log_service}:  " + log_content
        resp2 = f"response from service {msg_service}:  " + msg_content
        return '\n'.join([str(resp1), str(resp2)])


if __name__ == '__main__':
    ports = cf.get_kv("ports")
    client = HazelcastClient()
    queue = client.get_queue(cf.get_kv("hz_queue")["name"]).blocking()
    queue.clear()
    cf.register_service(name="facade-service", host="localhost", port=ports['facade'])
    app.run(port=ports['facade'])
    client.shutdown()
