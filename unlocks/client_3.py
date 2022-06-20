from hazelcast.client import HazelcastClient
import time


key = "1"
# Connect to Hazelcast cluster.
client = HazelcastClient()
distributed_map = client.get_map("map_unlock").blocking()

distributed_map.put_if_absent(key, 0)
print("Starting")
for k in range(0, 10):
    value = distributed_map.get(key)
    value = value + 1
    time.sleep(5)
    distributed_map.put(key, value)

time.sleep(5)
print(f"Finished! Result = {distributed_map.get(key)}")
# Shutdown the client.
client.shutdown()