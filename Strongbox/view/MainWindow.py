from Strongbox.server import ServerConstants as servconst
from PIL import Image, ImageTk
from Strongbox.view.ChatWindow import ChatWindow
from Strongbox.user.UserProfile import UserProfile as user
from Strongbox.control.ChatController import ChatController
import Strongbox.util.MessageConverter as mesconv
import tkinter as tk


class MainWindow:
    def __init__(self, protocol):
        self.user = None
        self.protocol = protocol

        # window configuration
        self.window = tk.Tk()
        self.window.title(servconst.APP_NAME)
        self.window.resizable(False, False)
        winWidth = 500
        winHeight = 500
        xPos = self.window.winfo_screenwidth() / 2 - winWidth / 2
        yPos = self.window.winfo_screenheight() / 2 - winHeight / 2
        self.window.geometry('{}x{}+{}+{}'.format(winWidth, winHeight, xPos, yPos))

        # logo
        logo = ImageTk.PhotoImage(Image.open('resources/logo.png'))
        logoLab = tk.Label(self.window, image=logo)
        logoLab.grid(row=0, columnspan=2, padx=(20, 20), pady=(10, 60))

        # name field
        clientNameLab = tk.Label(self.window, text='name:', font=('Futura-Light', 18))
        clientNameLab.grid(row=1, column=0, sticky=tk.E, padx=(10, 10), pady=(10, 10))

        self.nameBuffer = tk.StringVar()
        nameField = tk.Entry(self.window, textvariable=self.nameBuffer)
        nameField.grid(row=1, column=1, sticky=tk.W, padx=(10, 10), pady=(10, 10), ipady=3)

        # chat title field
        chatTitleLab = tk.Label(self.window, text='chat title:', font=('Futura-Light', 18))
        chatTitleLab.grid(row=2, column=0, sticky=tk.E, padx=(10, 10), pady=(10, 10))

        self.chatTitleBuffer = tk.StringVar()
        chatTitleField = tk.Entry(self.window, textvariable=self.chatTitleBuffer)
        chatTitleField.grid(row=2, column=1, sticky=tk.W, padx=(10, 10), pady=(10, 10), ipady=3)

        # enter button
        buttonImage = ImageTk.PhotoImage(Image.open('resources/enter_button.png'))
        enterButton = tk.Button(self.window, command=self.enter)
        enterButton.config(image=buttonImage, highlightthickness=0, bd=0)
        enterButton.grid(row=3, columnspan=2, pady=(40, 20))

        # receiveThread = Thread(target=self.receive)
        # receiveThread.start()
        self.window.mainloop()

    def enter(self):
        name = self.nameBuffer.get()
        title = self.chatTitleBuffer.get()

        # verify inputs
        if name != '' and name.replace(' ', '').isalpha() and title != '':
            self.user = user(name)
            msg = servconst.CHAT_REQUEST_MESSAGE + str([name, title])
            self.protocol.send(msg)

            # wait for response from server
            msg = self.protocol.receive()

            try:
                msg = mesconv.extractChatApproval(msg)

                if msg[0] == self.chatTitleBuffer.get() and msg[1] == str(True):
                    print 'Chat {} approved.'.format(title)
                    chatWindow = ChatWindow()
                    controller = ChatController(self.user)
                    controller.connect(self.protocol, chatWindow)
                else:
                    print 'Chat {} is full.'.format(title)
            except Exception:
                pass
        else:
            print 'Inputs not approved.'
