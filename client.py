# Command-line interface where a user can:
# 
    # search by city and max_price,
# 
    # list all available listings,
# 
    # exit.
# 


import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 5000))

while True:
    cmd = input("Say something.. ").strip('/n')
    print("<<", cmd)
    print(cmd, ">>")
    client_socket.send(cmd.encode('utf-8'))

    response = client_socket.recv(1024).decode('utf-8').strip()
    print("<<", response)

    if cmd == 'quit':
        break

print("QUITTING")
client_socket.close()