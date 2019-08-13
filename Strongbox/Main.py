import ChatController
import UserProfile
import ChatWindow
import Protocol


user = UserProfile.UserProfile('Alice', '10.100.102.8', 40022)
controller = ChatController.ChatController(user)
protocol = Protocol.Protocol()
window = ChatWindow.ChatWindow()
controller.connect(protocol, window)
