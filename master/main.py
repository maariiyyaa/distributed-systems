import time
import uuid
import logging

from multiprocessing.dummy import Pool
import requests
from flask import Flask
from flask import request

LOCAL_STORAGE = {}
SECONDARIES = []
app = Flask('master')


@app.route('/master', methods=['GET', 'POST'])
def master_app():
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
                return 'No replicas'
            else:
                app.logger.info('Requests sent')
                pool = Pool(10)
                futures = [pool.apply_async(requests.post,
                                         [f"http://{secondary}/secondary"],
                                         kwds={'json': {str(mess_id): message}, 'timeout': 500}
                                         ) for secondary in SECONDARIES]

                while sum([i.get().status_code == 200 for i in futures if hasattr(i, '_success')]) < write_concern - 1:
                    time.sleep(1)
                return f'Stored to local and {write_concern - 1} replicas'

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
