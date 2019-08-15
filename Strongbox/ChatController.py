from threading import Thread
import ServerConstants as servconst
import Codec
import Composer


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
        receiveThread = Thread(target=self.receive)
        receiveThread.start()

        headerMsg = ['', self.profile.door.getPublicKey(), self.profile.name]
        self.protocol.send(servconst.HEADER_REQUEST_MESSAGE + bytes(headerMsg))

    # receive a message from either the server or the other client
    def receive(self):
        while True:
            msg = self.protocol.receive()
            self.window.enableButton(True)
            print 'received', msg

            if not type(msg) is None and not msg == servconst.QUIT_MESSAGE:
                # welcome message from server
                if msg.startswith(servconst.WELCOME_MESSAGE):
                    self.window.append(msg)
                # encrypted message from other client
                else:
                    msg = Composer.decompose(msg, self.profile)

                    # message is not empty
                    if msg[len(msg) - 2] != ':' or msg.count(':') > 1:
                        self.profile.door.regenerate()
                        self.window.append(msg)
                        self.send('')
            else:  # client has possibly left the chat
                break

    # Send a message to the other client
    def send(self, msg):
        # close the window
        if msg == servconst.QUIT_MESSAGE:
            self.window.close()
        # client sends a legal message
        else:
            msg = Composer.compose(msg, self.profile)
            self.protocol.send(msg)
            self.window.enableButton(False)

        self.window.clearBuffer()

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
        self.send(servconst.QUIT_MESSAGE)
