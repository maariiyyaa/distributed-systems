from hazelcast.client import HazelcastClient
import time


key = "1"
# Connect to Hazelcast cluster.
client = HazelcastClient()
distributed_map = client.get_map("map_1")

distributed_map.put_if_absent(key, 0)
print("Starting")
for k in range(0, 10):
    if k % 5 == 0:
        print(f"At {k}")
    value = distributed_map.get(key).result()
    print(value)
    value = value + 1
    distributed_map.put(key, value)

print(f"Finished! Result = {distributed_map.get(key).result()}")
# Shutdown the client.
client.shutdown()