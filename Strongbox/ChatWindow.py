import ServerConstants as servconst
import tkinter as tk


class ChatWindow:
    def __init__(self):
        self.window = tk.Toplevel()

        self.window.title(servconst.APP_NAME)
        self.messagesFrame = tk.Frame(self.window)
        self.msgBuffer = tk.StringVar()  # for the messages to be sent
        self.scrollBar = tk.Scrollbar(self.messagesFrame)  # to navigate through past messages

        # the following will contain the messages
        self.msgList = tk.Listbox(self.messagesFrame, height=15, width=50, yscrollcommand=self.scrollBar.set)

        self.scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
        self.msgList.pack(side=tk.LEFT, fill=tk.BOTH)
        self.msgList.pack()
        self.messagesFrame.pack()
        self.entryField = None
        self.sendButton = None
        self.controller = None

    def connectController(self, controller):
        self.controller = controller

        self.entryField = tk.Entry(self.window, textvariable=self.msgBuffer)
        self.entryField.bind('<Return>', (lambda event: self.controller.bufferSend(self.msgBuffer)))
        self.entryField.pack()

        self.sendButton = tk.Button(self.window, text='Send', command=self.bufferSend)
        self.sendButton.pack()
        self.window.protocol('WM_DELETE_WINDOW', self.controller.closeChat)

    def bufferSend(self):
        self.controller.bufferSend(self.msgBuffer)

    def append(self, message):
        self.msgList.insert(tk.END, message)

    def clearBuffer(self):
        self.msgBuffer.set('')

    def enableButton(self, enable):
        switch = {True:tk.NORMAL, False:tk.DISABLED}
        self.sendButton.x.config(state=switch[enable])

    def close(self):
        self.window.quit()
        self.window.destroy()
