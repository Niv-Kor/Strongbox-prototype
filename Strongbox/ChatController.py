from threading import Thread
import ServerConstants as servconst
import Encrypter
import Codec


class ChatController:
    def __init__(self, profile):
        self.profile = profile
        self.protocol = None
        self.window = None
        self.partner = None

    def connect(self, protocol, window):
        self.protocol = protocol
        self.window = window
        self.window.connectController(self)
        self.protocol.bind()
        receiveThread = Thread(target=self.receive)
        receiveThread.start()

        self._headerSend()
        self.window.run()

    # receive a message from either the server or the other client
    def receive(self):
        while True:
            msg = self.protocol.receive()

            if not type(msg) is None:
                # header signal from the other client
                # contains the relevant public key
                if msg.startswith(servconst.HEADER_MESSAGE):
                    # store the partner's name, and his public key as my encryptor key
                    headerInfo = self._extractHeader(msg)
                    self.partner.name = headerInfo[0]
                    self.profile.door.setEncryptorKey(headerInfo[1])
                else:
                    # welcome message from server
                    if msg.startswith(servconst.WELCOME_MESSAGE):
                        self.window.append(msg)
                    # encrypted message from other client
                    else:
                        msg = Encrypter.decrypt(msg, self.profile.door)
                        self.window.append(str(self.partner.name) + ': ' + msg)
                        self.profile.door.regenerate()
                        self._headerSend()
            else:  # client has possibly left the chat
                break

    # Send a message to the other client
    def send(self, msg):
        # close the window
        if msg == servconst.QUIT_MESSAGE:
            self.window.close()
        # client sends a legal message
        else:
            msg = Encrypter.encrypt(msg, self.profile.door)
            self.protocol.send(msg)

        self.window.clearBuffer()

    # send the other client an opening signal, containing my public key.
    # if someone gets this message, it means that the chat includes two participants.
    # only the one getting this message is applicable of sending the next message.
    def _headerSend(self):
        name = self.profile.name
        publicKey = self.profile.door.getPublicKey()
        message = [name, publicKey]
        self.protocol.send(servconst.HEADER_MESSAGE + str(message))

        print 'sent', servconst.HEADER_MESSAGE + str(message)

    # Send a message to the other client using the send button
    def bufferSend(self, msgBuffer):
        msg = msgBuffer.get()

        # avoid sending a message with illegal characters
        if Codec.isLegal(msg):
            self.window.append('You: ' + msg)
            self.send(msg)
        else:
            self.window.clearBuffer()

    def closeChat(self):
        self.protocol.send(servconst.QUIT_MESSAGE)

    def _extractHeader(self, message):
        message = message[message.index(servconst.HEADER_MESSAGE):]
        message = message[len(servconst.HEADER_MESSAGE) + 1:]

        name = message[:message.index(',')]
        keyString = message[message.index(',') + 2:]
        n = int(keyString[1:keyString.index(',')])
        e = int(keyString[keyString.index(',') + 2:len(keyString) - 1])
        publicKey = (n, e)

        header = [name, publicKey]
        return header
