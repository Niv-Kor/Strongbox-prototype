import Strongbox.util.NumeralHandler as nums


# Take a string and create a new list with the encrypted data.
# The first item of the list is the product of encrypting the data using RSA.
# It's a very large number, and therefore represented as a string,
# The second item of the list is a tuple (n, e), which is used as the RSA public key.
# These values are later needed for encrypting the next received message.
def encrypt(secret, trapdoor):
    string = ''
    maxDigits = 1
    encList = []

    print 'secret is', secret

    if len(secret) > 0:
        # encrypt all items in secret
        for i in range(len(secret)):
            secret[i] = (int(secret[i]) ** trapdoor.encrypterKey[1]) % trapdoor.encrypterKey[0]
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
    else:
        encList.append('')

    # insert new public key
    encList.append(trapdoor.getPublicKey())

    return encList


# Take an encrypted message and decrypt it using the values in the trapdoor,
# and the public key that has been previously stored.
def decrypt(secret, trapdoor):
    decList = []
    finalList = [None, secret[1], secret[2]]

    if secret[0] != '':
        blockSize = int(secret[0][:3])

        # create a list of encrypted integers, using the first item in secret
        for i in range(3, len(secret[0]), blockSize):
            block = secret[0][i:i + blockSize]
            decList.append(block)

        # decrypt the integers back to normal using the decryptor key
        for i in range(len(decList)):
            decList[i] = (int(decList[i]) ** trapdoor.d) % trapdoor.n

    finalList[0] = decList
    return finalList
