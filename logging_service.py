from flask import Flask
from flask import request
from functools import reduce
import json

app = Flask('logging-service')

LOCAL_STORAGE = {}

@app.route('/')
def go_to():
    return '<a href=/logging> Go to App </a>'

@app.route('/logging', methods=['POST', 'GET'])
def logging_app():
    if request.method == 'POST':
        # print(request.json)
        LOCAL_STORAGE[list(request.json.keys())[0]] = list(request.json.values())[0]
        return "delivered"
    if request.method == 'GET':
        # print(list(LOCAL_STORAGE.values()))
        return reduce(lambda x, y: str(x) + ' / ' + str(y), list(LOCAL_STORAGE.values()))

if __name__ == '__main__':
    with open("configs/ports.json", 'r') as file:
        ports = json.load(file)
    app.run(port=ports['logging'])