import time

UNLOCK_TIME = 120 # number of seconds that must elapse since the device was unlocked for it to unlock again

currentlyLocked = True
timeSinceUnlock = None
knownHashes = []


# returns RFID code if read is successful, otherwise returns None
def tryReadRfid():
    #TODO read from sensor
    return None

# generates a hash from rfid data
def generateHash(rfidData):
    #TODO generate hash
    return None

# opens the container
def unlock():
    currentlyLocked = False
    #TODO set servo to unlocked position

# seals the container
def lock():
    currentlyLocked = True
    timeSinceUnlock = time.time()
    #TODO set servo to locked position



def mainLoop():
    timeElapsed = time.time() - timeSinceUnlock
    rfidData = tryReadRfid()
    if rfidData != None:
        rfidHash = generateHash(rfidData)
        if rfidHash in knownHashes:
            if currentlyLocked and timeElapsed > UNLOCK_TIME:
                unlock()
            elif not currentlyLocked:
                lock()

if __name__ == "__main__":
    timeSinceUnlock = time.time()
    while True:
        try:
            mainLoop()
        except KeyboardInterrupt:
            print("Exiting: Keyboard Interrupt")