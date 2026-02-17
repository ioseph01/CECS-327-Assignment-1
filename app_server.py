# Listens on another TCP port for client requests.

# Parses user queries, forwards data requests to the Data Server, ranks/filter results, and implements a cache of recent queries.

# Returns nicely formatted results to clients.

# Using an interceptor, write all the requests and replies in a log file called app_server.log

# SEARCH city=<CityName> max_price=<Integer>

#LIST

#QUIT


from collections import OrderedDict
import socket
import json
import re


class Cache:
    def __init__(self, size=10):
        self.size = size
        self.cache = OrderedDict()

    def search(self, k):
        if k in self.cache:
            self.cache.move_to_end(k)
            return self.cache[k]
        return None
    

    def insert(self, k, v):
        if k in self.cache:
            self.cache.move_to_end(k)
        elif len(self.cache) >= self.size:
            self.cache.popitem(last=False)
        self.cache[k] = v


def rank_results(results):
    return sorted(results, key=lambda x: (x['price'], -x['bedrooms']))


def send_json(socket, status, result):
    socket.sendall(json.dumps([status, result]).encode('utf-8'))


def request_data(data_socket, command, params=None):
    data_socket.sendall(json.dumps([command, params]).encode('utf-8'))
    raw = data_socket.recv(4096).decode('utf-8').strip()
    return json.loads(raw)

# Cache
cache = Cache()

# Bind app_server socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 5000))
server_socket.listen(5) # become a server socket, maximum 5 connections

client_socket, client_address = server_socket.accept()

# Connect to data socket

data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
data_socket.connect(('localhost', 6000))


while True:
    # Receive the input and clean the input
    raw_data = client_socket.recv(4096).decode('utf-8').strip()

    if not raw_data:
        break

    request = json.loads(raw_data)
    command = request[0].strip()

    # Cache check
    cache_result = cache.search(command)
    if cache_result is not None:
        # print("<<", data)
        # print("CACHE >>", cache_result)
        client_socket.sendall(json.dumps(cache_result).encode('utf-8'))
        continue

    try:
        if command == 'QUIT':
            request_data(data_socket, "QUIT")
            data_socket.send(command.encode('utf-8'))
            break

        elif command == 'LIST':
            status, result = request_data(data_socket, "RAW_LIST")
            response = [status, rank_results(result)]

        elif re.match(r"^SEARCH city=([A-Za-z]+) max_price=(\d+)$", command) is not None:
            case = re.match(r"^SEARCH city=([A-Za-z]+) max_price=(\d+)$", command)
            city = case.group(1)
            max_price = int(case.group(2))
            status, result = request_data(data_socket, "RAW_SEARCH", {"city": city, "max_price": max_price})
            response = [status, rank_results(result)]

        else:
            response = ["ERROR: Invalid command.", None] 

        cache.insert(command, response)
        client_socket.sendall(json.dumps(response).encode('utf-8'))
    
    except ValueError:
        raise RuntimeError
        
print("QUITTING")
client_socket.close()
data_socket.close()
server_socket.close()