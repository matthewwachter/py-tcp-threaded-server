import json
import socket

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 8008)
sock.connect(server_address)

# Create the data and load it into json
data = {
	'cmd': 'test',
	'data': ['foo', 'bar'],
}
msg = json.dumps(data)

# Send the message
sock.sendall(msg.encode('utf-8'))
