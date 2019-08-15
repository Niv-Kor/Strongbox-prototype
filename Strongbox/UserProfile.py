import TrapDoor


class UserProfile:
    BUFFER_SIZE = 2048

    def __init__(self, name):
        self.name = name
        self.door = TrapDoor.TrapDoor()

    def __eq__(self, other):
        if not isinstance(other, UserProfile):
            return False

        return self.name == other.name

