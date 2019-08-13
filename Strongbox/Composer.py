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
    print 'received', string

    encryptedNum = str(string[_nthIndex(string, '\'', 0) + 1:_nthIndex(string, '\'', 1)])
    print 'encrypted number:', encryptedNum

    n = int(string[_nthIndex(string, '(', 0) + 1:_nthIndex(string, ',', 1)])
    print 'n:', n

    e = int(string[_nthIndex(string, ',', 1) + 2:_nthIndex(string, ')', 0)])
    print 'e:', e

    name = str(string[_nthIndex(string, '\'', 2) + 1:_nthIndex(string, '\'', 3)])
    print 'name:', name

    return [encryptedNum, (n, e), name]


def _nthIndex(string, substring, n):
    parts = string.split(substring, n + 1)

    if len(parts) <= n + 1:
        return -1
    else:
        return len(string) - len(parts[-1]) - len(substring)
