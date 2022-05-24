from flask import Flask
from flask import request
import uuid
import requests
import json

app = Flask('facade-service')

@app.route('/')
def go_to():
    return '<a href=/facade> Go to App </a>'

@app.route('/facade', methods=['GET', 'POST'])
def facade_app():
    if request.method == 'POST':
        message = request.data.decode("utf-8")
        id = uuid.uuid4().hex
        resp = requests.post(f"http://localhost:{ports['logging']}/logging", json={str(id): message})
        if resp.status_code == 200:
            return f'message {json.dumps({str(id): message})} delivered'
        else:
            return resp.status_code
    elif request.method == 'GET':
        resp1 = requests.get(f"http://localhost:{ports['logging']}/logging")
        resp2 = requests.get(f"http://localhost:{ports['message']}/message")
        if (resp1.status_code == 200) and (resp2.status_code == 200):
            resp1 = "logging response:  " + resp1.content.decode("utf-8")
            resp2 = "message:  " + resp2.content.decode("utf-8")
            return '\n'.join([str(resp1), str(resp2)])
        else:
            return f'status message app: {resp2.status_code}\tstatus logging app: {resp1.status_code}'

if __name__ == '__main__':
    with open("configs/ports.json", 'r') as file:
        ports = json.load(file)
    app.run(port=ports['facade'])