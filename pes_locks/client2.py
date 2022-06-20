from hazelcast.client import HazelcastClient
import time

client = HazelcastClient()
distributed_map = client.get_map("map_pes").blocking()

key = "1"
distributed_map.put_if_absent(key, 0)

print("Starting")

for i in range(10):
    distributed_map.lock(key)
    try:
        value = distributed_map.get(key)
        value += 1
        distributed_map.put(key, value)
    finally:
        distributed_map.unlock(key)
time.sleep(5)
print("Finished! Result =", distributed_map.get(key))

client.shutdown()