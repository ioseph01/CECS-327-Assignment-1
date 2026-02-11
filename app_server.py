# Listens on another TCP port for client requests.

# Parses user queries, forwards data requests to the Data Server, ranks/filter results, and implements a cache of recent queries.

# Returns nicely formatted results to clients.

# Using an interceptor, write all the requests and replies in a log file called app_server.log


import socket


def check_cache(cmd):
    pass


def rank_results(results):
    return sorted(results, key=lambda x: (x['price'], -x['bedrooms']))



# Bind server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 5000))
server_socket.listen(5) # become a server socket, maximum 5 connections

client_socket, client_address = server_socket.accept()

data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
data_socket.connect(('localhost', 6000))



while True:
    data = client_socket.recv(1024).decode('utf-8').strip()
    if not data:
        break


    try:
        if data == 'quit':
            data_socket.send(str(result).encode('utf-8'))
            break
        num = int(data)
        result = num * 2
        print("<<", num)
        print(">>", result)


        data_socket.send(str(result).encode('utf-8'))

        returned_result = data_socket.recv(1024).decode('utf-8').strip()
        print("<<", returned_result)
        print(">>")

        client_socket.send(returned_result.encode('utf-8'))
    
    except ValueError:
        client_socket.send("Error: Bad Request".encode('utf-8'))
        
print("QUITTING")
client_socket.close()
data_socket.close()
server_socket.close()