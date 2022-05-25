from hazelcast.client import HazelcastClient
import time

client = HazelcastClient()
queue = client.get_queue("my-distributed-queue").blocking()
queue.clear()

for k in range(20):
    print(f"Put item_{k}")
    queue.put(f"item_{k}")
    time.sleep(0.25)
queue.put(-1)
queue.put(-1)

client.shutdown()