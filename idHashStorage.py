import hashlib

validHashes = []

# run this at startup
def setup():
    pass

# generates a hash from rfid data
def generateHash(string):
    return hashlib.sha256(bytes(string, "utf-8")).hexdigest()

# returns true if the string has a hash already stored
def getStringKnown(string):
    hash = generateHash(string)
    return hash in validHashes

# saves the hash of the string in the valid hash list
def setStringKnown(string):
    hash = generateHash(string)
    validHashes.append(hash)

# use this to test just the hashing and storage functionality
if __name__ == "__main__":
    setup()
    testStringA = "abcdef"
    testStringB = "ghijkl"

    setStringKnown(testStringA)
    print(getStringKnown(testStringA))
    print(getStringKnown(testStringB))
