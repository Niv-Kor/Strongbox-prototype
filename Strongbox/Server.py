from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import StringHandler as sthand
import ServerConstants as const


ADDRESS = (const.HOST, const.PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDRESS)

clients = {}
addresses = {}


# Set up handling for incoming clients
def accept():
    while True:
        (client, clientAddress) = SERVER.accept()
        print '>>>', clientAddress, 'has connected. socket', client

        welcomeMessage = const.WELCOME_MESSAGE

        if len(clients) == 1:
            welcomeMessage += 'You are currently here by yourself.'
        elif len(clients) == 2:
            welcomeMessage += 'You are here with another person. Start talking!'

        '''TEMP DEMO'''
        # client.send(bytes(welcomeMessage))

        addresses[client] = clientAddress
        handlingThread = Thread(target=handleClient, args=(client,))
        handlingThread.start()


# Handle a single client connection
def handleClient(client):
    msg = '>>> ', client, 'has joined the chat!'
    # broadcast(client, bytes(msg))
    clients[client] = 'Someone'

    # for some reason the client needs to receive a first dummy message
    # in order to be capable of receiving the next messages
    client.send(bytes('<CLIENT IGNITE MESSAGE>'))

    while True:
        msg = client.recv(const.BUFFER_SIZE)

        # received quit message
        if msg == const.QUIT_MESSAGE:
            client.close()
            del clients[client]
            broadcast(client, 'Someone' + ' has left the chat.')
            break
        # received header message
        elif _isHeader(msg):
            broadcast(client, msg)
        # received encrypted message
        else:
            broadcast(client, msg)


# Broadcast a message to all connected clients
def broadcast(sender, msg, prefix=''):
    print 'going to send', msg
    for sock in clients:
        if sock != sender:
            sock.send(bytes(prefix + msg))


def _isHeader(msg):
    encryptedNum = str(msg[sthand.nthIndex(msg, '\'', 0) + 1:sthand.nthIndex(msg, '\'', 1)])
    return encryptedNum == ''


SERVER.listen(const.BACKLOG)
print '>>> Waiting for connection...'
ACCEPT_THREAD = Thread(target=accept)
ACCEPT_THREAD.start()
ACCEPT_THREAD.join()
SERVER.close()
