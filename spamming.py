import requests

for step in range(10):
    resp = requests.post(f"http://localhost:8090/facade", data=f"msg_{step}")
    if resp.status_code ==200:
        print(resp.content.decode('utf-8'))
        continue
    else:
        raise Exception(f"message {step} in not sent")