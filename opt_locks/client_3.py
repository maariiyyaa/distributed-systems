from hazelcast.client import HazelcastClient
import time

client = HazelcastClient()
distributed_map = client.get_map("map_opt").blocking()

key = "1"
distributed_map.put_if_absent(key, 0)

print("Starting")

for k in range(10):
    while True:
        value = distributed_map.get(key)
        value_new = value + 1
        res = distributed_map.replace_if_same(key, value, value_new)
        if res:
            time.sleep(2)
            break

time.sleep(5)
print("Finished! Result =", distributed_map.get(key))

client.shutdown()
