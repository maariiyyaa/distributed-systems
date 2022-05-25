from hazelcast.client import HazelcastClient

# Connect to Hazelcast cluster.
client = HazelcastClient()

distributed_map = client.get_map("distributed-map_masha").blocking()
distributed_map.clear()

distributed_map.put_all({str(key): f"value_{key}" for key in range(1, 1001)})

# the get request below is non-blocking.
get_future = distributed_map.get("666")
get_future.add_done_callback(lambda future: print(future.result()))

print("\nMap size:", distributed_map.size().result())

# Shutdown the client.
client.shutdown()