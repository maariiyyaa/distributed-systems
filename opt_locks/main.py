from hazelcast.client import HazelcastClient
import time

client = HazelcastClient()
distributed_map = client.get_map("map").blocking()

key = "1"
distributed_map.put_if_absent(key, 0)

print("Starting")

for k in range(20):
    if k % 5 == 0:
        print(f"At {k}")
    while True:
        value = distributed_map.get(key)
        print(value)
        time.sleep(1)
        value_new = value + 1
        res = distributed_map.replace_if_same(key, value, value_new)
        if res:
            break

time.sleep(10)
print("Finished! Result =", distributed_map.get(key))

client.shutdown()
