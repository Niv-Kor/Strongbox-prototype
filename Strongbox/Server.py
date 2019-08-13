from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
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

    while True:
        msg = client.recv(const.BUFFER_SIZE)

        # received quit message
        if msg == const.QUIT_MESSAGE:
            client.close()
            del clients[client]
            broadcast(client, 'Someone' + ' has left the chat.')
            break
        # received header message
        elif msg.startswith(const.HEADER_MESSAGE):
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
            sock.send(bytes(prefix + msg))
            print 'sent', bytes(prefix + msg), 'to', sock


SERVER.listen(const.BACKLOG)
print '>>> Waiting for connection...'
ACCEPT_THREAD = Thread(target=accept)
ACCEPT_THREAD.start()
ACCEPT_THREAD.join()
SERVER.close()
