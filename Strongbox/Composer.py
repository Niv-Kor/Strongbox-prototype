import StringHandler as sthand
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
    string = msg[2] + ': ' + Codec.decode(msg[0])
    profile.door.setEncrypterKey(msg[1])
    return string


# Convert a string representation of encrypted data back to a list
def _stringToList(string):
    encryptedNum = str(string[sthand.nthIndex(string, '\'', 0) + 1:sthand.nthIndex(string, '\'', 1)])
    n = int(string[sthand.nthIndex(string, '(', 0) + 1:sthand.nthIndex(string, ',', 1)])
    e = int(string[sthand.nthIndex(string, ',', 1) + 2:sthand.nthIndex(string, ')', 0)])
    name = str(string[sthand.nthIndex(string, '\'', 2) + 1:sthand.nthIndex(string, '\'', 3)])
    return [encryptedNum, (n, e), name]
