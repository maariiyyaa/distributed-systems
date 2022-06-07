import time
import uuid
import logging
from sys import maxsize

from multiprocessing.dummy import Pool
from typing import List, Dict, Any

import requests
from flask import Flask
from flask import request
from apscheduler.schedulers.background import BackgroundScheduler
from requests.adapters import HTTPAdapter
from urllib3 import Retry
from copy import deepcopy

LOCAL_STORAGE = {}
SECONDARIES = set()
app = Flask('master')


def health_check() -> None:
    """
    Check health of all registered secondaries.
    If one not healthy, then remove from registry
    :return: None
    """
    for i in deepcopy(SECONDARIES):
        if requests.get(f'http://{i}/health').status_code != 200:
            SECONDARIES.remove(i)


def send_replicas(hosts: List[str], mess_id, message, http) -> List:
    """
    Post messages to secondaries asynchronously
    :param hosts: secondaries addresses
    :param mess_id: message id
    :param message: message
    :param http: requests.Session() object
    :return: list of future responses
    """
    pool = Pool(10)
    futures = [pool.apply_async(http.post,
                                [f"http://{secondary}/secondary"],
                                kwds={'json': {str(mess_id): message}, 'timeout': 500}
                                ) for secondary in hosts]
    return futures


@app.route('/register', methods=['LINK'])
def register() -> Dict[Any, Any]:
    """
    Register a secondary in master send missed messages to it
    :return: messages difference
    """
    SECONDARIES.add(request.remote_addr + ':8000')
    secondary_data = request.json
    diff = {k: LOCAL_STORAGE[k] for k in set(LOCAL_STORAGE) - set(secondary_data)}
    return diff


@app.route('/master', methods=['GET', 'POST'])
def master_app() -> str:
    """
    If POST - store message in local storage, then send it to the secondaries asynchronously
    If GET - return all messages from local storage
    :return: response message
    """
    if request.method == 'POST':
        try:
            message = request.data.decode("utf-8")
            write_concern = int(request.args.get('w', 1))
            mess_id = uuid.uuid4().hex
            LOCAL_STORAGE[str(mess_id)] = message
        except Exception as e:
            raise e
        else:
            if not SECONDARIES:
                return 'Stored to local'
            else:
                app.logger.info('Requests sent')
                retry_strategy = Retry(
                    total=maxsize,
                    status_forcelist=[500],
                    method_whitelist=["POST", "GET"]
                )
                adapter = HTTPAdapter(max_retries=retry_strategy)
                http = requests.Session()
                http.mount("https://", adapter)
                http.mount("http://", adapter)
                futures = send_replicas(SECONDARIES, mess_id, message, http)
                while sum([i.get().status_code == 200 for i in futures if hasattr(i, '_success')]) < write_concern - 1:
                    time.sleep(1)
                http.close()

                return f'Stored to local and {write_concern - 1} replicas'

    elif request.method == 'GET':
        try:
            messages = list(LOCAL_STORAGE.values())
        except Exception as e:
            raise e
        else:
            return '\t'.join(messages)



if __name__ == '__main__':
    """
    Create a Background Scheduler for secondaries health check
    """
    app.logger.setLevel(logging.INFO)
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=health_check, trigger="interval", seconds=10)
    scheduler.start()
    app.run(host='0.0.0.0', port=5000)
