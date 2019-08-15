import ServerConstants as servconst
from threading import Thread
import StringHandler as sthand


class ChatServer:
    def __init__(self, name):
        self.name = name
        self.clients = {}

        # store the public key of the first person to enter the chat
        # this message will only arrive to the other person when he enteres the chat as well
        self.headerBuffer = set()

    def invite(self, (client, name)):
        if not self.isFull():
            self.clients[client] = name
            handlingThread = Thread(target=self.handleClient, args=(client,))
            handlingThread.start()

    def kick(self, client):
        del self.clients[client]

    def clientCount(self):
        return len(self.clients)

    def isFull(self):
        return self.clientCount() == servconst.CHAT_BACKLOG

    def handleClient(self, client):
        while True:
            msg = client.recv(servconst.BUFFER_SIZE)

            # received a header message from the client
            # containing his opening public key
            if msg == servconst.HEADER_REQUEST_MESSAGE:
                # if this is the second person to enter the chat,
                # send him the public key from the buffer
                if len(self.headerBuffer) > 0:
                    headerTop = self.headerBuffer.pop()
                    self.headerBuffer.add(headerTop)
                    client.send(headerTop)

                # broadcast the header message
                self.broadcast(client, msg[len(servconst.HEADER_REQUEST_MESSAGE):])
            # received quit message
            elif msg == servconst.QUIT_MESSAGE:
                self.kick(client)
                self.broadcast(client, str(self.clients[client]) + ' has left the chat.')
                break
            else:
                self.broadcast(client, msg)

    # Broadcast a message to all connected clients except the sender
    def broadcast(self, sender, msg):
        # store the message in the buffer
        if self._isHeader(msg):
            self.headerBuffer.clear()
            self.headerBuffer.add(msg)

        # send to anyone but the sender himself
        for sock in self.clients:
            if sock != sender:
                sock.send(bytes(msg))

    # Check if a message is a header, which contains an empty string with crucial encryption info
    def _isHeader(self, msg):
        encryptedNum = str(msg[sthand.nthIndex(msg, '\'', 0) + 1:sthand.nthIndex(msg, '\'', 1)])
        return encryptedNum == ''
