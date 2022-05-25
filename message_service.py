from flask import Flask
from flask import request
import json

app = Flask('message-service')

@app.route('/')
def go_to():
    return '<a href=/message> Go to App </a>'

@app.route('/message', methods=['GET'])
def message_app():
    if request.method == 'GET':
        return "not implemented"
    else:
        raise Exception('method not implemented')

if __name__ == '__main__':
    with open("configs/ports.json", 'r') as file:
        ports = json.load(file)
    app.run(port=ports['message'])