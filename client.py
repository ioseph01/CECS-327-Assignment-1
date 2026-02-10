# Command-line interface where a user can:
# 
    # search by city and max_price,
# 
    # list all available listings,
# 
    # exit.
# 


import socket

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('localhost', 5000))
while True:
    cmd = input("Say something.. ")

    clientsocket.sendall((cmd + '\n').encode('utf-8'))

    if cmd == 'break':
        break

clientsocket.close()