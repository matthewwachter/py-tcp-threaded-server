# TCP_ThreadedServer

Here's an example of a threaded socket server for Python 3. This server uses the built in python threading module by creating an instance of a class (ThreadedServer) that inherits from threading.Thread. This allows the server to be run in the background.

Messages sent to the server should be a json dictionary that follows this format:

```python
	{
		'cmd': 'some_command_name',
		'data': 'some_data'
	}
```

Here's an example of a script sends a test message to the server (testSend.py):

```python
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
```

Here's another example of a script that sends a message and waits for a response from the server (testSendReceive.py):

```python
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

	# Receive the message back
	res = sock.recv(1024).decode('utf-8')
	data = json.loads(res)
	print(data)
```