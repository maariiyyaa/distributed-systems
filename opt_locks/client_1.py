from hazelcast.client import HazelcastClient
import time

class Value:
    def __init__(self,):
        self.amount = 0

    def __add__(self, value):
        self.amount = self.amount + value
        return self

    def __eq__(self, other):
        if isinstance(other, self):
            if self.amount == other.amount:
                return True
            else:
                return False
        else:
            return False



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
    while True:
        value = distributed_map.get(key).result()
        time.sleep(1)
        value_new = Value()
        value_new.amount = value.amount + 1
        if distributed_map.replace_if_same(key, value, value_new).result():
            break
print(f"Finished! Result = {value_new.amount}")
# Shutdown the client.
client.shutdown()