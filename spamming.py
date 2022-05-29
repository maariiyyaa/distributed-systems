import requests


def send_msg(msg):
    resp = requests.post(f"http://localhost:8090/facade", data=msg)
    if resp.status_code == 200:
        print(resp.content.decode('utf-8'))
    else:
        raise Exception(f"message {step} in not sent")


for step in range(10):
    send_msg(f"msg_{step}")



