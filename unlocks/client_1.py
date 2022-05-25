from hazelcast.client import HazelcastClient
import time

class Value:
    def __init__(self,):
        self.amount = 0


key = "my_key"
value = Value()

# Connect to Hazelcast cluster.
client = HazelcastClient()
distributed_map = client.get_map("distributed-map_masha")

distributed_map.put(key, value)
print("String")
for k in range(1, 20):
    if k % 5 == 0:
        print(f"At {k}")
    value = distributed_map.get(key).result()
    time.sleep(1)
    value.amount = value.amount + 1
    distributed_map.put(key, value)
print(f"Finished! Result = {value.amount}")
# Shutdown the client.
client.shutdown()