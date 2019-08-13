import NumeralHandler as nums


# Convert a string to a list, having the integer value of each character as an item
def encode(secret):
    decimalList = []

    for i in secret:
        decimalList.append(Strongbox.util.NumeralHandler.zeroPadding(ord(i), 3))

    return decimalList


# Convert a list of integers (up to 255) to a string of characters
def decode(secret):
    charString = ''

    for i in secret:
        print 'i is', i
        charString += chr(int(i))

    return charString


# Validate a message by checking if it contains illegal characters
def isLegal(message):
    for i in message:
        if ord(i) >= 256:
            return False

    return message != ''