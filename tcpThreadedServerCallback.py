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