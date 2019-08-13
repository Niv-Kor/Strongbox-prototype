from Strongbox.user import TrapDoor


class UserProfile:
    BUFFER_SIZE = 2048

    def __init__(self, name, ip, port):
        self.name = name
        self.door = TrapDoor.TrapDoor()
        self.address = (ip, port)

    def __eq__(self, other):
        if not isinstance(other, UserProfile):
            return False

        return self.name == other.name and self.address == other.address

