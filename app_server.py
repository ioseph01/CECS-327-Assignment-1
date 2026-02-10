# Listens on another TCP port for client requests.

# Parses user queries, forwards data requests to the Data Server, ranks/filter results, and implements a cache of recent queries.

# Returns nicely formatted results to clients.

# Using an interceptor, write all the requests and replies in a log file called app_server.log


import socket

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('localhost', 5000))
serversocket.listen(5) # become a server socket, maximum 5 connections

connection, address = serversocket.accept()

buffer = ''

while True:
    data = connection.recv(64)
    if not data:
        break

    buffer += data.decode('utf-8')

    while '\n' in buffer:
        message, buffer = buffer.split('\n', 1)
        print(message)

        if message == 'break':
            break
        
connection.close()
serversocket.close()