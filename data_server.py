# Listens on a TCP port.
#
# Manages a small housing “database” stored in a local JSON file.
#
# Supports simple commands from the Application Server (e.g., “LIST”, “SEARCH city=LongBeach max_price=2500”).


import socket
import json

DATA = json.load(open('listings.json'))

def RAW_LIST():
  return DATA


def RAW_SEARCH(city, max_price):
  # Filter by city and price
  return [entry for entry in DATA if entry['city'].lower() == city.lower() and entry['price'] <= max_price]


def ERROR_HANDLER():
  return 'Error: Bad Request'

data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
data_socket.bind(('localhost', 6000))  
data_socket.listen(1)

connection, address = data_socket.accept()

while True:    
    
    # Convert the received data to an integer and add 1
    try:
        # Receive data from the server
        data = connection.recv(1024).decode('utf-8').strip()
        
        if not data:
            break  # Exit if no data is received
        

        if data == 'quit':
           print("QUITTING?")
           break
        num = int(data)
        result = num + 1
        print("<<", num)
        print(">>", result)
        connection.send(str(result).encode('utf-8'))  # Send the result back to the server
    except ValueError:
        connection.send("Error: Bad Request.".encode('utf-8'))
        raise ValueError
    
    except ConnectionResetError:
       break

# Close the connection
print("QUITTING")
connection.close()
data_socket.close()