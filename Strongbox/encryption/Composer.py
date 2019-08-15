import Strongbox.util.MessageConverter as mesconv
import Codec
import Encrypter


def compose(msg, profile):
    msg = Codec.encode(msg)
    msg = Encrypter.encrypt(msg, profile.door)
    msg.append(profile.name)
    return msg


def decompose(msg, profile):
    msg = mesconv.extractRawMessage(msg)
    msg = Encrypter.decrypt(msg, profile.door)
    string = msg[2] + ': ' + Codec.decode(msg[0])
    profile.door.setEncrypterKey(msg[1])
    return string
