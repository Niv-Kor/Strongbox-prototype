from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import MessageConverter as mesconv
import ServerConstants as servconst
from ChatServer import ChatServer


ADDRESS = (servconst.HOST, servconst.PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDRESS)

clients = {}
addresses = {}
searching = {}
chats = {}


# Set up handling for incoming clients
def accept():
    while True:
        (client, clientAddress) = SERVER.accept()
        print '>>>', clientAddress, 'has connected the server.'

        welcomeMessage = servconst.WELCOME_MESSAGE

        if len(clients) == 1:
            welcomeMessage += 'You are currently here by yourself.'
        elif len(clients) == 2:
            welcomeMessage += 'You are here with another person. Start talking!'

        '''TEMP TODO'''
        # client.send(bytes(welcomeMessage))

        addresses[client] = clientAddress
        searching[client] = True
        handlingThread = Thread(target=handleClient, args=(client,))
        handlingThread.start()


# Handle a single client connection
def handleClient(client):
    # for some reason the client needs to receive a first dummy message
    # in order to be capable of receiving the next messages
    client.send(bytes('<DUMMY IGNITION MESSAGE>'))

    while searching[client]:
        msg = client.recv(servconst.BUFFER_SIZE)

        if msg.startswith(servconst.CHAT_REQUEST_MESSAGE):
            request = mesconv.extractChatRequest(msg)
            chatTitle = request[1]
            print '>>> Received request:', msg

            if chatTitle in chats and chats[chatTitle].isFull():
                approvalMsg = [chatTitle, False]
                client.send(str(approvalMsg))

                printChatCapacity(chats[chatTitle])
                print '>>> Request not approved.'
            else:
                if chatTitle not in chats:
                    chats[chatTitle] = ChatServer(chatTitle)
                    print '>>> Created new chat \'{}\''.format(request[1])

                printChatCapacity(chats[chatTitle])
                print '>>> Request approved.'

                chats[chatTitle].invite((client, request[0]))
                searching[client] = False
                approvalMsg = [chatTitle, True]
                client.send(str(approvalMsg))


def printChatCapacity(chat):
    title = chat.title
    capacity = '{}/{}'.format(chat.clientCount(), servconst.CHAT_BACKLOG)
    print '>>> The chat \'{}\' contains {} clients.'.format(title, capacity)


def terminateEmptyChats():
    pass
    '''
    while True:
        for chat in chats:
            if chats[chat].clientCount() == 0:
                del chats[chat]

        time.sleep(3)
    '''
    # TODO


def removeChat(chatServer):
    del chats[chatServer.name]


SERVER.listen(servconst.APP_BACKLOG)
print '>>> Waiting for connection...'

TERMINATE_THREAD = Thread(target=terminateEmptyChats)
TERMINATE_THREAD.start()

ACCEPT_THREAD = Thread(target=accept)
ACCEPT_THREAD.start()
ACCEPT_THREAD.join()
SERVER.close()
