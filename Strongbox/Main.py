from Strongbox.control import ChatController
from Strongbox.user import UserProfile
from Strongbox.view import ChatWindow
from Strongbox.server import Protocol


user = UserProfile.UserProfile('Niv', '10.100.102.8', 40022)
controller = ChatController.ChatController(user)
protocol = Protocol.Protocol()
window = ChatWindow.ChatWindow()
controller.connect(protocol, window)
