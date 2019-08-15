import ServerConstants as servconst


# Check if a message is a header, which contains an empty string with crucial encryption info
def isHeader(msg):
    encryptedNum = str(msg[_nthIndex(msg, '\'', 0) + 1:_nthIndex(msg, '\'', 1)])
    return encryptedNum == ''


def extractChatRequest(req):
    req = req[len(servconst.CHAT_REQUEST_MESSAGE):]
    clientName = req[_nthIndex(req, '\'', 0) + 1:_nthIndex(req, '\'', 1)]
    chatTitle = req[_nthIndex(req, '\'', 2) + 1:_nthIndex(req, '\'', 3)]
    return [clientName, chatTitle]


def extractChatApproval(msg):
    title = msg[_nthIndex(msg, '\'', 0) + 1:_nthIndex(msg, '\'', 1)]
    approval = msg[_nthIndex(msg, ',', 0) + 2:_nthIndex(msg, ']', 0)]
    return [title, approval]


# Convert a string representation of encrypted data back to a list
def extractRawMessage(msg):
    encryptedNum = str(msg[_nthIndex(msg, '\'', 0) + 1:_nthIndex(msg, '\'', 1)])
    n = int(msg[_nthIndex(msg, '(', 0) + 1:_nthIndex(msg, ',', 1)])
    e = int(msg[_nthIndex(msg, ',', 1) + 2:_nthIndex(msg, ')', 0)])
    name = str(msg[_nthIndex(msg, '\'', 2) + 1:_nthIndex(msg, '\'', 3)])
    return [encryptedNum, (n, e), name]


def _nthIndex(string, substring, n):
    parts = string.split(substring, n + 1)

    if len(parts) <= n + 1:
        return -1
    else:
        return len(string) - len(parts[-1]) - len(substring)