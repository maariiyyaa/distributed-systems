import time
import uuid
import logging

import requests
from flask import Flask
from flask import request

LOCAL_STORAGE = {}
SECONDARIES = []
app = Flask('master')


def post_to_secondaries(secondary, mess_id: str, message: str, retry_attempts=0):
    try:
        resp = requests.post(f"http://{secondary}/secondary", json={str(mess_id): message}, timeout=500)
    except requests.exceptions.ConnectionError as e:
        if retry_attempts >= 1:
            app.logger.warning(e.strerror)
            app.logger.warning(f'Retry sending to {secondary}')
            resp = post_to_secondaries(secondary, mess_id, message, retry_attempts - 1)
        else:
            raise e
    return resp


@app.route('/master', methods=['GET', 'POST'])
def master_app():
    if request.method == 'POST':
        try:
            message = request.data.decode("utf-8")
            mess_id = uuid.uuid4().hex
            LOCAL_STORAGE[str(mess_id)] = message
        except Exception as e:
            raise e
        else:
            if not SECONDARIES:
                return 'No replicas'
            for i in SECONDARIES:
                app.logger.info(
                    f'Delivery status to {i}: {post_to_secondaries(i, mess_id, message, retry_attempts=3).status_code}')
            return f'Stored to local and replicas {", ".join(SECONDARIES)}'

    elif request.method == 'GET':
        try:
            messages = list(LOCAL_STORAGE.values())
        except Exception as e:
            raise e
        else:
            return '\t'.join(messages)


@app.route('/register', methods=['LINK'])
def register():
    SECONDARIES.append(request.remote_addr + ':8000')
    return "True"


if __name__ == '__main__':
    app.logger.setLevel(logging.INFO)
    app.run(host='0.0.0.0', port=5000)
