# Listens on another TCP port for client requests.

# Parses user queries, forwards data requests to the Data Server, ranks/filter results, and implements a cache of recent queries.

# Returns nicely formatted results to clients.

# Using an interceptor, write all the requests and replies in a log file called app_server.log

# SEARCH city=<CityName> max_price=<Integer>

#LIST

#QUIT


from collections import OrderedDict
import socket
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
    data = client_socket.recv(1024).decode('utf-8').strip()
    if not data:
        break

    # Cache check
    cache_result = cache.search(data)
    if cache_result is not None:
        # print("<<", data)
        # print("CACHE >>", cache_result)
        client_socket.sendall(str(cache_result).encode('utf-8'))
        continue

    try:
        if data == 'QUIT':
            data_socket.send(data.encode('utf-8'))
            break
        elif data == 'LIST':
            data_socket.send("RAW_LIST".encode('utf-8'))
        elif re.match(r"^SEARCH city=([A-Za-z]+) max_price=(\d+)$", data) is not None:
            data_socket.send(("RAW_"+data).encode('utf-8'))
        else:
            client_socket.send("Error: Invalid Command".encode('utf-8'))   
            continue

        # num = int(data)
        # result = num * 2
        # print("<<", num)
        # print(">>", result)



        returned_result = data_socket.recv(1024).decode('utf-8').strip()
        # print("<<", returned_result)
        # print(">>", returned_result)

        cache.insert(str(data), returned_result)
        client_socket.send(returned_result.encode('utf-8'))
    
    except ValueError:
        client_socket.send("Error: Bad Request".encode('utf-8'))
        
print("QUITTING")
client_socket.close()
data_socket.close()
server_socket.close()