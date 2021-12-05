import time
import hashlib
import RPi.GPIO as GPIO
import rfid
import servo

UNLOCK_TIME = 120 # number of seconds that must elapse since the device was unlocked for it to unlock again
SERVO_LOCK_DIR = 0.25
SERVO_UNLOCK_DIR = 0.75

currentlyLocked = True
timeSinceUnlock = None
knownHashes = []


# returns RFID code if read is successful, otherwise returns None
def tryReadRfid():
    return rfid.read()

# generates a hash from rfid data
def generateHash(rfidDataString):
    return hashlib.sha256(bytes(rfidDataString)).hexdigest()

# opens the container
def unlock():
    global currentlyLocked
    currentlyLocked = False
    servo.setServo(SERVO_UNLOCK_DIR)

# seals the container
def lock():
    global timeSinceUnlock
    global currentlyLocked
    currentlyLocked = True
    timeSinceUnlock = time.time()
    servo.setServo(SERVO_LOCK_DIR)


def setup():
    servo.setup()
    lock()

def mainLoop():
    timeElapsed = time.time() - timeSinceUnlock
    rfidData = tryReadRfid()
    rfidHash = generateHash(rfidData)
    if len(knownHashes) == 0: #add the first card read into known cards (this is for debug purposes)
        knownHashes.append(rfidHash)
    if rfidHash in knownHashes:
        if currentlyLocked and timeElapsed > UNLOCK_TIME:
            unlock()
        elif not currentlyLocked:
            lock()

if __name__ == "__main__":
    setup()
    while True:
        try:
            mainLoop()
        except KeyboardInterrupt:
            print("Exiting: Keyboard Interrupt")
        finally:
            servo.stop()
            GPIO.cleanup()