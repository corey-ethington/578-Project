import time
import hashlib
import RPi.GPIO as GPIO
import rfid
import servo

STAY_CLOSED_TIME = 7 # number of seconds that must elapse since the device was unlocked for it to unlock again
TIME_UNLOCKED = 5 # amount of time the container will stay unlocked before automatically re-locking

# positioning info for servo
SERVO_LOCK_DIR = 0.25
SERVO_UNLOCK_DIR = 0.75

timeSinceUnlock = time.time()
knownHashes = []


# returns RFID code if read is successful, otherwise returns None
def tryReadRfid():
    return rfid.read()

# generates a hash from rfid data
def generateHash(rfidDataString):
    # return hashlib.sha256(bytes(rfidDataString)).hexdigest()
    return rfidDataString


# unlocks the conatiner, waits for a set amount of time, and re-locks the container
def unlockLock():
    global timeSinceUnlock

    # unlock
    print("Unlocking...")
    servo.setServo(SERVO_UNLOCK_DIR)
    print("Unlocked")
    time.sleep(5)

    # re-lock
    timeSinceUnlock = time.time()
    print("Locking...")
    servo.setServo(SERVO_LOCK_DIR)
    print("Locked")


def setup():
    servo.setup()
    rfid.setup()
    servo.secondarySetup()

def mainLoop():
    timeElapsed = time.time() - timeSinceUnlock
    rfidData = tryReadRfid()
    rfidHash = generateHash(rfidData)
    print(f"Read {rfidHash}")
    if len(knownHashes) == 0: #add the first card read into known cards (this is for debug purposes)
        knownHashes.append(rfidHash)
        print(f"Added {rfidHash} to known card ids")
    if rfidHash in knownHashes:
        if timeElapsed > STAY_CLOSED_TIME: unlockLock()
        else: print(f"Time elapsed: {int(timeElapsed)} / {STAY_CLOSED_TIME} seconds")

if __name__ == "__main__":
    setup()
    try:
        while True: mainLoop()
    except KeyboardInterrupt:
        print("Exiting: Keyboard Interrupt")
    finally:
        servo.stop()
        GPIO.cleanup()