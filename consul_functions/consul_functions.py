from consul import Consul
import json


def put_kv(key, value):
    """
    Puts key-value to Consul kv
    :param key:
    :param value:
    :return: Null
    """
    try:
        c = Consul()
        c.kv.put(key, str(value))
    except Exception as e:
        raise e
    else:
        print("kv is put to consul")


def get_kv(key):
    """
    Gets a value from Consul kv by key
    :param key: key of the value
    :return: value
    """
    try:
        c = Consul()
        response = c.kv.get(key)
        value = response[1]["Value"].decode('utf-8')
        try:
            value = json.loads(value)
        except ValueError as e:
            pass
        return value
    except Exception as e:
        raise e


def register_service(name, host, port, service_id=None):
    """
    Registers a service to Consul
    :param name: service name
    :param host: service Address
    :param port: service port
    :param service_id: service id
    :return: None
    """
    try:
        c = Consul()
        c.agent.service.register(name=name, service_id=service_id, address=host, port=port)
    except Exception as e:
        raise e
    else:
        print(f"service {name} registered")


def get_service_params(service_name):
    """
    Gets host and port of registered service
    :param service_name: name of the service
    :return: tuple of (host, port)
    """
    try:
        c = Consul()
        response = c.catalog.service(service_name)
        host = response[1][0]["ServiceAddress"]
        port = response[1][0]["ServicePort"]
        return host, port
    except Exception as e:
        raise e


