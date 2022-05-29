from hazelcast import HazelcastClient
from flask import Flask
from flask import request
from functools import reduce
import json

import consul_functions.consul_functions as cf

app = Flask('logging-service1')

@app.route('/')
def go_to():
    """
    The main page of the app.
    :return: web page link
    """
    return '<a href=/logging> Go to App </a>'


@app.route('/logging', methods=['POST', 'GET'])
def logging_app():
    """
    The app page from where the POST/GET request can be sent.
    :return: string - POST or GET response results
    """
    if request.method == 'POST':
        print('log1')  # to check the logging instance number
        if request.is_json:
            if not db.set(list(request.json.keys())[0], list(request.json.values())[0]).is_success():
                return "stored in Database"
            else:
                return "not stored in Database"
        else:
            return "the message is not in JSON format"
    if request.method == 'GET':
        values = db.values().result()
        return reduce(lambda x, y: str(x) + ' / ' + str(y), values if values else ['', ''])


if __name__ == '__main__':
    ports = cf.get_kv("ports")
    client = HazelcastClient()
    db = client.get_map(cf.get_kv("hz_map")["name"])
    cf.register_service(name="logging-service1", host="localhost", port=ports['logging1'])
    app.run(host="localhost", port=ports['logging1'])
    client.shutdown()