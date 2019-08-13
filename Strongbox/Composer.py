import Codec
import Encrypter


def compose(msg, profile):
    msg = Codec.encode(msg)
    msg = Encrypter.encrypt(msg, profile.door)
    msg.append(profile.name)
    return msg


def decompose(msg, profile):
    msg = _stringToList(msg)
    msg = Encrypter.decrypt(msg, profile.door)
    string = msg[2] + ':' + Codec.decode(msg[0])
    profile.door.setDecrypterKey(msg[1])
    return string


# Convert a string representation of encrypted data back to a list
def _stringToList(string):
    encryptedNum = str(string[2:string.rfind('\'')])
    n = int(string[string.index('(') + 1:string.rfind(',')])
    e = int(string[string.rfind(',') + 2:string.rfind(')')])
    name = str(string[string.rfind(',') + 3:string.rfind('\'')])
    return [encryptedNum, (n, e), name]
