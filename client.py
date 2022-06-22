import socket
import json
# Create a socket object
s = socket.socket()

# Define the port on which you want to connect
port = 8000

# connect to the server on local computer
s.connect(('127.0.0.1', port))

# receive data from the server and decoding to get the strin
json_data = ""

while True:
    try:
        json_data += s.recv(1024)
        print(json_data)
        #json.loads(json_data)
    except ValueError:
        continue
# close the connection
s.close()