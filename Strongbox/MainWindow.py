import ServerConstants as servconst
from PIL import Image, ImageTk
from ChatWindow import ChatWindow
from UserProfile import UserProfile as user
from ChatController import ChatController
from threading import Thread
import StringHandler as sthand
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
        logo = ImageTk.PhotoImage(Image.open('logo.png'))
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
        buttonImage = ImageTk.PhotoImage(Image.open('enter_button.png'))
        enterButton = tk.Button(self.window, command=self.enter)
        enterButton.config(image=buttonImage, highlightthickness=0, bd=0)
        enterButton.grid(row=3, columnspan=2, pady=(40, 20))

        # receiveThread = Thread(target=self.receive)
        # receiveThread.start()
        self.window.mainloop()

    def generate_new_window(self):
        print 'a'
        wind = tk.Toplevel()
        print 'b'
        label = tk.Label(wind, text="a generic Toplevel window")
        label.pack()

    def enter(self):
        name = self.nameBuffer.get()
        title = self.chatTitleBuffer.get()

        # verify inputs
        if name != '' and name.replace(' ', '').isalpha() and title != '':
            print 'entered'
            self.user = user(name)
            msg = servconst.CHAT_REQUEST_MESSAGE + str([name, title])
            self.protocol.send(msg)

            msg = self.protocol.receive()
            print 'received approval:', msg

            try:
                msg = self._extractChatApproval(msg)
                print 'received approval after try:', msg

                if msg[0] == self.chatTitleBuffer.get() and msg[1] == str(True):
                    print 'Approved'
                    chatWindow = ChatWindow()
                    controller = ChatController(user)
                    controller.connect(self.protocol, chatWindow)
            except Exception:
                pass

    def _extractChatApproval(self, msg):
        title = msg[sthand.nthIndex(msg, '\'', 0) + 1:sthand.nthIndex(msg, '\'', 1)]
        approval = msg[sthand.nthIndex(msg, ',', 0) + 2:sthand.nthIndex(msg, ']', 0)]
        return [title, approval]




