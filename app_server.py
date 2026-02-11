# Listens on another TCP port for client requests.

# Parses user queries, forwards data requests to the Data Server, ranks/filter results, and implements a cache of recent queries.

# Returns nicely formatted results to clients.

# Using an interceptor, write all the requests and replies in a log file called app_server.log

from collections import OrderedDict
import socket


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


def clean_input(cmd):
    return cmd.strip().lower()

cache = Cache()

# Bind server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 5000))
server_socket.listen(5) # become a server socket, maximum 5 connections

client_socket, client_address = server_socket.accept()

data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
data_socket.connect(('localhost', 6000))



while True:
    data = client_socket.recv(1024).decode('utf-8').strip()
    data = clean_input(data)
    if not data:
        break

    cache_result = cache.search(data)
    if cache_result is not None:
        print("<<", data)
        print("CACHE >>", cache_result)
        client_socket.sendall(str(cache_result).encode('utf-8'))
        continue

    try:
        if data == 'quit':
            data_socket.send("quit".encode('utf-8'))
            break

        num = int(data)
        result = num * 2
        print("<<", num)
        print(">>", result)


        data_socket.send(str(result).encode('utf-8'))

        returned_result = data_socket.recv(1024).decode('utf-8').strip()
        print("<<", returned_result)
        print(">>", returned_result)

        cache.insert(str(data), result)
        client_socket.send(returned_result.encode('utf-8'))
    
    except ValueError:
        client_socket.send("Error: Bad Request".encode('utf-8'))
        
print("QUITTING")
client_socket.close()
data_socket.close()
server_socket.close()