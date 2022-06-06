import logging
import random
import time

import requests
from flask import Flask
import os
from flask import request


LOCAL_STORAGE = {}
app = Flask('secondary')


@app.route('/secondary', methods=['GET', 'POST'])
def secondary_app():
    if request.method == 'POST':
        rnd = random.randint(3, 12)
        app.logger.info(f'Sleep time: {rnd}')
        time.sleep(rnd)
        try:
            if request.is_json:
                LOCAL_STORAGE[list(request.json.keys())[0]] = list(request.json.values())[0]
        except Exception as e:
            raise e
        else:
            return 'stored'

    elif request.method == 'GET':
        try:
            messages = list(LOCAL_STORAGE.values())
        except Exception as e:
            raise e
        else:
            return '\t'.join(messages)


if __name__ == '__main__':
    app.logger.setLevel(logging.INFO)
    if not os.environ.get("master"):
        os.environ["master"] = "localhost"
    requests.request('LINK', f'http://{os.environ.get("master")}:5000/register')
    app.run(host='0.0.0.0', port=8000)