# Command-line interface where a user can:
# 
    # search by city and max_price,
# 
    # list all available listings,
# 
    # exit.
# 


import socket
import json

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 5000))

while True:
    cmd = input("Enter command (LIST / SEARCH city=<City> max_price=<Int> / QUIT): ").strip()
    request = json.dumps([cmd, None])
    print("<<", cmd)
    print(cmd, ">>")
    client_socket.send(request.encode('utf-8'))
    if cmd == "QUIT":
        break

    raw_response = client_socket.recv(4096).decode('utf-8').strip()
    try:
        status, result = json.loads(raw_response)
        print(f"Server: {status}")
        if "OK RESULT" in status:
            for entry in result:
                print(f"\t{str(entry)[1:-1]}")
            print()
        
    except json.JSONDecodeError:
        print("Error: Invalid Response")

    if cmd == 'QUIT':
        break

print("QUITTING")
client_socket.close()