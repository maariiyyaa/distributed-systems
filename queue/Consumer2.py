from hazelcast.client import HazelcastClient
import time

client = HazelcastClient()
queue = client.get_queue("my-distributed-queue")

while True:
    item = queue.take().result()
    print("Consumer 2: item - ", item)
    if item == -1:
        print("End of the queue: ", item)
        break
    time.sleep(0.5)
client.shutdown()