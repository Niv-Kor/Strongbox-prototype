import ServerConstants as servconst
import tkinter


class ChatWindow:
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.title(servconst.APP_NAME)
        self.messagesFrame = tkinter.Frame(self.window)
        self.msgBuffer = tkinter.StringVar()  # for the messages to be sent
        self.scrollBar = tkinter.Scrollbar(self.messagesFrame)  # to navigate through past messages

        # the following will contain the messages
        self.msgList = tkinter.Listbox(self.messagesFrame,
                                       height=15, width=50,
                                       yscrollcommand=self.scrollBar.set)

        self.scrollBar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.msgList.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        self.msgList.pack()
        self.messagesFrame.pack()
        self.entryField = None
        self.sendButton = None
        self.controller = None

    def connectController(self, controller):
        self.controller = controller

        self.entryField = tkinter.Entry(self.window, textvariable=self.msgBuffer)
        self.entryField.bind('<Return>', self.controller.send)
        self.entryField.pack()
        self.sendButton = tkinter.Button(self.window, text='Send',
                                         command=self.bufferSend)

        self.sendButton.pack()
        self.window.protocol('WM_DELETE_WINDOW', self.controller.closeChat)

    def bufferSend(self):
        self.controller.bufferSend(self.msgBuffer)

    def run(self):
        self.window.mainloop()

    def append(self, message):
        self.msgList.insert(tkinter.END, message)

    def clearBuffer(self):
        self.msgBuffer.set('')

    def close(self):
        self.window.quit()
        self.window.destroy()
