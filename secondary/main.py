import json
import logging
import random
import time

import requests
from flask import Flask
import os
from flask import request


LOCAL_STORAGE = {}
app = Flask('secondary')

@app.route('/health', methods=['GET'])
def healthcheck_app() -> str:
    return "healthy"


@app.route('/secondary', methods=['GET', 'POST'])
def secondary_app() -> str:
    """
    Main secondary application.
    on POST - takes a message from master and puts to the local storage
    on GET - return all meaasges from local storage to client
    :return: response message
    """
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
    """
    Register the secondary in master and replicate messages from master
    """
    app.logger.setLevel(logging.INFO)
    if not os.environ.get("master"):
        os.environ["master"] = "localhost"
    diff = requests.request('LINK',
                            f'http://{os.environ.get("master")}:5000/register',
                            json=LOCAL_STORAGE
                        ).json()
    LOCAL_STORAGE = {**LOCAL_STORAGE, **diff}
    app.logger.info(f'LOCAL STORAGE contains {LOCAL_STORAGE}')
    app.run(host='0.0.0.0', port=8000)