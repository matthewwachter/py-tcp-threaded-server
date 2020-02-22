# py-tcp-threaded-server

Here's an example of a threaded socket server for Python 3. This server uses the built in python threading module by creating an instance of a class (ThreadedServer) that inherits from threading.Thread. This allows the server to be run in the background.

This might seem a bit overwhelming for such a simple task but this method is very robust, efficient, and also allows you to continue running python commands after your server has started.

Here's a version of the server that echoes the received message back to the client that sends it (tcpThreadedServer.py).

```python
from datetime import datetime
from json import loads, dumps
from pprint import pprint
import socket
from threading import Thread


class ThreadedServer(Thread):
    def __init__(self, host, port, timeout=60, debug=False):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.debug = debug
        Thread.__init__(self)

    # run by the Thread object
    def run(self):
        if self.debug:
            print(datetime.now())
            print('SERVER Starting...', '\n')

        self.listen()

    def listen(self):
        # create an instance of socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # bind the socket to its host and port
        self.sock.bind((self.host, self.port))
        if self.debug:
            print(datetime.now())
            print('SERVER Socket Bound', self.host, self.port, '\n')

        # start listening for a client
        self.sock.listen(5)
        if self.debug:
            print(datetime.now())
            print('SERVER Listening...', '\n')
        while True:
            # get the client object and address
            client, address = self.sock.accept()

            # set a timeout
            client.settimeout(self.timeout)

            if self.debug:
                print(datetime.now())
                print('CLIENT Connected:', client, '\n')

            # start a thread to listen to the client
            Thread(target=self.listenToClient, args=(client, address)).start()

            # send the client a connection message
            # res = {
            #     'cmd': 'connected',
            # }
            # response = dumps(res)
            # client.send(response.encode('utf-8'))

    def listenToClient(self, client, address):
        # set a buffer size ( could be 2048 or 4096 / power of 2 )
        size = 1024
        while True:
            try:
                # try to receive data from the client
                data = client.recv(size).decode('utf-8')
                if data:
                    data = loads(data.rstrip('\0'))
                    if self.debug:
                        print(datetime.now())
                        print('CLIENT Data Received', client)
                        print('Data:')
                        pprint(data, width=1)
                        print('\n')

                    # send a response back to the client
                    res = {
                        'cmd': data['cmd'],
                        'data': data['data']
                    }

                    response = dumps(res)
                    client.send(response.encode('utf-8'))
                else:
                    raise error('Client disconnected')

            except:
                if self.debug:
                    print(datetime.now())
                    print('CLIENT Disconnected:', client, '\n')
                client.close()
                return False


if __name__ == "__main__":
    ThreadedServer('127.0.0.1', 8008, timeout=86400, debug=True).start()
```

For this particular setup, messages sent to the server should be a json dictionary that follows this format:

```json
	{
		"cmd": "some_command_name",
		"data": "some_data"
	}
```
Typically 'cmd' would always be a string and 'data' could be anything json-able like a str, list, or dict. This message format isn't necessary for the server to work but is provided as a foundation to build your client/server interaction from. 


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

Another threaded server example that includes a callback function:

```python
from datetime import datetime
from json import loads, dumps
from pprint import pprint
import socket
from threading import Thread


class ThreadedServer(Thread):
    def __init__(self, host, port, timeout=60, callback=None, debug=False):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.callback = callback
        self.debug = debug
        Thread.__init__(self)

    # run by the Thread object
    def run(self):
        if self.debug:
            print(datetime.now())
            print('SERVER Starting...', '\n')

        self.listen()

    def listen(self):
        # create an instance of socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # bind the socket to its host and port
        self.sock.bind((self.host, self.port))
        if self.debug:
            print(datetime.now())
            print('SERVER Socket Bound', self.host, self.port, '\n')

        # start listening for a client
        self.sock.listen(5)
        if self.debug:
            print(datetime.now())
            print('SERVER Listening...', '\n')
        while True:
            # get the client object and address
            client, address = self.sock.accept()

            # set a timeout
            client.settimeout(self.timeout)

            if self.debug:
                print(datetime.now())
                print('CLIENT Connected:', client, '\n')

            # start a thread to listen to the client
            Thread(
                target=self.listenToClient,
                args=(client, address, self.callback)
            ).start()

            # send the client a connection message
            # res = {
            #     'cmd': 'connected',
            # }
            # response = dumps(res)
            # client.send(response.encode('utf-8'))

    def listenToClient(self, client, address, callback):
        # set a buffer size ( could be 2048 or 4096 / power of 2 )
        size = 1024
        while True:
            try:
                # try to receive data from the client
                data = client.recv(size).decode('utf-8')
                if data:
                    data = loads(data.rstrip('\0'))
                    if self.debug:
                        print(datetime.now())
                        print('CLIENT Data Received', client)
                        print('Data:')
                        pprint(data, width=1)
                        print('\n')

                    if callback is not None:
                        callback(client, address, data)

                else:
                    raise error('Client disconnected')

            except:
                if self.debug:
                    print(datetime.now())
                    print('CLIENT Disconnected:', client, '\n')
                client.close()
                return False


def some_callback(client, address, data):
    print('data received', data)
    # send a response back to the client

    res = {
        'cmd': data['cmd'],
        'data': data['data']
    }
    response = dumps(res)
    client.send(response.encode('utf-8'))


if __name__ == "__main__":
    ThreadedServer('127.0.0.1', 8008, timeout=86400, callback=some_callback, debug=True).start()

```
