# Listens on a TCP port.
#
# Manages a small housing “database” stored in a local JSON file.
#
# Supports simple commands from the Application Server (e.g., “LIST”, “SEARCH city=LongBeach max_price=2500”).


import socket
import json

DATA = json.load(open('listings.json'))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 6000))
server.listen(5)

