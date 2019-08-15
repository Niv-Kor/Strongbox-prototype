from Strongbox.server.Protocol import Protocol
from Strongbox.view.MainWindow import MainWindow


protocol = Protocol()
protocol.bind()
mainWindow = MainWindow(protocol)
