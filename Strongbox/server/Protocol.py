from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from Strongbox.server import ServerConstants as servconst


class Protocol:
    def __init__(self):
        self.clientSocket = None

    # Connect to the server
    def bind(self):
        address = (servconst.HOST, servconst.PORT)
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect(address)
        receiveThread = Thread(target=self.receive)
        receiveThread.start()

    def unbind(self):
        self.clientSocket.close()

    # Send a message to the other client
    def send(self, msg):
        try:
            self.clientSocket.send(bytes(msg))
        except (IOError, AttributeError):
            print 'Could not send the message', msg

    # receive a message from either the server or the other client
    def receive(self):
        try:
            return self.clientSocket.recv(servconst.BUFFER_SIZE).decode(servconst.DECODER)
        except OSError:
            return ''
