import Strongbox.util.NumeralHandler as nums
import Codec


# Take a string and create a new list with the encrypted data.
# The first item of the list is the product of encrypting the data using RSA.
# It's a very large number, and therefore represented as a string,
# The second item of the list is a tuple (n, e), which is used as the RSA public key.
# These values are later needed for encrypting the next received message.
def encrypt(secret, trapdoor):
    secret = Codec.encode(secret)
    string = ''
    maxDigits = 1
    encList = []

    # encrypt all items in secret
    for i in range(len(secret)):
        secret[i] = (int(secret[i]) ** trapdoor.decryptorKey[1]) % trapdoor.decryptorKey[0]
        mDigits = nums.countDigits(int(secret[i]))
        if mDigits > maxDigits:
            maxDigits = mDigits

    # concat all encrypted items into a string
    for i in range(len(secret)):
        m = nums.zeroPadding(secret[i], maxDigits)
        string += m

    # insert header info
    string = nums.zeroPadding(maxDigits, 3) + string
    encList.append(string)

    # insert new public key
    trapdoor.regenerate()
    encList.append(trapdoor.getPublicKey())

    return encList


# Take an encrypted message and decrypt it using the values in the trapdoor,
# and the public key that has been previously stored.
def decrypt(secret, trapdoor):
    # the message is received from the server as a string
    # cast it back to a list again
    secret = _stringToList(secret)

    decList = []
    blockSize = int(secret[0][:3:])

    # take the second item in secret and set it as a decryptor key
    trapdoor.setDecryptorKey(secret[1])

    # create a list of encrypted integers, using the first item in secret
    for i in range(3, len(secret[0]), blockSize):
        block = secret[0][i:i + blockSize:]
        decList.append(block)

    # decrypt the integers back to normal using the decryptor key
    for i in range(len(decList)):
        decList[i] = (int(decList[i]) ** trapdoor.d) % trapdoor.n

    return Codec.decode(decList)


# Convert a string representation of encrypted data back to a list
def _stringToList(string):
    encryptedNum = str(string[2:string.rfind('\'')])
    n = int(string[string.index('(') + 1:string.rfind(',')])
    e = int(string[string.rfind(',') + 2:string.rfind(')')])

    return [encryptedNum, (n, e)]
